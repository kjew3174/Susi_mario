"""결과 씬"""
import pygame
from utils.json_loader import load_json, save_json
import os


class ResultScene:
    """게임 결과 씬"""
    
    def __init__(self, result: dict, debug: bool = False):
        """
        ResultScene 초기화
        
        Args:
            result: 게임 결과 딕셔너리 {"victory": bool, "time": float, "lives": int}
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.result = result
        self.victory = result.get("victory", False)
        self.time = result.get("time", 0)
        self.lives = result.get("lives", 0)
        self.grade = self.calculate_grade()
        self.university = self.get_university()
        self.message = self.get_message()
        
        self.buttons = {}
        self.setup_buttons()
        
        # 기록 저장
        self.save_record()
    
    def calculate_grade(self) -> float:
        """
        등급 계산 (백분율)
        
        Returns:
            등급 (백분율)
        """
        # 시간 기반 등급 계산 (빠를수록 높은 등급)
        # 예시: 60초 기준으로 계산
        base_time = 60.0
        if self.time <= 0:
            return 100.0
        
        grade = max(0, min(100, (base_time / self.time) * 100))
        
        # 목숨 보너스
        grade += self.lives * 5
        
        return min(100, grade)
    
    def get_university(self) -> str:
        """
        등급에 따른 대학 반환
        
        Returns:
            대학 이름
        """
        if self.grade >= 90:
            return "서울대학교"
        elif self.grade >= 80:
            return "연세대학교"
        elif self.grade >= 70:
            return "고려대학교"
        elif self.grade >= 60:
            return "중앙대학교"
        elif self.grade >= 50:
            return "한국외국어대학교"
        else:
            return "한강 철교"
    
    def get_message(self) -> str:
        """
        결과 메시지 반환
        
        Returns:
            메시지
        """
        if self.victory:
            return f"축하합니다! {self.university}에 합격했습니다!"
        else:
            return "아쉽네요. 다시 도전해보세요!"
    
    def setup_buttons(self):
        """버튼 위치 설정"""
        screen_width = 1920
        screen_height = 1080
        
        self.buttons = {
            "retry": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 200, 400, 80),
            "menu": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 300, 400, 80)
        }
    
    def save_record(self):
        """기록 저장"""
        record_path = "data/record.json"
        records = load_json(record_path, self.debug)
        
        if not isinstance(records, list):
            records = []
        
        # 새 기록 추가
        records.append({
            "victory": self.victory,
            "time": self.time,
            "lives": self.lives,
            "grade": self.grade,
            "university": self.university
        })
        
        # 100개까지만 저장
        if len(records) > 100:
            records = records[-100:]
        
        # 시간순으로 정렬
        records.sort(key=lambda x: x.get("time", float('inf')))
        
        save_json(record_path, records, self.debug)
    
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
                if self.buttons["retry"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 다시하기 버튼 클릭")
                    return "game"
                elif self.buttons["menu"].collidepoint(mouse_pos):
                    if self.debug:
                        print("[DEBUG] 메뉴로 버튼 클릭")
                    return "menu"
        
        return ""
    
    def render(self, screen: pygame.Surface) -> None:
        """
        화면 렌더링
        
        Args:
            screen: 화면 Surface
        """
        # 배경
        if self.victory:
            screen.fill((50, 150, 50))  # 초록색
        else:
            screen.fill((150, 50, 50))  # 빨간색
        
        # 폰트
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # 결과 텍스트
        if self.victory:
            result_text = font_large.render("클리어!", True, (255, 255, 255))
        else:
            result_text = font_large.render("게임 오버", True, (255, 255, 255))
        
        result_rect = result_text.get_rect(center=(1920 // 2, 200))
        screen.blit(result_text, result_rect)
        
        # 시간 표시
        minutes = int(self.time // 60)
        seconds = int(self.time % 60)
        time_text = font_medium.render(f"시간: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(1920 // 2, 300))
        screen.blit(time_text, time_rect)
        
        # 등급 표시
        grade_text = font_medium.render(f"등급: {self.grade:.1f}%", True, (255, 255, 255))
        grade_rect = grade_text.get_rect(center=(1920 // 2, 350))
        screen.blit(grade_text, grade_rect)
        
        # 대학 표시
        university_text = font_large.render(self.university, True, (255, 255, 255))
        university_rect = university_text.get_rect(center=(1920 // 2, 450))
        screen.blit(university_text, university_rect)
        
        # 메시지 표시
        message_text = font_small.render(self.message, True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(1920 // 2, 550))
        screen.blit(message_text, message_rect)
        
        # 버튼 그리기
        mouse_pos = pygame.mouse.get_pos()
        button_labels = {
            "retry": "다시하기",
            "menu": "메뉴로"
        }
        
        for key, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                color = (100, 150, 255)
            else:
                color = (70, 130, 180)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
            text = font_medium.render(button_labels[key], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # 한강 철교 이미지 (등급이 낮을 때)
        # 이미지 로드는 나중에 추가될 예정
        if self.grade < 50:
            bridge_text = font_medium.render("한강 철교", True, (255, 255, 255))
            bridge_rect = bridge_text.get_rect(center=(1920 // 2, 700))
            screen.blit(bridge_text, bridge_rect)

