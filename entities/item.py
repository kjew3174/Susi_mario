"""아이템 엔티티 관리"""
import pygame
import random


def spawn_items(map_data: list[list[int]], block_size: int = 160, debug: bool = False) -> list[dict]:
    """
    맵 데이터를 기반으로 아이템 생성
    
    Args:
        map_data: 맵 데이터 (2D 리스트)
        block_size: 블록 크기
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        아이템 정보 리스트
    """
    items = []
    
    # 맵 데이터에서 아이템 위치 찾기 (예: 값 6 = 커피, 7 = 기타 아이템)
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 6:  # 커피 (무적)
                items.append({
                    "type": "coffee",
                    "x": x * block_size,
                    "y": y * block_size,
                    "rect": pygame.Rect(x * block_size, y * block_size, block_size, block_size),
                    "collected": False,
                    "effect_duration": 6000  # 6초
                })
            elif cell == 7:  # 기타 아이템
                items.append({
                    "type": "item",
                    "x": x * block_size,
                    "y": y * block_size,
                    "rect": pygame.Rect(x * block_size, y * block_size, block_size, block_size),
                    "collected": False
                })
    
    if debug:
        print(f"[DEBUG] {len(items)}개의 아이템 생성됨")
    
    return items


def update_items(items: list[dict], dt: float, debug: bool = False) -> None:
    """
    아이템 상태 업데이트 (애니메이션 등)
    
    Args:
        items: 아이템 리스트
        dt: 델타 타임 (초)
        debug: 디버깅 메시지 출력 여부
    """
    # 아이템 애니메이션 로직 (필요시 추가)
    pass


def draw_items(screen: pygame.Surface, items: list[dict], images: dict = None, debug: bool = False) -> None:
    """
    아이템 그리기
    
    Args:
        screen: 화면 Surface
        items: 아이템 리스트
        images: 아이템 이미지 딕셔너리 (선택사항)
        debug: 디버깅 메시지 출력 여부
    """
    for item in items:
        if item["collected"]:
            continue
        
        if images and item["type"] in images:
            img = images[item["type"]]
            screen.blit(img, item["rect"])
        else:
            # 이미지가 없으면 색상으로 표시
            if item["type"] == "coffee":
                color = (139, 69, 19)  # 갈색 (커피)
            else:
                color = (255, 215, 0)  # 금색 (일반 아이템)
            
            pygame.draw.rect(screen, color, item["rect"])
            pygame.draw.circle(screen, (255, 255, 255), item["rect"].center, item["rect"].width // 4)

