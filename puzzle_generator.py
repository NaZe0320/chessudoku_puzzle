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
        
        # 3. 전략적 한 칸씩 조각하기 시도
        holes_carved = 0
        max_attempts = max_holes * 3  # 무한 루프 방지
        attempts = 0
        
        while holes_carved < max_holes and attempts < max_attempts:
            attempts += 1
            
            # 전략적 후보들 찾기
            candidates = self.get_strategic_carve_candidates()
            
            # 모든 그룹이 비어있는지 확인
            if not any(candidates.values()):
                print("더 이상 조각할 수 있는 칸이 없습니다.")
                break
            
            # 가중치 기반으로 칸 선택
            selected_cell = self.select_carve_candidate(candidates)
            
            if selected_cell:
                row, col = selected_cell
                
                # 이 칸을 조각해도 논리적으로 풀 수 있는지 확인
                if self.carve_cell_and_verify(row, col):
                    holes_carved += 1
                    self.carved_cells.append((row, col))
                    
                    # 어떤 전략으로 선택되었는지 표시
                    strategy = self.get_cell_strategy(row, col, candidates)
                    print(f"칸 ({row}, {col}) {strategy} 조각 완료 - 현재 빈칸: {holes_carved}개")
                else:
                    print(f"칸 ({row}, {col}) 조각 실패 - 논리적 풀이 불가능")
            else:
                print("선택할 수 있는 칸이 없습니다.")
                break
        
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
                if self.is_carveable(row, col):
                    carveable.append((row, col))
        
        return carveable
    
    def is_carveable(self, row, col):
        """해당 칸이 조각 가능한지 확인"""
        # 이미 조각된 칸은 제외
        if (row, col) in self.carved_cells:
            return False
        
        # 기물이 있는 칸은 조각할 수 없음
        if self.is_piece_position(row, col):
            return False
        
        # 숫자가 있는 칸만 조각 가능
        return isinstance(self.puzzle_board.get_value(row, col), int)
    
    def is_piece_position(self, row, col):
        """해당 위치에 기물이 있는지 확인"""
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return True
        return False
    
    def find_completed_line_cells(self):
        """완성된 행, 열, 3x3 박스의 칸들을 찾기"""
        completed_cells = []
        
        # 완성된 행 찾기
        for row in range(9):
            if self.is_row_complete(row):
                for col in range(9):
                    if self.is_carveable(row, col):
                        completed_cells.append((row, col))
        
        # 완성된 열 찾기
        for col in range(9):
            if self.is_col_complete(col):
                for row in range(9):
                    if self.is_carveable(row, col):
                        completed_cells.append((row, col))
        
        # 완성된 3x3 박스 찾기
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                if self.is_box_complete(box_row, box_col):
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if self.is_carveable(r, c):
                                completed_cells.append((r, c))
        
        return completed_cells
    
    def is_row_complete(self, row):
        """해당 행이 완성되었는지 확인 (1-9 모든 숫자가 있는지)"""
        numbers = set()
        for col in range(9):
            value = self.puzzle_board.get_value(row, col)
            if isinstance(value, int):
                numbers.add(value)
        return len(numbers) == 9
    
    def is_col_complete(self, col):
        """해당 열이 완성되었는지 확인 (1-9 모든 숫자가 있는지)"""
        numbers = set()
        for row in range(9):
            value = self.puzzle_board.get_value(row, col)
            if isinstance(value, int):
                numbers.add(value)
        return len(numbers) == 9
    
    def is_box_complete(self, box_row, box_col):
        """해당 3x3 박스가 완성되었는지 확인 (1-9 모든 숫자가 있는지)"""
        numbers = set()
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                value = self.puzzle_board.get_value(r, c)
                if isinstance(value, int):
                    numbers.add(value)
        return len(numbers) == 9
    
    def find_unconstrained_cells(self):
        """기물의 공격 범위에 있지 않은 칸들 찾기"""
        unconstrained = []
        
        for row in range(9):
            for col in range(9):
                if self.is_carveable(row, col):
                    # 이 칸이 기물의 공격 범위에 있는지 확인
                    if not self.is_under_piece_constraint(row, col):
                        unconstrained.append((row, col))
        
        return unconstrained
    
    def is_under_piece_constraint(self, row, col):
        """해당 칸이 기물의 제약 조건 하에 있는지 확인"""
        # PiecePlacer 인스턴스 생성 (기물 제약 검사용)
        from validators import PiecePlacer
        piece_placer = PiecePlacer(self.puzzle_board)
        piece_placer.pieces = self.pieces
        
        for piece in self.pieces:
            if piece_placer._can_piece_attack(piece, row, col):
                return True
        return False
    
    def get_strategic_carve_candidates(self):
        """전략적 우선순위에 따라 조각할 수 있는 칸들을 반환"""
        
        # 1순위: 완성된 행/열/박스의 칸들
        completed_cells = self.find_completed_line_cells()
        
        # 2순위: 기물 제약이 없는 칸들 (기물 공격 범위 밖)
        unconstrained_cells = self.find_unconstrained_cells()
        
        # 3순위: 일반 칸들
        regular_cells = self.get_carveable_cells()
        
        # 우선순위별로 그룹화하여 반환
        return {
            'completed_lines': completed_cells,
            'unconstrained': unconstrained_cells, 
            'regular': regular_cells
        }
    
    def select_carve_candidate(self, candidates):
        """가중치를 적용하여 조각할 칸 선택"""
        
        # 우선순위별 가중치 설정
        weights = {
            'completed_lines': 0.6,  # 60% 확률로 완성된 라인 우선
            'unconstrained': 0.3,   # 30% 확률로 제약 없는 칸
            'regular': 0.1           # 10% 확률로 일반 칸
        }
        
        # 각 그룹에서 랜덤 선택
        selected_group = random.choices(
            list(weights.keys()), 
            weights=list(weights.values())
        )[0]
        
        if candidates[selected_group]:
            return random.choice(candidates[selected_group])
        
        # 선택된 그룹이 비어있으면 다른 그룹에서 선택
        for group in ['completed_lines', 'unconstrained', 'regular']:
            if candidates[group]:
                return random.choice(candidates[group])
        
        return None
    
    def get_cell_strategy(self, row, col, candidates):
        """선택된 칸이 어떤 전략으로 선택되었는지 반환"""
        if (row, col) in candidates['completed_lines']:
            return "완성라인"
        elif (row, col) in candidates['unconstrained']:
            return "제약없음"
        elif (row, col) in candidates['regular']:
            return "일반"
        else:
            return "알수없음"
    
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
        
        # 전략별 조각 통계
        strategy_stats = self.get_strategy_statistics()
        print(f"- 전략별 조각 통계:")
        print(f"  * 완성라인: {strategy_stats['completed_lines']}개")
        print(f"  * 제약없음: {strategy_stats['unconstrained']}개")
        print(f"  * 일반: {strategy_stats['regular']}개")
        
        print(f"- 조각된 칸들: {info['carved_cells']}")
    
    def get_strategy_statistics(self):
        """전략별 조각 통계 반환"""
        stats = {'completed_lines': 0, 'unconstrained': 0, 'regular': 0}
        
        # 현재 후보들 확인
        candidates = self.get_strategic_carve_candidates()
        
        for row, col in self.carved_cells:
            if (row, col) in candidates['completed_lines']:
                stats['completed_lines'] += 1
            elif (row, col) in candidates['unconstrained']:
                stats['unconstrained'] += 1
            else:
                stats['regular'] += 1
        
        return stats
    
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
