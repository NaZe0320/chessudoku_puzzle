import json
from datetime import datetime
from board import Board
from validators import Piece

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("경고: requests 모듈이 설치되지 않았습니다.")
    print("실제 서버 전송을 위해서는 'pip install requests'를 실행해주세요.")

class PuzzleDataFormatter:
    """퍼즐 데이터를 API 형식으로 변환하는 클래스"""
    
    @staticmethod
    def piece_type_to_name(piece_type):
        """체스 기물 타입을 이름으로 변환"""
        piece_map = {
            'K': 'king',
            'Q': 'queen', 
            'R': 'rook',
            'B': 'bishop',
            'N': 'knight'
        }
        return piece_map.get(piece_type, 'unknown')
    
    @staticmethod
    def board_to_array(board):
        """Board 객체를 2차원 배열로 변환"""
        result = []
        for row in range(9):
            board_row = []
            for col in range(9):
                value = board.get_value(row, col)
                # 기물이 있는 경우 0으로, 숫자가 있는 경우 그 숫자로, 빈칸은 0으로
                if value is None:
                    board_row.append(0)
                elif isinstance(value, str):  # 기물 타입 (K, Q, R, B, N)
                    board_row.append(0)  # 퍼즐에서는 기물 위치를 0으로 표시
                elif isinstance(value, int):
                    board_row.append(value)
                else:
                    board_row.append(0)
            result.append(board_row)
        return result
    
    @staticmethod
    def pieces_to_api_format(pieces):
        """기물 리스트를 API 형식으로 변환"""
        api_pieces = []
        for piece in pieces:
            api_piece = {
                "type": PuzzleDataFormatter.piece_type_to_name(piece.piece_type),
                "position": [piece.row, piece.col]
            }
            api_pieces.append(api_piece)
        return api_pieces
    
    @staticmethod
    def create_puzzle_payload(puzzle_board, answer_board, pieces, difficulty="medium", puzzle_type="normal", daily_date=None):
        """퍼즐 생성 API 요청 페이로드 생성"""
        payload = {
            "puzzle_type": puzzle_type,
            "difficulty": difficulty,
            "puzzle_data": {
                "board": PuzzleDataFormatter.board_to_array(puzzle_board),
                "pieces": PuzzleDataFormatter.pieces_to_api_format(pieces)
            },
            "answer_data": {
                "board": PuzzleDataFormatter.board_to_array(answer_board)
            }
        }
        
        # 데일리 퍼즐인 경우 날짜 추가
        if daily_date:
            payload["daily_date"] = daily_date
            
        return payload

class PuzzleAPIClient:
    """퍼즐 서버와 통신하는 API 클라이언트"""
    
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
        else:
            self.session = None
        
    def upload_puzzle(self, puzzle_board, answer_board, pieces, difficulty="medium", puzzle_type="normal", daily_date=None):
        """퍼즐을 서버에 업로드"""
        if not REQUESTS_AVAILABLE:
            print("❌ requests 모듈이 없어 서버 전송을 할 수 없습니다.")
            print("데이터 포맷팅만 테스트합니다...")
            
            # 데이터 포맷팅 테스트
            payload = PuzzleDataFormatter.create_puzzle_payload(
                puzzle_board, answer_board, pieces, difficulty, puzzle_type, daily_date
            )
            
            print("✅ 데이터 포맷팅 성공!")
            print(f"페이로드 크기: {len(json.dumps(payload))} bytes")
            print(f"기물 개수: {len(pieces)}개")
            print(f"난이도: {difficulty}")
            print(f"퍼즐 타입: {puzzle_type}")
            if daily_date:
                print(f"데일리 날짜: {daily_date}")
            
            return False, None
        
        try:
            # API 페이로드 생성
            payload = PuzzleDataFormatter.create_puzzle_payload(
                puzzle_board, answer_board, pieces, difficulty, puzzle_type, daily_date
            )
            
            # API 요청 전송
            url = f"{self.base_url}/api/puzzle"
            headers = {
                "Content-Type": "application/json"
            }
            
            print(f"서버로 퍼즐 전송 중... ({url})")
            print(f"난이도: {difficulty}, 타입: {puzzle_type}")
            print(f"기물 개수: {len(pieces)}개")
            
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 201:
                result = response.json()
                puzzle_id = result.get("data", {}).get("puzzle_id")
                print(f"✅ 퍼즐 업로드 성공! (ID: {puzzle_id})")
                return True, result
            else:
                print(f"❌ 퍼즐 업로드 실패: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"오류 메시지: {error_data.get('message', '알 수 없는 오류')}")
                except:
                    print(f"응답 내용: {response.text}")
                return False, None
                
        except Exception as e:
            if REQUESTS_AVAILABLE and "ConnectionError" in str(type(e)):
                print("❌ 서버 연결 실패: 서버가 실행 중인지 확인해주세요.")
                return False, None
            elif REQUESTS_AVAILABLE and "Timeout" in str(type(e)):
                print("❌ 요청 시간 초과: 서버 응답이 너무 느립니다.")
                return False, None
            else:
                print(f"❌ 예상치 못한 오류: {str(e)}")
                return False, None
    
    def set_server_url(self, url):
        """서버 URL 설정"""
        self.base_url = url
        print(f"서버 URL 설정: {url}")

class DifficultyManager:
    """난이도별 설정 관리"""
    
    DIFFICULTY_SETTINGS = {
        "easy": {
            "max_holes": 35,
            "description": "쉬움 (35개 이하 빈칸)"
        },
        "medium": {
            "max_holes": 50, 
            "description": "보통 (50개 이하 빈칸)"
        },
        "hard": {
            "max_holes": 65,
            "description": "어려움 (65개 이하 빈칸)"
        },
        "expert": {
            "max_holes": 75,
            "description": "전문가 (75개 이하 빈칸)"
        }
    }
    
    @classmethod
    def get_max_holes(cls, difficulty):
        """난이도에 따른 최대 빈칸 개수 반환"""
        return cls.DIFFICULTY_SETTINGS.get(difficulty, {}).get("max_holes", 50)
    
    @classmethod
    def get_difficulty_by_holes(cls, holes_count):
        """빈칸 개수에 따른 난이도 결정"""
        if holes_count <= 35:
            return "easy"
        elif holes_count <= 50:
            return "medium"
        elif holes_count <= 65:
            return "hard"
        else:
            return "expert"
    
    @classmethod
    def list_difficulties(cls):
        """사용 가능한 난이도 목록 출력"""
        print("사용 가능한 난이도:")
        for difficulty, settings in cls.DIFFICULTY_SETTINGS.items():
            print(f"  - {difficulty}: {settings['description']}")

# 사용 예시 및 테스트 함수
def test_data_formatting():
    """데이터 포맷팅 테스트"""
    print("=" * 50)
    print("데이터 포맷팅 테스트")
    print("=" * 50)
    
    # 테스트용 보드 생성
    board = Board()
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 2)
    board.set_value(1, 0, None)  # 빈칸
    
    # 테스트용 기물 생성
    pieces = [
        Piece('K', 4, 4),
        Piece('Q', 3, 3)
    ]
    
    # 포맷팅 테스트
    board_array = PuzzleDataFormatter.board_to_array(board)
    pieces_array = PuzzleDataFormatter.pieces_to_api_format(pieces)
    
    print("보드 배열:")
    for row in board_array[:3]:  # 처음 3줄만 출력
        print(row)
    
    print("\n기물 배열:")
    for piece in pieces_array:
        print(piece)
    
    # 전체 페이로드 생성
    payload = PuzzleDataFormatter.create_puzzle_payload(
        board, board, pieces, "medium", "normal"
    )
    
    print(f"\n생성된 페이로드 크기: {len(json.dumps(payload))} bytes")
    print("페이로드 구조 확인 완료!")

if __name__ == "__main__":
    # 테스트 실행
    test_data_formatting()
    
    # 난이도 목록 출력
    print("\n")
    DifficultyManager.list_difficulties()
