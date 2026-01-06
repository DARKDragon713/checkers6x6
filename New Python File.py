import copy
import random

# تعریف مقادیر ثابت برای راحتی کار
KHALI = 0
SIAH = 1
SEFID = 2
SIAH_SHAH = 3
SEFID_SHAH = 4

# اندازه صفحه
ROWS = 6
COLS = 6

class Checkers6x6:
    def __init__(self):
        # ساختن صفحه بازی به صورت یک لیست دو بعدی
        self.board = []
        self.nobat = SIAH  # نوبت اول با سیاه است
        self.create_board()

    def create_board(self):
        # پر کردن صفحه با صفر
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                row.append(KHALI)
            self.board.append(row)
        
        # چیدن مهره های سیاه (بالای صفحه)
        # سیاه ها در ردیف 0 و 1 قرار می گیرند
        for r in range(2):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    self.board[r][c] = SIAH
                    
        # چیدن مهره های سفید (پایین صفحه)
        # سفیدها در ردیف 4 و 5 قرار می گیرند
        for r in range(4, 6):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    self.board[r][c] = SEFID

    def print_board(self):
        print("   0  1  2  3  4  5")
        print("  ------------------")
        for r in range(ROWS):
            line = str(r) + "| "
            for c in range(COLS):
                piece = self.board[r][c]
                if piece == KHALI:
                    line += "0  "
                elif piece == SIAH:
                    line += "b  "
                elif piece == SEFID:
                    line += "w  "
                elif piece == SIAH_SHAH:
                    line += "B "
                elif piece == SEFID_SHAH:
                    line += "W "
            print(line)
        print()

    def is_inside(self, r, c):
        # چک میکنیم که مختصات بیرون از صفحه نباشه
        return 0 <= r < ROWS and 0 <= c < COLS
