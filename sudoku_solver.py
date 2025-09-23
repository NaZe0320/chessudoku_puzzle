from board import Board
from pieces import PiecePlacer

class SudokuSolver:
    """스도쿠 솔버 클래스"""
    
    def __init__(self, board, piece_placer):
        self.board = board
        self.piece_placer = piece_placer
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 검사 (스도쿠 기본 규칙)"""
        # 같은 행에 동일한 숫자가 있는지 확인
        for c in range(9):
            if c != col and self.board.get_value(row, c) == number:
                return False
        
        # 같은 열에 동일한 숫자가 있는지 확인
        for r in range(9):
            if r != row and self.board.get_value(r, col) == number:
                return False
        
        # 같은 3x3 박스에 동일한 숫자가 있는지 확인
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.board.get_value(r, c) == number:
                    return False
        
        return True
    
    def is_valid_number_with_pieces(self, row, col, number):
        """스도쿠 규칙 + 기물 규칙을 모두 만족하는지 검사"""
        # 스도쿠 기본 규칙 검사
        if not self.is_valid_number(row, col, number):
            return False
        
        # 기물 규칙 검사
        if not self.piece_placer.is_valid_number_for_piece(row, col, number):
            return False
        
        return True
    
    def find_empty_cell(self):
        """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
        for row in range(9):
            for col in range(9):
                if self.board.is_empty(row, col):
                    return (row, col)
        return None
    
    def solve_sudoku(self):
        """백트래킹을 사용한 스도쿠 해결"""
        empty_cell = self.find_empty_cell()
        
        # 빈 칸이 없으면 완성
        if empty_cell is None:
            return True
        
        row, col = empty_cell
        
        # 1부터 9까지 시도
        for number in range(1, 10):
            if self.is_valid_number_with_pieces(row, col, number):
                # 숫자 배치
                self.board.set_value(row, col, number)
                
                # 재귀적으로 다음 빈 칸 해결
                if self.solve_sudoku():
                    return True
                
                # 백트래킹: 숫자 제거
                self.board.set_value(row, col, None)
        
        return False
    
    def solve_sudoku_basic(self):
        """기본 스도쿠만 해결 (기물 규칙 제외)"""
        empty_cell = self.find_empty_cell()
        
        if empty_cell is None:
            return True
        
        row, col = empty_cell
        
        for number in range(1, 10):
            if self.is_valid_number(row, col, number):
                self.board.set_value(row, col, number)
                
                if self.solve_sudoku_basic():
                    return True
                
                self.board.set_value(row, col, None)
        
        return False
    
    def count_solutions(self, max_solutions=2):
        """해의 개수를 세는 함수 (최대 max_solutions까지만)"""
        empty_cell = self.find_empty_cell()
        
        if empty_cell is None:
            return 1
        
        row, col = empty_cell
        solutions = 0
        
        for number in range(1, 10):
            if self.is_valid_number_with_pieces(row, col, number):
                self.board.set_value(row, col, number)
                
                solutions += self.count_solutions(max_solutions - solutions)
                
                if solutions >= max_solutions:
                    self.board.set_value(row, col, None)
                    return solutions
                
                self.board.set_value(row, col, None)
        
        return solutions
    
    def is_unique_solution(self):
        """유일한 해가 있는지 확인"""
        return self.count_solutions(2) == 1
