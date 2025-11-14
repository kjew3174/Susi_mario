# 필요한 이미지 파일 목록

## 현재 가지고 있는 이미지 (10개)
이미지 파일이 있다고 하셨으니, 다음 이름으로 사용하시면 됩니다.

## 추가로 필요한 이미지 파일

### 게임 플레이 UI
1. **lives_icon.png** - 목숨 아이콘 (예: 하트 모양)
   - 크기: 40x40px (또는 적절한 크기)
   - 용도: 목숨 표시용 아이콘

2. **time_icon.png** - 시간 아이콘
   - 크기: 40x40px (또는 적절한 크기)
   - 용도: 시간 표시용 아이콘

3. **pause_bg.png** - 일시정지 배경
   - 크기: 400x300px (또는 적절한 크기)
   - 용도: 일시정지 메뉴 배경

### 메뉴 화면 버튼
4. **button_start.png** - 시작하기 버튼
   - 크기: 400x80px
   - 용도: 메뉴의 시작하기 버튼

5. **button_start_hover.png** - 시작하기 버튼 (호버)
   - 크기: 400x80px
   - 용도: 마우스 오버 시 표시

6. **button_setting.png** - 설정 버튼
   - 크기: 400x80px

7. **button_setting_hover.png** - 설정 버튼 (호버)
   - 크기: 400x80px

8. **button_explanation.png** - 게임 설명 버튼
   - 크기: 400x80px

9. **button_explanation_hover.png** - 게임 설명 버튼 (호버)
   - 크기: 400x80px

10. **button_exit.png** - 종료 버튼
    - 크기: 400x80px

11. **button_exit_hover.png** - 종료 버튼 (호버)
    - 크기: 400x80px

### 결과 화면
12. **result_background_victory.png** - 클리어 배경
    - 크기: 1920x1080px
    - 용도: 클리어 시 배경

13. **result_background_gameover.png** - 게임 오버 배경
    - 크기: 1920x1080px
    - 용도: 게임 오버 시 배경

14. **button_retry.png** - 다시하기 버튼
    - 크기: 400x80px

15. **button_retry_hover.png** - 다시하기 버튼 (호버)
    - 크기: 400x80px

16. **button_menu.png** - 메뉴로 버튼
    - 크기: 400x80px

17. **button_menu_hover.png** - 메뉴로 버튼 (호버)
    - 크기: 400x80px

18. **bridge.png** - 한강 철교 이미지
    - 크기: 800x400px (또는 적절한 크기)
    - 용도: 등급 50% 미만 시 표시

### 설정 화면
19. **setting_background.png** - 설정 화면 배경
    - 크기: 1920x1080px

20. **button_volume_down.png** - 볼륨 감소 버튼
    - 크기: 100x50px

21. **button_volume_up.png** - 볼륨 증가 버튼
    - 크기: 100x50px

22. **button_difficulty_easy.png** - 쉬움 난이도 버튼
    - 크기: 200x50px

23. **button_difficulty_easy_selected.png** - 쉬움 난이도 버튼 (선택됨)
    - 크기: 200x50px

24. **button_difficulty_normal.png** - 보통 난이도 버튼
    - 크기: 200x50px

25. **button_difficulty_normal_selected.png** - 보통 난이도 버튼 (선택됨)
    - 크기: 200x50px

26. **button_difficulty_hard.png** - 어려움 난이도 버튼
    - 크기: 200x50px

27. **button_difficulty_hard_selected.png** - 어려움 난이도 버튼 (선택됨)
    - 크기: 200x50px

28. **button_back.png** - 뒤로가기 버튼
    - 크기: 400x80px

29. **button_back_hover.png** - 뒤로가기 버튼 (호버)
    - 크기: 400x80px

## 이미지 로드 방법

이미지 파일들을 `assets/images/` 폴더에 저장하고, `main.py`에서 다음과 같이 로드하세요:

```python
# 예시 (main.py에 추가)
def load_all_images():
    images = {
        "player": "assets/images/player.png",
        "background": "assets/images/background.png",
        # ... 게임 이미지들
    }
    
    ui_images = {
        "lives_icon": "assets/images/lives_icon.png",
        "time_icon": "assets/images/time_icon.png",
        "pause_bg": "assets/images/pause_bg.png",
        "button_start": "assets/images/button_start.png",
        # ... UI 이미지들
    }
    
    return images, ui_images
```

## 요약
- **총 추가 필요 이미지**: 약 29개
- **기존 이미지**: 10개 (게임 플레이용 이미지로 추정)
- **모든 이미지는 PNG 형식 권장** (투명도 지원)

