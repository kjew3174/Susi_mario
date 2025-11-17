"""게임 씬"""
import pygame
import time
import os
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
        
        # 게임 상태
        self.countdown_active = True  # 카운트다운 활성화
        self.countdown_time = 3.0  # 3초 카운트다운
        self.game_started = False  # 게임 시작 여부
        
        # 사망 연출
        self.death_animation = False
        self.death_timer = 0
        self.death_duration = 1.0  # 1초 정지
        
        # 보스전
        self.boss_battle = False
        self.boss_switch_rect = None  # 보스 스위치 위치
        self.camera_locked = False  # 카메라 고정 여부
        
        # 카메라 오프셋 (플레이어를 화면 중앙에 고정)
        self.camera_x = 0
        self.player_screen_x = 1920 // 2  # 플레이어가 화면상 고정될 x좌표
        
        # 이미지 딕셔너리
        self.images = {}
        self.background_image = None
        
        # UI 이미지
        self.ui_images = {}
        
        # 일시정지 버튼 이미지
        self.button_rect = None
        self.button_rect_hover = None
        
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
            # 보스전 정보
            if "boss_battle" in data:
                boss_info = data["boss_battle"]
                self.boss_battle = boss_info.get("enabled", False)
                if "switch" in boss_info:
                    switch_info = boss_info["switch"]
                    self.boss_switch_rect = pygame.Rect(
                        switch_info.get("x", 0) * 160,
                        switch_info.get("y", 0) * 160,
                        160,
                        160
                    )
                    self.camera_locked = True
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
    
    def load_images(self, images: dict, ui_images: dict = None, button_rect: str = None, button_rect_hover: str = None):
        """
        이미지 로드
        
        Args:
            images: 게임 이미지 딕셔너리
            ui_images: UI 이미지 딕셔너리
            button_rect: 400x80px 버튼 이미지 경로
            button_rect_hover: 400x80px 버튼 호버 이미지 경로
        """
        self.images = images
        if "player" in images and self.player:
            self.player.load_images(images["player"], images.get("player_crouch"))
        if "background" in images:
            self.background_image = images["background"]
        if ui_images:
            self.ui_images = ui_images
        if button_rect:
            self.button_rect = pygame.image.load(button_rect).convert_alpha()
        if button_rect_hover:
            self.button_rect_hover = pygame.image.load(button_rect_hover).convert_alpha()
    
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
                        if not self.paused:
                            self.paused = True
                        else:
                            self.paused = False
                        return ""
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.stop_jump()
            
            # 플레이어 업데이트 (점프 키 상태 전달)
            self.player.update(dt, self.blocks, jump_keys_pressed, self.debug)
            
            # 낭떠러지 추락 감지 (화면 아래로 떨어지면 사망)
            if self.player.rect.top > 1080 + 200:  # 화면 아래로 많이 떨어지면
                if not self.death_animation:
                    self.death_animation = True
                    self.death_timer = 0
                    if self.debug:
                        print("[DEBUG] 낭떠러지 추락!")
                return ""
            
            # 적 업데이트
            update_enemies(self.enemies, dt, self.blocks, self.debug)
            
            # 아이템 업데이트
            update_items(self.items, dt, self.debug)
            
            # 충돌 검사
            self.check_collisions()
            
            # 시간 업데이트
            if self.game_started:
                self.elapsed_time = time.time() - self.start_time
            
            # 카메라 업데이트 (플레이어를 화면 중앙에 고정)
            if not self.camera_locked:
                self.camera_x = self.player.rect.centerx - self.player_screen_x
            # 보스전일 때는 카메라 고정
            
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
                    if not self.player.invincible and not self.death_animation:
                        self.death_animation = True
                        self.death_timer = 0
                        if self.debug:
                            print("[DEBUG] 적에게 맞음! 사망 연출 시작")
        
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
        
        # 토관 상호작용 (논술) - 아래에서 위로 올라가는 경우
        for btype, rects in self.block_types.items():
            if btype == "pipe":
                for pipe_rect in rects:
                    if self.player.rect.colliderect(pipe_rect):
                        # 토관과 상호작용 (아래에서 위로 올라가는 경우)
                        if self.player.rect.bottom <= pipe_rect.top + 20 and self.player.velocity_y < 0:
                            # 다른 맵 불러오기 (고난도 지름길)
                            alt_map = self.map_path.replace("level1", "level1_hard")
                            if os.path.exists(alt_map):
                                self.map_path = alt_map
                                self.load_map()
                                self.setup_game()
                                self.countdown_active = True
                                self.countdown_time = 3.0
                                self.game_started = False
                                if self.debug:
                                    print(f"[DEBUG] 토관을 통해 맵 변경: {alt_map}")
                            break
        
        # 보스전 스위치 상호작용
        if self.boss_battle and self.boss_switch_rect:
            if self.player.rect.colliderect(self.boss_switch_rect):
                # 보스 사망 연출
                for enemy in self.enemies:
                    if enemy["type"] == "boss":
                        enemy["health"] = 0
                        self.enemies.remove(enemy)
                        if self.debug:
                            print("[DEBUG] 보스 사망!")
                        # 엔딩 연출 후 결과 화면
                        self.victory = True
                        break
    
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
        
        # 카운트다운 표시
        if self.countdown_active:
            countdown_font = get_korean_font(144, self.debug)
            countdown_num = int(self.countdown_time) + 1
            if countdown_num > 0:
                countdown_text = countdown_font.render(str(countdown_num), True, (255, 255, 255))
                countdown_rect = countdown_text.get_rect(center=(1920 // 2, 1080 // 2))
                screen.blit(countdown_text, countdown_rect)
        
        # 사망 연출 표시
        if self.death_animation:
            # 반투명 배경
            overlay = pygame.Surface((1920, 1080))
            overlay.set_alpha(180)
            overlay.fill((255, 0, 0))
            screen.blit(overlay, (0, 0))
            
            death_font = get_korean_font(72, self.debug)
            death_text = death_font.render("사망!", True, (255, 255, 255))
            death_rect = death_text.get_rect(center=(1920 // 2, 1080 // 2))
            screen.blit(death_text, death_rect)
        
        # 일시정지 메뉴 렌더링
        if self.paused:
            self.render_pause_menu(screen)
    
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
        
        # 일시정지 메뉴는 render에서 별도로 처리됨
    
    def render_pause_menu(self, screen: pygame.Surface):
        """일시정지 메뉴 렌더링"""
        # 반투명 배경
        overlay = pygame.Surface((1920, 1080))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font_large = get_korean_font(72, self.debug)
        font_medium = get_korean_font(48, self.debug)
        
        # 일시정지 제목
        pause_text = font_large.render("일시정지", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(1920 // 2, 300))
        screen.blit(pause_text, pause_rect)
        
        # 일시정지 버튼들
        mouse_pos = pygame.mouse.get_pos()
        pause_buttons = {
            "continue": pygame.Rect(1920 // 2 - 200, 400, 400, 80),
            "restart": pygame.Rect(1920 // 2 - 200, 500, 400, 80),
            "exit": pygame.Rect(1920 // 2 - 200, 600, 400, 80)
        }
        
        button_labels = {
            "continue": "계속하기",
            "restart": "다시하기",
            "exit": "종료하기"
        }
        
        for key, rect in pause_buttons.items():
            if self.button_rect:
                btn_img = self.button_rect
                if rect.collidepoint(mouse_pos) and self.button_rect_hover:
                    btn_img = self.button_rect_hover
                btn_img = pygame.transform.scale(btn_img, (rect.width, rect.height))
                screen.blit(btn_img, rect)
            else:
                if rect.collidepoint(mouse_pos):
                    color = (100, 150, 255)
                else:
                    color = (70, 130, 180)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
            text = font_medium.render(button_labels[key], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    def handle_pause_menu(self, events: list) -> str:
        """
        일시정지 메뉴 이벤트 처리
        
        Returns:
            다음 씬 이름 ("", "game", "menu")
        """
        mouse_pos = pygame.mouse.get_pos()
        pause_buttons = {
            "continue": pygame.Rect(1920 // 2 - 200, 400, 400, 80),
            "restart": pygame.Rect(1920 // 2 - 200, 500, 400, 80),
            "exit": pygame.Rect(1920 // 2 - 200, 600, 400, 80)
        }
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_buttons["continue"].collidepoint(mouse_pos):
                    self.paused = False
                    return ""
                elif pause_buttons["restart"].collidepoint(mouse_pos):
                    # 게임 재시작
                    self.load_map()
                    self.setup_game()
                    self.countdown_active = True
                    self.countdown_time = 3.0
                    self.game_started = False
                    self.paused = False
                    return "game"
                elif pause_buttons["exit"].collidepoint(mouse_pos):
                    return "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = False
                    return ""
        
        return ""
    
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

