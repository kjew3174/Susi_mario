"""적 엔티티 관리"""
import pygame
import random


def spawn_enemies(map_data: list[list[int]], block_size: int = 160, debug: bool = False) -> list[dict]:
    """
    맵 데이터를 기반으로 적 생성
    
    Args:
        map_data: 맵 데이터 (2D 리스트)
        block_size: 블록 크기
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        적 정보 리스트
    """
    enemies = []
    
    # 맵 데이터에서 적 위치 찾기 (예: 값 3 = 강한 적, 4 = 약한 적, 5 = 보스)
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 3:  # 강한 적 (박건률)
                enemies.append({
                    "type": "strong",
                    "name": "박건률",
                    "x": x * block_size,
                    "y": y * block_size,
                    "rect": pygame.Rect(x * block_size, y * block_size, block_size, block_size),
                    "velocity_x": -2,
                    "health": 2,
                    "damage": 2,
                    "patrol_distance": block_size * 3,
                    "start_x": x * block_size,
                    "direction": -1
                })
            elif cell == 4:  # 약한 적 (오유준)
                enemies.append({
                    "type": "weak",
                    "name": "오유준",
                    "x": x * block_size,
                    "y": y * block_size,
                    "rect": pygame.Rect(x * block_size, y * block_size, block_size, block_size),
                    "velocity_x": -1,
                    "health": 1,
                    "damage": 1,
                    "patrol_distance": block_size * 2,
                    "start_x": x * block_size,
                    "direction": -1
                })
            elif cell == 5:  # 보스 (청마)
                enemies.append({
                    "type": "boss",
                    "name": "청마",
                    "x": x * block_size,
                    "y": y * block_size,
                    "rect": pygame.Rect(x * block_size, y * block_size, block_size * 2, block_size * 2),
                    "velocity_x": -1,
                    "health": 10,
                    "damage": 3,
                    "patrol_distance": block_size * 5,
                    "start_x": x * block_size,
                    "direction": -1
                })
    
    if debug:
        print(f"[DEBUG] {len(enemies)}개의 적 생성됨")
    
    return enemies


def update_enemies(enemies: list[dict], dt: float, blocks: list, debug: bool = False) -> None:
    """
    적 위치 및 상태 업데이트
    
    Args:
        enemies: 적 리스트
        dt: 델타 타임 (초)
        blocks: 충돌할 블록 리스트
        debug: 디버깅 메시지 출력 여부
    """
    for enemy in enemies:
        # 순찰 이동
        enemy["x"] += enemy["velocity_x"] * dt * 60
        enemy["rect"].x = int(enemy["x"])
        
        # 순찰 범위 체크
        distance = abs(enemy["x"] - enemy["start_x"])
        if distance >= enemy["patrol_distance"]:
            enemy["velocity_x"] *= -1
            enemy["direction"] *= -1
        
        # 블록과의 충돌 검사
        for block in blocks:
            if enemy["rect"].colliderect(block):
                if enemy["velocity_x"] > 0:
                    enemy["rect"].right = block.left
                    enemy["x"] = enemy["rect"].x
                    enemy["velocity_x"] *= -1
                    enemy["direction"] *= -1
                elif enemy["velocity_x"] < 0:
                    enemy["rect"].left = block.right
                    enemy["x"] = enemy["rect"].x
                    enemy["velocity_x"] *= -1
                    enemy["direction"] *= -1


def draw_enemies(screen: pygame.Surface, enemies: list[dict], images: dict = None, debug: bool = False) -> None:
    """
    적 그리기
    
    Args:
        screen: 화면 Surface
        enemies: 적 리스트
        images: 적 이미지 딕셔너리 (선택사항)
        debug: 디버깅 메시지 출력 여부
    """
    for enemy in enemies:
        if images and enemy["type"] in images:
            img = images[enemy["type"]]
            if enemy["direction"] < 0:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, enemy["rect"])
        else:
            # 이미지가 없으면 색상으로 표시
            if enemy["type"] == "strong":
                color = (255, 100, 100)  # 빨간색
            elif enemy["type"] == "weak":
                color = (255, 200, 100)  # 주황색
            elif enemy["type"] == "boss":
                color = (200, 0, 200)  # 보라색
            else:
                color = (100, 100, 100)  # 회색
            
            pygame.draw.rect(screen, color, enemy["rect"])
            
            # 이름 표시
            font = pygame.font.Font(None, 24)
            text = font.render(enemy["name"], True, (255, 255, 255))
            screen.blit(text, (enemy["rect"].x, enemy["rect"].y - 20))

