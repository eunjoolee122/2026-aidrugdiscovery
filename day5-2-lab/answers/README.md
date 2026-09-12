# 리더보드 정답

**예측 파일을 저장한 뒤에 연다.** 먼저 보면 이 단계에서 배울 것이 없어진다.

| 파일 | 내용 |
|---|---|
| `leaderboard_answer.csv` | 26개의 실측 ER · log ER |
| `leaderboard_idmap.csv` | `C01`~`C26` ↔ ChEMBL ID |
| `score.py` | 제출 CSV 채점 |

## 자기 예측을 채점하려면

```bash
python day5-2-lab/answers/score.py 내제출.csv
```

ER로 냈든 log ER로 냈든 알아서 맞춰 준다.

## 점수가 낮아도 정상이다

학습 데이터는 Biogen 한 실험실에서, 이 26개는 다른 논문에서 나왔다.
**같은 화합물을 다른 실험실에서 재면 평균 5.2배 차이가 난다.**
낮은 점수 자체보다 **왜 낮은지 설명할 수 있는가**가 이 실습의 목표였다.

**출처** — ChEMBL. `nn_tanimoto` 는 학습 데이터와의 최근접 이웃 유사도다.
