"""설정 씬"""
import pygame
from utils.font_loader import get_korean_font


class SettingScene:
    """설정 씬"""
    
    def __init__(self, config: dict, debug: bool = False):
        """
        SettingScene 초기화
        
        Args:
            config: 설정 딕셔너리
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.config = config
        self.buttons = {}
        self.button_images = {}
        self.background_image = None
        self.setup_buttons()
    
    def setup_buttons(self):
        """버튼 위치 설정"""
        screen_width = 1920
        screen_height = 1080
        
        self.buttons = {
            "back": pygame.Rect(screen_width // 2 - 200, screen_height - 100, 400, 80),
            "volume_up": pygame.Rect(screen_width // 2 + 100, 300, 100, 50),
            "volume_down": pygame.Rect(screen_width // 2 - 200, 300, 100, 50),
            "difficulty_easy": pygame.Rect(screen_width // 2 - 300, 400, 200, 50),
            "difficulty_normal": pygame.Rect(screen_width // 2 - 100, 400, 200, 50),
            "difficulty_hard": pygame.Rect(screen_width // 2 + 100, 400, 200, 50)
        }
    
    def update(self, events: list) -> str:
        """
        이벤트 처리 및 업데이트
        
        Args:
            events: pygame 이벤트 리스트
            
        Returns:
            다음 씬 이름 ("menu", "")
        """
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["back"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 뒤로가기 버튼 클릭")
                    return "menu"
                elif self.buttons["volume_up"].collidepoint(mouse_pos):
                    self.config["volume"] = min(1.0, self.config["volume"] + 0.1)
                    if self.debug:
                        print(f"[DEBUG] 볼륨 증가: {self.config['volume']}")
                elif self.buttons["volume_down"].collidepoint(mouse_pos):
                    self.config["volume"] = max(0.0, self.config["volume"] - 0.1)
                    if self.debug:
                        print(f"[DEBUG] 볼륨 감소: {self.config['volume']}")
                elif self.buttons["difficulty_easy"].collidepoint(mouse_pos):
                    self.config["difficulty"] = "easy"
                    if self.debug:
                        print("[DEBUG] 난이도: 쉬움")
                elif self.buttons["difficulty_normal"].collidepoint(mouse_pos):
                    self.config["difficulty"] = "normal"
                    if self.debug:
                        print("[DEBUG] 난이도: 보통")
                elif self.buttons["difficulty_hard"].collidepoint(mouse_pos):
                    self.config["difficulty"] = "hard"
                    if self.debug:
                        print("[DEBUG] 난이도: 어려움")
        
        return ""
    
    def render(self, screen: pygame.Surface) -> None:
        """
        화면 렌더링
        
        Args:
            screen: 화면 Surface
        """
        # 배경 이미지
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((50, 50, 50))  # 어두운 배경
        
        font_large = get_korean_font(72, self.debug)
        font_medium = get_korean_font(48, self.debug)
        font_small = get_korean_font(36, self.debug)
        
        # 제목
        title_text = font_large.render("설정", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(1920 // 2, 100))
        screen.blit(title_text, title_rect)
        
        # 볼륨 설정
        volume_text = font_medium.render(f"볼륨: {int(self.config['volume'] * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(1920 // 2, 250))
        screen.blit(volume_text, volume_rect)
        
        # 볼륨 버튼 (이미지 기반)
        if "volume_down" in self.button_images:
            screen.blit(self.button_images["volume_down"], self.buttons["volume_down"])
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.buttons["volume_down"])
            down_text = font_small.render("-", True, (255, 255, 255))
            screen.blit(down_text, down_text.get_rect(center=self.buttons["volume_down"].center))
        
        if "volume_up" in self.button_images:
            screen.blit(self.button_images["volume_up"], self.buttons["volume_up"])
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.buttons["volume_up"])
            up_text = font_small.render("+", True, (255, 255, 255))
            screen.blit(up_text, up_text.get_rect(center=self.buttons["volume_up"].center))
        
        # 난이도 설정
        difficulty_text = font_medium.render(f"난이도: {self.config['difficulty']}", True, (255, 255, 255))
        difficulty_rect = difficulty_text.get_rect(center=(1920 // 2, 350))
        screen.blit(difficulty_text, difficulty_rect)
        
        # 난이도 버튼 (이미지 기반)
        difficulties = ["easy", "normal", "hard"]
        difficulty_labels = ["쉬움", "보통", "어려움"]
        for i, (diff, label) in enumerate(zip(difficulties, difficulty_labels)):
            key = f"difficulty_{diff}"
            if key in self.buttons:
                if key in self.button_images:
                    btn_img = self.button_images[key]
                    if self.config["difficulty"] == diff and f"{key}_selected" in self.button_images:
                        btn_img = self.button_images[f"{key}_selected"]
                    btn_img = pygame.transform.scale(btn_img, (self.buttons[key].width, self.buttons[key].height))
                    screen.blit(btn_img, self.buttons[key])
                else:
                    color = (150, 150, 150) if self.config["difficulty"] == diff else (100, 100, 100)
                    pygame.draw.rect(screen, color, self.buttons[key])
                    btn_text = font_small.render(label, True, (255, 255, 255))
                    screen.blit(btn_text, btn_text.get_rect(center=self.buttons[key].center))
        
        # 뒤로가기 버튼 (이미지 기반)
        mouse_pos = pygame.mouse.get_pos()
        if "back" in self.button_images:
            back_img = self.button_images["back"]
            if self.buttons["back"].collidepoint(mouse_pos) and "back_hover" in self.button_images:
                back_img = self.button_images["back_hover"]
            back_img = pygame.transform.scale(back_img, (self.buttons["back"].width, self.buttons["back"].height))
            screen.blit(back_img, self.buttons["back"])
        else:
            if self.buttons["back"].collidepoint(mouse_pos):
                color = (100, 150, 255)
            else:
                color = (70, 130, 180)
            pygame.draw.rect(screen, color, self.buttons["back"])
            pygame.draw.rect(screen, (255, 255, 255), self.buttons["back"], 3)
        
        back_text = font_medium.render("뒤로가기", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.buttons["back"].center)
        screen.blit(back_text, back_rect)

