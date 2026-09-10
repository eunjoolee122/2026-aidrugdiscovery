"""실습 환경 점검 — 이 파일을 먼저 실행한다.

    python 00_check.py

모두 [OK]가 나오면 실습을 시작할 수 있다.
하나라도 [FAIL]이면 SETUP.md의 «문제 해결»을 본다.
"""
import sys, io, os, platform

# Windows 콘솔이 cp949라 한글 출력이 깨지는 것을 막는다
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

OK, FAIL, WARN = "[OK]  ", "[FAIL]", "[WARN]"
problems = []

def check(label, fn):
    try:
        msg = fn()
        print(f"{OK} {label:<28} {msg}")
        return True
    except Exception as e:
        print(f"{FAIL} {label:<28} {type(e).__name__}: {str(e)[:70]}")
        problems.append(label)
        return False

print("=" * 62)
print(f" 실습 환경 점검   {platform.system()} {platform.machine()}")
print("=" * 62)

# 1. 파이썬 버전 — chemprop 2.x는 3.11 이상을 요구한다
v = sys.version_info
if (3, 11) <= (v.major, v.minor) < (3, 15):
    print(f"{OK} Python 버전                  {v.major}.{v.minor}.{v.micro}")
else:
    print(f"{FAIL} Python 버전                  {v.major}.{v.minor} — 3.11 ~ 3.14가 필요하다")
    problems.append("Python 버전")

check("rdkit",        lambda: __import__("rdkit").__version__ if hasattr(__import__("rdkit"),"__version__") else "설치됨")
check("scikit-learn", lambda: __import__("sklearn").__version__)
check("pandas",       lambda: __import__("pandas").__version__)
check("numpy",        lambda: __import__("numpy").__version__)
check("torch",        lambda: __import__("torch").__version__)
check("chemprop",     lambda: __import__("importlib.metadata", fromlist=["x"]).version("chemprop"))
check("PyTDC",        lambda: __import__("importlib.metadata", fromlist=["x"]).version("PyTDC"))

def admetai():
    import warnings; warnings.filterwarnings("ignore")
    import importlib.metadata as md
    v = md.version("admet_ai")
    if not v.startswith("2."):
        raise RuntimeError(f"{v} — GitHub v_2.0.1이 아니다. 강의자료와 값이 다르다")
    return v
check("admet_ai (2.0.1이어야 함)", admetai)

def admetai_value():
    import warnings; warnings.filterwarnings("ignore")
    import pandas as pd
    from admet_ai import ADMETModel
    p = ADMETModel().predict(smiles=["CC(=O)Oc1ccccc1C(=O)O"])
    if not isinstance(p, pd.DataFrame): p = pd.DataFrame(p)
    v = float(p.iloc[0]["VDss_Lombardo"])
    if abs(v - (-2.70)) > 0.01:
        raise RuntimeError(f"aspirin VDss {v:.2f} — 자료값 −2.70과 다르다 (버전 확인)")
    return f"aspirin VDss {v:.2f} · 열 {p.shape[1]}개 — 자료와 일치"
check("ADMET-AI 값 대조", admetai_value)

# 2. TDC 데이터 다운로드 (네트워크 필요 · 82 KB)
DATA_DIR = os.path.join(os.getcwd(), "tdc_data")

def tdc_data():
    import warnings; warnings.filterwarnings("ignore")
    from tdc.single_pred import ADME
    os.makedirs(DATA_DIR, exist_ok=True)   # TDC는 폴더가 있으면 그냥 쓴다
    d = ADME(name="Caco2_Wang", path=DATA_DIR)
    n = len(d.get_data())
    return f"Caco2_Wang {n}개"
if not check("TDC 데이터 다운로드", tdc_data):
    print(f"{WARN} TDC 다운로드가 막혀도 실습은 된다 — data/ 폴더의 CSV를 쓴다.")

# 3. 끝에서 끝까지 — 특징 계산 → 학습 → 평가
def end_to_end():
    """TDC가 막히면 같은 폴더의 data/ CSV로 대신한다."""
    import warnings; warnings.filterwarnings("ignore")
    import numpy as np, pandas as pd
    from rdkit import Chem, RDLogger
    from rdkit.Chem import rdFingerprintGenerator
    RDLogger.DisableLog("rdApp.*")
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error
    src = "TDC"
    try:
        from tdc.single_pred import ADME
        os.makedirs(DATA_DIR, exist_ok=True)
        d = ADME(name="Caco2_Wang", path=DATA_DIR)
        sp = d.get_split(method="scaffold", seed=1, frac=[0.8, 0.1, 0.1])
        tr, te = sp["train"], sp["test"]
    except Exception:
        here = os.path.dirname(os.path.abspath(__file__))
        f_tr = os.path.join(here, "data", "caco2_train_val.csv")
        f_te = os.path.join(here, "data", "caco2_test.csv")
        if not (os.path.exists(f_tr) and os.path.exists(f_te)):
            raise RuntimeError("TDC 다운로드 실패 + data/ CSV도 없음")
        tr, te = pd.read_csv(f_tr), pd.read_csv(f_te)
        src = "data/ CSV"
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fp = lambda ss: np.array([gen.GetFingerprintAsNumPy(Chem.MolFromSmiles(s)) for s in ss])
    m = RandomForestRegressor(n_estimators=50, random_state=0, n_jobs=1).fit(fp(tr["Drug"]), tr["Y"])
    mae = mean_absolute_error(te["Y"], m.predict(fp(te["Drug"])))
    return f"MAE {mae:.3f} ({src} 사용 · 참고값 0.3~0.5)"
check("학습·평가 전체 실행", end_to_end)

# 4. chemprop 학습 한 스텝 (가장 무거운 부분)
def chemprop_step():
    import warnings; warnings.filterwarnings("ignore")
    import numpy as np, torch
    from lightning import pytorch as pl
    from chemprop import data, featurizers, models, nn
    pts = [data.MoleculeDatapoint.from_smi(s, np.array([y])) for s, y in
           (("CCO", 1.0), ("CCC", 2.0), ("CCN", 1.5), ("CCCl", 2.5))]
    ds = data.MoleculeDataset(pts, featurizers.SimpleMoleculeMolGraphFeaturizer())
    sc = ds.normalize_targets()
    dl = data.build_dataloader(ds, num_workers=0, batch_size=2)
    mdl = models.MPNN(nn.BondMessagePassing(), nn.MeanAggregation(),
                      nn.RegressionFFN(output_transform=nn.UnscaleTransform.from_standard_scaler(sc)),
                      batch_norm=True)
    t = pl.Trainer(max_epochs=1, accelerator="cpu", devices=1, logger=False,
                   enable_checkpointing=False, enable_progress_bar=False,
                   enable_model_summary=False)
    t.fit(mdl, dl)
    return "D-MPNN 1에폭 통과"
check("chemprop 학습", chemprop_step)

print("=" * 62)
fatal = [p for p in problems if p != "TDC 데이터 다운로드"]
if problems:
    print(f" {FAIL if fatal else WARN} 실패 항목: {', '.join(problems)}")
    print("      SETUP.md의 «문제 해결»을 본다.")
if fatal:
    sys.exit(1)
if problems:
    print(" TDC 다운로드만 실패했다 — data/ 폴더의 CSV로 실습할 수 있다.")
    sys.exit(0)
print(" 모두 통과. 실습을 시작할 수 있다.")
print("=" * 62)
