from board import Board
from validators import PiecePlacer
import random

class RandomPiecePlacer:
    """랜덤하게 기물을 배치하는 클래스"""
    
    def __init__(self, board):
        self.board = board
        self.placer = PiecePlacer(board)
    
    def place_pieces_randomly(self, piece_counts=None):
        """랜덤하게 기물들을 배치"""
        if piece_counts is None:
            # 기본 기물 개수 설정 (더 적게 배치하여 풀이 가능성 높이기)
            piece_counts = {'K': 1, 'Q': 0, 'R': 1, 'B': 2, 'N': 1}
        
        # 기물 타입과 개수를 리스트로 변환하여 랜덤하게 섞기
        pieces_to_place = []
        for piece_type, count in piece_counts.items():
            for _ in range(count):
                pieces_to_place.append(piece_type)
        
        # 기물 배치 순서를 랜덤하게 섞기
        random.shuffle(pieces_to_place)
        
        placed_count = 0
        
        # 랜덤하게 섞인 순서로 기물 배치
        for piece_type in pieces_to_place:
            placed = False
            attempts = 0
            max_attempts = 200  # 시도 횟수 증가
            
            while not placed and attempts < max_attempts:
                # 매번 새로운 랜덤 위치 선택
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                
                # 해당 위치가 비어있고 기물 배치가 가능한지 확인
                if self.board.is_empty(row, col):
                    # 임시로 기물 배치해서 유효성 검사
                    if self.placer.place_piece(piece_type, row, col):
                        # 유효성 검사 (다른 기물과 충돌하지 않는지)
                        if self.is_valid_piece_placement():
                            placed = True
                            placed_count += 1
                        else:
                            # 충돌하면 되돌리기
                            self.placer.pieces.pop()
                            self.board.set_value(row, col, None)
                
                attempts += 1
            
            if not placed:
                print(f"경고: {piece_type} 기물을 배치하지 못했습니다. ({attempts}번 시도)")
        
        return placed_count
    
    def is_valid_piece_placement(self):
        """현재 기물 배치가 유효한지 검사 (기물끼리 충돌하지 않는지)"""
        for i, piece1 in enumerate(self.placer.pieces):
            for j, piece2 in enumerate(self.placer.pieces):
                if i >= j:  # 같은 기물이거나 이미 검사한 조합은 스킵
                    continue
                
                # 같은 위치에 두 기물이 있으면 충돌
                if piece1.row == piece2.row and piece1.col == piece2.col:
                    return False
                
                # 각 기물의 공격 범위 확인
                if self.pieces_attack_each_other(piece1, piece2):
                    return False
        
        return True
    
    def pieces_attack_each_other(self, piece1, piece2):
        """두 기물이 서로를 공격할 수 있는지 확인"""
        # 룩과 퀸의 경우
        if piece1.piece_type in ['R', 'Q']:
            if self.can_rook_attack(piece1.row, piece1.col, piece2.row, piece2.col):
                return True
        
        if piece2.piece_type in ['R', 'Q']:
            if self.can_rook_attack(piece2.row, piece2.col, piece1.row, piece1.col):
                return True
        
        # 비숍과 퀸의 경우
        if piece1.piece_type in ['B', 'Q']:
            if self.can_bishop_attack(piece1.row, piece1.col, piece2.row, piece2.col):
                return True
        
        if piece2.piece_type in ['B', 'Q']:
            if self.can_bishop_attack(piece2.row, piece2.col, piece1.row, piece1.col):
                return True
        
        # 나이트의 경우
        if piece1.piece_type == 'N':
            knight_moves = self.placer.get_knight_moves(piece1.row, piece1.col)
            if (piece2.row, piece2.col) in knight_moves:
                return True
        
        if piece2.piece_type == 'N':
            knight_moves = self.placer.get_knight_moves(piece2.row, piece2.col)
            if (piece1.row, piece1.col) in knight_moves:
                return True
        
        # 킹의 경우
        if piece1.piece_type == 'K':
            king_moves = self.placer.get_king_moves(piece1.row, piece1.col)
            if (piece2.row, piece2.col) in king_moves:
                return True
        
        if piece2.piece_type == 'K':
            king_moves = self.placer.get_king_moves(piece2.row, piece2.col)
            if (piece1.row, piece1.col) in king_moves:
                return True
        
        return False
    
    def can_rook_attack(self, row1, col1, row2, col2):
        """룩이 목표를 공격할 수 있는지 확인"""
        return row1 == row2 or col1 == col2
    
    def can_bishop_attack(self, row1, col1, row2, col2):
        """비숍이 목표를 공격할 수 있는지 확인"""
        return abs(row1 - row2) == abs(col1 - col2)
    
    def get_pieces(self):
        """배치된 기물들 반환"""
        return self.placer.pieces
