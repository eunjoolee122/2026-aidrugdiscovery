# 5일차 2부 — ADMET 예측 모델 만들기

## 설치 — 제일 먼저

터미널에서 `claude` 를 실행하고 **아래를 그대로 붙여넣습니다.**

```
https://github.com/eunjoolee122/2026-aidrugdiscovery 를 클론하고
day5-2-lab/setup/SETUP.md 대로 실습 환경을 만들어줘.
다 되면 00_check.py 를 돌리고, [FAIL]이 있으면 고쳐서 다시 돌려줘.
내가 직접 해야 할 게 있으면 알려줘. 프로그래밍은 잘 몰라.
```

설치가 도는 동안 **[LAB.md](LAB.md) 를 끝까지 한 번 읽습니다.**
오늘 무엇을 하는지 알고 시작해야 설치가 끝나자마자 바로 들어갈 수 있습니다.

자세한 설치 안내는 [setup/SETUP_PROMPT.md](setup/SETUP_PROMPT.md) 에 있습니다.

## 끝나면 이 두 줄을 확인합니다

```
[OK]   admet_ai (2.0.1이어야 함)        2.0.1
[OK]   ADMET-AI 값 대조                aspirin VDss -2.70 · 열 104개 — 자료와 일치
```

**하나라도 `[FAIL]` 이면 알려 주세요.**

## 실습 시간

**[LAB.md](LAB.md)** 를 따라갑니다.

---

## 폴더 안내

| | |
|---|---|
| `LAB.md` | **실습 때 이것만 보면 됩니다** |
| `setup/` | 설치 — 제일 먼저 합니다 |
| `data/er_dataset.csv` | 학습 데이터 2,642개 |
| `data/leaderboard_compounds.csv` | 리더보드용 26개 (정답 없음) |
| `data/admetlab3_leaderboard.csv` | 선택 단계용 — ADMETlab 3.0 결과를 미리 받아 둔 것 |
| `answers/` | 리더보드 정답과 채점 스크립트 — **예측을 저장한 뒤에 연다** |

## 필요한 것

| | |
|---|---|
| Claude Code | 이미 설치되어 있어야 합니다 |
| Python | **3.11 ~ 3.14** (3.10 이하는 안 됩니다) |
| 디스크 | 1.5 GB · 설치 중 약 400 MB 내려받습니다 |

> 설치가 오래 걸리는 것은 `torch`(124 MB)와 `rdkit`(25 MB) 때문입니다. 정상입니다.
