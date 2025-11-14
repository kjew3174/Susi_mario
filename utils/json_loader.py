"""JSON 파일 로딩 및 저장 유틸리티"""
import json
import os


def load_json(path: str, debug: bool = False) -> dict | list:
    """
    JSON 파일을 읽어서 dict 또는 list로 반환
    
    Args:
        path: JSON 파일 경로
        debug: 디버깅 메시지 출력 여부
        
    Returns:
        JSON 데이터 (dict 또는 list)
    """
    try:
        if not os.path.exists(path):
            if debug:
                print(f"[DEBUG] JSON 파일이 없습니다: {path}")
            return {}
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if debug:
                print(f"[DEBUG] JSON 파일 로드 성공: {path}")
            return data
    except json.JSONDecodeError as e:
        if debug:
            print(f"[DEBUG] JSON 파싱 오류: {e}")
        return {}
    except Exception as e:
        if debug:
            print(f"[DEBUG] JSON 로드 오류: {e}")
        return {}


def save_json(path: str, data: dict | list, debug: bool = False) -> None:
    """
    데이터를 JSON 파일로 저장
    
    Args:
        path: 저장할 JSON 파일 경로
        data: 저장할 데이터 (dict 또는 list)
        debug: 디버깅 메시지 출력 여부
    """
    try:
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            if debug:
                print(f"[DEBUG] JSON 파일 저장 성공: {path}")
    except Exception as e:
        if debug:
            print(f"[DEBUG] JSON 저장 오류: {e}")

