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
        
        # 각 칸의 가능한 값들을 추적하는 딕셔너리
        # 키: (row, col) 튜플, 값: 가능한 숫자들의 set
        self.possible_values = {}
        self.initialize_possible_values()
    
    def initialize_possible_values(self):
        """모든 빈 칸의 가능한 값들을 초기화"""
        self.possible_values.clear()
        
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:  # 빈 칸인 경우
                    self.possible_values[(row, col)] = set()
                    
                    # 1부터 9까지 각 숫자가 가능한지 확인
                    for number in range(1, 10):
                        if self.is_valid_number(row, col, number):
                            self.possible_values[(row, col)].add(number)
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 검사"""
        # 1. 기본 스도쿠 규칙 검사
        if not self.sudoku_validator.is_valid_number(row, col, number):
            return False
        
        # 2. 체스 기물 규칙 검사
        if not self.piece_placer.is_valid_number_for_piece(row, col, number):
            return False
        
        return True
    
    def forward_check(self, row, col, number):
        """숫자를 배치한 후 영향을 받는 칸들의 가능한 값들을 업데이트"""
        affected_cells = []
        
        # 같은 행, 열, 3x3 박스의 빈 칸들 찾기
        for r in range(9):
            for c in range(9):
                if self.board.get_value(r, c) is None:  # 빈 칸인 경우
                    # 같은 행, 열, 또는 박스에 있으면 영향받음
                    if (r == row or c == col or 
                        (r//3 == row//3 and c//3 == col//3)):
                        
                        # 이 칸에서 해당 숫자를 제거
                        if number in self.possible_values.get((r, c), set()):
                            self.possible_values[(r, c)].discard(number)
                            affected_cells.append((r, c))
                            
                            # 가능한 값이 0개가 되면 실패
                            if len(self.possible_values[(r, c)]) == 0:
                                return False, affected_cells
        
        return True, affected_cells
    
    def restore_possible_values(self, affected_cells, number):
        """백트래킹 시 가능한 값들을 복원"""
        for row, col in affected_cells:
            if self.is_valid_number(row, col, number):
                self.possible_values[(row, col)].add(number)
    
    def find_best_empty_cell(self):
        """MRV를 적용하여 가장 제약이 많은 빈 칸을 찾아서 반환"""
        best_cell = None
        min_possible_values = float('inf')
        
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:  # 빈 칸인 경우
                    # possible_values에서 가능한 값 개수 확인
                    possible_count = len(self.possible_values.get((row, col), set()))
                    
                    if possible_count < min_possible_values:
                        min_possible_values = possible_count
                        best_cell = (row, col)
                        
                        # 가능한 값이 0개면 즉시 반환 (백트래킹 필요)
                        if possible_count == 0:
                            return best_cell
        
        return best_cell
    
    # def find_empty_cell(self):
    #     """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
    #     for row in range(9):
    #         for col in range(9):
    #             value = self.board.get_value(row, col)
    #             if value is None:
    #                 return (row, col)
    #     return None
    
    def solve_with_mrv_and_forward_checking(self):
        """MRV와 Forward Checking을 적용한 솔버"""
        # MRV로 가장 제약이 많은 칸 선택
        best_cell = self.find_best_empty_cell()
        
        if best_cell is None:
            return True  # 모든 칸이 채워짐
        
        row, col = best_cell
        
        # 가능한 값들을 복사해서 순서대로 시도
        possible_numbers = list(self.possible_values.get((row, col), set()))
        random.shuffle(possible_numbers)
        
        for number in possible_numbers:
            # 숫자 배치
            self.board.set_value(row, col, number)
            
            # Forward Checking 수행
            success, affected_cells = self.forward_check(row, col, number)
            
            if success:
                # 재귀적으로 다음 단계 진행
                if self.solve_with_mrv_and_forward_checking():
                    return True
            
            # 백트래킹: 복원
            self.board.set_value(row, col, None)
            self.restore_possible_values(affected_cells, number)
        
        return False
    
    # def solve(self):
    #     """백트래킹을 사용한 스도쿠 솔버 (기존 방식)"""
    #     empty_cell = self.find_empty_cell()
    #     
    #     # 모든 칸이 채워졌으면 성공
    #     if empty_cell is None:
    #         return True
    #     
    #     row, col = empty_cell
    #     
    #     # 1부터 9까지 숫자를 랜덤 순서로 시도
    #     numbers = list(range(1, 10))
    #     random.shuffle(numbers)
    #     for number in numbers:
    #         if self.is_valid_number(row, col, number):
    #             # 숫자 배치
    #             self.board.set_value(row, col, number)
    #             
    #             # 재귀적으로 다음 빈 칸 채우기
    #             if self.solve():
    #                 return True
    #             
    #             # 실패하면 되돌리기
    #             self.board.set_value(row, col, None)
    #     
    #     # 모든 숫자를 시도했지만 실패
    #     return False
    
    def generate_complete_board(self):
        """완전한 스도쿠 보드 생성 (MRV + Forward Checking 사용)"""
        print("체스 기물과 스도쿠 제약 조건으로 숫자 채우기 시작...")
        print("MRV + Forward Checking 방식 사용")
        
        if self.solve_with_mrv_and_forward_checking():
            print("스도쿠 보드 생성 성공!")
            return True
        else:
            print("스도쿠 보드 생성 실패 - 해가 존재하지 않습니다.")
            return False
    
    # def generate_complete_board(self, use_mrv=True):
    #     """완전한 스도쿠 보드 생성"""
    #     print("체스 기물과 스도쿠 제약 조건으로 숫자 채우기 시작...")
    #     
    #     if use_mrv:
    #         print("MRV + Forward Checking 방식 사용")
    #         if self.solve_with_mrv_and_forward_checking():
    #             print("스도쿠 보드 생성 성공!")
    #             return True
    #         else:
    #             print("스도쿠 보드 생성 실패 - 해가 존재하지 않습니다.")
    #             return False
    #     else:
    #         print("기존 백트래킹 방식 사용")
    #         if self.solve():
    #             print("스도쿠 보드 생성 성공!")
    #             return True
    #         else:
    #             print("스도쿠 보드 생성 실패 - 해가 존재하지 않습니다.")
    #             return False