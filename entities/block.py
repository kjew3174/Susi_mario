"""블록 엔티티 관리"""
import pygame


def load_blocks(map_data: list[list[int]], block_size: int = 160, debug: bool = False) -> list[pygame.Rect]:
    """
    맵 데이터를 읽어 충돌용 블록 좌표 생성
    
    Args:
        map_data: 맵 데이터 (2D 리스트)
        block_size: 블록 크기
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        블록 Rect 리스트
    """
    blocks = []
    
    # 맵 데이터에서 블록 위치 찾기 (예: 값 1 = 일반 블록, 2 = 아이템 블록)
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 1 or cell == 2:  # 일반 블록 또는 아이템 블록
                blocks.append(pygame.Rect(x * block_size, y * block_size, block_size, block_size))
    
    if debug:
        print(f"[DEBUG] {len(blocks)}개의 블록 로드됨")
    
    return blocks


def get_block_types(map_data: list[list[int]], block_size: int = 160, debug: bool = False) -> dict:
    """
    블록 타입별 위치 정보 반환
    
    Args:
        map_data: 맵 데이터 (2D 리스트)
        block_size: 블록 크기
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        블록 타입별 딕셔너리 {"normal": [...], "item": [...], "pipe": [...]}
    """
    block_types = {
        "normal": [],
        "item": [],
        "pipe": []
    }
    
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 1:  # 일반 블록
                block_types["normal"].append(pygame.Rect(x * block_size, y * block_size, block_size, block_size))
            elif cell == 2:  # 아이템 블록
                block_types["item"].append(pygame.Rect(x * block_size, y * block_size, block_size, block_size))
            elif cell == 8:  # 토관 (논술)
                block_types["pipe"].append(pygame.Rect(x * block_size, y * block_size, block_size, block_size * 2))
    
    if debug:
        print(f"[DEBUG] 블록 타입별 로드: 일반={len(block_types['normal'])}, 아이템={len(block_types['item'])}, 토관={len(block_types['pipe'])}")
    
    return block_types


def draw_blocks(screen: pygame.Surface, blocks: list[pygame.Rect], block_types: dict = None, images: dict = None, debug: bool = False) -> None:
    """
    블록 그리기
    
    Args:
        screen: 화면 Surface
        blocks: 블록 Rect 리스트
        block_types: 블록 타입별 딕셔너리 (선택사항)
        images: 블록 이미지 딕셔너리 (선택사항)
        debug: 디버깅 메시지 출력 여부
    """
    if block_types and images:
        # 타입별로 다른 이미지 사용
        for block_type, rects in block_types.items():
            if block_type in images:
                img = images[block_type]
                for rect in rects:
                    screen.blit(img, rect)
    else:
        # 이미지가 없으면 색상으로 표시
        for block in blocks:
            pygame.draw.rect(screen, (139, 69, 19), block)  # 갈색
            pygame.draw.rect(screen, (0, 0, 0), block, 2)  # 검은 테두리

