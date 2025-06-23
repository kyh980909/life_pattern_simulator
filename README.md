# life_pattern_simulator

간단한 생활 패턴 시뮬레이터 예제입니다. 다음과 같은 모듈을 포함합니다.

* `test.py` – Tkinter 기반 시뮬레이션 UI.
  탭 메뉴(학습데이터 생성/학습/서비스/환경설정/조회메뉴)를 제공하며
  `rules.json`에 저장된 규칙을 불러와 시뮬레이션 시간을 진행합니다.
* `chatbot.py` – 터미널 챗봇. `"22:00에 거실 조명 꺼줘"`와 같은 문장을
  입력하면 시간과 동작을 추출하여 규칙을 제안하고 `rules.json`에 저장합니다.
  데이터셋 CSV를 인자로 주면 패턴을 분석해 권고를 제안합니다.
* `rule_set.py` – 규칙을 관리하고 로드/저장하는 모듈.
* `data_generator.py` – 스크립트 기반 데이터셋을 생성하여 CSV 파일로 저장
  할 수 있는 도구.
* `pattern_analyzer.py` – CSV 데이터에서 반복 패턴을 찾아 자동화 규칙을
  추천합니다.

데이터 생성 예시:

```bash
python data_generator.py  # sample_data.csv 생성
```

실행 예시:

```bash
python chatbot.py generated_data.csv  # 데이터셋 분석 후 규칙 생성
python test.py                       # 탭 기반 UI 실행
```

## 모의 사용패턴 입력 UI
- 디바이스/시간/동작을 직접 입력하여 Treeview에 추가하는 예시 기능을 준비했습니다.

