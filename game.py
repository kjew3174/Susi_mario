"""게임 실행 함수"""
import pygame
from scenes.game import GameScene
from utils.json_loader import load_json


def run_game(map_path: str = "data/maps/level1.json", debug: bool = False) -> dict:
    """
    게임 실행 함수
    
    Args:
        map_path: 맵 파일 경로
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        게임 결과 딕셔너리 {"victory": bool, "time": float, "lives": int}
    """
    # 게임 씬 생성
    game_scene = GameScene(map_path, debug)
    
    # 게임 루프는 main.py에서 관리하므로 여기서는 씬만 반환
    # 실제로는 main.py에서 씬을 관리하므로 이 함수는 호환성을 위해 유지
    return game_scene.get_result() if game_scene.game_over or game_scene.victory else {}


def handle_collision(player_rect: pygame.Rect, blocks: list, items: list, enemies: list, debug: bool = False) -> dict:
    """
    충돌 여부를 판별하고 결과 반환
    
    Args:
        player_rect: 플레이어 Rect
        blocks: 블록 리스트
        items: 아이템 리스트
        enemies: 적 리스트
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        충돌 결과 딕셔너리 {"hit_enemy": bool, "got_item": bool, "hit_block": bool}
    """
    result = {
        "hit_enemy": False,
        "got_item": False,
        "hit_block": False
    }
    
    # 적과의 충돌
    for enemy in enemies:
        if player_rect.colliderect(enemy["rect"]):
            result["hit_enemy"] = True
            if debug:
                print(f"[DEBUG] 적 충돌: {enemy['name']}")
            break
    
    # 아이템과의 충돌
    for item in items:
        if not item.get("collected", False) and player_rect.colliderect(item["rect"]):
            result["got_item"] = True
            if debug:
                print(f"[DEBUG] 아이템 획득: {item['type']}")
            break
    
    # 블록과의 충돌
    for block in blocks:
        if player_rect.colliderect(block):
            result["hit_block"] = True
            break
    
    return result


def reset_game(game_scene: GameScene, debug: bool = False) -> None:
    """
    모든 게임 오브젝트를 초기 상태로 복구
    
    Args:
        game_scene: GameScene 인스턴스
        debug: 디버깅 메시지 출력 여부
    """
    if game_scene:
        game_scene.setup_game()
        if debug:
            print("[DEBUG] 게임 리셋 완료")
