# 실습 환경 설치 — Windows · macOS · Linux

> **[SETUP_PROMPT.md](SETUP_PROMPT.md) 의 프롬프트를 Claude에 붙여넣는 것이 가장 쉽습니다.**
> 이 문서는 그게 막혔을 때 손으로 하는 방법입니다.

> 15~25분 · 내려받기 약 400 MB · 설치 후 가상환경 크기 약 1.2 GB

---

## 0. 파이썬 버전 확인

**Python 3.11 ~ 3.14** 가 필요합니다.

```
python3 --version
```

> **왜 3.11 이상인가** — 실습에서 쓰는 `chemprop 2.x` 의 요구사항입니다.
> 3.10에서 `pip install chemprop` 을 하면 **API가 완전히 다른 1.6.1이 설치되어**
> 실습 코드가 하나도 돌지 않습니다.

### 3.10 이하가 나왔다면

**macOS는 이게 기본입니다.** 대부분 3.12를 새로 설치해야 합니다 —
[python.org](https://www.python.org/downloads/) 에서 **3.12** 를 받는 것이 가장 확실합니다.

다만 conda·Homebrew를 쓰고 있다면 **이미 3.11 이상이 들어 있을 수 있으니** 먼저 확인해 봅니다.

```bash
# macOS · Linux — 아래를 하나씩 쳐 봅니다
python3.12 --version
ls /opt/homebrew/bin/python3.1*        # Homebrew
ls ~/opt/*/envs/*/bin/python           # conda · mambaforge
conda env list                          # conda를 쓴다면
```

```powershell
# Windows
py -0                                   # 설치된 파이썬 목록
```

하나도 없으면 [python.org](https://www.python.org/downloads/) 에서 **3.12** 를 받습니다.
**Windows는 설치 첫 화면의 "Add python.exe to PATH" 를 반드시 체크**합니다.
설치 후 `python3.12 --version` (Windows는 `py -3.12 --version`) 으로 확인합니다.

> conda·mambaforge 안의 파이썬을 써도 됩니다.
> 다만 **그 환경을 지우면 실습 환경도 함께 깨집니다.**

---

## 1. 자료 내려받기

```bash
git clone https://github.com/eunjoolee122/2026-aidrugdiscovery.git
cd 2026-aidrugdiscovery/day5-2-lab/setup
```

`git` 이 없으면 [git-scm.com](https://git-scm.com/downloads) 에서 받거나,
저장소 페이지의 **Code → Download ZIP** 으로 받아 풀어도 됩니다.

> **이 `setup` 폴더 안에서 계속 작업합니다.**
> `requirements*.txt` · `00_check.py` · `data/` 가 모두 여기 있으므로
> 파일을 어디로 옮길 필요가 없습니다.

---

## 2. 가상환경 만들고 설치하기

### Windows (PowerShell)

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps -r requirements-tdc.txt
pip install --no-deps -r requirements-admetai.txt
```

**`Activate.ps1` 실행이 차단되면** — 한 번만 실행합니다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**한글이 깨지면** — 같은 창에서 실행합니다.

```powershell
$env:PYTHONUTF8 = "1"
```

### macOS · Linux

```bash
python3.12 -m venv venv          # 0절에서 찾은 파이썬 경로를 씁니다
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps -r requirements-tdc.txt
pip install --no-deps -r requirements-admetai.txt
```

### 왜 설치를 세 번 나눠서 하는가

`PyTDC` 와 `admet_ai` 가 `scikit-learn==1.2.2` · `numpy<2.0` · `pandas<3.0` 을
**고정으로** 요구합니다. 한꺼번에 설치하면 이렇게 실패합니다.

```
ERROR: pytdc 1.1.15 depends on cellxgene-census==1.15.0
ERROR: ResolutionImpossible
```

`--no-deps` 로 본체만 넣고 실제로 필요한 것들은 requirements 파일에 따로 적어 두었습니다.
**순서를 바꾸거나 `--no-deps` 를 빼면 안 됩니다.**

> **세 번째 줄에서 몇 분간 멈춘 것처럼 보입니다.** `admet_ai` 를 GitHub에서
> 소스로 받아 직접 빌드하기 때문입니다. 정상이니 기다립니다.

---

## 3. 점검 — 반드시 실행합니다

```
python 00_check.py
```

이렇게 **13줄**이 나오면 성공입니다.
첫 줄의 `Darwin arm64` 자리에는 자기 운영체제가 나옵니다 — Windows면 `Windows AMD64` 입니다.

```
==============================================================
 실습 환경 점검   Darwin arm64
==============================================================
[OK]   Python 버전                  3.12.x
[OK]   rdkit                        2026.03.x
[OK]   scikit-learn                 1.9.x
[OK]   pandas                       3.0.x
[OK]   numpy                        2.x
[OK]   torch                        2.x
[OK]   chemprop                     2.3.x
[OK]   PyTDC                        1.1.x
[OK]   admet_ai (2.0.1이어야 함)        2.0.1
[OK]   ADMET-AI 값 대조                aspirin VDss -2.70 · 열 104개 — 자료와 일치
[OK]   TDC 데이터 다운로드                 Caco2_Wang 910개
[OK]   학습·평가 전체 실행                  MAE 0.4xx (TDC 사용 · 참고값 0.3~0.5)
[OK]   chemprop 학습                  D-MPNN 1에폭 통과
==============================================================
 모두 통과. 실습을 시작할 수 있다.
==============================================================
```

**아래 두 줄을 특히 확인합니다.**

```
[OK]   admet_ai (2.0.1이어야 함)        2.0.1
[OK]   ADMET-AI 값 대조                aspirin VDss -2.70 · 열 104개 — 자료와 일치
```

여기가 `[FAIL]` 이면 버전이 잘못 깔린 것입니다.

**하나라도 `[FAIL]` 이면 쉬는 시간에 알려 주세요.** 실습 시작 전에 고치면 됩니다.

---

## 4. 문제 해결

### `ERROR: Could not open requirements file`

`setup` 폴더 밖에서 실행했습니다. 1절의 `cd` 로 돌아갑니다.

```bash
cd 2026-aidrugdiscovery/day5-2-lab/setup
```

### `chemprop` 이 1.6.1로 깔렸다

파이썬이 3.10 이하입니다. 0절로 돌아가 3.11 이상으로 가상환경을 새로 만듭니다.

### `ModuleNotFoundError: No module named 'pkg_resources'`

`setuptools` 가 81 이상입니다. TDC가 아직 그 모듈을 씁니다.

```
pip install "setuptools<81"
```

### `torch` 설치가 매우 느리다 / 끊긴다

파일이 124 MB입니다. 유선 네트워크에서 다시 시도하거나 CPU 전용판을 받습니다.

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**GPU는 필요 없습니다.** 실습 전체가 CPU에서 돌아갑니다.

### `admet_ai` 설치에서 git 오류

`requirements-admetai.txt` 는 GitHub에서 소스를 받습니다.
[git-scm.com](https://git-scm.com/downloads) 에서 git을 설치한 뒤 그 줄만 다시 실행합니다.

### Windows에서 한글이 `?` 로 나온다

```powershell
$env:PYTHONUTF8 = "1"
```

영구 적용은 **설정 → 시간 및 언어 → 언어 및 지역 → 관리 언어 설정 →
시스템 로캘 변경 → "세계 언어 지원을 위한 Beta: UTF-8 사용"** 체크.

### TDC 다운로드가 실패한다

**실습에 지장이 없습니다.** 점검 스크립트도 이 항목만 실패하면 경고로 넘어갑니다.
회사·학교 네트워크의 프록시나 방화벽이 원인인 경우가 많습니다.

같은 폴더의 `data/` 에 CSV가 들어 있고 점검 스크립트가 자동으로 그걸 씁니다.

---

## 5. 다음에 다시 시작할 때

설치는 반복하지 않습니다. 가상환경만 다시 켭니다.

**Windows (PowerShell)**

```powershell
cd 2026-aidrugdiscovery\day5-2-lab\setup
.\venv\Scripts\Activate.ps1
```

**macOS · Linux**

```bash
cd 2026-aidrugdiscovery/day5-2-lab/setup
source venv/bin/activate
```

> 가상환경은 **폴더 경로가 바뀌면 깨집니다.** 만들고 나서 폴더를 옮기지 않습니다.
> 옮겨야 한다면 `venv` 를 지우고 2절을 다시 합니다.

---

## 참고 — 왜 이 구성인가

| 패키지 | 배포 형태 | Windows |
|---|---|---|
| chemprop 2.3.1 · lightning | `py3-none-any` (순수 파이썬) | 문제 없음 |
| PyTDC | 소스 배포 (순수 파이썬) | 컴파일러 불필요 |
| torch 2.14 | Windows 휠 (124 MB) | cp311~cp314 제공 |
| rdkit | Windows 휠 (25 MB) | cp310~cp314 제공 |

**ADMET-AI는 GitHub 태그에서 받습니다.** PyPI의 1.4.0은 값이 다릅니다
(aspirin VDss가 −2.70이 아니라 +6.69, 열이 104개가 아니라 98개).
`v_2.0.1` 태그로 설치하면 강의자료의 값이 그대로 재현됩니다.
MIT 라이선스이고 모델 가중치 13 MB가 패키지에 동봉되어 있어 별도 다운로드가 없습니다.
