"""미니 리더보드 채점

    python score.py                      # submissions/ 안의 모든 CSV를 채점
    python score.py --dir 다른폴더
    python score.py --detail 홍길동       # 한 사람의 화합물별 오차까지

학생이 낸 CSV는 형식이 제각각이다. 아래를 자동으로 맞춘다.
  · 열 이름이 pred_log_er / pred / prediction / y_pred / log_er 무엇이든
  · 헤더가 있든 없든
  · log ER이 아니라 ER 원값을 낸 경우 (자동 감지 후 log 변환)
  · 순서가 뒤바뀌었거나 일부 화합물이 빠진 경우 (SMILES로 맞춘다)
"""
import sys, os, glob, argparse
import numpy as np, pandas as pd
try:
    from rdkit import Chem, RDLogger; RDLogger.DisableLog('rdApp.*')
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
PRED_NAMES = ["pred_log_er","pred","prediction","predicted","y_pred","log_er","logher","value"]
SMI_NAMES  = ["smiles","smi","canonical_smiles","structure","mol"]

def canon(s):
    if not HAS_RDKIT: return str(s).strip()
    m = Chem.MolFromSmiles(str(s).strip())
    return Chem.MolToSmiles(m) if m else None

def read_submission(path):
    """제각각인 CSV를 (smiles, pred) 두 열로 정규화한다."""
    for header in (0, None):
        try:
            d = pd.read_csv(path, header=header)
        except Exception:
            continue
        if d.shape[1] < 2: continue
        d.columns = [str(c).strip().lower() for c in d.columns]
        smi = next((c for c in d.columns if c in SMI_NAMES), None)
        prd = next((c for c in d.columns if c in PRED_NAMES), None)
        if smi is None or prd is None:
            # 열 이름을 못 찾으면 위치로: 첫 열 = SMILES, 마지막 숫자 열 = 예측
            num = [c for c in d.columns if pd.to_numeric(d[c], errors="coerce").notna().mean() > .8]
            if not num: continue
            smi, prd = d.columns[0], num[-1]
        out = pd.DataFrame({"smiles": d[smi].astype(str),
                            "pred": pd.to_numeric(d[prd], errors="coerce")}).dropna()
        if len(out) >= 5: return out
    raise ValueError("SMILES 열과 숫자 예측 열을 찾지 못했습니다")

def to_log(v, name):
    """ER 원값을 냈으면 log로 바꾼다.

    판정은 최댓값으로만 한다. log ER의 실제 범위는 0.15~1.79이고 넉넉히 봐도
    -2~3을 넘지 않는다. 최댓값이 4를 넘으면 원값(ER)을 낸 것이다.
    (ER은 1보다 작을 수 있으므로 최솟값으로는 판정하지 않는다.)
    """
    v = np.asarray(v, float)
    if v.max() > 4.0 and v.min() > 0:
        lg = np.log10(v)
        print(f"     · {name}: ER 원값으로 보여 log10을 취했습니다 "
              f"({v.min():.2f}~{v.max():.1f} → {lg.min():.2f}~{lg.max():.2f})")
        return lg
    if v.max() > 4.0:                              # 음수가 섞였다면 판단할 수 없다
        print(f"     ⚠ {name}: 값이 {v.min():.2f}~{v.max():.1f}입니다. "
              f"log ER인지 ER 원값인지 판단할 수 없어 그대로 씁니다.")
    return v

def score_one(sub, ans, name):
    sub = sub.copy()
    sub["c"] = [canon(s) for s in sub.smiles]
    sub = sub.dropna(subset=["c"]).drop_duplicates("c")
    j = ans.merge(sub[["c","pred"]], on="c", how="left")
    matched = j.pred.notna()
    n = int(matched.sum())
    if n < 5:
        return dict(이름=name, 매칭=n, 비고="화합물이 맞지 않습니다")
    y, p = j.log_er[matched].values, to_log(j.pred[matched].values, name)
    if np.ptp(p) == 0:                             # 전부 같은 값을 냈다
        mae = float(np.abs(y - p).mean())
        return dict(이름=name, 매칭=n, Spearman=0.0, MAE=round(mae,3),
                    R2=round(float(1-((y-p)**2).sum()/((y-y.mean())**2).sum()),3),
                    비고="예측이 전부 같은 값입니다")
    rho = spearmanr(y, p).statistic
    mae = float(np.abs(y - p).mean())
    r2 = 1 - ((y-p)**2).sum() / ((y-y.mean())**2).sum()
    return dict(이름=name, 매칭=n, Spearman=round(float(rho),3), MAE=round(mae,3),
                R2=round(float(r2),3),
                비고="" if n == len(ans) else f"{len(ans)-n}개 빠짐")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(HERE,"submissions"))
    ap.add_argument("--answer", default=os.path.join(HERE,"leaderboard_answer.csv"))
    ap.add_argument("--detail", default=None, help="한 사람의 화합물별 오차를 본다")
    a = ap.parse_args()

    if not HAS_RDKIT:
        print("⚠ rdkit이 없어 SMILES를 문자 그대로 비교합니다. 표기가 다르면 매칭이 어긋납니다.\n")
    ans = pd.read_csv(a.answer)
    ans["c"] = [canon(s) for s in ans.smiles]
    ans = ans.dropna(subset=["c"])
    files = sorted(glob.glob(os.path.join(a.dir,"*.csv")))
    if not files:
        print(f"제출 파일이 없습니다: {a.dir}"); return
    print(f"정답 {len(ans)}개 · 제출 {len(files)}건\n")

    rows = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        try:
            rows.append(score_one(read_submission(f), ans, name))
        except Exception as e:
            rows.append(dict(이름=name, 매칭=0, 비고=f"읽기 실패 — {str(e)[:44]}"))
    r = pd.DataFrame(rows)
    ok = r[r.get("Spearman").notna()] if "Spearman" in r else r.iloc[0:0]
    bad = r[~r.index.isin(ok.index)]

    if len(ok):
        ok = ok.sort_values(["Spearman","MAE"], ascending=[False,True]).reset_index(drop=True)
        ok.insert(0, "순위", range(1, len(ok)+1))
        print("═" * 74)
        print(" 순위 — Spearman 순 (26개뿐이라 순위를 주로 봅니다)")
        print("═" * 74)
        print(ok[["순위","이름","Spearman","MAE","R2","매칭","비고"]].to_string(index=False))
        print()
        y = ans.log_er.values; base = ans.log_er.median()
        print(f" 기준선 — 전부 중앙값({base:.2f})으로만 찍으면  MAE {np.abs(y-base).mean():.3f} · Spearman 0.000 · R2 {1-((y-base)**2).sum()/((y-y.mean())**2).sum():+.3f}")
        print(" 이 기준선을 못 넘으면 «맞혔다»고 할 수 없습니다.")
    if len(bad):
        print("\n 채점하지 못한 제출:")
        for _, b in bad.iterrows(): print(f"   {b['이름']:<16} {b['비고']}")

    if a.detail:
        f = [x for x in files if a.detail in os.path.basename(x)]
        if not f: print(f"\n'{a.detail}' 제출을 찾지 못했습니다"); return
        sub = read_submission(f[0]); sub["c"] = [canon(s) for s in sub.smiles]
        j = ans.merge(sub[["c","pred"]], on="c").copy()
        j["pred"] = to_log(j.pred.values, a.detail)
        j["오차"] = (j.pred - j.log_er).round(3)
        j = j.sort_values("오차", key=np.abs, ascending=False)
        print(f"\n═══ {a.detail} — 많이 틀린 순 ═══")
        print(j[["chembl_id","ER","log_er","pred","오차","nn_tanimoto"]].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
