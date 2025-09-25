from board import Board

class ChesSudokuSolver:
    """체스 기물과 스도쿠 제약 조건을 모두 고려한 솔버"""
    
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces
    
