import math
 
class Colors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'
 
class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.player = Colors.RED + 'X' + Colors.ENDC  # Red 'X'
        self.ai = Colors.BLUE + 'O' + Colors.ENDC    # Blue 'O'
 
    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('  ' + '   '.join(str(i) for i in range(self.cols)))
 
    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[0][col] == ' '
 
    def get_next_open_row(self, col):
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == ' ':
                return r
        return None
 
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
 
    def winning_move(self, piece):
        for c in range(self.cols - 3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and \
                   self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and \
                   self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
        for c in range(self.cols - 3):
            for r in range(self.rows - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and \
                   self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
        for c in range(self.cols - 3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and \
                   self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
 
        return False
 
    def is_terminal_node(self):
        return self.winning_move(self.player) or self.winning_move(self.ai) or \
               all(cell != ' ' for row in self.board for cell in row)
 
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.player if piece == self.ai else self.ai
 
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(' ') == 2:
            score += 2
 
        if window.count(opp_piece) == 3 and window.count(' ') == 1:
            score -= 4
 
        return score
 
    def score_position(self, piece):
        score = 0
        center_array = [self.board[r][self.cols // 2] for r in range(self.rows)]
        center_count = center_array.count(piece)
        score += center_count * 3
 
        for r in range(self.rows):
            row_array = [self.board[r][c] for c in range(self.cols)]
            for c in range(self.cols - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)
 
        for c in range(self.cols):
            col_array = [self.board[r][c] for r in range(self.rows)]
            for r in range(self.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)
 
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
 
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                window = [self.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
 
        return score
 
    def minimax(self, depth, maximizing_player):
        terminal = self.is_terminal_node()
        if depth == 0 or terminal:
            if terminal:
                if self.winning_move(self.ai):
                    return (None, 100000000000000)
                elif self.winning_move(self.player):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(self.ai))
 
        if maximizing_player:
            value = -math.inf
            column = None
            for col in range(self.cols):
                if self.is_valid_move(col):
                    row = self.get_next_open_row(col)
                    b_copy = [row[:] for row in self.board]
                    self.drop_piece(row, col, self.ai)
                    new_score = self.minimax(depth - 1, False)[1]
                    self.board = b_copy
                    if new_score > value:
                        value = new_score
                        column = col
            return column, value
 
        else:
            value = math.inf
            column = None
            for col in range(self.cols):
                if self.is_valid_move(col):
                    row = self.get_next_open_row(col)
                    b_copy = [row[:] for row in self.board]
                    self.drop_piece(row, col, self.player)
                    new_score = self.minimax(depth - 1, True)[1]
                    self.board = b_copy
                    if new_score < value:
                        value = new_score
                        column = col
            return column, value
 
    def get_ai_move(self):
        col, minimax_score = self.minimax(5, True)
        return col
 
    def play_game(self):
        game_over = False
        self.print_board()
 
        first_player = input("Who should play first? (player/ai): ").strip().lower()
        player_turn = first_player == "player"
 
        difficulty = input("Choose difficulty level (Easy, Medium, Hard): ").strip().lower()
        if difficulty == "Easy":
            self.depth = 2
        elif difficulty == "Medium":
            self.depth = 4
        else:
            self.depth = 6
 
        while not game_over:
            if player_turn:
                try:
                    col = int(input(f"Player ({self.player}), choose a column (0-{self.cols - 1}): "))
                    if self.is_valid_move(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, self.player)
                        if self.winning_move(self.player):
                            self.print_board()
                            print("Player wins!")
                            game_over = True
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                col = self.get_ai_move()
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, self.ai)
                if self.winning_move(self.ai):
                    self.print_board()
                    print("AI wins!")
                    game_over = True
            self.print_board()
            player_turn = not player_turn
 
if __name__ == "__main__":
    game = ConnectFour()
    game.play_game()
