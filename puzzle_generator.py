from board import Board
from sudoku_solver import ChesSudokuSolver
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
        """해의 개수를 세는 함수 (최대 max_count개까지만) - 참조 코드 방식"""
        # 현재 퍼즐 보드 복사
        test_board = Board()
        self._copy_board(self.puzzle_board, test_board)
        
        # 솔버 생성
        solver = ChesSudokuSolver(test_board, self.pieces)
        
        # 해의 개수 세기 (참조 코드 방식)
        return self._count_solutions_reference_style(solver, max_count)
    
    def _count_solutions_reference_style(self, solver, max_count):
        """참조 코드 방식의 해 개수 세기 함수"""
        empty_cells = solver._get_empty_cells()
        
        if not empty_cells:
            return 1  # 모든 칸이 채워져 있음
        
        return self._count_solutions_recursive_reference(solver, empty_cells, 0, max_count)
    
    def _count_solutions_recursive_reference(self, solver, empty_cells, cell_index, max_count):
        """참조 코드 방식의 재귀적 해 개수 세기"""
        if cell_index >= len(empty_cells):
            return 1  # 모든 칸이 채워졌음
        
        # MRV 전략으로 최적의 빈 칸 선택
        best_cell = solver._select_cell_mrv(empty_cells)
        if best_cell is None:
            return 1
        
        row, col = best_cell
        solutions_found = 0
        
        # 후보 숫자들을 시도
        candidates = solver._candidates_for(row, col)
        for value in candidates:
            # 숫자 배치
            solver.board.set_value(row, col, value)
            solver._add_constraint(row, col, value)
            
            # 재귀적으로 해 개수 세기
            solutions_found += self._count_solutions_recursive_reference(solver, empty_cells, cell_index + 1, max_count)
            
            # 최대 개수에 도달하면 조기 종료
            if solutions_found >= max_count:
                solver._remove_constraint(row, col, value)
                solver.board.set_value(row, col, None)
                return solutions_found
            
            # 되돌리기
            solver._remove_constraint(row, col, value)
            solver.board.set_value(row, col, None)
        
        return solutions_found