from board import Board
from logical_solver import LogicalSolver
import copy
import random

class PuzzleGenerator:
    """완성된 스도쿠 보드에서 빈칸을 조각하여 퍼즐을 생성하는 클래스
    
    한 칸씩 조각(carve)하면서 논리적으로 풀 수 있는지 검증하여
    사람이 실제로 풀 수 있는 퍼즐을 생성합니다.
    """
    
    def __init__(self, complete_board, pieces):
        """퍼즐 생성기 초기화
        
        Args:
            complete_board (Board): 완성된 스도쿠 보드
            pieces (list): 배치된 체스 기물들
        """
        self.complete_board = complete_board
        self.pieces = pieces
        self.puzzle_board = None
        self.carved_cells = []  # 조각된 칸들의 목록
        self.logical_solver = None
        
    def generate_puzzle(self, max_holes=25, min_holes=10):
        """빈칸을 조각하여 퍼즐 생성
        
        Args:
            max_holes (int): 최대 빈칸 개수
            min_holes (int): 최소 빈칸 개수
            
        Returns:
            Board: 생성된 퍼즐 보드
        """
        print(f"퍼즐 생성 시작 (최대 {max_holes}개 빈칸)")
        
        # 1. 완성된 보드 복사
        self.puzzle_board = copy.deepcopy(self.complete_board)
        self.carved_cells = []
        
        # 2. 논리적 솔버 초기화
        self.logical_solver = LogicalSolver(self.puzzle_board, self.pieces)
        
        # 3. 한 칸씩 조각하기 시도
        holes_carved = 0
        max_attempts = max_holes * 3  # 무한 루프 방지
        attempts = 0
        
        while holes_carved < max_holes and attempts < max_attempts:
            attempts += 1
            
            # 조각할 수 있는 칸들 찾기
            candidate_cells = self.get_carveable_cells()
            
            if not candidate_cells:
                print("더 이상 조각할 수 있는 칸이 없습니다.")
                break
            
            # 랜덤하게 칸 선택
            row, col = random.choice(candidate_cells)
            
            # 이 칸을 조각해도 논리적으로 풀 수 있는지 확인
            if self.carve_cell_and_verify(row, col):
                holes_carved += 1
                self.carved_cells.append((row, col))
                print(f"칸 ({row}, {col}) 조각 완료 - 현재 빈칸: {holes_carved}개")
            else:
                print(f"칸 ({row}, {col}) 조각 실패 - 논리적 풀이 불가능")
        
        # 최소 빈칸 개수 확인
        if holes_carved < min_holes:
            print(f"경고: 최소 빈칸 개수({min_holes})에 도달하지 못했습니다. ({holes_carved}개)")
        
        print(f"퍼즐 생성 완료: {holes_carved}개 빈칸 조각됨")
        return self.puzzle_board
    
    def get_carveable_cells(self):
        """조각할 수 있는 칸들의 목록 반환
        
        Returns:
            list: 조각 가능한 칸들의 (row, col) 튜플 리스트
        """
        carveable = []
        
        for row in range(9):
            for col in range(9):
                # 이미 조각된 칸은 제외
                if (row, col) in self.carved_cells:
                    continue
                
                # 기물이 있는 칸은 조각할 수 없음
                if self.is_piece_position(row, col):
                    continue
                
                # 숫자가 있는 칸만 조각 가능
                if isinstance(self.puzzle_board.get_value(row, col), int):
                    carveable.append((row, col))
        
        return carveable
    
    def is_piece_position(self, row, col):
        """해당 위치에 기물이 있는지 확인"""
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return True
        return False
    
    def carve_cell_and_verify(self, row, col):
        """칸을 조각하고 논리적으로 풀 수 있는지 검증
        
        Args:
            row (int): 행 번호
            col (int): 열 번호
            
        Returns:
            bool: 조각 성공 여부
        """
        # 원본 값 저장
        original_value = self.puzzle_board.get_value(row, col)
        
        # 칸을 빈칸으로 만들기
        self.puzzle_board.set_value(row, col, None)
        
        # 논리적 솔버 업데이트
        self.logical_solver = LogicalSolver(self.puzzle_board, self.pieces)
        
        # 논리적으로 풀 수 있는지 확인
        is_solvable = self.logical_solver.is_solvable_logically()
        
        if is_solvable:
            # 조각 성공
            return True
        else:
            # 조각 실패 - 원본 값 복원
            self.puzzle_board.set_value(row, col, original_value)
            return False
    
    def get_puzzle_difficulty(self):
        """퍼즐의 난이도 평가
        
        Returns:
            str: 난이도 ('easy', 'medium', 'hard', 'expert')
        """
        holes_count = len(self.carved_cells)
        
        if holes_count <= 25:
            return 'easy'
        elif holes_count <= 40:
            return 'medium'
        elif holes_count <= 50:
            return 'hard'
        else:
            return 'expert'
    
    def get_puzzle_info(self):
        """퍼즐 정보 반환"""
        return {
            'holes_count': len(self.carved_cells),
            'difficulty': self.get_puzzle_difficulty(),
            'carved_cells': self.carved_cells.copy(),
            'pieces_count': len(self.pieces)
        }
    
    def print_puzzle_summary(self):
        """퍼즐 요약 정보 출력"""
        info = self.get_puzzle_info()
        print(f"\n퍼즐 요약:")
        print(f"- 조각된 빈칸: {info['holes_count']}개")
        print(f"- 난이도: {info['difficulty']}")
        print(f"- 기물 개수: {info['pieces_count']}개")
        print(f"- 조각된 칸들: {info['carved_cells']}")
    
    def verify_puzzle_solvability(self):
        """생성된 퍼즐의 풀이 가능성 재검증"""
        if self.puzzle_board is None:
            print("퍼즐이 생성되지 않았습니다.")
            return False
        
        solver = LogicalSolver(self.puzzle_board, self.pieces)
        is_solvable = solver.is_solvable_logically()
        
        if is_solvable:
            print("✓ 퍼즐이 논리적으로 풀 수 있습니다.")
            return True
        else:
            print("✗ 퍼즐이 논리적으로 풀 수 없습니다.")
            return False
    
    def get_solution_hints(self):
        """퍼즐 풀이 힌트 제공 (고급 기능)"""
        if self.puzzle_board is None:
            return None
        
        solver = LogicalSolver(self.puzzle_board, self.pieces)
        solver.initialize_possible_values()
        
        hints = []
        for row in range(9):
            for col in range(9):
                if self.puzzle_board.get_value(row, col) is None:
                    possible = solver.possible_values.get((row, col), set())
                    if len(possible) <= 3:  # 가능한 값이 3개 이하인 칸만 힌트로 제공
                        hints.append({
                            'position': (row, col),
                            'possible_values': list(possible),
                            'count': len(possible)
                        })
        
        # 가능한 값 개수 순으로 정렬
        hints.sort(key=lambda x: x['count'])
        return hints
