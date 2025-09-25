class Board:
    """9x9 보드를 관리하는 클래스"""
    
    def __init__(self):
        """빈 9x9 보드로 초기화"""
        self.board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(None)  # 빈칸으로 초기화
            self.board.append(row)
    
    def is_empty(self, row, col):
        """해당 위치가 빈 칸인지 확인"""
        return self.board[row][col] is None
    
    def set_value(self, row, col, value):
        """해당 위치에 값 설정"""
        self.board[row][col] = value
    
    def get_value(self, row, col):
        """해당 위치의 값 조회"""
        return self.board[row][col]
    
    def print_board(self):
        """보드를 출력하는 함수"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] is None:
                    print(".", end=" ")  # 빈칸은 .으로 표시
                elif isinstance(self.board[i][j], str):
                    print(f"{self.board[i][j]}", end=" ") 
                else:
                    print(self.board[i][j], end=" ")  # 숫자는 그대로 표시
            print()  # 줄바꿈
    
    def clear_board(self):
        """보드를 모두 빈칸으로 초기화"""
        for i in range(9):
            for j in range(9):
                self.board[i][j] = None
