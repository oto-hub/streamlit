import random
import streamlit as st

# 牌の種類を定義
suits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
winds = ["東", "南", "西", "北"]
dragons = ["白", "發", "中"]

# 役の定義
def is_pinghu(hand):
    """平和（ピンフ）: すべての順子と一対（刻子がない）"""
    pairs = 0
    sequences = 0
    for tile in hand:
        if tile[-1] in ['m', 'p', 's']:  # マンズ、ピンズ、ソーズ
            num = tile[:-1]
            if num in ['1', '9']:
                return False  # 1と9が含まれていたら平和にはならない
            sequences += 1  # 順子であればカウント
        elif tile in winds or tile in dragons:
            pairs += 1
    return pairs == 1 and sequences == 4  # 一対と順子だけで構成されていれば平和




def sort_hand(hand):
    """手牌を種類ごとにソート"""
    manzu = sorted([tile for tile in hand if tile[-1] == 'm'])  # 萬子
    pinzu = sorted([tile for tile in hand if tile[-1] == 'p'])  # 筒子
    souzu = sorted([tile for tile in hand if tile[-1] == 's'])  # 索子
    others = sorted([tile for tile in hand if tile[-1] not in ['m', 'p', 's']])  # 風牌やドラ牌

    return manzu + pinzu + souzu + others



def is_sanshoku(hand):
    """三色同順: 同じ数字で、異なる種類の順子"""
    hand = sorted(hand)
    for num in suits:
        m_sequence = [f"{x}{num}" for x in ["1", "2", "3"]]
        p_sequence = [f"{x}{num}" for x in ["4", "5", "6"]]
        s_sequence = [f"{x}{num}" for x in ["7", "8", "9"]]
        if all(t in hand for t in m_sequence + p_sequence + s_sequence):
            return True
    return False


def is_chiitoitsu(hand):
    """七対子（チートイツ）: 7つの対子がある"""
    tile_counts = {tile: hand.count(tile) for tile in hand}
    pair_count = sum(1 for count in tile_counts.values() if count == 2)
    return pair_count == 7  # 7つの対子があれば成立


def is_chinitsu(hand):
    """チンイツ（清一色）: 同一の種類（マンズ、ピンズ、ソーズ）のみで構成"""
    suits_in_hand = [tile[-1] for tile in hand if tile[-1] in ['m', 'p', 's']]  # マンズ、ピンズ、ソーズ
    return len(set(suits_in_hand)) == 1  # 同じ種類の牌だけで構成されていれば成立


def is_kokushimusou(hand):
    """国士無双: 13種類の風牌とドラ牌を1枚ずつ、さらに1枚の牌を加える"""
    required_tiles = ["東", "南", "西", "北", "白", "發", "中"]
    tile_counts = {tile: hand.count(tile) for tile in hand}
    
    # 13種類の風牌とドラ牌がすべて1枚ずつ揃っている
    if all(tile_counts.get(tile, 0) == 1 for tile in required_tiles):
        # 残りの1枚はどの牌でもOK（追加の1枚が必要）
        for tile in hand:
            if tile_counts.get(tile, 0) == 1:
                return True
    return False


def is_suanko(hand):
    """四暗刻: 4つの暗刻が揃っている"""
    tile_counts = {tile: hand.count(tile) for tile in hand}
    return sum(1 for count in tile_counts.values() if count == 3) == 4  # 4つの暗刻があれば成立


def is_shosangen(hand):
    """小三元: 白發中のうち2つが刻子、残り1つが対子"""
    required_tiles = ["白", "發", "中"]
    tile_counts = {tile: hand.count(tile) for tile in hand}
    
    # 2つの刻子と1つの対子が揃っているかどうかをチェック
    pairs = sum(1 for tile in required_tiles if tile_counts.get(tile, 0) == 2)
    pongs = sum(1 for tile in required_tiles if tile_counts.get(tile, 0) == 3)
    
    return pairs == 1 and pongs == 2  # 2つの刻子と1つの対子


def calculate_score(hand):
    """点数計算: 役に応じて点数を決定"""
    score = 0
    completed_hands = []  # 完成した役を格納するリスト
    
    if is_pinghu(hand):
        score += 20  # 平和の点数
        completed_hands.append("平和")

    if is_sanshoku(hand):
        score += 40  # 三色同順の点数
        completed_hands.append("三色同順")
    if is_chiitoitsu(hand):
        score += 50  # 七対子の点数
        completed_hands.append("七対子")
    if is_chinitsu(hand):
        score += 60  # 清一色の点数
        completed_hands.append("清一色")
    if is_kokushimusou(hand):
        score += 100  # 国士無双の点数
        completed_hands.append("国士無双")
    if is_suanko(hand):
        score += 80  # 四暗刻の点数
        completed_hands.append("四暗刻")
    if is_shosangen(hand):
        score += 70  # 小三元の点数
        completed_hands.append("小三元")
    
    return score, completed_hands


# 牌を組み合わせてデッキを作る
def generate_deck():
    deck = []
    # 数字牌（1-9のマンズ、ピンズ、ソーズ）
    for suit in ['m', 'p', 's']:  # m: マンズ, p: ピンズ, s: ソーズ
        for num in suits:
            for _ in range(4):  # 各牌は4枚
                deck.append(f"{num}{suit}")
    
    # 風牌（東南西北）
    for wind in winds:
        for _ in range(4):
            deck.append(wind)
    
    # ドラ牌（白、發、中）
    for dragon in dragons:
        for _ in range(4):
            deck.append(dragon)
    
    random.shuffle(deck)
    return deck

# プレイヤーに手牌を配る
def deal_hand(deck):
    hand = [deck.pop() for _ in range(13)]  # 初期手牌13枚
    return hand

# 牌を引く
def draw_tile(deck):
    return deck.pop()

# 手牌を昇順にソートする
def sort_hand(hand):
    """手牌を種類ごとにソート"""
    # 萬子、筒子、索子、その他に分けてソート
    manzu = sorted([tile for tile in hand if tile[-1] == 'm'])  # 萬子
    pinzu = sorted([tile for tile in hand if tile[-1] == 'p'])  # 筒子
    souzu = sorted([tile for tile in hand if tile[-1] == 's'])  # 索子
    others = sorted([tile for tile in hand if tile[-1] not in ['m', 'p', 's']])  # 風牌やドラ牌

    # 萬子、筒子、索子、その他の順で統合
    return manzu + pinzu + souzu + others


def main():
    st.title("🀄 麻雀ゲーム - 役判定と点数計算")

    if "deck" not in st.session_state:
        st.session_state.deck = generate_deck()  # 新しいデッキを生成

    if "player_hand" not in st.session_state:
        st.session_state.player_hand = deal_hand(st.session_state.deck)  # プレイヤーに手牌を配る

    if "ai_hand" not in st.session_state:
        st.session_state.ai_hand = deal_hand(st.session_state.deck)  # AIに手牌を配る

    # ゲーム開始ボタン
    if st.button("ゲーム開始"):
        st.session_state.deck = generate_deck()
        st.session_state.player_hand = deal_hand(st.session_state.deck)
        st.session_state.ai_hand = deal_hand(st.session_state.deck)
        st.session_state.game_result = ""

    # プレイヤーの手牌をソートして表示
    sorted_player_hand = sort_hand(st.session_state.player_hand)
    st.subheader("あなたの手牌")
    st.write(sorted_player_hand)

    # AIの手牌をソートして表示
    sorted_ai_hand = sort_hand(st.session_state.ai_hand)
    st.subheader("AIの手牌")
    st.write(sorted_ai_hand)

    # 点数計算
    player_score, player_completed_hands = calculate_score(sorted_player_hand)
    ai_score, ai_completed_hands = calculate_score(sorted_ai_hand)

    st.write(f"あなたの点数: {player_score}")
    st.write(f"AIの点数: {ai_score}")

    # プレイヤーの完成した役を表示
    st.subheader("あなたの完成した役")
    if player_completed_hands:
        st.write(", ".join(player_completed_hands))
    else:
        st.write("なし")

    # AIの完成した役を表示
    st.subheader("AIの完成した役")
    if ai_completed_hands:
        st.write(", ".join(ai_completed_hands))
    else:
        st.write("なし")

if __name__ == "__main__":
    main()
