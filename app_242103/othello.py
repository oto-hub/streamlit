import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import streamlit as st

# 定数定義
EMPTY = 0
BLACK = 1
WHITE = 2

def create_board():
    """初期盤面を作成する"""
    board = np.zeros((8, 8), dtype=int)
    # 初期配置
    board[3:5, 3:5] = np.array([[WHITE, BLACK], [BLACK, WHITE]])
    return board

def draw_board(board, filename=None):
    """盤面を描画する"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 背景を緑色に
    ax.set_facecolor('forestgreen')
    
    # グリッドを描画
    for i in range(9):
        ax.axhline(i, color='black', linewidth=1)
        ax.axvline(i, color='black', linewidth=1)
    
    # ラベルを設定
    ax.set_xticks(np.arange(8))
    ax.set_yticks(np.arange(8))
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7', '8'])
    
    # 石を描画
    for i in range(8):
        for j in range(8):
            if board[i, j] == BLACK:
                circle = plt.Circle((j + 0.5, 7.5 - i), 0.4, color='black')
                ax.add_patch(circle)
            elif board[i, j] == WHITE:
                circle = plt.Circle((j + 0.5, 7.5 - i), 0.4, color='white')
                ax.add_patch(circle)
    
    ax.set_aspect('equal')
    
    if filename:
        plt.savefig(filename)
    plt.close()

def convert_position(x, y):
    """座標を内部表現に変換する"""
    if not isinstance(x, str) or len(x) != 1:
        raise ValueError("x must be a single character")

    x = x.upper()
    if x not in "ABCDEFGH":
        raise ValueError("x must be between A and H")

    if not isinstance(y, int) or y < 1 or y > 8:
        raise ValueError("y must be between 1 and 8")

    return 8 - y, ord(x) - ord("A")

def is_valid_move(board, row, col, color):
    """指定位置に石を置けるかチェックする"""
    if board[row, col] != EMPTY:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    valid = False
    for dx, dy in directions:
        if check_direction(board, row, col, dx, dy, color):
            valid = True

    return valid

def check_direction(board, row, col, dx, dy, color):
    """特定の方向に石を裏返せるかチェックする"""
    opponent = WHITE if color == BLACK else BLACK
    x, y = row + dx, col + dy

    if not (0 <= x < 8 and 0 <= y < 8) or board[x, y] != opponent:
        return False

    while 0 <= x < 8 and 0 <= y < 8:
        if board[x, y] == EMPTY:
            return False
        if board[x, y] == color:
            return True
        x, y = x + dx, y + dy

    return False

def put_disc(x, y, color, board):
    """石を置く"""
    row, col = convert_position(x, y)

    if not is_valid_move(board, row, col, color):
        raise ValueError("Invalid move")

    new_board = board.copy()
    new_board[row, col] = color

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dx, dy in directions:
        if check_direction(board, row, col, dx, dy, color):
            x, y = row + dx, col + dy
            while board[x, y] != color:
                new_board[x, y] = color
                x, y = x + dx, y + dy

    return new_board

def judge(board):
    """勝敗を判定する"""
    black_count = np.sum(board == BLACK)
    white_count = np.sum(board == WHITE)
    empty_count = np.sum(board == EMPTY)

    if empty_count == 0:
        if black_count > white_count:
            return BLACK
        elif white_count > black_count:
            return WHITE
        else:
            return None

    # まだ空きマスがある場合
    return None

def get_valid_moves(board, color):
    """有効な手を取得する"""
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move(board, i, j, color):
                # 内部座標を変換して追加
                col = chr(j + ord('A'))
                row = 8 - i
                valid_moves.append(f"{col}{row}")
    return valid_moves

def evaluate_board(board, color):
    """盤面の評価関数"""
    black_count = np.sum(board == BLACK)
    white_count = np.sum(board == WHITE)
    
    if color == BLACK:
        return black_count - white_count
    else:
        return white_count - black_count

def minimax(board, depth, is_maximizing, color, alpha=-float('inf'), beta=float('inf')):
    """ミニマックス法を使って最適な手を選ぶ"""
    
    # opponent変数をここで定義します
    opponent = WHITE if color == BLACK else BLACK

    # 勝敗判定
    result = judge(board)
    if result == color:
        return 1000  # AIが勝った
    elif result == opponent:
        return -1000  # AIが負けた
    elif result is None and depth == 0:
        return evaluate_board(board, color)  # 評価関数による評価
    
    # 最大化プレイヤー（AI）のターン
    if is_maximizing:
        max_eval = -float('inf')
        for move in get_valid_moves(board, color):
            x, y = move[0], int(move[1])  # 例: 'C5' -> 'C', 5
            new_board = put_disc(x, y, color, board)
            eval_score = minimax(new_board, depth-1, False, color, alpha, beta)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    
    # 最小化プレイヤー（相手）のターン
    else:
        min_eval = float('inf')
        for move in get_valid_moves(board, opponent):
            x, y = move[0], int(move[1])  # 例: 'C5' -> 'C', 5
            new_board = put_disc(x, y, opponent, board)
            eval_score = minimax(new_board, depth-1, True, color, alpha, beta)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def ai_move(board, color, depth=4):
    """AIの手を選ぶ"""
    best_move = None
    best_value = -float('inf')

    for move in get_valid_moves(board, color):
        x, y = move[0], int(move[1])  # 'C5' -> 'C', 5
        new_board = put_disc(x, y, color, board)
        move_value = minimax(new_board, depth, False, color)
        
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

def save_board_image(board):
    """盤面画像を一時ファイルとして保存し、そのパスを返す"""
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'othello_board.png')
    draw_board(board, temp_path)
    return temp_path

def main():
    st.title("Othello vs AI")
    
    # セッションステートの初期化
    if 'board' not in st.session_state:
        st.session_state.board = create_board()
        st.session_state.game_over = False
        st.session_state.turn = BLACK  # 最初は黒のターン
    
    # 盤面の画像を保存して表示
    board_path = save_board_image(st.session_state.board)
    st.image(board_path)
    
    # 現在の石の数を表示
    black_count = np.sum(st.session_state.board == BLACK)
    white_count = np.sum(st.session_state.board == WHITE)
    st.write(f"Black (You): {black_count} stones")
    st.write(f"White (AI): {white_count} stones")
    
    # プレイヤーの入力を取得
    if st.session_state.turn == BLACK and not st.session_state.game_over:
        move = st.text_input("Enter your move (e.g., A3):")
        if move:
            try:
                row, col = convert_position(*move)
                new_board = put_disc(row, col, BLACK, st.session_state.board)
                st.session_state.board = new_board
                st.session_state.turn = WHITE  # AIのターン
            except ValueError:
                st.error("Invalid move! Please enter a valid position.")
    
    # AIのターン
    if st.session_state.turn == WHITE and not st.session_state.game_over:
        ai_move_position = ai_move(st.session_state.board, WHITE)
        if ai_move_position:
            row, col = convert_position(*ai_move_position)
            new_board = put_disc(row, col, WHITE, st.session_state.board)
            st.session_state.board = new_board
            st.session_state.turn = BLACK  # プレイヤーのターン
    
    # ゲームの勝敗判定
    result = judge(st.session_state.board)
    if result is not None:
        st.session_state.game_over = True
        if result == BLACK:
            st.write("You win!")
        elif result == WHITE:
            st.write("AI wins!")
        else:
            st.write("It's a draw!")



