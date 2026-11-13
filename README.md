# 2026 AI 신약개발 — 실습 자료

일차별 실습 안내입니다. **먼저 해당 일차의 안내 문서를 열어 보세요.**

## 4일차 — 리간드 기반 신약설계와 생성모델

| | |
|---|---|
| 안내 | **[day4-lab/README.md](day4-lab/README.md)** |
| 노트북 | [ligand_denovo_reinvent4.ipynb](ligand_denovo_reinvent4.ipynb) |
| 환경 | **Google Colab** — 브라우저만 있으면 됩니다 |

REINVENT4로 de novo 분자 설계를 합니다. 강화학습으로 물성을 최적화하고(sigma·diversity
filter), 생성한 분자를 sampling·scoring으로 평가하며, LibInvent로 골격을 고정한 채
R-group을 설계합니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eunjoolee122/2026-aidrugdiscovery/blob/main/ligand_denovo_reinvent4.ipynb)

## 5일차 — ADMET 예측

### 1부 — ADMET 예측과 결과 해석

Claude와 대화하며 진행합니다. 아래 노트북은 **대체용**입니다 — Claude에서 코드 실행이
되지 않거나 `pip install`이 막혔을 때 Colab에서 같은 내용을 따라갈 수 있습니다.

| | |
|---|---|
| 대체용 노트북 | [admet_day5.ipynb](admet_day5.ipynb) · Colab |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eunjoolee122/2026-aidrugdiscovery/blob/main/admet_day5.ipynb)

### 2부 — ADMET 예측 모델 만들기

| | |
|---|---|
| 안내 | **[day5-2-lab/README.md](day5-2-lab/README.md)** |
| 실습 | [day5-2-lab/LAB.md](day5-2-lab/LAB.md) |
| 환경 | **내 컴퓨터 + Claude Code** — 설치가 필요하므로 안내 문서를 먼저 보세요 |
