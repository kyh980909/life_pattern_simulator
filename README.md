# life_pattern_simulator

간단한 생활 패턴 시뮬레이터 예제입니다. 다음과 같은 모듈을 포함합니다.

* `test.py` – Tkinter 기반 시뮬레이션 UI. `rules.json`에 저장된 규칙을 읽어
  시뮬레이션 시간에 맞춰 자동화 이벤트를 발생시킵니다.
* `chatbot.py` – 터미널 챗봇. `"22:00에 거실 조명 꺼줘"`와 같은 문장을
  입력하면 시간과 동작을 추출하여 규칙을 제안하고 `rules.json`에 저장합니다.
* `rule_set.py` – 규칙을 관리하고 로드/저장하는 모듈.
* `data_generator.py` – 스크립트 기반 데이터셋을 생성하여 CSV 파일로 저장
  할 수 있는 도구.

예시:

```bash
python chatbot.py  # 규칙 생성
python test.py     # 시뮬레이션 UI 실행
```
