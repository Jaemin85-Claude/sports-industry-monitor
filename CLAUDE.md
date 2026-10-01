# sports-industry-monitor — Claude Code 작업 규칙

스포츠 브랜드·유통사 재무, 공시, 국내 지표, 뉴스를 GitHub Actions로 매일 모아
단일 HTML 대시보드(GitHub Pages, `docs/index.html`)로 보여주는 레포.

## 역할 분담 (가장 중요)

- 코드는 **claude.ai 채팅에서 작성·검증된 최종본**을 받는다. Claude Code는 **반영 · 실행 · 보고**만 한다.
- 받은 파일의 내용을 고치지 않는다. 문제가 보이면 커밋하지 말고 그대로 보고한다.
- 보고는 한국어로, 짧게.

## 운영 구조

| 워크플로우 파일 | 이름 | 실행하는 코드 | 만드는 파일 | 자동 실행(KST) |
|---|---|---|---|---|
| `update.yml` | update-dashboard | fetch_data.py → history_append.py → build_dashboard.py | `docs/` (data·history·index.html) | 매일 07:30 |
| `news.yml` | update-news | news_monitor.py | `docs/news.json` | 매일 06:30 |
| `segments.yml` | extract-segments | extract_segments.py | `docs/segments.json` | 매주 월 05:00 |
| `ir.yml` | update-ir | ir_fetch.py | `docs/segments_ir.json` | 매주 일 06:00 |
| `dart.yml` | update-dart | dart_fetch.py | `docs/kr_domestic.json`, `docs/kr_listed_fin.json` | 매월 15일 07:00 |
| `kosis.yml` | update-kosis | kosis_fetch.py | `docs/kosis.json` | 매월 5일 06:00 |

- 데이터 워크플로우가 `docs/*.json`을 만들고, **update-dashboard가 마지막에 화면을 다시 만든다.**
- 워크플로우들이 main에 직접 커밋하므로, 로컬 작업 전후에 항상 `git pull --rebase origin main`.

## 파일 식별표 (반영 전 반드시 확인)

파이썬 파일은 **3번째 줄**에 아래 문구가 있어야 한다. 다르면 다른 파일 내용이 섞인 것이다.

| 파일 | 3번째 줄에 있어야 할 문구 | 위치 |
|---|---|---|
| fetch_data.py | `Phase 1 데이터 수집` | 최상위 |
| news_monitor.py | `Phase 4: 뉴스 모니터링` | 최상위 |
| build_dashboard.py | `단일 HTML 대시보드 빌드` | 최상위 |
| extract_segments.py | `Phase 2: 공시 추출` | 최상위 |
| dart_fetch.py | `Phase 6: DART` | 최상위 |
| kosis_fetch.py | `Phase 5: KOSIS` | 최상위 |
| history_append.py | `히스토리 축적` | 최상위 |
| ir_fetch.py | `Phase 7` | 최상위 |
| worldmap.json | JSON 최상위 키에 `viewBox`, `europe` | `docs/` |
| *.yml | 첫 `name:` 줄 = 위 운영 구조표의 이름 | `.github/workflows/` |

표에 없는 새 파일은 넣기 전에 위치를 물어본다.

## 반영 루틴 ("반영해줘")

1. `git pull --rebase origin main`
2. 다운로드 폴더(`C:\Users\night\Downloads`)에서 지시받은 파일을 찾는다.
   브라우저가 `fetch_data (1).py`처럼 이름을 바꿨을 수 있으니, 같은 이름 계열 중 **가장 최근에 받은 파일**을 쓴다.
3. **식별표로 확인**한다. 하나라도 다르면 전부 멈추고, 그 파일의 3번째 줄을 그대로 인용해 보고한다.
4. 원래 이름으로 제자리에 복사한다.
5. 검사: `.py`는 `python -m py_compile <파일>`, `.json`은 파싱. 실패하면 멈추고 보고.
6. 커밋 메시지: 각 파일 설명 블록의 맨 위 버전 줄(예: `v29:`, `v4.3:`)을 모아
   `반영: build_dashboard v29 · fetch_data v4.3 · news_monitor v2.3` 형식.
7. `git push`. 거절되면 `git pull --rebase origin main` 후 재시도(최대 2회).
8. 워크플로우 실행 — 지시가 있으면 그대로. 없으면 바뀐 파일 기준:
   - news_monitor → `news.yml` · extract_segments → `segments.yml` · ir_fetch → `ir.yml`
   - dart_fetch → `dart.yml` · kosis_fetch → `kosis.yml`
   - 그리고 **항상 마지막에** `update.yml` (화면 다시 만들기)
   - **하나씩 차례로**: `gh workflow run <파일>` → 10초 대기 →
     `gh run list --workflow <파일> --event workflow_dispatch --limit 1 --json databaseId,status,createdAt` →
     `gh run watch <id> --exit-status` (끝날 때까지 기다림)
9. 로그 핵심 줄만 뽑는다: `gh run view <id> --log` 에서
   - 공통: `saved`, `ERROR`, `FATAL`, `Traceback`, `실패`, `Error:`
   - update-dashboard: `재시도`, `비어 있음`, `환율`, `병합`, 그리고 채팅에서 지정한 줄
   - update-news: `수집`, `신규`
10. `git pull --rebase origin main` (워크플로우가 만든 커밋 받기)
11. 보고:
    - 반영한 파일과 버전
    - 워크플로우별 성공/실패와 걸린 시간
    - 로그 핵심 줄(원문 그대로)
    - 대표가 화면에서 확인할 것(채팅에서 받은 확인 항목이 있으면 그대로 옮김)

## 하지 말 것

- API 키 등 비밀값을 출력하거나 커밋하지 않는다(키는 GitHub Secrets에만 있음).
- `docs/`의 데이터 파일(`*.json`, `index.html`)을 손으로 고치지 않는다. 워크플로우가 만든다. 예외: worldmap.json처럼 채팅에서 받은 고정 파일.
- 강제 푸시(`--force`) 금지. 브랜치 만들지 않음(main만 사용).
- 워크플로우를 동시에 여러 개 돌리지 않는다(같은 파일을 커밋하다 충돌남).

## 참고

- 대시보드: https://jaemin85-claude.github.io/sports-industry-monitor/
- 수집이 멈추면 대시보드 종합 탭 맨 아래 "수집 상태"에 지연으로 표시된다.
- 반영 직후 화면이 그대로면 GitHub Pages 반영(1~2분)과 브라우저 캐시 때문이다.
