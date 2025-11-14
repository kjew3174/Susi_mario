"""메뉴 씬"""
import pygame
from utils.json_loader import load_json


class MenuScene:
    """메인 메뉴 씬"""
    
    def __init__(self, debug: bool = False):
        """
        MenuScene 초기화
        
        Args:
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.buttons = {}
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.background_image = None
        self.title_image = None
        
        # 버튼 위치 설정
        self.setup_buttons()
        
    def setup_buttons(self):
        """버튼 위치 설정"""
        screen_width = 1920
        screen_height = 1080
        
        self.buttons = {
            "start": pygame.Rect(screen_width // 2 - 200, screen_height // 2, 400, 80),
            "setting": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 100, 400, 80),
            "explanation": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 200, 400, 80),
            "exit": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 300, 400, 80)
        }
    
    def load_images(self, background_path: str = None, title_path: str = None):
        """
        이미지 로드
        
        Args:
            background_path: 배경 이미지 경로
            title_path: 타이틀 이미지 경로
        """
        try:
            if background_path:
                self.background_image = pygame.image.load(background_path).convert()
                self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
            if title_path:
                self.title_image = pygame.image.load(title_path).convert_alpha()
        except:
            if self.debug:
                print("[DEBUG] 메뉴 이미지 로드 실패")
    
    def update(self, events: list) -> str:
        """
        이벤트 처리 및 업데이트
        
        Args:
            events: pygame 이벤트 리스트
            
        Returns:
            다음 씬 이름 ("game", "setting", "explanation", "exit", "")
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in events:
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons["start"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 시작 버튼 클릭")
                    return "game"
                elif self.buttons["setting"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 설정 버튼 클릭")
                    return "setting"
                elif self.buttons["explanation"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 게임 설명 버튼 클릭")
                    return "explanation"
                elif self.buttons["exit"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 종료 버튼 클릭")
                    return "exit"
        
        return ""
    
    def render(self, screen: pygame.Surface) -> None:
        """
        화면 렌더링
        
        Args:
            screen: 화면 Surface
        """
        # 배경
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((135, 206, 235))  # 하늘색
        
        # 폰트 초기화
        if not self.font_large:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 36)
        
        # 타이틀
        if self.title_image:
            title_rect = self.title_image.get_rect(center=(1920 // 2, 200))
            screen.blit(self.title_image, title_rect)
        else:
            title_text = self.font_large.render("수시마리오", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(1920 // 2, 200))
            screen.blit(title_text, title_rect)
        
        # 버튼 그리기
        mouse_pos = pygame.mouse.get_pos()
        button_labels = {
            "start": "시작하기",
            "setting": "설정",
            "explanation": "게임 설명",
            "exit": "종료"
        }
        
        for key, rect in self.buttons.items():
            # 호버 효과
            if rect.collidepoint(mouse_pos):
                color = (100, 150, 255)
            else:
                color = (70, 130, 180)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
            # 버튼 텍스트
            text = self.font_medium.render(button_labels[key], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

