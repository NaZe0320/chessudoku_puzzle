from board import Board
from validators import PiecePlacer, SudokuValidator
import random

class ChessSudokuSolver:
    """체스 기물과 스도쿠 제약 조건을 모두 고려한 솔버"""
    
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces  # 배치된 기물들
        self.sudoku_validator = SudokuValidator(board)
        self.piece_placer = PiecePlacer(board)
        self.piece_placer.pieces = pieces  # 기물 정보 설정
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 체스 기물과 스도쿠 규칙 모두 검사"""
        # 1. 기본 스도쿠 규칙 검사
        if not self.sudoku_validator.is_valid_number(row, col, number):
            return False
        
        # 2. 체스 기물 규칙 검사
        if not self.piece_placer.is_valid_number_for_piece(row, col, number):
            return False
        
        return True
    
    def find_empty_cell(self):
        """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
        # 기물이 있는 위치도 숫자로 채워야 하므로 직접 검사
        for row in range(9):
            for col in range(9):
                value = self.board.get_value(row, col)
                # None이거나 기물 문자인 경우 빈 칸으로 간주
                if value is None or isinstance(value, str):
                    return (row, col)
        return None
    
    def solve(self):
        """백트래킹을 사용한 스도쿠 솔버"""
        empty_cell = self.find_empty_cell()
        
        # 모든 칸이 채워졌으면 성공
        if empty_cell is None:
            return True
        
        row, col = empty_cell
        
        # 1부터 9까지 숫자를 랜덤 순서로 시도
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for number in numbers:
            if self.is_valid_number(row, col, number):
                # 숫자 배치
                self.board.set_value(row, col, number)
                
                # 재귀적으로 다음 빈 칸 채우기
                if self.solve():
                    return True
                
                # 실패하면 되돌리기
                self.board.set_value(row, col, None)
        
        # 모든 숫자를 시도했지만 실패
        return False
    
    def solve_with_pieces(self, max_attempts=10):
        """기물이 배치된 상태에서 스도쿠 풀기"""
        print("체스 기물과 스도쿠 제약 조건으로 숫자 채우기 시작...")
        
        for attempt in range(max_attempts):
            # 보드를 초기 상태로 복원 (기물만 남기고)
            self._reset_board_to_pieces()
            
            if self.solve():
                # 해를 찾은 후 제약 조건 검증
                if self.verify_solution():
                    print("스도쿠 풀이 성공!")
                    return True
                else:
                    print(f"시도 {attempt + 1}: 제약 조건 위반 발견, 다시 시도...")
                    continue
            else:
                print(f"시도 {attempt + 1}: 해를 찾지 못함, 다시 시도...")
                continue
        
        print("스도쿠 풀이 실패 - 최대 시도 횟수 초과")
        return False
    
    def _reset_board_to_pieces(self):
        """보드를 기물만 있는 초기 상태로 복원"""
        # 모든 칸을 None으로 초기화
        for row in range(9):
            for col in range(9):
                self.board.set_value(row, col, None)
        
        # 기물 위치에만 기물 문자 배치
        for piece in self.pieces:
            self.board.set_value(piece.row, piece.col, piece.piece_type)
    
    def verify_solution(self):
        """완성된 해가 모든 제약 조건을 만족하는지 검증"""
        print("제약 조건 검증 중...")
        
        # 1. 스도쿠 기본 규칙 검증
        for row in range(9):
            for col in range(9):
                value = self.board.get_value(row, col)
                if not isinstance(value, int) or value < 1 or value > 9:
                    print(f"❌ ({row}, {col})에 잘못된 값: {value}")
                    return False
        
        # 2. 기물 제약 조건 검증
        for piece in self.pieces:
            piece_value = self.board.get_value(piece.row, piece.col)
            if not isinstance(piece_value, int):
                print(f"❌ 기물 위치 ({piece.row}, {piece.col})에 숫자가 없음: {piece_value}")
                return False
            
            # 이 기물이 영향을 미치는 모든 위치 확인
            for row in range(9):
                for col in range(9):
                    if row == piece.row and col == piece.col:
                        continue
                    
                    target_value = self.board.get_value(row, col)
                    if isinstance(target_value, int) and target_value == piece_value:
                        # 기물이 이 위치를 공격할 수 있는지 확인
                        if self.piece_placer._can_piece_attack(piece, row, col):
                            print(f"❌ 기물 제약 조건 위반: {piece.piece_type} ({piece.row}, {piece.col})={piece_value}와 ({row}, {col})={target_value}")
                            return False
        
        print("✅ 모든 제약 조건 만족!")
        return True
    
