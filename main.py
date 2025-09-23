from board import Board
from random_placer import RandomPiecePlacer
from sudoku_solver import ChessSudokuSolver

# 테스트
board = Board()
random_placer = RandomPiecePlacer(board)

print("랜덤 기물 배치 테스트:")
print("빈 보드:")
board.print_board()

# 랜덤 기물 배치
print("\n랜덤 기물 배치 중...")
placed_count = random_placer.place_pieces_randomly()

print("\n기물 배치 후:")
board.print_board()

# 스도쿠 솔버로 숫자 채우기
print("\n체스 기물과 스도쿠 제약 조건으로 숫자 채우기:")
solver = ChessSudokuSolver(board, random_placer.get_pieces())
success = solver.solve_with_pieces()

if success:
    print("\n완성된 보드:")
    board.print_board()
else:
    print("숫자 채우기 실패!")
