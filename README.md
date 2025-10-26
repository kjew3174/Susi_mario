# Susi_mario

수시마리오

목표: 수시 원서에 도달 -> 교사 박 모씨 제거
과정: 마리오 형식으로
결과: 시간 기록 기반 등급(백분율), 대응되는 대학 + 메시지 or 한강 철교 이미지

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

Susi_Mario/
├─ main.py
│ ├─ main() -> None
│ │ ├─ 초기화 및 첫 씬(menu) 실행
│ │ └─ 씬 전환 제어 (menu → game → result)
│
├─ game.py
│ ├─ run_game(map_path: str) -> dict
│ │ ├─ 맵 로드(load_map)
│ │ ├─ 루프: handle_events → update → render
│ │ ├─ 종료 조건: 클리어 or 사망
│ │ └─ return {"status": "clear"/"dead", "time": float}
│ │
│ ├─ load_map(map_path: str) -> dict
│ │ └─ JSON 파일에서 블럭, 몹, 아이템 정보 불러오기
│ │
│ ├─ handle_events(keys: dict) -> None
│ │ └─ 이동, 점프, 웅크리기 등 입력 처리
│ │
│ ├─ update(dt: float, player: dict, enemies: list, items: list) -> None
│ │ ├─ 중력 적용
│ │ ├─ 충돌 판정 (player vs block / enemy / item)
│ │ └─ 효과 적용 (아이템, 피격 등)
│ │
│ ├─ render(screen: pygame.Surface, data: dict) -> None
│ │ └─ 배경, 플레이어, 몹, UI(시간·목숨) 렌더링
│ │
│ ├─ reset_player() -> dict
│ │ └─ 플레이어 초기 좌표, 상태(dict) 반환
│ │
│ └─ reset_boss() -> dict
│ └─ 보스 초기 좌표, 체력 상태(dict) 반환
│
├─ editor.py
│ ├─ run_editor() -> None
│ │ └─ 맵 수정 루프 (오브젝트 추가·삭제)
│ │
│ ├─ load_map(path: str) -> dict
│ ├─ save_map(path: str, data: dict) -> None
│ ├─ add_object(obj_type: str, x: int, y: int) -> None
│ └─ remove_object(x: int, y: int) -> None
│
├─ scenes/
│ ├─ menu.py
│ │ ├─ run_menu(screen: pygame.Surface) -> str
│ │ │ ├─ 시작 / 설정 / 종료 중 선택
│ │ │ └─ return "start" / "setting" / "quit"
│ │
│ ├─ result.py
│ │ ├─ run_result(screen: pygame.Surface, result: dict) -> str
│ │ │ ├─ 결과 표시, 기록 저장(save_record)
│ │ │ └─ return "retry" / "menu"
│ │
│ └─ setting.py
│ ├─ run_setting(screen: pygame.Surface) -> None
│ │ ├─ 볼륨, 키 변경 등 설정 UI
│ │ └─ 저장(save_settings)
│ ├─ load_settings() -> dict
│ └─ save_settings(settings: dict) -> None
│
├─ entities/
│ ├─ enemy.py
│ │ ├─ create_enemy(x: int, y: int, speed: float) -> dict
│ │ │ └─ {"x": int, "y": int, "speed": float, "dir": 1}
│ │ ├─ move_enemy(enemy: dict, dt: float, blocks: list) -> None
│ │ └─ check_collision(enemy: dict, player_rect: pygame.Rect) -> bool
│ │
│ ├─ item.py
│ │ ├─ create_item(x: int, y: int, item_type: str) -> dict
│ │ │ └─ {"x": int, "y": int, "type": "coffee"/"extra_life"}
│ │ └─ apply_item_effect(player: dict, item_type: str) -> None
│ │ └─ 무적/체력 증가 등 처리
│ │
│ └─ block.py
│ ├─ create_block(x: int, y: int, block_type: str) -> dict
│ │ └─ {"x": int, "y": int, "type": "ground"/"item"}
│ └─ hit_block(block: dict, player: dict, items: list) -> None
│
├─ assets/
│ ├─ images/ ← 스프라이트 이미지
│ └─ sounds/ ← 효과음, 배경음악
│
├─ data/
│ ├─ maps/
│ │ └─ stage1.json
│ └─ record.json
│ ├─ save_record(result: dict) -> None
│ └─ load_records() -> list[dict]
│
└─ utils/
├─ json_loader.py
│ ├─ load_json(path: str) -> dict
│ └─ save_json(path: str, data: dict) -> None
│
└─ config.py
├─ SETTINGS = {...}
└─ (화면 크기, FPS, 중력, 기본 속도 등 상수)
