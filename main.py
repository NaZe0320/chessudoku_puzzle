from board import Board
from random_placer import RandomPiecePlacer
from sudoku_solver import ChessSudokuSolver
from puzzle_generator import PuzzleGenerator, PuzzleSolver

def main():
    # 1. 기물 배치
    print("=" * 50)
    print("1단계: 랜덤 기물 배치")
    print("=" * 50)
    
    board = Board()
    random_placer = RandomPiecePlacer(board)
    
    print("빈 보드:")
    board.print_board()
    
    print("\n랜덤 기물 배치 중...")
    placed_count = random_placer.place_pieces_randomly()
    
    print("\n기물 배치 후:")
    board.print_board()
    
    # 2. 스도쿠 솔버로 숫자 채우기
    print("\n" + "=" * 50)
    print("2단계: 체스 기물과 스도쿠 제약 조건으로 숫자 채우기")
    print("=" * 50)
    
    solver = ChessSudokuSolver(board, random_placer.get_pieces())
    success = solver.solve_with_pieces()
    
    if not success:
        print("숫자 채우기 실패!")
        return
    
    print("\n완성된 보드:")
    board.print_board()
    
    # 3. 퍼즐 생성 (빈칸 뚫기)
    print("\n" + "=" * 50)
    print("3단계: 퍼즐 생성 (빈칸 뚫기)")
    print("=" * 50)
    
    max_holes = 50  # 원하는 빈칸 개수 설정
    puzzle_generator = PuzzleGenerator(board, random_placer.get_pieces(), max_holes)
    puzzle_board = puzzle_generator.generate_puzzle()
    
    print(f"\n생성된 퍼즐 ({puzzle_generator.holes_count}개 빈칸):")
    puzzle_board.print_board()
    
    # 4. 제약 전파 + 백트래킹으로 퍼즐 풀기
    print("\n" + "=" * 50)
    print("4단계: 제약 전파 + 백트래킹으로 퍼즐 풀기")
    print("=" * 50)
    
    puzzle_solver = PuzzleSolver(puzzle_board, random_placer.get_pieces())
    success, solved_board = puzzle_solver.solve_puzzle()
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("최종 결과")
    print("=" * 50)
    if success:
        print("퍼즐 풀이 성공! 🎉")
    else:
        print("퍼즐 풀이 실패 😞")

if __name__ == "__main__":
    main()
