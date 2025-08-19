import numpy as np
import streamlit as st
import tempfile
import os
import app_242103.othello

def save_board_image(board):
    """盤面画像を一時ファイルとして保存し、そのパスを返す"""
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'othello_board.png')
    app_242103.othello.draw_board(board, temp_path)
    return temp_path

def evaluate_board(board, color):
    """盤面を評価する関数。AIのターンは`color`（白）として、できるだけ石を増やす戦略を取る"""
    opponent = app_242103.othello.WHITE if color == app_242103.othello.BLACK else app_242103.othello.BLACK
    score = 0
    
    # 石の数を評価
    score += np.sum(board == color) * 10
    score -= np.sum(board == opponent) * 10
    
    # 中心に近い石にボーナスを与える
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for (i, j) in center:
        if board[i, j] == color:
            score += 5
        elif board[i, j] == opponent:
            score -= 5

    return score

def minimax(board, depth, is_maximizing, color, alpha=-float('inf'), beta=float('inf')):
    """ミニマックス法を使って最適な手を選ぶ"""
    opponent = app_242103.othello.WHITE if color == app_242103.othello.BLACK else app_242103.othello.BLACK  # opponentを初期化
    # 勝敗判定
    result = app_242103.othello.judge(board)
    if result == color:
        return 1000  # AIが勝った
    elif result == opponent:
        return -1000  # AIが負けた
    elif result is None and depth == 0:
        return evaluate_board(board, color)  # 評価関数による評価
    
    # 最大化プレイヤー（AI）のターン
    if is_maximizing:
        max_eval = -float('inf')
        for move in app_242103.othello.get_valid_moves(board, color):
            x, y = move[0], int(move[1])  # 例: 'C5' -> 'C', 5
            new_board = app_242103.othello.put_disc(x, y, color, board)
            eval_score = minimax(new_board, depth-1, False, color, alpha, beta)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    
    # 最小化プレイヤー（相手）のターン
    else:
        min_eval = float('inf')
        for move in app_242103.othello.get_valid_moves(board, opponent):
            x, y = move[0], int(move[1])  # 例: 'C5' -> 'C', 5
            new_board = app_242103.othello.put_disc(x, y, opponent, board)
            eval_score = minimax(new_board, depth-1, True, color, alpha, beta)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def ai_move(board):
    """AIの最適手を選ぶ"""
    best_move = None
    best_score = -float('inf')
    for move in app_242103.othello.get_valid_moves(board, app_242103.othello.WHITE):
        x, y = move[0], int(move[1])  # 例: 'C5' -> 'C', 5
        new_board = app_242103.othello.put_disc(x, y, app_242103.othello.WHITE, board)
        move_score = minimax(new_board, 3, False, app_242103.othello.WHITE)  # 探索の深さを3に設定
        if move_score > best_score:
            best_score = move_score
            best_move = move
    
    # 最適な手を置く
    x, y = best_move[0], int(best_move[1])  # 例: 'C5' -> 'C', 5
    new_board = app_242103.othello.put_disc(x, y, app_242103.othello.WHITE, board)
    return new_board, True

def main():
    st.title("Othello vs AI")
    
    # セッションステートの初期化
    if 'board' not in st.session_state:
        st.session_state.board = app_242103.othello.create_board()
        st.session_state.game_over = False
        st.session_state.turn = app_242103.othello.BLACK  # 最初は黒のターン
    
    # 盤面の画像を保存して表示
    board_path = save_board_image(st.session_state.board)
    st.image(board_path)
    
    # 現在の石の数を表示
    black_count = np.sum(st.session_state.board == app_242103.othello.BLACK)
    white_count = np.sum(st.session_state.board == app_242103.othello.WHITE)
    st.write(f"Black (You): {black_count} stones")
    st.write(f"White (AI): {white_count} stones")
    
    # プレイヤーの手の入力
    if not st.session_state.game_over:
        valid_moves = app_242103.othello.get_valid_moves(st.session_state.board, st.session_state.turn)
        
        if valid_moves:
            col1, col2 = st.columns(2)
            with col1:
                x = st.selectbox("Column (A-H)", list("ABCDEFGH"))
            with col2:
                y = st.number_input("Row (1-8)", min_value=1, max_value=8)
            
            st.write("Valid moves:", ", ".join(valid_moves))
            
            if st.button("Place Stone"):
                try:
                    # プレイヤーの手を実行
                    st.session_state.board = app_242103.othello.put_disc(x, y, st.session_state.turn, st.session_state.board)
                    print(f"\nPlayer's move: {x}{y}")
                    
                    # 勝敗判定
                    result = app_242103.othello.judge(st.session_state.board)
                    if result is not None:
                        st.session_state.game_over = True
                    else:
                        # ターン交代
                        st.session_state.turn = app_242103.othello.WHITE if st.session_state.turn == app_242103.othello.BLACK else app_242103.othello.BLACK
                    
                    st.rerun()
                    
                except ValueError as e:
                    st.error(f"Invalid move: {e}")
                    print(f"Error: {e}")
        else:
            st.write("No valid moves available for you. Skipping turn...")
            # ターン交代
            st.session_state.turn = app_242103.othello.WHITE if st.session_state.turn == app_242103.othello.BLACK else app_242103.othello.BLACK
            st.rerun()

    # AIのターン
    if st.session_state.turn == app_242103.othello.WHITE and not st.session_state.game_over:
        new_board, moved = app_242103.othello.ai_move(st.session_state.board)
        if moved:
            st.session_state.board = new_board
            print(f"AI's move: {new_board}")
            # 勝敗判定
            result = app_242103.othello.judge(st.session_state.board)
            if result is not None:
                st.session_state.game_over = True
            else:
                # ターン交代
                st.session_state.turn = app_242103.othello.BLACK

            st.rerun()
    
    # ゲーム終了時の表示
    if st.session_state.game_over:
        result = app_242103.othello.judge(st.session_state.board)
        if result == app_242103.othello.BLACK:
            st.success("You win!")
        elif result == app_242103.othello.WHITE:
            st.error("AI wins!")
        else:
            st.info("Draw!")
        
        if st.button("New Game"):
            st.session_state.board = app_242103.othello.create_board()
            st.session_state.game_over = False
            st.session_state.turn = app_242103.othello.BLACK  # 最初は黒のターン
            st.rerun()

if __name__ == "__main__":
    main()

