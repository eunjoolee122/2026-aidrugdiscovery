# 4일차 실습 — REINVENT4로 de novo 분자 설계

**Google Colab에서 진행합니다.** 설치할 것도, 내려받을 것도 없습니다. 브라우저만 있으면 됩니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eunjoolee122/2026-aidrugdiscovery/blob/main/ligand_denovo_reinvent4.ipynb)

> 위 배지를 누르면 노트북이 Colab에서 바로 열립니다.

## 시작하기 — 이 순서대로

### 1. 노트북을 열고 내 드라이브에 복사합니다

배지를 눌러 노트북이 열리면 **파일 > 드라이브에 사본 저장**을 누릅니다.
사본에서 작업해야 중간에 바꾼 것이 남습니다. (복사하지 않아도 실습은 되지만, 닫으면 사라집니다.)

### 2. 런타임을 GPU로 바꿉니다 — 제일 먼저

**런타임 > 런타임 유형 변경 > T4 GPU > 저장**

학습 셀을 직접 돌려 보려면 GPU가 필요합니다. CPU로도 노트북 전체가 돌아가지만,
학습 셀은 전부 건너뛰고 미리 학습해 둔 결과를 받아 쓰게 됩니다.
노트북이 GPU를 자동으로 감지해 설정하므로, 그 외에 바꿀 것은 없습니다.

### 3. 위에서부터 순서대로 실행합니다

첫 셀(설치)에 **약 5분** 걸립니다. 코드와 모델을 합쳐 약 120 MB를 내려받고 패키지를 설치합니다.
설치가 끝난 뒤 Colab이 **세션 재시작**을 요구하면, 재시작하고 그 다음 셀부터 이어서 실행합니다.

`REINVENT 4.6.22 ...` 가 찍히면 정상입니다.

## 오늘 하는 것

| | 내용 | 직접 학습 |
|---|---|---|
| 3절 | **sigma 비교** — 같은 보상에 sigma만 128 / 16으로 바꿔 학습 양상을 비교 | 선택 |
| 4절 | **회전결합 보상 + diversity filter** — 생성 → sampling → scoring 전체 흐름 | 선택 |
| 5절 | **TrxR 과제** — 알려진 저해제 13개의 물성 프로파일을 목표로 RL, 상위 10% 선별, 다양성(IntDiv·#Circles) 측정 | 선택 |
| 6절 | **LibInvent** — 골격(4-anilinoquinazoline)은 고정하고 R-group만 설계 | 선택 |

**학습 셀은 전부 선택 사항입니다.** 건너뛰어도 그 다음 분석은 그대로 진행됩니다 —
같은 설정으로 미리 학습해 둔 체크포인트와 TensorBoard 로그를 노트북이 자동으로 받아
오기 때문입니다(`ensure(...)` 셀이 그 일을 합니다). 시간이 남으면 직접 돌려 보고,
부족하면 건너뛰십시오. **중요한 것은 학습을 기다리는 것이 아니라 결과를 읽는 것입니다.**

GPU에서도 RL 학습은 수 분에서 수십 분까지 걸립니다. 진행 상황은 화면이 아니라 로그
파일에 쌓이므로, 다른 셀에서 `!tail -20 {log}` 로 확인합니다.

## 산출물이 쌓이는 곳

```
/content/REINVENT4/work/
├── 01_sigma/       3절 — TOML · 로그 · 체크포인트
├── 02_rotbond/     4절
├── 03_trxr/        5절
└── 04_libinvent/   6절
```

직접 학습한 로그는 이름 뒤에 `_mine` 이 붙습니다. 미리 받아 둔 비교용 로그를
덮어쓰지 않기 위해서입니다.

**노트북이 쓰는 배포 자료** — 직접 내려받을 필요는 없습니다.

| | |
|---|---|
| [`reinvent4_slim.zip`](https://github.com/eunjoolee122/2026-aidrugdiscovery/releases/tag/asset-v3) | REINVENT4 코드 + prior 2종 (약 120 MB) |
| [`assets.zip`](https://github.com/eunjoolee122/2026-aidrugdiscovery/releases/tag/asset-v3) | 미리 학습한 체크포인트 · TensorBoard 로그 · 결과 CSV (약 320 MB) |

## 막혔을 때

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: reinvent` | 설치 셀 뒤 세션 재시작을 하지 않은 경우입니다. **런타임 > 세션 다시 시작** 후 설치 셀 다음부터 이어서 실행합니다. |
| 세션이 끊기고 `/content` 가 비었다 | Colab이 유휴 상태에서 런타임을 회수한 것입니다. 첫 셀부터 다시 실행하면 됩니다(설치 포함 5분). 드라이브 사본에 저장해 두었다면 코드는 그대로 있습니다. |
| 내려받기에 실패했습니다 | 네트워크 일시 오류가 대부분입니다. 셀을 다시 실행하세요. 계속 실패하면 강사에게 알려 주세요. |
| TensorBoard가 빈 화면이다 | 로그를 다 읽기 전입니다. 10~20초 기다렸다가 오른쪽 위 새로고침을 누릅니다. 그래도 비어 있으면 셀을 다시 실행하세요. |
| LibInvent에서 골격을 읽지 못한다 | 부착점 표기 문제입니다. 골격 SMILES의 `[*]` 를 `*` 로 바꿔 보세요. |
| GPU가 안 잡힌다 | **런타임 > 런타임 유형 변경**에서 T4 GPU인지 확인합니다. 무료 한도를 다 쓰면 CPU로 떨어질 수 있는데, 그래도 실습은 끝까지 진행됩니다. |

## 실습이 끝나고

노트북 각 절 끝의 **🎯 이제 여러분 차례** 를 꼭 보십시오. 보상 컴포넌트와 가중치,
transform 범위를 바꿔 가며 생성 분자가 어떻게 달라지는지 관찰하는 것이 이 실습의 핵심입니다.
정답은 하나가 아닙니다.

---

<details>
<summary>출처와 라이선스</summary>

REINVENT4 — AstraZeneca, Apache License 2.0.
<https://github.com/MolecularAI/REINVENT4>

Loeffler HH, et al. *Reinvent 4: Modern AI–driven generative molecule design.*
J Cheminform 16, 20 (2024).

</details>
