from board import Board
from sudoku_solver import ChessSudokuSolver
import random
import copy

class PuzzleGenerator:
    """완성된 보드에서 빈칸을 뚫어 퍼즐을 생성하는 클래스"""
    
    def __init__(self, completed_board, pieces, max_holes):
        self.completed_board = completed_board  # 완성된 보드 (원본)
        self.pieces = pieces
        self.max_holes = max_holes
        self.holes_count = 0
        
        # 퍼즐용 보드 생성 (완성된 보드 복사)
        self.puzzle_board = Board()
        self._copy_board(completed_board, self.puzzle_board)
    
    def _copy_board(self, source_board, target_board):
        """보드 내용 복사"""
        for row in range(9):
            for col in range(9):
                target_board.set_value(row, col, source_board.get_value(row, col))
    
    def generate_puzzle(self):
        """백트래킹으로 빈칸을 뚫어서 퍼즐 생성"""
        print(f"퍼즐 생성 시작... (최대 {self.max_holes}개 빈칸)")
        
        # 1. 기물이 없는 칸들 찾기 (숫자만 있는 칸들)
        number_cells = self._find_number_only_cells()
        print(f"기물이 없는 칸: {len(number_cells)}개")
        
        # 2. 무작위 순서로 섞기
        random.shuffle(number_cells)
        
        # 3. 각 칸을 빈칸으로 만들어보면서 유일해 검증
        for row, col in number_cells:
            if self.holes_count >= self.max_holes:
                break
                
            # 원래 숫자 백업
            original_number = self.puzzle_board.get_value(row, col)
            
            # 임시로 빈칸으로 만들기
            self.puzzle_board.set_value(row, col, None)
            
            # 유일해 검증
            if self.has_unique_solution():
                # 유일해이면 빈칸 유지
                self.holes_count += 1
            else:
                # 유일해가 아니면 원래 숫자로 복원
                self.puzzle_board.set_value(row, col, original_number)
        
        print(f"퍼즐 생성 완료! 총 {self.holes_count}개 빈칸")
        return self.puzzle_board
    
    def _find_number_only_cells(self):
        """기물이 없는 칸들 (숫자만 있는 칸들) 찾기"""
        number_cells = []
        
        # 기물이 있는 위치들 수집
        piece_positions = set()
        for piece in self.pieces:
            piece_positions.add((piece.row, piece.col))
        
        # 기물이 없고 숫자가 있는 칸들 찾기
        for row in range(9):
            for col in range(9):
                if (row, col) not in piece_positions:
                    if not self.puzzle_board.is_empty(row, col):
                        number_cells.append((row, col))
        
        return number_cells
    
    def has_unique_solution(self):
        """현재 퍼즐이 유일한 해를 가지는지 검증"""
        solution_count = self.count_solutions(max_count=2)
        return solution_count == 1
    
    def count_solutions(self, max_count=2):
        """해의 개수를 세는 함수 (최대 max_count개까지만)"""
        # 현재 퍼즐 보드 복사
        test_board = Board()
        self._copy_board(self.puzzle_board, test_board)
        
        # 솔버 생성
        solver = ChessSudokuSolver(test_board, self.pieces)
        
        # 해의 개수 세기
        return self._count_solutions_recursive(solver, 0, max_count)
    
    def _count_solutions_recursive(self, solver, current_count, max_count):
        """재귀적으로 해의 개수를 세는 함수"""
        if current_count >= max_count:
            return current_count
        
        # 빈 칸 찾기
        empty_cell = solver.find_empty_cell()
        
        # 모든 칸이 채워졌으면 해를 하나 발견
        if empty_cell is None:
            return current_count + 1
        
        row, col = empty_cell
        solutions_found = current_count
        
        # 1부터 9까지 숫자를 순서대로 시도 (랜덤 X)
        for number in range(1, 10):
            if solver.is_valid_number(row, col, number):
                # 숫자 배치
                solver.board.set_value(row, col, number)
                
                # 재귀적으로 해 개수 세기
                solutions_found = self._count_solutions_recursive(solver, solutions_found, max_count)
                
                # 최대 개수에 도달하면 조기 종료
                if solutions_found >= max_count:
                    solver.board.set_value(row, col, None)
                    return solutions_found
                
                # 되돌리기
                solver.board.set_value(row, col, None)
        
        return solutions_found

class PuzzleSolver:
    """다양한 풀이 전략을 제공하는 퍼즐 솔버"""
    
    def __init__(self, puzzle_board, pieces):
        self.original_board = Board()
        self._copy_board(puzzle_board, self.original_board)
        self.pieces = pieces
    
    def _copy_board(self, source_board, target_board):
        """보드 내용 복사"""
        for row in range(9):
            for col in range(9):
                target_board.set_value(row, col, source_board.get_value(row, col))
    
    
    def solve_constraint_propagation(self):
        """제약 전파 + 백트래킹"""
        print("풀이 방법: 제약 전파 + 백트래킹")
        board_copy = Board()
        self._copy_board(self.original_board, board_copy)
        
        # 고급 제약 전파 적용
        solver = ConstraintPropagationSolver(board_copy, self.pieces)
        success = solver.solve_with_constraint_propagation()
        
        if success:
            print("풀이 성공!")
            board_copy.print_board()
        else:
            print("풀이 실패!")
        
        return success, board_copy
    
    
    
    def solve_puzzle(self):
        """제약 전파 + 백트래킹으로 퍼즐 풀기"""
        print("=" * 50)
        print("제약 전파 + 백트래킹으로 퍼즐 풀기")
        print("=" * 50)
        
        success, result_board = self.solve_constraint_propagation()
        return success, result_board


class ConstraintPropagationSolver:
    """제약 전파를 활용한 고급 스도쿠 솔버"""
    
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces
        self.solver = ChessSudokuSolver(board, pieces)
        
        # 각 칸의 가능한 숫자들을 저장하는 3차원 배열
        self.candidates = [[[True for _ in range(10)] for _ in range(9)] for _ in range(9)]
        self._initialize_candidates()
    
    def _initialize_candidates(self):
        """각 칸의 초기 후보 숫자들 설정"""
        for row in range(9):
            for col in range(9):
                if not self.board.is_empty(row, col):
                    # 이미 채워진 칸은 모든 후보를 False로
                    for num in range(1, 10):
                        self.candidates[row][col][num] = False
                else:
                    # 빈 칸은 유효한 숫자들만 True로
                    for num in range(1, 10):
                        self.candidates[row][col][num] = self.solver.is_valid_number(row, col, num)
    
    def solve_with_constraint_propagation(self):
        """제약 전파 + 백트래킹으로 풀이"""
        # 1단계: 제약 전파로 확실한 칸들 채우기
        progress = True
        while progress:
            progress = False
            
            # Naked Singles: 후보가 하나뿐인 칸 채우기
            if self._apply_naked_singles():
                progress = True
            
            # Hidden Singles: 특정 숫자가 들어갈 곳이 하나뿐인 경우
            if self._apply_hidden_singles():
                progress = True
            
            # 후보 업데이트
            if self._update_candidates():
                progress = True
        
        # 2단계: 남은 빈 칸들은 백트래킹으로 해결
        empty_count = sum(1 for row in range(9) for col in range(9) if self.board.is_empty(row, col))
        if empty_count > 0:
            return self._backtrack_with_candidates()
        else:
            return True
    
    def _apply_naked_singles(self):
        """Naked Singles: 후보가 하나뿐인 칸 찾아서 채우기"""
        changed = False
        
        for row in range(9):
            for col in range(9):
                if self.board.is_empty(row, col):
                    # 이 칸의 후보 숫자들 확인
                    candidates = [num for num in range(1, 10) if self.candidates[row][col][num]]
                    
                    if len(candidates) == 1:
                        # 후보가 하나뿐이면 바로 채우기
                        num = candidates[0]
                        self.board.set_value(row, col, num)
                        changed = True
                        
                        # 이 칸의 모든 후보를 False로
                        for n in range(1, 10):
                            self.candidates[row][col][n] = False
        
        return changed
    
    def _apply_hidden_singles(self):
        """Hidden Singles: 특정 숫자가 들어갈 수 있는 곳이 하나뿐인 경우"""
        changed = False
        
        # 각 행, 열, 3x3 박스별로 확인
        for num in range(1, 10):
            # 행별 확인
            for row in range(9):
                possible_cols = [col for col in range(9) 
                               if self.board.is_empty(row, col) and self.candidates[row][col][num]]
                if len(possible_cols) == 1:
                    col = possible_cols[0]
                    self.board.set_value(row, col, num)
                    changed = True
                    for n in range(1, 10):
                        self.candidates[row][col][n] = False
            
            # 열별 확인
            for col in range(9):
                possible_rows = [row for row in range(9) 
                               if self.board.is_empty(row, col) and self.candidates[row][col][num]]
                if len(possible_rows) == 1:
                    row = possible_rows[0]
                    self.board.set_value(row, col, num)
                    changed = True
                    for n in range(1, 10):
                        self.candidates[row][col][n] = False
            
            # 3x3 박스별 확인
            for box_row in range(3):
                for box_col in range(3):
                    possible_cells = []
                    for r in range(box_row * 3, (box_row + 1) * 3):
                        for c in range(box_col * 3, (box_col + 1) * 3):
                            if self.board.is_empty(r, c) and self.candidates[r][c][num]:
                                possible_cells.append((r, c))
                    
                    if len(possible_cells) == 1:
                        row, col = possible_cells[0]
                        self.board.set_value(row, col, num)
                        changed = True
                        for n in range(1, 10):
                            self.candidates[row][col][n] = False
        
        return changed
    
    def _update_candidates(self):
        """새로 채워진 숫자들을 바탕으로 후보 업데이트"""
        changed = False
        
        for row in range(9):
            for col in range(9):
                if not self.board.is_empty(row, col):
                    continue
                
                # 이 칸의 현재 후보들을 다시 검증
                for num in range(1, 10):
                    if self.candidates[row][col][num]:
                        if not self.solver.is_valid_number(row, col, num):
                            self.candidates[row][col][num] = False
                            changed = True
        
        return changed
    
    def _backtrack_with_candidates(self):
        """후보 정보를 활용한 스마트 백트래킹"""
        # 가장 후보가 적은 빈 칸 찾기
        min_candidates = 10
        best_cell = None
        
        for row in range(9):
            for col in range(9):
                if self.board.is_empty(row, col):
                    candidate_count = sum(1 for num in range(1, 10) if self.candidates[row][col][num])
                    if candidate_count < min_candidates:
                        min_candidates = candidate_count
                        best_cell = (row, col)
        
        # 모든 칸이 채워졌으면 성공
        if best_cell is None:
            return True
        
        # 후보가 없는 칸이 있으면 실패
        if min_candidates == 0:
            return False
        
        row, col = best_cell
        
        # 이 칸의 후보 숫자들을 시도
        candidate_numbers = [num for num in range(1, 10) if self.candidates[row][col][num]]
        
        for num in candidate_numbers:
            if self.solver.is_valid_number(row, col, num):
                # 숫자 배치
                self.board.set_value(row, col, num)
                
                # 후보 정보 백업
                old_candidates = [[[self.candidates[r][c][n] for n in range(10)] 
                                 for c in range(9)] for r in range(9)]
                
                # 후보 업데이트
                for n in range(1, 10):
                    self.candidates[row][col][n] = False
                self._update_candidates()
                
                # 재귀 호출
                if self._backtrack_with_candidates():
                    return True
                
                # 실패하면 되돌리기
                self.board.set_value(row, col, None)
                self.candidates = old_candidates
        
        return False
