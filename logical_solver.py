from board import Board
from validators import PiecePlacer, SudokuValidator
import copy

class LogicalSolver:
    """논리적 기법만을 사용하여 스도쿠를 풀이하는 클래스
    
    백트래킹이나 추측 없이 순수하게 논리적 기법만 사용:
    - 제약 전파 (Constraint Propagation)
    - 단일 후보 찾기 (Naked Singles)
    - 숨겨진 단일 후보 찾기 (Hidden Singles)
    - 쌍 제거 (Naked Pairs)
    """
    
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
    
    def solve_logically(self):
        """논리적 기법만으로 스도쿠 풀이 시도
        
        Returns:
            bool: 풀이 성공 여부
        """
        max_iterations = 100  # 무한 루프 방지
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            progress_made = False
            
            # 1. 제약 전파 적용
            if self.apply_constraint_propagation():
                progress_made = True
            
            # 2. 단일 후보 찾기
            if self.find_naked_singles():
                progress_made = True
            
            # 3. 숨겨진 단일 후보 찾기
            if self.find_hidden_singles():
                progress_made = True
            
            # 4. 쌍 제거 (고급 기법)
            if self.find_naked_pairs():
                progress_made = True
            
            # 더 이상 진행할 수 없으면 중단
            if not progress_made:
                break
            
            # 모든 칸이 채워졌는지 확인
            if self.is_complete():
                return True
        
        # 논리적으로 더 이상 풀 수 없음
        return False
    
    def apply_constraint_propagation(self):
        """제약 전파를 적용하여 가능한 값들을 업데이트"""
        progress_made = False
        
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:  # 빈 칸인 경우
                    old_possible = self.possible_values.get((row, col), set()).copy()
                    
                    # 가능한 값들을 다시 계산
                    new_possible = set()
                    for number in range(1, 10):
                        if self.is_valid_number(row, col, number):
                            new_possible.add(number)
                    
                    self.possible_values[(row, col)] = new_possible
                    
                    # 값이 변경되었으면 진행 상황이 있었다고 표시
                    if old_possible != new_possible:
                        progress_made = True
        
        return progress_made
    
    def find_naked_singles(self):
        """단일 후보 찾기 - 가능한 값이 1개인 칸을 찾아서 채우기"""
        progress_made = False
        
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:  # 빈 칸인 경우
                    possible = self.possible_values.get((row, col), set())
                    
                    if len(possible) == 1:
                        # 유일한 가능한 값으로 채우기
                        number = list(possible)[0]
                        self.board.set_value(row, col, number)
                        del self.possible_values[(row, col)]
                        progress_made = True
        
        return progress_made
    
    def find_hidden_singles(self):
        """숨겨진 단일 후보 찾기 - 행/열/박스에서 특정 숫자가 들어갈 수 있는 칸이 1개인 경우"""
        progress_made = False
        
        # 각 숫자(1-9)에 대해 검사
        for number in range(1, 10):
            # 행별로 검사
            for row in range(9):
                possible_cells = []
                for col in range(9):
                    if (self.board.get_value(row, col) is None and 
                        number in self.possible_values.get((row, col), set())):
                        possible_cells.append((row, col))
                
                if len(possible_cells) == 1:
                    # 이 행에서 이 숫자가 들어갈 수 있는 칸이 1개뿐
                    row, col = possible_cells[0]
                    self.board.set_value(row, col, number)
                    del self.possible_values[(row, col)]
                    progress_made = True
            
            # 열별로 검사
            for col in range(9):
                possible_cells = []
                for row in range(9):
                    if (self.board.get_value(row, col) is None and 
                        number in self.possible_values.get((row, col), set())):
                        possible_cells.append((row, col))
                
                if len(possible_cells) == 1:
                    # 이 열에서 이 숫자가 들어갈 수 있는 칸이 1개뿐
                    row, col = possible_cells[0]
                    self.board.set_value(row, col, number)
                    del self.possible_values[(row, col)]
                    progress_made = True
            
            # 3x3 박스별로 검사
            for box_row in range(0, 9, 3):
                for box_col in range(0, 9, 3):
                    possible_cells = []
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if (self.board.get_value(r, c) is None and 
                                number in self.possible_values.get((r, c), set())):
                                possible_cells.append((r, c))
                    
                    if len(possible_cells) == 1:
                        # 이 박스에서 이 숫자가 들어갈 수 있는 칸이 1개뿐
                        row, col = possible_cells[0]
                        self.board.set_value(row, col, number)
                        del self.possible_values[(row, col)]
                        progress_made = True
        
        return progress_made
    
    def find_naked_pairs(self):
        """쌍 제거 - 두 칸에만 가능한 값이 정확히 2개인 경우"""
        progress_made = False
        
        # 행별로 검사
        for row in range(9):
            empty_cells = []
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    empty_cells.append((row, col))
            
            # 두 칸씩 비교
            for i in range(len(empty_cells)):
                for j in range(i + 1, len(empty_cells)):
                    cell1, cell2 = empty_cells[i], empty_cells[j]
                    possible1 = self.possible_values.get(cell1, set())
                    possible2 = self.possible_values.get(cell2, set())
                    
                    # 두 칸의 가능한 값이 정확히 2개이고 동일한 경우
                    if (len(possible1) == 2 and len(possible2) == 2 and 
                        possible1 == possible2):
                        
                        # 같은 행의 다른 칸들에서 이 두 값을 제거
                        for col in range(9):
                            if col != cell1[1] and col != cell2[1]:
                                cell = (row, col)
                                if cell in self.possible_values:
                                    old_size = len(self.possible_values[cell])
                                    self.possible_values[cell] -= possible1
                                    if len(self.possible_values[cell]) != old_size:
                                        progress_made = True
        
        # 열별로 검사 (동일한 로직)
        for col in range(9):
            empty_cells = []
            for row in range(9):
                if self.board.get_value(row, col) is None:
                    empty_cells.append((row, col))
            
            for i in range(len(empty_cells)):
                for j in range(i + 1, len(empty_cells)):
                    cell1, cell2 = empty_cells[i], empty_cells[j]
                    possible1 = self.possible_values.get(cell1, set())
                    possible2 = self.possible_values.get(cell2, set())
                    
                    if (len(possible1) == 2 and len(possible2) == 2 and 
                        possible1 == possible2):
                        
                        for row in range(9):
                            if row != cell1[0] and row != cell2[0]:
                                cell = (row, col)
                                if cell in self.possible_values:
                                    old_size = len(self.possible_values[cell])
                                    self.possible_values[cell] -= possible1
                                    if len(self.possible_values[cell]) != old_size:
                                        progress_made = True
        
        return progress_made
    
    def is_complete(self):
        """보드가 완성되었는지 확인"""
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    return False
        return True
    
    def is_solvable_logically(self):
        """논리적 기법만으로 풀 수 있는지 확인
        
        Returns:
            bool: 논리적으로 풀 수 있으면 True, 아니면 False
        """
        # 보드 복사본 생성
        original_board = copy.deepcopy(self.board)
        original_possible_values = copy.deepcopy(self.possible_values)
        
        try:
            # 논리적 풀이 시도
            success = self.solve_logically()
            return success
        finally:
            # 원본 보드 복원
            self.board.board = original_board.board
            self.possible_values = original_possible_values
            # 논리적 솔버도 새로 초기화
            self.initialize_possible_values()
    
    def get_empty_cells_count(self):
        """빈 칸의 개수 반환"""
        count = 0
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    count += 1
        return count
    
    def get_possible_values_summary(self):
        """각 칸의 가능한 값 개수 요약 반환"""
        summary = {}
        for row in range(9):
            for col in range(9):
                if self.board.get_value(row, col) is None:
                    count = len(self.possible_values.get((row, col), set()))
                    summary[(row, col)] = count
        return summary
