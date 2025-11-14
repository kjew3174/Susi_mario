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
        self.invincible_duration = 2000  # 2초 (밀리초) - 부활 후 무적 시간
        self.facing_right = True
        
        # 점프 관련 (마리오 스타일)
        self.is_jumping = False
        self.jump_held = False
        self.max_jump_time = 0.3  # 최대 점프 시간 (초)
        self.jump_time = 0
        self.max_jump_height = 400  # 최대 점프 높이 (픽셀)
        self.jump_start_y = 0
        
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
    
    def update(self, dt: float, blocks: list, jump_held: bool = False, debug: bool = False) -> None:
        """
        플레이어 상태 업데이트
        
        Args:
            dt: 델타 타임 (초)
            blocks: 충돌할 블록 리스트
            jump_held: 점프 키가 눌려있는지 여부
            debug: 디버깅 메시지 출력 여부
        """
        # 점프 중 처리 (마리오 스타일)
        if self.is_jumping and jump_held:
            self.jump_time += dt
            # 최대 점프 시간 내에서만 계속 올라가기
            if self.jump_time < self.max_jump_time:
                # 점프 높이 제한 확인
                current_height = self.jump_start_y - self.rect.y
                if current_height < self.max_jump_height:
                    self.velocity_y = self.jump_power
                else:
                    # 최대 높이 도달 시 중력 적용
                    self.velocity_y += self.gravity
            else:
                # 최대 점프 시간 초과 시 중력 적용
                self.velocity_y += self.gravity
        else:
            # 점프가 끝났거나 키를 떼면 중력 적용
            if self.is_jumping:
                self.is_jumping = False
                self.jump_time = 0
            
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
                    self.is_jumping = False
                    self.jump_time = 0
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
        점프 시작
        
        Args:
            power: 점프 파워 (None이면 기본값 사용, 마리오 스타일에서는 사용 안 함)
        """
        if self.on_ground and not self.is_crouching and not self.is_jumping:
            self.is_jumping = True
            self.jump_held = True
            self.jump_time = 0
            self.jump_start_y = self.rect.y
            self.velocity_y = self.jump_power
            self.on_ground = False
            if self.debug:
                print("[DEBUG] 점프 시작!")
    
    def stop_jump(self):
        """점프 중단 (키를 뗄 때)"""
        self.jump_held = False
    
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
        데미지 받기 (체력 없이 바로 죽고 목숨 감소)
        
        Returns:
            게임 오버 여부 (목숨이 1일 때 죽으면 True)
        """
        if not self.invincible:
            self.lives -= 1
            if self.debug:
                print(f"[DEBUG] 사망! 남은 목숨: {self.lives}")
            # 목숨이 1일 때 죽으면 게임 오버
            if self.lives <= 0:
                return True
            # 목숨이 남아있으면 부활 (무적 상태 활성화)
            self.activate_invincibility(self.invincible_duration)
            # 시작 위치로 리셋 (또는 체크포인트로)
            return False
        return False
    
    def draw(self, screen: pygame.Surface, camera_x: int = 0) -> None:
        """
        플레이어 그리기
        
        Args:
            screen: 화면 Surface
            camera_x: 카메라 x 오프셋
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        
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
                screen.blit(img, (draw_rect.x, draw_rect.y + self.size // 2))
            else:
                screen.blit(img, draw_rect)
            
            # 무적 상태일 때 깜빡임 효과
            if self.invincible:
                alpha = 128 + int(127 * (self.invincible_timer / self.invincible_duration))
                img_copy = img.copy()
                img_copy.set_alpha(alpha)
                screen.blit(img_copy, draw_rect)
        else:
            # 이미지가 없으면 색상으로 표시
            color = (255, 0, 0) if not self.invincible else (255, 255, 0)
            if self.invincible and int(self.invincible_timer / 100) % 2 == 0:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, draw_rect)

