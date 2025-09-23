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
        piece = None
        for p in self.pieces:
            if p.row == row and p.col == col:
                piece = p
                break
        
        if not piece:
            return True  # 기물이 없는 위치는 자유롭게
        
        # 각 기물별 규칙 검사
        if piece.piece_type == 'N':  # 나이트
            knight_moves = self.get_knight_moves(row, col)
            for r, c in knight_moves:
                if self.board.get_value(r, c) == number:
                    return False
        
        elif piece.piece_type == 'R':  # 룩 (스도쿠 기본 규칙과 동일)
            # 같은 행 검사
            for c in range(9):
                if c != col and self.board.get_value(row, c) == number:
                    return False
            # 같은 열 검사
            for r in range(9):
                if r != row and self.board.get_value(r, col) == number:
                    return False
        
        elif piece.piece_type == 'B':  # 비숍
            # 오른대각선 검사
            right_diag = self.get_diagonal_positions(row, col, 'right')
            for r, c in right_diag:
                if self.board.get_value(r, c) == number:
                    return False
            # 왼대각선 검사
            left_diag = self.get_diagonal_positions(row, col, 'left')
            for r, c in left_diag:
                if self.board.get_value(r, c) == number:
                    return False
        
        elif piece.piece_type == 'Q':  # 퀸 (룩 + 비숍)
            # 룩 규칙
            for c in range(9):
                if c != col and self.board.get_value(row, c) == number:
                    return False
            for r in range(9):
                if r != row and self.board.get_value(r, col) == number:
                    return False
            # 비숍 규칙
            right_diag = self.get_diagonal_positions(row, col, 'right')
            for r, c in right_diag:
                if self.board.get_value(r, c) == number:
                    return False
            left_diag = self.get_diagonal_positions(row, col, 'left')
            for r, c in left_diag:
                if self.board.get_value(r, c) == number:
                    return False
        
        elif piece.piece_type == 'K':  # 킹
            king_moves = self.get_king_moves(row, col)
            for r, c in king_moves:
                if self.board.get_value(r, c) == number:
                    return False
        
        return True

class SudokuValidator:
    """스도쿠 규칙 검사 클래스"""
    
    def __init__(self, board):
        self.board = board
    
    def is_valid_number(self, row, col, number):
        """해당 위치에 숫자를 놓을 수 있는지 스도쿠 규칙으로 검사"""
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
    
    def find_empty_cell(self):
        """빈 칸을 찾아서 (row, col) 반환, 없으면 None"""
        for row in range(9):
            for col in range(9):
                if self.board.is_empty(row, col):
                    return (row, col)
        return None
    