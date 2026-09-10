# 실습 환경 설치 — Windows · macOS · Linux

> 소요 시간 15~25분 · 다운로드 약 400 MB
> **강의가 시작될 때 걸어 두고 강의를 듣는다.** 쉬는 시간에 결과만 확인하면 된다.

## 0. 준비물

| | |
|---|---|
| **Python** | **3.11 · 3.12 · 3.13 중 하나** (3.10 이하 · 3.15 이상은 안 된다) |
| 디스크 | 약 1.5 GB |
| 네트워크 | 설치와 첫 데이터 다운로드에 필요 |

**왜 3.11 이상인가** — 실습에서 쓰는 `chemprop 2.x`가 `>=3.11,<3.15`를 요구한다.
3.10에서 `pip install chemprop`을 하면 **API가 완전히 다른 1.6.1이 설치되어** 실습 코드가 돌지 않는다.

### 지금 버전 확인

```
python --version
```

macOS·Linux에서는 `python3 --version`도 확인한다.

> **주의 — `python3.12`라는 이름이 없을 수 있다.**
> macOS 기본 `python3`는 3.9~3.10인 경우가 많다.
> `python3 --version`이 **3.10 이하이면 그대로 쓰면 안 된다.**
> 그대로 진행하면 `chemprop`이 2.x가 아니라 **1.6.1**로 깔리는데,
> API가 완전히 달라서 실습 코드가 하나도 돌지 않는다.

**3.11~3.14가 아니면** [python.org](https://www.python.org/downloads/)에서 **3.12**를 받는다.

- **Windows** — 설치 첫 화면의 **"Add python.exe to PATH"를 반드시 체크**한다
- **macOS** — python.org 설치본을 쓰면 `python3.12` 명령이 생긴다.
  Homebrew를 쓴다면 `brew install python@3.12`
- **Linux** — `sudo apt install python3.12 python3.12-venv`

설치 후 `python3.12 --version`으로 확인한다.

---

## 1. Windows

**PowerShell**을 연다 (시작 메뉴 → `powershell`).

```powershell
cd $HOME\Desktop
mkdir admet-lab
cd admet-lab

py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps -r requirements-tdc.txt
pip install --no-deps -r requirements-admetai.txt
```

> `requirements-admetai.txt`는 **git**이 필요하다. 없으면
> [git-scm.com](https://git-scm.com/download/win)에서 설치한다.

**`Activate.ps1` 실행이 차단되면** — PowerShell에서 한 번만 실행한다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**한글이 깨지면** — 같은 창에서 실행한다.

```powershell
$env:PYTHONUTF8 = "1"
```

---

## 2. macOS · Linux

**터미널**을 연다.

```bash
cd ~/Desktop
mkdir admet-lab && cd admet-lab

python3.12 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps -r requirements-tdc.txt
pip install --no-deps -r requirements-admetai.txt
```

**`python3.12` 명령이 없다면** — `python3 --version`을 확인한다.

| 결과 | 어떻게 |
|---|---|
| 3.11 ~ 3.14 | `python3 -m venv venv`로 진행해도 된다 |
| **3.10 이하** | **그대로 쓰면 안 된다.** 위 「0. 준비물」로 돌아가 3.12를 설치한다 |

conda/mambaforge를 쓰고 있다면 그 안의 파이썬을 써도 되지만,
**그 환경을 지우면 실습 환경도 함께 깨진다.** 독립적으로 쓰려면 python.org 설치본을 권한다.

---

### 왜 설치를 두 번 하는가

`PyTDC`가 `scikit-learn==1.2.2` · `cellxgene-census` · `numpy<2.0` · `pandas<3.0`을
**고정으로** 요구한다. 한꺼번에 설치하면 이렇게 실패한다.

```
ERROR: pytdc 1.1.15 depends on cellxgene-census==1.15.0
ERROR: ResolutionImpossible
```

`--no-deps`로 PyTDC 본체만 넣고, 실제로 쓰는 몇 개(`requests` 등)를 직접 지정하면
최신 패키지를 그대로 두고 쓸 수 있다. 이 방식으로 실제 검증을 마쳤다.

---

## 3. 점검 — 반드시 실행한다

`requirements*.txt` 세 개와 `00_check.py`를 같은 폴더에 두고 실행한다.

```
python 00_check.py
```

이렇게 나오면 성공이다.

```
==============================================================
 실습 환경 점검   Windows AMD64
==============================================================
[OK]   Python 버전                  3.12.x
[OK]   rdkit                        2026.03.x
[OK]   scikit-learn                 1.9.x
[OK]   pandas                       3.0.x
[OK]   numpy                        2.x
[OK]   torch                        2.x
[OK]   chemprop                     2.3.x
[OK]   PyTDC                        1.1.x
[OK]   TDC 데이터 다운로드                 Caco2_Wang 910개 내려받음
[OK]   학습·평가 전체 실행                  MAE 0.4xx (참고값 0.4~0.5)
[OK]   chemprop 학습                  D-MPNN 1에폭 통과
==============================================================
 모두 통과. 실습을 시작할 수 있다.
==============================================================
```

**하나라도 `[FAIL]`이면 쉬는 시간에 알려 준다.** 실습 시작 전에 고치면 된다.

---

## 4. 문제 해결

### `chemprop`이 1.6.1로 깔렸다

파이썬이 3.10 이하다. 3.11 이상으로 새 가상환경을 만든다.
`pip index versions chemprop`으로 확인하면 3.10에서는 1.6.1까지만 보인다.

### `ModuleNotFoundError: No module named 'pkg_resources'`

`setuptools`가 81 이상이다. TDC가 아직 `pkg_resources`를 쓴다.

```
pip install "setuptools<81"
```

### `torch` 설치가 매우 느리다 / 중간에 끊긴다

파일이 124 MB다. 유선 네트워크에서 다시 시도하거나 아래로 CPU 전용판을 받는다.

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**GPU는 필요 없다.** 실습 전체가 CPU에서 몇 분 안에 끝난다.

### Windows에서 한글이 `?`로 나온다

콘솔 인코딩이 cp949다.

```powershell
$env:PYTHONUTF8 = "1"
```

영구 적용은 **시스템 → 국가 또는 지역 → 관리자 언어 설정 →
시스템 로캘 변경 → "세계 언어 지원을 위한 Beta: UTF-8 사용"** 체크.

### TDC 다운로드가 실패한다

**실습에 지장이 없다.** 점검 스크립트도 이 항목만 실패하면 경고로 넘어간다.
회사·학교 네트워크의 프록시나 방화벽이 원인인 경우가 많다.

**같은 폴더의 `data/`** 에 같은 데이터가 CSV로 들어 있다. 점검 스크립트가 자동으로 이걸 쓴다.

| 파일 | 내용 |
|---|---|
| `caco2_full.csv` | 전체 910행 |
| `caco2_train_val.csv` | 공식 train_val 728 |
| `caco2_test.csv` | 공식 test 182 (고정) |
| `caco2_official_splits.csv` | 시드 1~5의 train/valid 인덱스 |

이 CSV만으로 리더보드와 같은 절차를 재현할 수 있다.

### `pip install`에서 «Microsoft Visual C++ 14.0 required»

Windows에서 컴파일이 필요한 패키지를 소스로 받을 때 나온다.
`pip`을 먼저 최신으로 올리면 미리 만들어진 파일(휠)을 받아 해결되는 경우가 대부분이다.

```
python -m pip install --upgrade pip
```

---

## 5. 다음 실습 때 다시 시작하기

가상환경만 다시 켜면 된다. 설치는 반복하지 않는다.

```powershell
cd $HOME\Desktop\admet-lab
.\venv\Scripts\Activate.ps1
```

```bash
cd ~/Desktop/admet-lab
source venv/bin/activate
```

---

## 참고 — 왜 이 구성인가

| 패키지 | 배포 형태 | Windows |
|---|---|---|
| chemprop 2.3.1 | `py3-none-any` (순수 파이썬) | 문제 없음 |
| lightning | `py3-none-any` | 문제 없음 |
| PyTDC | 소스 배포 (순수 파이썬) | 컴파일러 불필요 |
| torch 2.14 | Windows 전용 휠 (124 MB) | cp311~cp314 제공 |
| rdkit | Windows 전용 휠 (25 MB) | cp310~cp314 제공 |
| scikit-learn | Windows 전용 휠 | 제공 |

**ADMET-AI는 GitHub 태그에서 받는다.** PyPI의 1.4.0은 값이 다르다
(aspirin VDss가 −2.70이 아니라 +6.69, 열이 104개가 아니라 98개).
`v_2.0.1` 태그로 설치하면 **강의자료의 값이 그대로 재현된다** — 빈 가상환경에서 9/9 일치를 확인했다.
MIT 라이선스이고 모델 가중치 13 MB가 패키지에 동봉되어 있어 별도 다운로드가 없다.
