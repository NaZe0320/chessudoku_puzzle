from board import Board
from validators import PiecePlacer, SudokuValidator
import random

class BoardGenerator:
    """체스 기물과 스도쿠 제약 조건을 모두 고려한 보드 생성기"""
    
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces
        self.piece_placer = PiecePlacer(board)
        self.piece_placer.pieces = pieces
        self.sudoku_validator = SudokuValidator(board)
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 검사"""
        # 1. 기본 스도쿠 규칙 검사
        if not self.sudoku_validator.is_valid_number(row, col, number):
            return False
        
        # 2. 체스 기물 규칙 검사
        if not self.piece_placer.is_valid_number_for_piece(row, col, number):
            return False
        
        return True
    
    def find_empty_cell(self):
        """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
        for row in range(9):
            for col in range(9):
                value = self.board.get_value(row, col)
                if value is None:
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
    
    def generate_complete_board(self):
        """완전한 스도쿠 보드 생성"""
        print("체스 기물과 스도쿠 제약 조건으로 숫자 채우기 시작...")
        
        if self.solve():
            print("스도쿠 보드 생성 성공!")
            return True
        else:
            print("스도쿠 보드 생성 실패 - 해가 존재하지 않습니다.")
            return False