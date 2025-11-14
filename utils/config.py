"""게임 설정 관리 클래스"""
import os
from utils.json_loader import load_json, save_json


class Config:
    """게임 설정을 관리하는 클래스"""
    
    def __init__(self, debug: bool = False):
        """
        Config 초기화
        
        Args:
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.screen_width = 1920
        self.screen_height = 1080
        self.volume = 0.7
        self.difficulty = "normal"  # "easy", "normal", "hard"
        self.block_size = 160
        self.player_size = 160
        
    def load(self, path: str = "data/config.json") -> None:
        """
        설정 파일에서 데이터 로드
        
        Args:
            path: 설정 파일 경로
        """
        data = load_json(path, self.debug)
        if data:
            self.screen_width = data.get("screen_width", self.screen_width)
            self.screen_height = data.get("screen_height", self.screen_height)
            self.volume = data.get("volume", self.volume)
            self.difficulty = data.get("difficulty", self.difficulty)
            self.block_size = data.get("block_size", self.block_size)
            self.player_size = data.get("player_size", self.player_size)
            if self.debug:
                print(f"[DEBUG] 설정 로드 완료: {path}")
    
    def save(self, path: str = "data/config.json") -> None:
        """
        현재 설정을 파일로 저장
        
        Args:
            path: 저장할 설정 파일 경로
        """
        data = {
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "volume": self.volume,
            "difficulty": self.difficulty,
            "block_size": self.block_size,
            "player_size": self.player_size
        }
        save_json(path, data, self.debug)
        if self.debug:
            print(f"[DEBUG] 설정 저장 완료: {path}")

