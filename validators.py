from board import Board

class Piece:
    """체스 기물을 나타내는 클래스"""
    
    def __init__(self, piece_type, row, col):
        self.piece_type = piece_type  # 'K', 'Q', 'R', 'B', 'N'
        self.row = row
        self.col = col

class PiecePlacer:
    """기물 배치를 관리하는 클래스"""
    
    def __init__(self, board):
        self.board = board
        self.pieces = []  # 배치된 기물들
    
    def place_piece(self, piece_type, row, col):
        """기물을 보드에 배치"""
        if self.board.is_empty(row, col):
            piece = Piece(piece_type, row, col)
            self.pieces.append(piece)
            self.board.set_value(row, col, piece_type)
            return True
        return False
    
    def get_knight_moves(self, row, col):
        """나이트가 갈 수 있는 위치들 반환"""
        moves = []
        knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 9 and 0 <= new_col < 9:
                moves.append((new_row, new_col))
        return moves
    
    def get_king_moves(self, row, col):
        """킹이 갈 수 있는 위치들 반환"""
        moves = []
        king_moves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 9 and 0 <= new_col < 9:
                moves.append((new_row, new_col))
        return moves
    
    def get_diagonal_positions(self, row, col, direction):
        """대각선 위치들 반환 (direction: 'right' 또는 'left')"""
        positions = []
        
        if direction == 'right':  # 오른대각선 (/)
            # 위쪽 대각선
            r, c = row - 1, col + 1
            while r >= 0 and c < 9:
                positions.append((r, c))
                r -= 1
                c += 1
            
            # 아래쪽 대각선
            r, c = row + 1, col - 1
            while r < 9 and c >= 0:
                positions.append((r, c))
                r += 1
                c -= 1
                
        elif direction == 'left':  # 왼대각선 (\)
            # 위쪽 대각선
            r, c = row - 1, col - 1
            while r >= 0 and c >= 0:
                positions.append((r, c))
                r -= 1
                c -= 1
            
            # 아래쪽 대각선
            r, c = row + 1, col + 1
            while r < 9 and c < 9:
                positions.append((r, c))
                r += 1
                c += 1
        
        return positions
    
    def is_valid_number_for_piece(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 기물 규칙으로 검사"""
        # 모든 기물에 대해 검사
        for piece in self.pieces:
            # 경우 1: 기물이 있는 위치에 이미 같은 숫자가 있고, 그 기물이 현재 위치를 공격할 수 있는 경우
            piece_value = self.board.get_value(piece.row, piece.col)
            if isinstance(piece_value, int) and piece_value == number:
                if self._can_piece_attack(piece, row, col):
                    return False
            
            # 경우 2: 현재 위치에 숫자를 놓으려는데, 그 위치가 기물 위치이고 기물의 영향 범위에 같은 숫자가 있는 경우
            if piece.row == row and piece.col == col:
                # 이 기물이 공격할 수 있는 모든 위치에 같은 숫자가 있는지 확인
                for target_row in range(9):
                    for target_col in range(9):
                        if target_row == row and target_col == col:
                            continue
                        target_value = self.board.get_value(target_row, target_col)
                        if isinstance(target_value, int) and target_value == number:
                            if self._can_piece_attack(piece, target_row, target_col):
                                return False
        
        return True
    
    def _can_piece_attack(self, piece, target_row, target_col):
        """기물이 목표 위치를 공격할 수 있는지 확인"""
        piece_row, piece_col = piece.row, piece.col
        
        # 같은 위치면 공격할 수 없음
        if piece_row == target_row and piece_col == target_col:
            return False
        
        if piece.piece_type == 'N':  # 나이트
            knight_moves = self.get_knight_moves(piece_row, piece_col)
            return (target_row, target_col) in knight_moves
        
        elif piece.piece_type == 'R':  # 룩
            # 같은 행 또는 같은 열
            return piece_row == target_row or piece_col == target_col
        
        elif piece.piece_type == 'B':  # 비숍
            # 대각선상에 있는지 확인
            right_diag = self.get_diagonal_positions(piece_row, piece_col, 'right')
            left_diag = self.get_diagonal_positions(piece_row, piece_col, 'left')
            return (target_row, target_col) in right_diag or (target_row, target_col) in left_diag
        
        elif piece.piece_type == 'Q':  # 퀸 (룩 + 비숍)
            # 룩 규칙
            if piece_row == target_row or piece_col == target_col:
                return True
            # 비숍 규칙
            right_diag = self.get_diagonal_positions(piece_row, piece_col, 'right')
            left_diag = self.get_diagonal_positions(piece_row, piece_col, 'left')
            return (target_row, target_col) in right_diag or (target_row, target_col) in left_diag
        
        elif piece.piece_type == 'K':  # 킹
            king_moves = self.get_king_moves(piece_row, piece_col)
            return (target_row, target_col) in king_moves
        
        return False

class SudokuValidator:
    """스도쿠 규칙 검사 클래스"""
    
    def __init__(self, board):
        self.board = board
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 스도쿠 규칙으로 검사"""
        # 같은 행에 동일한 숫자가 있는지 확인
        for c in range(9):
            if c != col:
                value = self.board.get_value(row, c)
                # 숫자인 경우만 비교 (기물 문자는 무시)
                if isinstance(value, int) and value == number:
                    return False
        
        # 같은 열에 동일한 숫자가 있는지 확인
        for r in range(9):
            if r != row:
                value = self.board.get_value(r, col)
                # 숫자인 경우만 비교 (기물 문자는 무시)
                if isinstance(value, int) and value == number:
                    return False
        
        # 같은 3x3 박스에 동일한 숫자가 있는지 확인
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col):
                    value = self.board.get_value(r, c)
                    # 숫자인 경우만 비교 (기물 문자는 무시)
                    if isinstance(value, int) and value == number:
                        return False
        
        return True
    
    def find_empty_cell(self):
        """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
        for row in range(9):
            for col in range(9):
                if self.board.is_empty(row, col):
                    return (row, col)
        return None