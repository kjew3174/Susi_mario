# 필요한 이미지 파일 목록

## 현재 가지고 있는 이미지 (18개)
### 메뉴 화면

	menu_background.png - 메인 메뉴 배경 (1920x1080)
	
	title.png - 게임 타이틀 이미지 (선택사항)

### 게임 플레이

	player.png - 플레이어 기본 이미지 (160x160)
	
	✅ background.png - 게임 배경 (천고 배경, 가로로 긴 타일 가능)
	
	application_form.png - 수시 원서 이미지 (160x160)

### 블록

	block_normal.png - 일반 블록 (160x160)
	
	block_item.png - 아이템 블록 (160x160)
	
	block_pipe.png - 토관/논술 (160x320, 세로로 긴 형태)

### 적 (Enemies)

	enemy_strong.png - 강한 적 (박건률) (160x160)
	
	enemy_weak.png - 약한 적 (오유준) (160x160)
	
	enemy_boss.png - 보스 (청마) (320x320, 2배 크기)

### 아이템

	item_coffee.png - 커피 아이템 (무적) (160x160)
	
	item_general.png - 일반 아이템 (160x160)

### 결과 화면

	bridge.png - 한강 철교 이미지 (선택사항, 등급 50% 미만 시 표시)
    univ_logo0.png - 대학 로고 이미지

### UI 요소 (선택사항)

	button.png - 버튼 이미지
	
	button_hover.png - 버튼 호버 이미지
	
	pause_menu.png - 일시정지 메뉴 배경

## 추가로 필요한 이미지 파일

## 모든 이미지는 사각형 기반 또는 픽셀아트, 버튼 호버 이미지는 내부 색을 조금 어둡게 변경

### 버튼 이미지 (4개) - 모든 버튼에 재활용
1. **button_rect.png** - 직사각형 버튼 (400x80px)
   - 용도: 메뉴, 결과 화면의 모든 버튼에 사용

2. **button_rect_hover.png** - 직사각형 버튼 호버 (400x80px)
   - 용도: 마우스 오버 시 표시

3. **button_square.png** - 정사각형 버튼 (80x80px)
   - 용도: 일시정지, 스테이지 선택, 설정 화면의 작은 버튼들에 사용
   - 볼륨 버튼, 난이도 버튼 등에 크기 조정하여 재활용

4. **button_square_hover.png** - 정사각형 버튼 호버 (80x80px)
   - 용도: 마우스 오버 시 표시, 선택된 난이도 버튼에도 사용

### 게임 플레이 UI (2개)
5. **lives_icon.png** - 목숨 아이콘 (하트 모양)
   - 크기: 40x40px (또는 적절한 크기)
   - 용도: 목숨 표시용 아이콘

6. **time_icon.png** - 시간 아이콘 (시계 모양)
   - 크기: 40x40px (또는 적절한 크기)
   - 용도: 시간 표시용 아이콘

7. **pause_bg.png** - 일시정지 배경
   - 크기: 400x300px (또는 적절한 크기)
   - 용도: 일시정지 메뉴 배경
   - 참고: pause_menu.png가 있으면 재활용 가능

### 결과 화면 배경 (2개)
8. **result_background_victory.png** - 클리어 배경
   - 크기: 1920x1080px
   - 용도: 클리어 시 배경

9. **result_background_gameover.png** - 게임 오버 배경
   - 크기: 1920x1080px
   - 용도: 게임 오버 시 배경

### 설정 화면 배경 (1개)
10. **setting_background.png** - 설정 화면 배경
    - 크기: 1920x1080px

## 이미지 로드 방법

이미지 파일들을 `assets/images/` 폴더에 저장하고, 각 씬에서 다음과 같이 로드하세요:

```python
# 예시 (main.py에 추가)
def load_all_images():
    # 게임 플레이 이미지
    images = {
        "player": "assets/images/player.png",
        "player_crouch": "assets/images/player_crouch.png",
        "background": "assets/images/background.png",
        "application_form": "assets/images/application_form.png",
        "blocks": {
            "normal": "assets/images/block_normal.png",
            "item": "assets/images/block_item.png",
            "pipe": "assets/images/block_pipe.png"
        },
        "enemies": {
            "strong": "assets/images/enemy_strong.png",
            "weak": "assets/images/enemy_weak.png",
            "boss": "assets/images/enemy_boss.png"
        },
        "items": {
            "coffee": "assets/images/item_coffee.png",
            "item": "assets/images/item_general.png"
        }
    }
    
    # UI 이미지
    ui_images = {
        "lives_icon": "assets/images/lives_icon.png",
        "time_icon": "assets/images/time_icon.png",
        "pause_bg": "assets/images/pause_bg.png",  # 또는 pause_menu.png
    }
    
    # 버튼 이미지 (공통)
    button_images = {
        "rect": "assets/images/button_rect.png",
        "rect_hover": "assets/images/button_rect_hover.png",
        "square": "assets/images/button_square.png",
        "square_hover": "assets/images/button_square_hover.png"
    }
    
    return images, ui_images, button_images
```

## 버튼 사용 규칙

### 400x80px 버튼 (button_rect) 사용 위치:
- 메뉴 화면: 시작하기, 설정, 게임 설명, 종료
- 결과 화면: 다시하기, 메뉴로
- 설정 화면: 뒤로가기

### 80x80px 버튼 (button_square) 사용 위치:
- 설정 화면: 볼륨 증가/감소 (100x50으로 크기 조정)
- 설정 화면: 난이도 선택 버튼 (200x50으로 크기 조정, 선택 시 hover 이미지 사용)
- 일시정지 메뉴 버튼 (향후 추가 시)
- 스테이지 선택 버튼 (향후 추가 시)

## 요약
- **총 추가 필요 이미지**: 약 10개
  - 버튼: 4개 (모든 버튼에 재활용)
  - UI 아이콘: 2개
  - 일시정지 배경: 1개
  - 결과 화면 배경: 2개
  - 설정 화면 배경: 1개
- **기존 이미지**: 18개 (게임 플레이용 이미지)
- **모든 이미지는 PNG 형식 권장** (투명도 지원)
