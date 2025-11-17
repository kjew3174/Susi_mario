"""결과 씬"""
import pygame
from utils.json_loader import load_json, save_json
from utils.font_loader import get_korean_font
import os
import math


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
        
        # 기록이 없으면 메시지 출력
        if self.grade is None:
            print("기록이 없습니다. 백분율과 대학 로고를 표시할 수 없습니다.")
            self.university = None
            self.message = "기록이 없습니다."
        else:
            self.university = self.get_university()
            self.message = self.get_message()
        
        self.buttons = {}
        self.button_rect = None  # 400x80px 버튼
        self.button_rect_hover = None  # 400x80px 버튼 호버
        self.background_image = None
        self.bridge_image = None
        self.university_logo = None  # 대학 로고 이미지
        self.university_logos = {}  # 대학 로고 딕셔너리
        self.setup_buttons()
        
        # 기록 저장
        self.save_record()
    
    def load_images(self, background_path: str = None, bridge_path: str = None, button_rect: str = None, button_rect_hover: str = None, university_logos: dict = None):
        """
        이미지 로드
        
        Args:
            background_path: 배경 이미지 경로 (victory 또는 gameover에 따라 다름)
            bridge_path: 한강 철교 이미지 경로
            button_rect: 400x80px 버튼 이미지 경로
            button_rect_hover: 400x80px 버튼 호버 이미지 경로
            university_logos: 대학 로고 이미지 딕셔너리 {"서울대학교": path, ...}
        """
        try:
            if background_path:
                self.background_image = pygame.image.load(background_path).convert()
                self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
            if bridge_path:
                self.bridge_image = pygame.image.load(bridge_path).convert_alpha()
            if button_rect:
                self.button_rect = pygame.image.load(button_rect).convert_alpha()
            if button_rect_hover:
                self.button_rect_hover = pygame.image.load(button_rect_hover).convert_alpha()
            if university_logos:
                self.university_logos = university_logos
                # 현재 대학의 로고 로드
                if self.university in university_logos:
                    try:
                        self.university_logo = pygame.image.load(university_logos[self.university]).convert_alpha()
                    except:
                        if self.debug:
                            print(f"[DEBUG] 대학 로고 로드 실패: {self.university}")
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 결과 화면 이미지 로드 실패: {e}")
    
    def calculate_grade(self, mean_time: float = None, std_dev: float = None) -> float:
        """
        등급 계산 (백분율) - 정규분포 기반
        
        Args:
            mean_time: 평균 시간 (초). None이면 기록에서 계산
            std_dev: 표준 편차 (초). None이면 기록에서 계산
        
        Returns:
            등급 (백분율)
        """
        # 평균과 표준 편차가 제공되지 않으면 기록에서 계산
        if mean_time is None or std_dev is None:
            stats = self._calculate_statistics()
            if stats is None:
                # 기록이 없음
                return None
            mean_time, std_dev = stats
        
        # 표준 편차가 0이거나 너무 작으면 기본 계산 사용
        if std_dev <= 0 or std_dev < 0.1:
            # 기본 계산 (빠를수록 높은 등급)
            if self.time <= 0:
                return 100.0
            base_time = mean_time if mean_time > 0 else 60.0
            grade = max(0, min(100, (base_time / self.time) * 100))
        else:
            # 정규분포 기반 백분율 계산
            grade = self._calculate_percentage_from_normal_distribution(
                mean_time, std_dev, self.time
            )
        
        return min(100, grade)
    
    def _calculate_statistics(self) -> tuple:
        """
        기록에서 평균 시간과 표준 편차 계산
        
        Returns:
            (평균 시간, 표준 편차) 튜플 또는 None (기록이 없을 때)
        """
        record_path = "data/record.json"
        records = load_json(record_path, self.debug)
        
        if not isinstance(records, list) or len(records) == 0:
            # 기록이 없음
            return None
        
        # 클리어한 기록만 사용
        clear_times = [r.get("time", 0) for r in records if r.get("victory", False) and r.get("time", 0) > 0]
        
        if len(clear_times) == 0:
            # 클리어 기록이 없음
            return None
        
        # 평균 계산
        mean_time = sum(clear_times) / len(clear_times)
        
        # 표준 편차 계산
        if len(clear_times) < 2:
            std_dev = 15.0  # 기본 표준 편차
        else:
            variance = sum((t - mean_time) ** 2 for t in clear_times) / len(clear_times)
            std_dev = math.sqrt(variance)
            
            # 표준 편차가 너무 작으면 기본값 사용
            if std_dev < 1.0:
                std_dev = 15.0
        
        return (mean_time, std_dev)
    
    def _calculate_percentage_from_normal_distribution(self, mean: float, std_dev: float, actual_time: float) -> float:
        """
        정규분포를 사용하여 백분율 계산
        
        Args:
            mean: 평균 시간
            std_dev: 표준 편차
            actual_time: 실제 기록 시간
        
        Returns:
            백분율 (0-100)
        """
        if actual_time <= 0:
            return 100.0
        
        # Z-score 계산 (빠를수록 높은 점수이므로 평균 - 실제 기록)
        z_score = (mean - actual_time) / std_dev
        
        # 정규분포의 누적분포함수(CDF)를 사용하여 백분율 계산
        # math.erf를 사용한 근사값
        # CDF = 0.5 * (1 + erf(z / sqrt(2)))
        cdf = 0.5 * (1 + math.erf(z_score / math.sqrt(2)))
        
        # 백분율로 변환 (0-100)
        percentage = cdf * 100
        
        # 범위 제한
        return max(0, min(100, percentage))
    
    def get_university(self) -> str:
        """
        등급에 따른 대학 반환
        
        Returns:
            대학 이름
        """
        if self.grade is None:
            return None
        
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
        
        # 새 기록 추가 (grade가 None이 아닐 때만)
        if self.grade is not None:
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
        # 배경 이미지
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            # 배경 색상
            if self.victory:
                screen.fill((50, 150, 50))  # 초록색
            else:
                screen.fill((150, 50, 50))  # 빨간색
        
        # 폰트
        font_large = get_korean_font(72, self.debug)
        font_medium = get_korean_font(48, self.debug)
        font_small = get_korean_font(36, self.debug)
        
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
        
        # 등급 표시 (기록이 있을 때만)
        if self.grade is not None:
            grade_text = font_medium.render(f"등급: {self.grade:.1f}%", True, (255, 255, 255))
            grade_rect = grade_text.get_rect(center=(1920 // 2, 350))
            screen.blit(grade_text, grade_rect)
        
        # 대학 표시 (기록이 있을 때만)
        if self.grade is not None and self.university:
            if self.victory and self.university_logo:
                # 대학 로고 이미지 표시
                logo_rect = self.university_logo.get_rect(center=(1920 // 2, 450))
                screen.blit(self.university_logo, logo_rect)
            else:
                # 텍스트로 표시
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
            # 400x80px 버튼 이미지 사용
            if self.button_rect:
                button_img = self.button_rect
                if rect.collidepoint(mouse_pos) and self.button_rect_hover:
                    button_img = self.button_rect_hover
                button_img = pygame.transform.scale(button_img, (rect.width, rect.height))
                screen.blit(button_img, rect)
            else:
                # 이미지가 없으면 색상으로 표시
                if rect.collidepoint(mouse_pos):
                    color = (100, 150, 255)
                else:
                    color = (70, 130, 180)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
            text = font_medium.render(button_labels[key], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # 한강 철교 이미지 (패배 시 또는 등급이 낮을 때)
        if not self.victory and self.bridge_image:
            bridge_rect = self.bridge_image.get_rect(center=(1920 // 2, 700))
            screen.blit(self.bridge_image, bridge_rect)
        elif self.victory and self.grade < 50 and self.bridge_image:
            bridge_rect = self.bridge_image.get_rect(center=(1920 // 2, 700))
            screen.blit(self.bridge_image, bridge_rect)

