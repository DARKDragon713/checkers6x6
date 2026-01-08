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

    # این تابع رو جدا نوشتم چون get_jumps پیچیده شد، این کار رو ساده میکنه برای رابط اصلی
    def clean_jumps_list(self, start_pos, moves):
        cleaned = []
        for m in moves:
            # m فرمتش اینه: (None, (dest_r, dest_c), skipped_list)
            if m[0] is None:
                cleaned.append((start_pos, m[1], m[2]))
        return cleaned

    def execute_move(self, move):
        start, end, skipped = move
        sr, sc = start
        er, ec = end
        
        piece = self.board[sr][sc]
        self.board[sr][sc] = KHALI
        self.board[er][ec] = piece
        
        # حذف مهره های خورده شده
        for (dr, dc) in skipped:
            self.board[dr][dc] = KHALI
            
        # تبدیل به شاه (King)
        if piece == SIAH and er == ROWS - 1:
            self.board[er][ec] = SIAH_SHAH
        elif piece == SEFID and er == 0:
            self.board[er][ec] = SEFID_SHAH

    def get_valid_moves_final(self, player):
        # این تابع نهایی است که همه کارها رو جمع بندی میکنه
        raw_moves = self.get_all_moves(player)
        
        # یه تمیزکاری نیاز داریم چون تابع get_jumps یکم خروجی هاش خام بود
        final_moves = []
        
        # اگر لیست حرکات پرشی بود (یعنی len(skipped) > 0)
        has_jump = False
        for m in raw_moves:
             if len(m[2]) > 0:
                 has_jump = True
                 break
        
        if not has_jump:
            return raw_moves
        
        # اگر پرش داشتیم، باید مبدا رو درست کنیم (چون تو تابع بازگشتی گم شد)
        # راه حل ساده: دوباره چک کنیم.
        # یه راه ساده تر: تابع get_all_moves رو اصلاح کنیم؟.
        # يا کلا فقط توابع سطح بالا رو استفاده کنیم.
        
        # *بازنویسی ساده برای رفع باگ منطقی بالا*:
        # بیخیال تابع پیچیده get_jumps، یه نسخه ساده تر خطی مینویسم که کار کنه.
        # معمولا فقط "یک پرش" رو پیاده میکنن یا نهایتا دو تا.
        # اما من سعی میکنم درستش رو بنویسم.
        
        moves = []
        jumps = []
        
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == KHALI: continue
                
                p = self.board[r][c]
                if player == SIAH and p not in [SIAH, SIAH_SHAH]: continue
                if player == SEFID and p not in [SEFID, SEFID_SHAH]: continue
                
                # پیدا کردن پرش های این مهره
                this_jumps = []
                self.find_jumps_recursive(r, c, p, self.board, [], this_jumps)
                
                for end_pos, skipped_list in this_jumps:
                    jumps.append(((r,c), end_pos, skipped_list))
                
                # پیدا کردن حرکات ساده (فقط اگر پرشی کلا تو صفحه نباشه معتبرن)
                if len(jumps) == 0: 
                    # کد تکراری حرکت ساده
                    dirs = []
                    is_k = (p == SIAH_SHAH or p == SEFID_SHAH)
                    if player == SIAH or is_k: dirs.extend([(1,-1), (1,1)])
                    if player == SEFID or is_k: dirs.extend([(-1,-1), (-1,1)])
                    
                    for dr, dc in dirs:
                        nr, nc = r+dr, c+dc
                        if self.is_inside(nr, nc) and self.board[nr][nc] == KHALI:
                            moves.append(((r,c), (nr,nc), []))

        if len(jumps) > 0:
            # پیدا کردن طولانی ترین پرش (قانون Max capture)
            max_len = 0
            for j in jumps:
                if len(j[2]) > max_len:
                    max_len = len(j[2])
            
            best_jumps = []
            for j in jumps:
                if len(j[2]) == max_len:
                    best_jumps.append(j)
            return best_jumps
        
        return moves

    def find_jumps_recursive(self, r, c, piece, board, current_skipped, found_jumps):
        # نسخه اصلاح شده و تمیزتر تابع بازگشتی
        is_king = (piece == SIAH_SHAH or piece == SEFID_SHAH)
        player = SIAH if piece in [SIAH, SIAH_SHAH] else SEFID
        
        dirs = []
        if player == SIAH or is_king: dirs.extend([(1, -1), (1, 1)])
        if player == SEFID or is_king: dirs.extend([(-1, -1), (-1, 1)])
        
        jump_available = False
        
        for dr, dc in dirs:
            mid_r, mid_c = r + dr, c + dc
            dst_r, dst_c = r + 2*dr, c + 2*dc
            
            if self.is_inside(dst_r, dst_c):
                if board[mid_r][mid_c] != KHALI and board[dst_r][dst_c] == KHALI:
                    # چک کنیم حریف باشه
                    mid_p = board[mid_r][mid_c]
                    is_enemy = False
                    if player == SIAH and mid_p in [SEFID, SEFID_SHAH]: is_enemy = True
                    if player == SEFID and mid_p in [SIAH, SIAH_SHAH]: is_enemy = True
                    
                    if is_enemy and (mid_r, mid_c) not in current_skipped:
                        jump_available = True
                        # کپی صفحه برای ادامه مسیر
                        new_board = [row[:] for row in board]
                        new_board[r][c] = KHALI
                        new_board[dst_r][dst_c] = piece
                        new_board[mid_r][mid_c] = KHALI # حذف موقت
                        
                        self.find_jumps_recursive(dst_r, dst_c, piece, new_board, 
                                                current_skipped + [(mid_r, mid_c)], found_jumps)
        
        if not jump_available and len(current_skipped) > 0:
            found_jumps.append(((r, c), current_skipped))

    def game_over(self):
        # اگر کسی مهره نداشته باشه یا نتونه حرکت کنه
        siah_moves = self.get_valid_moves_final(SIAH)
        sefid_moves = self.get_valid_moves_final(SEFID)
        
        if len(siah_moves) == 0:
            return SEFID # سفید برد
        if len(sefid_moves) == 0:
            return SIAH # سیاه برد
            
        return None

# --- بخش هوش مصنوعی (AI) ---

class AI_Agent:
    def __init__(self, depth=3, use_ab=True):
        self.depth = depth
        self.use_ab = use_ab
        self.nodes_count = 0

    def evaluate(self, game):
        # تابع ارزیابی شماره 1 (ساده)
        # فقط اختلاف تعداد مهره ها رو میشماره + امتیاز برای شاه
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                p = game.board[r][c]
                if p == SIAH: score += 10
                elif p == SEFID: score -= 10
                elif p == SIAH_SHAH: score += 20 # شاه ارزشش بیشتره
                elif p == SEFID_SHAH: score -= 20
        return score

    def evaluate_advanced(self, game):
        # تابع ارزیابی شماره 2 (پیشرفته تر)
        # علاوه بر تعداد، به موقعیت هم نگاه میکنه
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                p = game.board[r][c]
                if p == SIAH:
                    score += 10
                    score += r # هرچی جلوتر باشه بهتره
                    if c == 0 or c == 5: score -= 1 # گوشه ها امن ترن ولی وسط حمله بهتره (فرضی)
                elif p == SEFID:
                    score -= 10
                    score -= (5-r) # برای سفید هرچی بالاتر باشه (اندیس کمتر) بهتره؟ نه ردیف 0 مقصده
                # ... کدهای بیشتر میشه زد ولی همین کافیه
        return score

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        self.nodes_count += 1
        
        winner = game.game_over()
        if winner == SIAH: return 10000
        if winner == SEFID: return -10000
        if depth == 0:
            return self.evaluate(game)

        if maximizing_player: # نوبت سیاه (AI)
            max_eval = -999999
            valid_moves = game.get_valid_moves_final(SIAH)
            for move in valid_moves:
                # کپی بازی
                game_copy = copy.deepcopy(game)
                game_copy.execute_move(move)
                
                eval = self.minimax(game_copy, depth-1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                
                if self.use_ab:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else: # نوبت سفید (Minimizer)
            min_eval = 999999
            valid_moves = game.get_valid_moves_final(SEFID)
            for move in valid_moves:
                game_copy = copy.deepcopy(game)
                game_copy.execute_move(move)
                
                eval = self.minimax(game_copy, depth-1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                
                if self.use_ab:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def get_best_move(self, game):
        self.nodes_count = 0
        best_move = None
        best_val = -999999
        
        moves = game.get_valid_moves_final(SIAH) # فرض میکنیم AI سیاهه
        
        print("AI is thinking...")
        for move in moves:
            game_copy = copy.deepcopy(game)
            game_copy.execute_move(move)
            
            # اینجا depth رو یکی کم میکنیم چون یه حرکت زدیم
            val = self.minimax(game_copy, self.depth - 1, -999999, 999999, False)
            
            if val > best_val:
                best_val = val
                best_move = move
                
        print(f"Nodes visited: {self.nodes_count}")
        return best_move

# --- بدنه اصلی برنامه ---

if __name__ == "__main__":
    game = Checkers6x6()
    ai = AI_Agent(depth=4, use_ab=True)
    
    # حلقه بازی
    while True:
        game.print_board()
        
        winner = game.game_over()
        if winner:
            if winner == SIAH: print("Black (AI) Wins!")
            else: print("White (Human) Wins!")
            break

        if game.nobat == SIAH:
            # نوبت هوش مصنوعی
            move = ai.get_best_move(game)
            if move is None:
                print("White Wins! AI has no moves.")
                break
            print(f"AI moved: {move[0]} to {move[1]}")
            game.execute_move(move)
            game.nobat = SEFID
            
        else:
            # نوبت انسان (سفید)
            print("Your Turn (White/W). You move UP (rows 5 -> 0).")
            moves = game.get_valid_moves_final(SEFID)
            
            if len(moves) == 0:
                print("Black Wins! You have no moves.")
                break

            # نمایش حرکات مجاز به کاربر
            print("Valid moves:")
            for i, m in enumerate(moves):
                print(f"{i}: {m[0]} -> {m[1]} (eats: {len(m[2])})")
            
            try:
                choice = int(input("Enter move number: "))
                if 0 <= choice < len(moves):
                    game.execute_move(moves[choice])
                    game.nobat = SIAH
                else:
                    print("Invalid number. Try again.")
            except:
                print("Please enter a number.")
        
        print("-" * 30)
