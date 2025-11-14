"""게임 씬"""
import pygame
import time
from entities.player import Player
from entities.enemy import spawn_enemies, update_enemies, draw_enemies
from entities.item import spawn_items, update_items, draw_items
from entities.block import load_blocks, get_block_types, draw_blocks
from utils.json_loader import load_json
from utils.font_loader import get_korean_font


class GameScene:
    """게임 플레이 씬"""
    
    def __init__(self, map_path: str = "data/maps/level1.json", debug: bool = False):
        """
        GameScene 초기화
        
        Args:
            map_path: 맵 파일 경로
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.map_path = map_path
        self.map_data = []
        self.blocks = []
        self.block_types = {}
        self.enemies = []
        self.items = []
        self.player = None
        self.background_image = None
        self.start_time = 0
        self.elapsed_time = 0
        self.paused = False
        self.game_over = False
        self.victory = False
        self.application_form_rect = None  # 수시 원서 위치
        
        # 카메라 오프셋
        self.camera_x = 0
        
        # 이미지 딕셔너리
        self.images = {}
        self.background_image = None
        
        # UI 이미지
        self.ui_images = {}
        
        self.load_map()
        self.setup_game()
    
    def load_map(self):
        """맵 데이터 로드"""
        data = load_json(self.map_path, self.debug)
        if data:
            self.map_data = data.get("map", [])
            self.application_form_rect = pygame.Rect(
                data.get("application_form", {}).get("x", 0) * 160,
                data.get("application_form", {}).get("y", 0) * 160,
                160,
                160
            )
        else:
            # 기본 맵 생성
            self.map_data = self.create_default_map()
            if self.debug:
                print("[DEBUG] 기본 맵 생성됨")
    
    def create_default_map(self) -> list:
        """기본 맵 데이터 생성"""
        # 간단한 테스트 맵
        map_data = []
        # 바닥
        for y in range(10, 15):
            row = []
            for x in range(20):
                if y == 10:
                    row.append(1)  # 블록
                else:
                    row.append(0)  # 빈 공간
            map_data.append(row)
        
        # 플랫폼
        map_data[8][5] = 1
        map_data[8][6] = 1
        map_data[8][12] = 1
        map_data[8][13] = 1
        
        # 아이템 블록
        map_data[7][5] = 2
        map_data[7][12] = 2
        
        # 적
        map_data[9][8] = 4  # 약한 적
        map_data[9][15] = 3  # 강한 적
        
        # 아이템
        map_data[6][10] = 6  # 커피
        
        # 토관
        map_data[9][18] = 8
        map_data[8][18] = 8
        
        # 수시 원서 (목표)
        if not self.application_form_rect:
            self.application_form_rect = pygame.Rect(18 * 160, 7 * 160, 160, 160)
        
        return map_data
    
    def setup_game(self):
        """게임 초기 설정"""
        # 블록 로드
        self.blocks = load_blocks(self.map_data, 160, self.debug)
        self.block_types = get_block_types(self.map_data, 160, self.debug)
        
        # 적 생성
        self.enemies = spawn_enemies(self.map_data, 160, self.debug)
        
        # 아이템 생성
        self.items = spawn_items(self.map_data, 160, self.debug)
        
        # 플레이어 생성 (시작 위치)
        start_x = 100
        start_y = 0
        # 바닥 찾기
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == 1 and y > 0:
                    start_y = (y - 1) * 160
                    start_x = x * 160
                    break
            if start_y > 0:
                break
        
        self.player = Player(start_x, start_y, 160, self.debug)
        self.start_x = start_x
        self.start_y = start_y
        
        # 시작 시간 기록
        self.start_time = time.time()
    
    def reset_player_position(self):
        """플레이어를 시작 위치로 리셋"""
        self.player.rect.x = self.start_x
        self.player.rect.y = self.start_y
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.is_jumping = False
        self.player.jump_time = 0
    
    def load_images(self, images: dict, ui_images: dict = None):
        """
        이미지 로드
        
        Args:
            images: 게임 이미지 딕셔너리
            ui_images: UI 이미지 딕셔너리
        """
        self.images = images
        if "player" in images and self.player:
            self.player.load_images(images["player"], images.get("player_crouch"))
        if "background" in images:
            self.background_image = images["background"]
        if ui_images:
            self.ui_images = ui_images
    
    def update(self, events: list, dt: float) -> str:
        """
        게임 상태 업데이트
        
        Args:
            events: pygame 이벤트 리스트
            dt: 델타 타임 (초)
            
        Returns:
            다음 씬 이름 ("menu", "result", "pause", "")
        """
        if self.game_over or self.victory:
            return "result"
        
        if not self.paused:
            # 이벤트 처리
            keys = pygame.key.get_pressed()
            
            # 플레이어 이동
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.crouch()
            else:
                self.player.stand_up()
            
            # 점프 처리 (마리오 스타일 - 키를 누르고 있는 동안 계속 올라가기)
            jump_keys_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
            
            for event in events:
                if event.type == pygame.QUIT:
                    return "menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                        if self.player.on_ground and not self.player.is_jumping:
                            self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        return "pause"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.stop_jump()
            
            # 플레이어 업데이트 (점프 키 상태 전달)
            self.player.update(dt, self.blocks, jump_keys_pressed, self.debug)
            
            # 적 업데이트
            update_enemies(self.enemies, dt, self.blocks, self.debug)
            
            # 아이템 업데이트
            update_items(self.items, dt, self.debug)
            
            # 충돌 검사
            self.check_collisions()
            
            # 시간 업데이트
            self.elapsed_time = time.time() - self.start_time
            
            # 카메라 업데이트 (플레이어를 따라가기)
            self.camera_x = self.player.rect.centerx - 1920 // 2
            
            # 수시 원서 도달 확인
            if self.application_form_rect and self.player.rect.colliderect(self.application_form_rect):
                self.victory = True
                if self.debug:
                    print("[DEBUG] 수시 원서 도달!")
        
        return ""
    
    def check_collisions(self):
        """충돌 검사"""
        # 적과의 충돌
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy["rect"]):
                if self.player.velocity_y > 0 and self.player.rect.bottom < enemy["rect"].top + 20:
                    # 적을 밟음
                    enemy["health"] -= 1
                    if enemy["health"] <= 0:
                        self.enemies.remove(enemy)
                        if self.debug:
                            print(f"[DEBUG] 적 제거: {enemy['name']}")
                    self.player.velocity_y = -5  # 튀어오르기
                else:
                    # 적에게 맞음 (체력 없이 바로 죽고 목숨 감소)
                    if not self.player.invincible:
                        if self.player.take_damage():
                            # 목숨이 1일 때 죽으면 게임 오버
                            self.game_over = True
                            if self.debug:
                                print("[DEBUG] 게임 오버!")
                        else:
                            # 목숨이 남아있으면 시작 위치로 리셋
                            self.reset_player_position()
                            if self.debug:
                                print(f"[DEBUG] 부활! 남은 목숨: {self.player.lives}")
        
        # 아이템과의 충돌
        for item in self.items:
            if not item["collected"] and self.player.rect.colliderect(item["rect"]):
                item["collected"] = True
                if item["type"] == "coffee":
                    self.player.activate_invincibility(item["effect_duration"])
                    if self.debug:
                        print("[DEBUG] 커피 획득! 무적 상태")
                else:
                    if self.debug:
                        print(f"[DEBUG] 아이템 획득: {item['type']}")
    
    def render(self, screen: pygame.Surface) -> None:
        """
        화면 렌더링
        
        Args:
            screen: 화면 Surface
        """
        # 배경
        if self.background_image:
            screen.blit(self.background_image, (-self.camera_x, 0))
        else:
            screen.fill((135, 206, 235))  # 하늘색
        
        # 블록 그리기 (카메라 오프셋 적용)
        for block in self.blocks:
            block_screen_rect = block.copy()
            block_screen_rect.x -= self.camera_x
            if block_screen_rect.colliderect(pygame.Rect(0, 0, 1920, 1080)):
                if self.images.get("blocks"):
                    # 타입별 이미지 사용
                    block_type = None
                    for btype, rects in self.block_types.items():
                        if block in rects:
                            block_type = btype
                            break
                    if block_type and block_type in self.images["blocks"]:
                        screen.blit(self.images["blocks"][block_type], block_screen_rect)
                    else:
                        pygame.draw.rect(screen, (139, 69, 19), block_screen_rect)
                        pygame.draw.rect(screen, (0, 0, 0), block_screen_rect, 2)
                else:
                    pygame.draw.rect(screen, (139, 69, 19), block_screen_rect)
                    pygame.draw.rect(screen, (0, 0, 0), block_screen_rect, 2)
        
        # 수시 원서 그리기
        if self.application_form_rect:
            form_rect = self.application_form_rect.copy()
            form_rect.x -= self.camera_x
            if form_rect.colliderect(pygame.Rect(0, 0, 1920, 1080)):
                if "application_form" in self.images:
                    screen.blit(self.images["application_form"], form_rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 0), form_rect)
                    font = get_korean_font(36, self.debug)
                    text = font.render("수시 원서", True, (0, 0, 0))
                    text_rect = text.get_rect(center=form_rect.center)
                    screen.blit(text, text_rect)
        
        # 적 그리기 (카메라 오프셋 적용)
        for enemy in self.enemies:
            enemy_screen_rect = enemy["rect"].copy()
            enemy_screen_rect.x -= self.camera_x
            if enemy_screen_rect.colliderect(pygame.Rect(0, 0, 1920, 1080)):
                if self.images.get("enemies") and enemy["type"] in self.images["enemies"]:
                    img = self.images["enemies"][enemy["type"]]
                    if enemy["direction"] < 0:
                        img = pygame.transform.flip(img, True, False)
                    screen.blit(img, enemy_screen_rect)
                else:
                    # 이미지가 없으면 색상으로 표시
                    if enemy["type"] == "strong":
                        color = (255, 100, 100)
                    elif enemy["type"] == "weak":
                        color = (255, 200, 100)
                    elif enemy["type"] == "boss":
                        color = (200, 0, 200)
                    else:
                        color = (100, 100, 100)
                    pygame.draw.rect(screen, color, enemy_screen_rect)
                    font = get_korean_font(24, self.debug)
                    text = font.render(enemy["name"], True, (255, 255, 255))
                    screen.blit(text, (enemy_screen_rect.x, enemy_screen_rect.y - 20))
        
        # 아이템 그리기 (카메라 오프셋 적용)
        for item in self.items:
            if item["collected"]:
                continue
            item_screen_rect = item["rect"].copy()
            item_screen_rect.x -= self.camera_x
            if item_screen_rect.colliderect(pygame.Rect(0, 0, 1920, 1080)):
                if self.images.get("items") and item["type"] in self.images["items"]:
                    screen.blit(self.images["items"][item["type"]], item_screen_rect)
                else:
                    # 이미지가 없으면 색상으로 표시
                    if item["type"] == "coffee":
                        color = (139, 69, 19)
                    else:
                        color = (255, 215, 0)
                    pygame.draw.rect(screen, color, item_screen_rect)
                    pygame.draw.circle(screen, (255, 255, 255), item_screen_rect.center, item_screen_rect.width // 4)
        
        # 플레이어 그리기 (카메라 오프셋 적용)
        player_screen_rect = self.player.rect.copy()
        player_screen_rect.x -= self.camera_x
        if player_screen_rect.colliderect(pygame.Rect(0, 0, 1920, 1080)):
            self.player.draw(screen, self.camera_x)
        
        # UI 그리기
        self.render_ui(screen)
    
    def render_ui(self, screen: pygame.Surface):
        """UI 렌더링"""
        font = get_korean_font(48, self.debug)
        
        # 목숨 표시 (이미지 기반)
        if "lives_icon" in self.ui_images:
            for i in range(self.player.lives):
                icon = self.ui_images["lives_icon"]
                screen.blit(icon, (20 + i * (icon.get_width() + 10), 20))
        else:
            # 이미지가 없으면 텍스트로 표시
            lives_text = font.render(f"목숨: {self.player.lives}", True, (255, 255, 255))
            screen.blit(lives_text, (20, 20))
        
        # 시간 표시 (이미지 기반)
        if "time_icon" in self.ui_images:
            screen.blit(self.ui_images["time_icon"], (20, 70))
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            time_text = font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            screen.blit(time_text, (20 + self.ui_images["time_icon"].get_width() + 10, 70))
        else:
            # 이미지가 없으면 텍스트로 표시
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            time_text = font.render(f"시간: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            screen.blit(time_text, (20, 70))
        
        # 일시정지 표시
        if self.paused:
            if "pause_bg" in self.ui_images:
                pause_bg = self.ui_images["pause_bg"]
                pause_rect = pause_bg.get_rect(center=(1920 // 2, 1080 // 2))
                screen.blit(pause_bg, pause_rect)
            else:
                pause_font = get_korean_font(72, self.debug)
                pause_text = pause_font.render("일시정지", True, (255, 255, 255))
                pause_rect = pause_text.get_rect(center=(1920 // 2, 1080 // 2))
                screen.blit(pause_text, pause_rect)
    
    def get_result(self) -> dict:
        """
        게임 결과 반환
        
        Returns:
            결과 딕셔너리 {"victory": bool, "time": float, "lives": int}
        """
        return {
            "victory": self.victory,
            "time": self.elapsed_time,
            "lives": self.player.lives
        }

