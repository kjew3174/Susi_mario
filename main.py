"""게임 메인 진입점"""
import pygame
import sys
from scenes.menu import MenuScene
from scenes.stage_select import StageSelectScene
from scenes.game import GameScene
from scenes.result import ResultScene
from scenes.setting import SettingScene
from utils.config import Config


def main(debug: bool = False) -> None:
    """
    게임 전체를 실행하는 메인 루프
    
    Args:
        debug: 디버깅 메시지 출력 여부
    """
    pygame.init()
    
    # 설정 로드
    config = Config(debug)
    config.load()
    
    # 화면 모드 설정
    if config.fullscreen:
        screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption("수시마리오")
    clock = pygame.time.Clock()
    
    # 현재 씬
    current_scene = "menu"
    scene_instances = {}
    
    # 게임 결과 및 선택된 스테이지
    game_result = None
    selected_stage = None
    
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # 씬 전환 처리
        next_scene = None
        
        if current_scene == "menu":
            if "menu" not in scene_instances:
                scene_instances["menu"] = MenuScene(debug)
            next_scene = scene_instances["menu"].update(events)
            scene_instances["menu"].render(screen)
            
        elif current_scene == "stage_select":
            if "stage_select" not in scene_instances:
                scene_instances["stage_select"] = StageSelectScene(debug)
            next_scene = scene_instances["stage_select"].update(events)
            scene_instances["stage_select"].render(screen)
            
            # 스테이지 선택 시
            if next_scene == "game":
                selected_stage = scene_instances["stage_select"].selected_stage
                scene_instances.pop("stage_select", None)
            
        elif current_scene == "game":
            if "game" not in scene_instances:
                map_path = selected_stage if selected_stage else "data/maps/level1.json"
                scene_instances["game"] = GameScene(map_path, debug)
            next_scene = scene_instances["game"].update(events, dt)
            scene_instances["game"].render(screen)
            
            # 게임 종료 시 결과 저장
            if next_scene == "result":
                game_result = scene_instances["game"].get_result()
                scene_instances.pop("game", None)
                selected_stage = None
            
        elif current_scene == "result":
            if "result" not in scene_instances and game_result:
                scene_instances["result"] = ResultScene(game_result, debug)
            if "result" in scene_instances:
                next_scene = scene_instances["result"].update(events)
                scene_instances["result"].render(screen)
            
        elif current_scene == "setting":
            if "setting" not in scene_instances:
                config_dict = {
                    "volume": config.volume,
                    "difficulty": config.difficulty,
                    "fullscreen": config.fullscreen
                }
                scene_instances["setting"] = SettingScene(config_dict, debug)
            next_scene = scene_instances["setting"].update(events)
            scene_instances["setting"].render(screen)
            
            # 설정 저장 및 전체화면 적용
            if "setting" in scene_instances:
                config.volume = scene_instances["setting"].config["volume"]
                config.difficulty = scene_instances["setting"].config["difficulty"]
                fullscreen_changed = config.fullscreen != scene_instances["setting"].config.get("fullscreen", False)
                config.fullscreen = scene_instances["setting"].config.get("fullscreen", False)
                
                # 전체화면 변경 시 화면 모드 업데이트
                if fullscreen_changed:
                    if config.fullscreen:
                        screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        
        elif current_scene == "pause":
            # 일시정지 화면은 game 씬에서 처리
            # ESC 키로 일시정지 해제는 game 씬에서 처리됨
            pass
        
        elif current_scene == "explanation":
            # 게임 설명 화면
            from utils.font_loader import get_korean_font
            screen.fill((50, 50, 50))
            font_large = get_korean_font(72)
            font_medium = get_korean_font(48)
            
            title = font_large.render("게임 설명", True, (255, 255, 255))
            screen.blit(title, (config.screen_width // 2 - 150, 100))
            
            explanations = [
                "목표: 수시 원서에 도달하여 교사 박 모씨를 제거하세요",
                "조작: 방향키 또는 WASD로 이동, 스페이스바로 점프",
                "기록: 시간이 빠를수록 높은 등급을 받습니다",
                "등급에 따라 합격 대학이 결정됩니다",
                "ESC: 일시정지"
            ]
            
            y_offset = 250
            for explanation in explanations:
                text = font_medium.render(explanation, True, (255, 255, 255))
                screen.blit(text, (100, y_offset))
                y_offset += 60
            
            back_button = pygame.Rect(config.screen_width // 2 - 200, config.screen_height - 100, 400, 80)
            pygame.draw.rect(screen, (70, 130, 180), back_button)
            back_text = font_medium.render("뒤로가기", True, (255, 255, 255))
            back_rect = back_text.get_rect(center=back_button.center)
            screen.blit(back_text, back_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(mouse_pos):
                        next_scene = "menu"
        
        # 씬 전환
        if next_scene:
            if next_scene == "exit":
                running = False
            elif next_scene == "game":
                # 게임 재시작 시 새 인스턴스 생성
                scene_instances.pop("game", None)
            elif next_scene == "stage_select":
                # 스테이지 선택 화면으로
                pass
            elif next_scene == "menu":
                # 메뉴로 돌아갈 때 일부 씬 정리
                scene_instances.pop("result", None)
                scene_instances.pop("setting", None)
                scene_instances.pop("explanation", None)
                scene_instances.pop("stage_select", None)
            
            current_scene = next_scene
        
        pygame.display.flip()
    
    # 설정 저장
    config.save()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # 디버그 모드 (명령줄 인자로 제어 가능)
    debug_mode = "--debug" in sys.argv
    main(debug=debug_mode)

