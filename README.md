# Susi_mario

수시마리오

목표: 수시 원서에 도달 -> 교사 박 모씨 제거
과정: 마리오 형식으로
결과: 시간 기록 기반 등급(백분율), 대응되는 대학 + 메시지 or 한강 철교 이미지

이미지:
	캐릭터 높이 160: 블록 1개
	점프 높이 블록 0~5칸
	너비 블록 1개	
	메뉴 화면
	menu_background.png - 메인 메뉴 배경 (1920x1080)
	title.png - 게임 타이틀 이미지 (선택사항)
	게임 플레이
	player.png - 플레이어 기본 이미지 (160x160)
	player_crouch.png - 플레이어 웅크리기 이미지 (160x80, 선택사항)
	background.png - 게임 배경 (천고 배경, 가로로 긴 타일 가능)
	application_form.png - 수시 원서 이미지 (160x160)
	블록
	block_normal.png - 일반 블록 (160x160)
	block_item.png - 아이템 블록 (160x160)
	block_pipe.png - 토관/논술 (160x320, 세로로 긴 형태)
	적 (Enemies)
	enemy_strong.png - 강한 적 (박건률) (160x160)
	enemy_weak.png - 약한 적 (오유준) (160x160)
	enemy_boss.png - 보스 (청마) (320x320, 2배 크기)
	아이템
	item_coffee.png - 커피 아이템 (무적) (160x160)
	item_general.png - 일반 아이템 (160x160)
	결과 화면
	bridge.png - 한강 철교 이미지 (선택사항, 등급 50% 미만 시 표시)
	UI 요소 (선택사항)
	button.png - 버튼 이미지
	button_hover.png - 버튼 호버 이미지
	pause_menu.png - 일시정지 메뉴 배경
	
시스템: 맵 불러오기(Json), 에디터
	메뉴 화면: 시작하기
			게임 제목
			배경
			설정
			게임 설명(목표, 기록 처리, 보상)

로직: 메인 파일(메뉴) + 목숨 표시
	게임 실행 함수(tq)
	사망 또는 클리어 시 함수 반환
	타이머
	
몹: 경쟁자(강-박건률 약-오유준 2개)
보스(청마 예정)

토관: 논술

커피(예정) = 무적 6초

아이템 블럭

효과음(예정)


배경: 천고

기록 저장: Json

기능: 점프(길이 조절), 아이템 소환, 웅크리기, 수시 원서 상호작용 연출

이미지: 배경, 플레이어, 보스, 몹, 아이템, 수시 원서, 한강 철교, 토관, 블럭(바닥, 아이템 블럭 등 종류별), 대학 로고, 메인 화면 배경, 버튼, 일시정지 버튼(나가기, 다시하기, 계속하기)

등급: 통계 제작(100개) -> 데이터 저장 -> 정렬 -> 백분률 계산 -> 등급

**개발**
파라미터: debug: bool = False
=> 디버깅 메시지 출력 여부
모든 함수에 추가

# 🎮 Susi_Mario 프로젝트 구조 및 설계

## main.py  
- **설명**: 게임의 진입점으로, 초기 설정 및 씬 전환 관리.  
- **함수**
  - `main() -> None`  
    - 게임 전체를 실행하는 메인 루프.  
    - 초기화 후 `MenuScene`으로 진입.

---

## game.py  
- **설명**: 실제 게임 진행을 담당. (맵 로딩, 충돌 처리, 점수 관리 등)
- **함수**
  - `run_game() -> int`  
    - 스테이지를 실행하고 클리어 또는 사망 시 점수를 반환.
  - `handle_collision(player_rect: pygame.Rect, blocks: list, items: list, enemies: list) -> dict`  
    - 충돌 여부를 판별하고 결과(`{"hit_enemy": bool, "got_item": bool}`)를 반환.
  - `reset_game() -> None`  
    - 모든 게임 오브젝트를 초기 상태로 복구.

---

## editor.py  
- **설명**: 간단한 맵 에디터 기능 (테스트용)
- **함수**
  - `open_editor() -> None`  
    - 맵 편집 인터페이스를 실행.
  - `save_map(map_data: list[list[int]]) -> None`  
    - 편집된 맵 데이터를 JSON 파일로 저장.

---

## scenes/

### menu.py  
- **클래스**: `MenuScene`
  - **메서드**
    - `__init__(self) -> None`
    - `update(self, events: list) -> str`  
      - 버튼 클릭 등 이벤트를 감지하고 다음 씬 이름(`"game"`, `"setting"`, `"exit"`) 반환.
    - `render(self, screen: pygame.Surface) -> None`

---

### result.py  
- **클래스**: `ResultScene`
  - **메서드**
    - `__init__(self, score: int) -> None`
    - `update(self, events: list) -> str`  
      - 다시하기 / 메뉴로 돌아가기 버튼 처리.
    - `render(self, screen: pygame.Surface) -> None`

---

### setting.py  
- **클래스**: `SettingScene`
  - **메서드**
    - `__init__(self, config: dict) -> None`
    - `update(self, events: list) -> str`  
      - 사운드 on/off, 난이도 변경 등.
    - `render(self, screen: pygame.Surface) -> None`

---

## entities/

### enemy.py  
- **함수**
  - `spawn_enemies(map_data: list[list[int]]) -> list[dict]`  
    - 맵 정보에 따라 적의 위치를 생성해 리스트 반환.  
  - `update_enemies(enemies: list[dict], dt: float) -> None`  
    - 각 적의 위치 및 상태 업데이트.  
  - `draw_enemies(screen: pygame.Surface, enemies: list[dict]) -> None`

---

### item.py  
- **함수**
  - `spawn_items(map_data: list[list[int]]) -> list[dict]`
  - `update_items(items: list[dict], dt: float) -> None`
  - `draw_items(screen: pygame.Surface, items: list[dict]) -> None`

---

### block.py  
- **함수**
  - `load_blocks(map_data: list[list[int]]) -> list[pygame.Rect]`  
    - 맵 데이터를 읽어 충돌용 블록 좌표 생성.
  - `draw_blocks(screen: pygame.Surface, blocks: list[pygame.Rect]) -> None`

---

## assets/

### images/
- 배경, 블록, 적, 아이템 등의 이미지 파일 (.png)

### sounds/
- 효과음, 배경음악 파일 (.wav, .mp3)

---

## data/

### maps/
- 스테이지 맵 데이터 (.json 또는 .txt)

### record.json  
- 최고 점수, 설정값 저장 파일

---

## utils/

### json_loader.py  
- **함수**
  - `load_json(path: str) -> dict | list`  
    - JSON 파일 읽기  
  - `save_json(path: str, data: dict | list) -> None`

### config.py  
- **클래스**: `Config`
  - **속성**: `screen_width`, `screen_height`, `volume`, `difficulty`
  - **메서드**
    - `load(self, path: str) -> None`
    - `save(self, path: str) -> None`

---

## 요약
- **씬 구조**: `Menu → Game → Result`  
- **엔티티 구조**: 적, 아이템, 블록은 함수 기반으로 관리  
- **데이터 관리**: JSON 기반 (맵, 설정, 기록)  
- **확장성**: 스테이지 1개 기준으로 최소 구조 유지
