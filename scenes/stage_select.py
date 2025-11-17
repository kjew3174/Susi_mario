"""스테이지 선택 씬"""
import pygame
from utils.font_loader import get_korean_font
from utils.json_loader import load_json
import os


class StageSelectScene:
    """스테이지 선택 씬"""
    
    def __init__(self, debug: bool = False):
        """
        StageSelectScene 초기화
        
        Args:
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.buttons = {}
        self.stage_buttons = []
        self.button_rect = None  # 400x80px 버튼
        self.button_rect_hover = None  # 400x80px 버튼 호버
        self.button_square = None  # 80x80px 버튼
        self.button_square_hover = None  # 80x80px 버튼 호버
        self.background_image = None
        self.selected_stage = None
        
        self.setup_buttons()
        self.load_stages()
    
    def load_stages(self):
        """스테이지 목록 로드"""
        stages_dir = "data/maps"
        self.stages = []
        
        if os.path.exists(stages_dir):
            for filename in os.listdir(stages_dir):
                if filename.endswith(".json"):
                    stage_name = filename.replace(".json", "")
                    self.stages.append({
                        "name": stage_name,
                        "path": os.path.join(stages_dir, filename)
                    })
        
        # 스테이지가 없으면 기본 스테이지 추가
        if not self.stages:
            self.stages.append({
                "name": "level1",
                "path": "data/maps/level1.json"
            })
        
        # 스테이지 버튼 생성 (가로 5개씩)
        self.stage_buttons = []
        button_width = 200
        button_height = 200
        start_x = 1920 // 2 - (button_width * 2.5 + 20 * 2)
        start_y = 300
        
        for i, stage in enumerate(self.stages):
            row = i // 5
            col = i % 5
            x = start_x + col * (button_width + 20)
            y = start_y + row * (button_height + 20)
            
            self.stage_buttons.append({
                "rect": pygame.Rect(x, y, button_width, button_height),
                "stage": stage,
                "index": i
            })
    
    def setup_buttons(self):
        """버튼 위치 설정"""
        screen_width = 1920
        screen_height = 1080
        
        self.buttons = {
            "back": pygame.Rect(screen_width // 2 - 200, screen_height - 100, 400, 80)
        }
    
    def load_images(self, background_path: str = None, button_rect: str = None, button_rect_hover: str = None, button_square: str = None, button_square_hover: str = None):
        """
        이미지 로드
        
        Args:
            background_path: 배경 이미지 경로
            button_rect: 400x80px 버튼 이미지 경로
            button_rect_hover: 400x80px 버튼 호버 이미지 경로
            button_square: 80x80px 버튼 이미지 경로
            button_square_hover: 80x80px 버튼 호버 이미지 경로
        """
        try:
            if background_path:
                self.background_image = pygame.image.load(background_path).convert()
                self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
            if button_rect:
                self.button_rect = pygame.image.load(button_rect).convert_alpha()
            if button_rect_hover:
                self.button_rect_hover = pygame.image.load(button_rect_hover).convert_alpha()
            if button_square:
                self.button_square = pygame.image.load(button_square).convert_alpha()
            if button_square_hover:
                self.button_square_hover = pygame.image.load(button_square_hover).convert_alpha()
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 스테이지 선택 화면 이미지 로드 실패: {e}")
    
    def update(self, events: list) -> str:
        """
        이벤트 처리 및 업데이트
        
        Args:
            events: pygame 이벤트 리스트
            
        Returns:
            다음 씬 이름 ("menu", "game", "")
        """
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 뒤로가기 버튼
                if self.buttons["back"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 뒤로가기 버튼 클릭")
                    return "menu"
                
                # 스테이지 버튼
                for btn_info in self.stage_buttons:
                    if btn_info["rect"].collidepoint(mouse_pos):
                        self.selected_stage = btn_info["stage"]["path"]
                        if self.debug:
                            print(f"[DEBUG] 스테이지 선택: {btn_info['stage']['name']}")
                        return "game"
        
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
            screen.fill((50, 50, 50))
        
        # 폰트
        font_large = get_korean_font(72, self.debug)
        font_medium = get_korean_font(48, self.debug)
        font_small = get_korean_font(36, self.debug)
        
        # 제목
        title_text = font_large.render("스테이지 선택", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(1920 // 2, 150))
        screen.blit(title_text, title_rect)
        
        # 스테이지 버튼 그리기
        mouse_pos = pygame.mouse.get_pos()
        for btn_info in self.stage_buttons:
            rect = btn_info["rect"]
            stage = btn_info["stage"]
            
            # 정사각형 버튼 사용 (크기 조정)
            if self.button_square:
                btn_img = self.button_square
                if rect.collidepoint(mouse_pos) and self.button_square_hover:
                    btn_img = self.button_square_hover
                btn_img = pygame.transform.scale(btn_img, (rect.width, rect.height))
                screen.blit(btn_img, rect)
            else:
                # 이미지가 없으면 색상으로 표시
                if rect.collidepoint(mouse_pos):
                    color = (100, 150, 255)
                else:
                    color = (70, 130, 180)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
            # 스테이지 번호 표시
            stage_text = font_medium.render(f"{btn_info['index'] + 1}", True, (255, 255, 255))
            stage_rect = stage_text.get_rect(center=rect.center)
            screen.blit(stage_text, stage_rect)
        
        # 뒤로가기 버튼
        if self.button_rect:
            back_img = self.button_rect
            if self.buttons["back"].collidepoint(mouse_pos) and self.button_rect_hover:
                back_img = self.button_rect_hover
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

