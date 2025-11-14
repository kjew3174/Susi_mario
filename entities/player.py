"""플레이어 엔티티 클래스"""
import pygame


class Player:
    """플레이어 캐릭터 클래스"""
    
    def __init__(self, x: int, y: int, size: int = 160, debug: bool = False):
        """
        Player 초기화
        
        Args:
            x: 초기 x 좌표
            y: 초기 y 좌표
            size: 캐릭터 크기 (기본 160x160)
            debug: 디버깅 메시지 출력 여부
        """
        self.debug = debug
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.is_crouching = False
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 6000  # 6초 (밀리초)
        self.facing_right = True
        
        # 이미지 로드 (나중에 추가될 예정)
        self.image = None
        self.crouch_image = None
        
    def load_images(self, image_path: str, crouch_path: str = None):
        """
        플레이어 이미지 로드
        
        Args:
            image_path: 기본 이미지 경로
            crouch_path: 웅크리기 이미지 경로
        """
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            if crouch_path:
                self.crouch_image = pygame.image.load(crouch_path).convert_alpha()
                self.crouch_image = pygame.transform.scale(self.crouch_image, (self.size, self.size // 2))
        except:
            if self.debug:
                print(f"[DEBUG] 이미지 로드 실패: {image_path}")
    
    def update(self, dt: float, blocks: list, debug: bool = False) -> None:
        """
        플레이어 상태 업데이트
        
        Args:
            dt: 델타 타임 (초)
            blocks: 충돌할 블록 리스트
            debug: 디버깅 메시지 출력 여부
        """
        # 중력 적용
        if not self.on_ground:
            self.velocity_y += self.gravity
        
        # 수평 이동
        self.rect.x += int(self.velocity_x * dt * 60)
        
        # 수직 이동
        self.rect.y += int(self.velocity_y * dt * 60)
        
        # 블록과의 충돌 검사
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block):
                # 아래에서 충돌 (땅에 착지)
                if self.velocity_y > 0 and self.rect.bottom > block.top:
                    self.rect.bottom = block.top
                    self.velocity_y = 0
                    self.on_ground = True
                # 위에서 충돌 (천장)
                elif self.velocity_y < 0 and self.rect.top < block.bottom:
                    self.rect.top = block.bottom
                    self.velocity_y = 0
                # 좌우 충돌
                if self.velocity_x > 0 and self.rect.right > block.left and self.rect.left < block.left:
                    self.rect.right = block.left
                    self.velocity_x = 0
                elif self.velocity_x < 0 and self.rect.left < block.right and self.rect.right > block.right:
                    self.rect.left = block.right
                    self.velocity_x = 0
        
        # 화면 밖으로 나가지 않도록
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1920:  # 화면 너비
            self.rect.right = 1920
        
        # 무적 타이머 업데이트
        if self.invincible:
            self.invincible_timer -= dt * 1000
            if self.invincible_timer <= 0:
                self.invincible = False
                if debug:
                    print("[DEBUG] 무적 상태 해제")
        
        # 속도 감소 (마찰)
        self.velocity_x *= 0.9
    
    def jump(self, power: float = None) -> None:
        """
        점프
        
        Args:
            power: 점프 파워 (None이면 기본값 사용)
        """
        if self.on_ground and not self.is_crouching:
            self.velocity_y = power if power else self.jump_power
            self.on_ground = False
            if self.debug:
                print("[DEBUG] 점프!")
    
    def move_left(self) -> None:
        """왼쪽으로 이동"""
        self.velocity_x = -self.speed
        self.facing_right = False
    
    def move_right(self) -> None:
        """오른쪽으로 이동"""
        self.velocity_x = self.speed
        self.facing_right = True
    
    def crouch(self) -> None:
        """웅크리기"""
        if self.on_ground:
            self.is_crouching = True
            self.rect.height = self.size // 2
    
    def stand_up(self) -> None:
        """일어서기"""
        self.is_crouching = False
        self.rect.height = self.size
    
    def activate_invincibility(self, duration: int = 6000) -> None:
        """
        무적 상태 활성화
        
        Args:
            duration: 무적 지속 시간 (밀리초)
        """
        self.invincible = True
        self.invincible_timer = duration
        if self.debug:
            print(f"[DEBUG] 무적 상태 활성화: {duration}ms")
    
    def take_damage(self) -> bool:
        """
        데미지 받기
        
        Returns:
            사망 여부 (True면 사망)
        """
        if not self.invincible:
            self.lives -= 1
            if self.debug:
                print(f"[DEBUG] 데미지! 남은 목숨: {self.lives}")
            return self.lives <= 0
        return False
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        플레이어 그리기
        
        Args:
            screen: 화면 Surface
        """
        if self.image:
            # 방향에 따라 이미지 뒤집기
            img = self.image
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            
            # 웅크리기 상태면 웅크리기 이미지 사용
            if self.is_crouching and self.crouch_image:
                img = self.crouch_image
                if not self.facing_right:
                    img = pygame.transform.flip(img, True, False)
                screen.blit(img, (self.rect.x, self.rect.y + self.size // 2))
            else:
                screen.blit(img, self.rect)
            
            # 무적 상태일 때 깜빡임 효과
            if self.invincible:
                alpha = 128 + int(127 * (self.invincible_timer / self.invincible_duration))
                img_copy = img.copy()
                img_copy.set_alpha(alpha)
                screen.blit(img_copy, self.rect)
        else:
            # 이미지가 없으면 색상으로 표시
            color = (255, 0, 0) if not self.invincible else (255, 255, 0)
            if self.invincible and int(self.invincible_timer / 100) % 2 == 0:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, self.rect)

