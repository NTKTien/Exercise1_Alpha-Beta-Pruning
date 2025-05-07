import sys

# Kiem tra xem player co phai nguoi thang khong
def is_winner(board, player):
    # Kiem tra hang ngang
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Kiem tra hang doc
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Kiem tra duong cheo
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Dem so nuoc di cua player tren bang
def count_in_board(board, player):
    count = sum(row.count(player) for row in board)
    return count

# Kiem tra tinh hop le cua bang nhap vao
def is_valid(board):
    # Tinh so nuoc di cua X va O
    x_count = count_in_board(board, 'X')
    o_count = count_in_board(board, 'O')
    # Neu X thang ma O = X hoac O thang ma X > O thi khong hop le
    if (is_winner(board, 'X') and o_count == x_count) or (is_winner(board, 'O') and x_count > o_count):
        return False
    # Neu X=O hoac X=O+1 thi hop le
    return x_count == o_count or x_count == o_count + 1

# Kiem tra xem X co phai luot di khong
def is_X_turn(board):
    x_count = count_in_board(board, 'X')
    o_count = count_in_board(board, 'O')
    return x_count == o_count

# Kiem tra bang da day chua
def is_full(board):
    # Neu tat ca cac o da duoc danh dau thi board da day
    return all(cell in ['X', 'O'] for row in board for cell in row)

def is_game_over(board):
    # Kiem tra xem co nguoi thang khong
    if is_winner(board, 'X') or is_winner(board, 'O'):
        return True
    # Kiem tra xem board da day chua
    if is_full(board):
        return True
    return False

# Tinh diem trang thai cuoi cho board: X thang +1, O thua -1, hoa 0, chua thang phan bai None
def validate(board):
    if is_winner(board, 'X'):
        return 1
    elif is_winner(board, 'O'):
        return -1
    # Khong co ai thang ma bang da day thi hoa
    elif is_full(board):
            return 0
    else:
        return None

# Trien khai thuat toan minimax ket hop alpha beta pruning de tim nuoc di tot nhat cho player
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    score = validate(board)
    # Thang voi it nuoc di duoc uu tien, thua voi it nuoc di duoc uu tien
    if score is not None:
        return score/depth

    # Toi da hoa so diem cho nguoi choi X
    if maximizing_player:
        max_eval = float('-inf')
        # Duyet tat ca cac o trong bang
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    board[i][j] = 'X'
                    # De quy danh gia nuoc di
                    eval = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                    # Hoan tac nuoc di
                    board[i][j] = '.'
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    # Tia nhanh
                    if alpha >= beta:
                        break
        return max_eval
    # Toi thieu hoa so diem cho nguoi choi O
    else:
        min_eval = float('inf')
        # Duyet tat ca cac o trong bang
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    board[i][j] = 'O'
                    # De quy danh gia nuoc di
                    eval = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                    # Hoan tac nuoc di
                    board[i][j] = '.'
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    # Tia nhanh
                    if alpha >= beta:
                        break
        return min_eval

def find_best_move(board):
    # Nuoc di tot nhanh nhat cho nguoi choi X
    best_move = None
    # Gia tri cho nuoc di tot nhat
    best_value = float('-inf')
    # Duyet tat ca cac vi tri trong trong bang
    for i in range(3):
        for j in range(3):
            if board[i][j] == '.':
                board[i][j] = 'X'
                # Danh gia nuoc di cho nguoi choi X
                move_value = minimax_alpha_beta(board, 0, float('-inf'), float('inf'), False)
                # Hoan tac nuoc di
                board[i][j] = '.'
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
    return best_move

def main():
    # Nhap du lieu tu ban phim
    board = [list(input().strip()) for _ in range(3)]
    
    # Kiem tra hop le: Neu bang chua day hoac chua ket thuc game ma khong phai luot di cua X thi cung khong hop le
    if not is_valid(board) or (not is_game_over(board) and not is_X_turn(board)):
        print("Invalid board")
        return
    
    # Kiem tra tinh trang van game
    if is_game_over(board):
        print("Game over")
        return
    
    # Tim nuoc di tot nhat cho player X
    best_possible_move = find_best_move(board)
    if best_possible_move:
        print(f"({best_possible_move[0]}, {best_possible_move[1]})")
    else:
        print("No valid moves available!")
        
if __name__ == "__main__":
    main()