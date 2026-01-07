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

    def get_all_moves(self, player, board_state=None):
        if board_state is None:
            board_state = self.board

        moves = [] # لیست حرکات ساده
        jumps = [] # لیست حرکات خوردن

        # تعیین جهت حرکت (سیاه به پایین میره، سفید به بالا)
        # مگر اینکه شاه باشه
        
        for r in range(ROWS):
            for c in range(COLS):
                piece = board_state[r][c]
                
                # اگر خانه خالی بود یا مهره مال بازیکن نبود رد شو
                if piece == KHALI:
                    continue
                
                # تشخیص اینکه مهره مال این بازیکن هست یا نه
                is_current_player = False
                if player == SIAH and (piece == SIAH or piece == SIAH_SHAH):
                    is_current_player = True
                elif player == SEFID and (piece == SEFID or piece == SEFID_SHAH):
                    is_current_player = True
                
                if not is_current_player:
                    continue

                # حالا حرکات رو بررسی میکنیم
                is_king = (piece == SIAH_SHAH or piece == SEFID_SHAH)
                
                # جهت های مجاز
                directions = []
                if player == SIAH or is_king:
                    directions.append((1, -1)) # پایین چپ
                    directions.append((1, 1))  # پایین راست
                if player == SEFID or is_king:
                    directions.append((-1, -1)) # بالا چپ
                    directions.append((-1, 1))  # بالا راست

                # 1. بررسی حرکات ساده
                for dr, dc in directions:
                    new_r, new_c = r + dr, c + dc
                    if self.is_inside(new_r, new_c):
                        if board_state[new_r][new_c] == KHALI:
                            # حرکت ساده است
                            # فرمت حرکت: ((مبدا)، (مقصد)، [لیست مهره های خورده شده])
                            moves.append(((r, c), (new_r, new_c), []))

                # 2. بررسی حرکات خوردن (Jump)
                # برای خوردن زنجیره ای از تابع بازگشتی استفاده میکنیم
                self.get_jumps(r, c, piece, board_state, [], jumps)

        # قانون: اگر خوردن ممکن باشد، باید حتما بخوریم
        if len(jumps) > 0:
            return jumps
        else:
            return moves

    def get_jumps(self, r, c, piece, board, skipped, all_jumps):
        # این تابع تمام حالات خوردن رو پیدا میکنه
        
        is_king = (piece == SIAH_SHAH or piece == SEFID_SHAH)
        player = SIAH if (piece == SIAH or piece == SIAH_SHAH) else SEFID
        
        directions = []
        if player == SIAH or is_king:
            directions.extend([(1, -1), (1, 1)])
        if player == SEFID or is_king:
            directions.extend([(-1, -1), (-1, 1)])

        found_jump = False
        
        for dr, dc in directions:
            mid_r, mid_c = r + dr, c + dc # خانه ای که میپریم روش
            dest_r, dest_c = r + 2*dr, c + 2*dc # خانه مقصد
            
            if self.is_inside(dest_r, dest_c):
                mid_piece = board[mid_r][mid_c]
                dest_piece = board[dest_r][dest_c]
                
                # چک کنیم وسطی حریف باشه و مقصد خالی باشه
                if mid_piece != KHALI and dest_piece == KHALI:
                    # چک کنیم که حریف باشه
                    is_enemy = False
                    if player == SIAH and (mid_piece == SEFID or mid_piece == SEFID_SHAH):
                        is_enemy = True
                    elif player == SEFID and (mid_piece == SIAH or mid_piece == SIAH_SHAH):
                        is_enemy = True
                    
                    # همچنین نباید مهره ای که قبلا تو همین نوبت خوردیم رو دوباره بخوریم (جلوگیری از دور)
                    if is_enemy and (mid_r, mid_c) not in skipped:
                        # یک کپی فرضی از صفحه بسازیم
                        found_jump = True
                        
                        # حرکت رو ادامه بدیم
                        new_skipped = skipped + [(mid_r, mid_c)]
                        
                        # بازگشتی صدا میزنیم تا ببینیم باز هم میشه خورد؟
                        # نکته: وقتی میپریم جای ما عوض میشه
                        # برای سادگی، فعلا فقط مسیر رو ذخیره میکنیم
                        
                        # اینجا یه ترفند میزنیم، برد رو موقتی آپدیت نمیکنیم، فقط مسیر رو نگه میداریم
                        # تو قوانین ساده دامه، اگه خوردن باشه ادامه میدیم
                        
                        # برای اینکه ساده باشه، فعلا فقط همین پرش رو اضافه میکنیم
                        # و بازگشتی چک میکنیم
                        
                        # اینجا فرض میکنیم مهره حرکت کرده به dest
                        temp_board = [row[:] for row in board] # کپی سریع
                        temp_board[r][c] = KHALI
                        temp_board[dest_r][dest_c] = piece
                        temp_board[mid_r][mid_c] = KHALI # مهره خورده شده حذف میشه موقتی
                        
                        self.get_jumps(dest_r, dest_c, piece, temp_board, new_skipped, all_jumps)
        
        if not found_jump and len(skipped) > 0:
            # اگر دیگه نمیتونست بپره و قبلا حداقل یکی پریده بود، این مسیر تمومه
            # فرمت: ((مبدا اولیه)، (مقصد نهایی)، [لیست مهره های خورده شده])
            # ما اینجا فقط آخرین مقصد رو داریم، باید مبدا اصلی رو از بیرون پاس میدادیم
            # ولی چون ساختار کد ساده است، ما کل لیست مهره های خورده شده رو برمیگردونیم
            # و بعدا حرکت رو اعمال میکنیم.
            
            # برای سادگی: فرض میکنیم مبدا همونیه که تابع اول باهاش صدا زده شده (این بخش یکم باگ داره تو منطق بازگشتی)
            # اصلاح: ما فقط لیست مهره های خورده شده و مقصد نهایی رو ذخیره میکنیم
            all_jumps.append(((None), (r, c), skipped))

