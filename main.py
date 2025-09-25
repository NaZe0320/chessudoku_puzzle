from board import Board
from random_placer import RandomPiecePlacer
from sudoku_solver import ChesSudokuSolver
from puzzle_generator import PuzzleGenerator, PuzzleSolver
from puzzle_api_client import PuzzleAPIClient, DifficultyManager
from config import config

def main(server_url=None, custom_difficulty=None, puzzle_type="normal", daily_date=None):
    # 1. 기물 배치 (빈 보드에)
    print("=" * 50)
    print("1단계: 랜덤 기물 배치")
    print("=" * 50)
    
    board = Board()
    
    print("빈 보드:")
    board.print_board()
    
    random_placer = RandomPiecePlacer(board)
    placed_count = random_placer.place_pieces_randomly()
    
    print(f"\n기물 배치 완료: {placed_count}개")
    print("\n기물 배치 후:")
    board.print_board()
    
    # 2. 완전한 스도쿠 보드 생성 (기물 제약 조건 고려)
    print("\n" + "=" * 50)
    print("2단계: 완전한 스도쿠 보드 생성 (기물 제약 조건 고려)")
    print("=" * 50)
    
    solver = ChesSudokuSolver(board, random_placer.get_pieces())
    success = solver.solve_with_pieces()
    
    if not success:
        print("기물 제약 조건을 만족하는 스도쿠 보드 생성 실패!")
        return
    
    print("\n기물 제약 조건을 만족하는 완성된 보드:")
    board.print_board()
    
    # 3. 퍼즐 생성 (빈칸 뚫기 - 하나씩 뚫으면서 풀이 검증)
    print("\n" + "=" * 50)
    print("3단계: 퍼즐 생성 (빈칸 뚫기 - 하나씩 뚫으면서 풀이 검증)")
    print("=" * 50)
    
    max_holes = 35  # 원하는 빈칸 개수 설정
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
    
    # 5. 서버로 퍼즐 전송 (주석 처리)
    # print("\n" + "=" * 50)
    # print("5단계: 서버로 퍼즐 전송")
    # print("=" * 50)
    # 
    # # 난이도 결정
    # if custom_difficulty:
    #     difficulty = custom_difficulty
    #     print(f"사용자 지정 난이도: {difficulty} (빈칸 {puzzle_generator.holes_count}개)")
    # else:
    #     difficulty = DifficultyManager.get_difficulty_by_holes(puzzle_generator.holes_count)
    #     print(f"자동 결정된 난이도: {difficulty} (빈칸 {puzzle_generator.holes_count}개)")
    # 
    # # API 클라이언트 생성
    # api_client = PuzzleAPIClient()
    # 
    # # 서버 URL 설정
    # if server_url:
    #     api_client.set_server_url(server_url)
    # 
    # # 퍼즐 업로드
    # upload_success, upload_result = api_client.upload_puzzle(
    #     puzzle_board=puzzle_board,
    #     answer_board=board,  # 완성된 보드가 정답
    #     pieces=random_placer.get_pieces(),
    #     difficulty=difficulty,
    #     puzzle_type=puzzle_type,
    #     daily_date=daily_date
    # )
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("최종 결과")
    print("=" * 50)
    if success:
        print("퍼즐 풀이 성공! 🎉")
    else:
        print("퍼즐 풀이 실패 😞")
    
    # if upload_success:
    #     print("서버 업로드 성공! 🚀")
    #     if upload_result and "data" in upload_result:
    #         puzzle_id = upload_result["data"].get("puzzle_id")
    #         if puzzle_id:
    #             print(f"퍼즐 ID: {puzzle_id}")
    # else:
    #     print("서버 업로드 실패 📤")

# 사용자 편의 함수들
def create_normal_puzzle(server_url=None, difficulty=None):
    """일반 퍼즐 생성 및 업로드"""
    print("일반 퍼즐 생성 모드")
    return main(server_url=server_url, custom_difficulty=difficulty, puzzle_type="normal")

def create_daily_puzzle(daily_date, server_url=None, difficulty=None):
    """데일리 퍼즐 생성 및 업로드"""
    print(f"데일리 퍼즐 생성 모드 (날짜: {daily_date})")
    return main(server_url=server_url, custom_difficulty=difficulty, puzzle_type="daily_challenge", daily_date=daily_date)

def show_help():
    """사용법 도움말"""
    print("=" * 60)
    print("체스도쿠 퍼즐 생성기 사용법")
    print("=" * 60)
    print("1. 기본 실행:")
    print("   python main.py")
    print()
    print("2. Python에서 함수 호출:")
    print("   from main import create_normal_puzzle, create_daily_puzzle")
    print()
    print("   # 일반 퍼즐 생성")
    print("   create_normal_puzzle()")
    print("   create_normal_puzzle(server_url='https://your-server.com')")
    print("   create_normal_puzzle(difficulty='hard')")
    print()
    print("   # 데일리 퍼즐 생성")
    print("   create_daily_puzzle('2024-01-01')")
    print("   create_daily_puzzle('2024-01-01', difficulty='expert')")
    print()
    print("3. 사용 가능한 난이도:")
    DifficultyManager.list_difficulties()
    print()
    print("4. 서버 설정:")
    print(f"   - 현재 설정: {config.get_server_url()}")
    print("   - 환경변수: CHESSUDOKU_SERVER_URL=https://your-server.com")
    print("   - 설정파일: config.json 생성")
    print("   - 사용자 지정: server_url 매개변수 사용")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_help()
    else:
        main()
