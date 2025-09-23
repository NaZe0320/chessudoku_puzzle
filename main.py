from board import Board
from pieces import PiecePlacer
from sudoku_solver import SudokuSolver

# 테스트
board = Board()
placer = PiecePlacer(board)
solver = SudokuSolver(board, placer)

print("스도쿠 솔버 테스트:")
print("빈 보드:")
board.print_board()

# 기물 배치
placer.place_piece('N', 1, 1)  # 나이트
placer.place_piece('R', 3, 3)  # 룩

print("\n기물 배치 후:")
board.print_board()

# 스도쿠 해결 시도
print("\n스도쿠 해결 시도...")
if solver.solve_sudoku():
    print("해결 완료!")
    board.print_board()
else:
    print("해결 불가능!")

print(f"\n배치된 기물 수: {len(placer.pieces)}")
for piece in placer.pieces:
    print(f"{piece.piece_type} at ({piece.row}, {piece.col})")
