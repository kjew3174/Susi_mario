"""맵 에디터"""
import pygame
import sys
from utils.json_loader import load_json, save_json


def open_editor(map_path: str = "data/maps/level1.json", debug: bool = False) -> None:
    """
    맵 편집 인터페이스를 실행
    
    Args:
        map_path: 맵 파일 경로
        debug: 디버깅 메시지 출력 여부
    """
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("맵 에디터")
    clock = pygame.time.Clock()
    
    block_size = 160
    map_data = load_json(map_path, debug)
    
    if not map_data or "map" not in map_data:
        # 기본 맵 생성
        map_data = {
            "map": [[0 for _ in range(20)] for _ in range(15)]
        }
    
    current_map = map_data["map"]
    
    # 선택된 블록 타입
    selected_type = 1  # 0=빈공간, 1=블록, 2=아이템블록, 3=강한적, 4=약한적, 5=보스, 6=커피, 7=아이템, 8=토관
    
    # 카메라
    camera_x = 0
    camera_y = 0
    
    # 그리드 표시
    show_grid = True
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_map(current_map, map_path, debug)
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
                # 블록 타입 선택
                elif event.key == pygame.K_0:
                    selected_type = 0
                elif event.key == pygame.K_1:
                    selected_type = 1
                elif event.key == pygame.K_2:
                    selected_type = 2
                elif event.key == pygame.K_3:
                    selected_type = 3
                elif event.key == pygame.K_4:
                    selected_type = 4
                elif event.key == pygame.K_5:
                    selected_type = 5
                elif event.key == pygame.K_6:
                    selected_type = 6
                elif event.key == pygame.K_7:
                    selected_type = 7
                elif event.key == pygame.K_8:
                    selected_type = 8
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 클릭
                    mouse_x, mouse_y = event.pos
                    grid_x = (mouse_x + camera_x) // block_size
                    grid_y = (mouse_y + camera_y) // block_size
                    
                    if 0 <= grid_y < len(current_map) and 0 <= grid_x < len(current_map[0]):
                        current_map[grid_y][grid_x] = selected_type
                        if debug:
                            print(f"[DEBUG] 블록 설정: ({grid_x}, {grid_y}) = {selected_type}")
                elif event.button == 3:  # 오른쪽 클릭
                    mouse_x, mouse_y = event.pos
                    grid_x = (mouse_x + camera_x) // block_size
                    grid_y = (mouse_y + camera_y) // block_size
                    
                    if 0 <= grid_y < len(current_map) and 0 <= grid_x < len(current_map[0]):
                        current_map[grid_y][grid_x] = 0
                        if debug:
                            print(f"[DEBUG] 블록 제거: ({grid_x}, {grid_y})")
            elif event.type == pygame.MOUSEWHEEL:
                camera_y -= event.y * block_size
        
        # 카메라 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_x += 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
            camera_y += 5
        
        # 화면 그리기
        screen.fill((135, 206, 235))
        
        # 맵 그리기
        for y, row in enumerate(current_map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * block_size - camera_x, y * block_size - camera_y, block_size, block_size)
                
                if cell == 1:  # 블록
                    pygame.draw.rect(screen, (139, 69, 19), rect)
                elif cell == 2:  # 아이템 블록
                    pygame.draw.rect(screen, (255, 215, 0), rect)
                elif cell == 3:  # 강한 적
                    pygame.draw.rect(screen, (255, 100, 100), rect)
                elif cell == 4:  # 약한 적
                    pygame.draw.rect(screen, (255, 200, 100), rect)
                elif cell == 5:  # 보스
                    pygame.draw.rect(screen, (200, 0, 200), rect)
                elif cell == 6:  # 커피
                    pygame.draw.rect(screen, (139, 69, 19), rect)
                    pygame.draw.circle(screen, (255, 255, 255), rect.center, 20)
                elif cell == 7:  # 아이템
                    pygame.draw.rect(screen, (255, 215, 0), rect)
                    pygame.draw.circle(screen, (255, 255, 255), rect.center, 20)
                elif cell == 8:  # 토관
                    pygame.draw.rect(screen, (0, 150, 0), rect)
                
                # 그리드
                if show_grid:
                    pygame.draw.rect(screen, (200, 200, 200), rect, 1)
        
        # UI
        font = pygame.font.Font(None, 36)
        
        # 선택된 타입 표시
        type_names = {
            0: "빈공간",
            1: "블록",
            2: "아이템블록",
            3: "강한적",
            4: "약한적",
            5: "보스",
            6: "커피",
            7: "아이템",
            8: "토관"
        }
        
        type_text = font.render(f"선택: {type_names.get(selected_type, '알 수 없음')} ({selected_type})", True, (255, 255, 255))
        screen.blit(type_text, (10, 10))
        
        help_text = font.render("0-8: 타입 선택 | S+Ctrl: 저장 | G: 그리드 토글 | ESC: 종료", True, (255, 255, 255))
        screen.blit(help_text, (10, 50))
        
        pygame.display.flip()
    
    pygame.quit()


def save_map(map_data: list[list[int]], map_path: str, debug: bool = False) -> None:
    """
    편집된 맵 데이터를 JSON 파일로 저장
    
    Args:
        map_data: 맵 데이터 (2D 리스트)
        map_path: 저장할 맵 파일 경로
        debug: 디버깅 메시지 출력 여부
    """
    data = {
        "map": map_data,
        "application_form": {
            "x": 18,
            "y": 7
        }
    }
    save_json(map_path, data, debug)
    if debug:
        print(f"[DEBUG] 맵 저장 완료: {map_path}")

