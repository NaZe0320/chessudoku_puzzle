from board import Board
from validators import SudokuValidator
from random_placer import RandomPiecePlacer

# 테스트
board = Board()
random_placer = RandomPiecePlacer(board)
validator = SudokuValidator(board)

print("랜덤 기물 배치 테스트:")
print("빈 보드:")
board.print_board()

# 랜덤 기물 배치
print("\n랜덤 기물 배치 중...")
placed_count = random_placer.place_pieces_randomly()

print("\n기물 배치 후:")
board.print_board()

# 스도쿠 검사 테스트
print("\n스도쿠 검사 테스트:")
print("빈 칸 찾기:", validator.find_empty_cell())
print("유일해 검사:", validator.is_unique_solution())

print(f"\n배치된 기물 수: {len(random_placer.get_pieces())}")
for piece in random_placer.get_pieces():
    print(f"{piece.piece_type} at ({piece.row}, {piece.col})")
