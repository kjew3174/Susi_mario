"""한글 폰트 로더"""
import pygame
import os


def get_korean_font(size: int, debug: bool = False):
    """
    한글 폰트 가져오기
    
    Args:
        size: 폰트 크기
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        pygame.font.Font 객체
    """
    # Windows 기본 한글 폰트 경로들
    font_paths = [
        "C:/Windows/Fonts/malgun.ttf",  # 맑은 고딕
        "C:/Windows/Fonts/gulim.ttc",   # 굴림
        "C:/Windows/Fonts/batang.ttc",  # 바탕
        "C:/Windows/Fonts/msgothic.ttc",  # MS 고딕
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = pygame.font.Font(path, size)
                if debug:
                    print(f"[DEBUG] 한글 폰트 로드 성공: {path}")
                return font
            except Exception as e:
                if debug:
                    print(f"[DEBUG] 폰트 로드 실패: {path}, {e}")
    
    # 폰트를 찾지 못하면 기본 폰트 사용 (한글 미지원)
    if debug:
        print("[DEBUG] 한글 폰트를 찾지 못했습니다. 기본 폰트 사용")
    return pygame.font.Font(None, size)

