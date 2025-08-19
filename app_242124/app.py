import streamlit as st #Streamlitライブラリをインポートします。

st.markdown("""
    <style>
    .subtitle {
        color: #43A047; /* サブタイトルの文字色を緑に変更 */
        text-align: center;
        
    }
    
    .result {
        color: #8E24AA; /* 結果の文字色を紫に変更 */
        text-align: center;
        
    }
    </style>
""", unsafe_allow_html=True)

#MBTI診断のための質問リストを定義します。
#各質問には対応する性格タイプ(E, I, S, N, T, F, J, P)が設定されています。
questions = [
    {"question": "初対面の人と話すのって、けっこう楽しいと思う？", "type": "E"},
    {"question": "休みの日は、一人でのんびりする時間がほしい？", "type": "I"},
    {"question": "友達といると元気が出るタイプ？", "type": "E"},
    {"question": "自分の考えをまとめてから話すことが多い？", "type": "I"},
    {"question": "にぎやかな場所にいると元気が出る", "type": "E"},

    {"question": "料理をするとき、レシピ通りに作る方が安心する？", "type": "S"},
    {"question": "「これやってみたら面白そう！」って直感で行動しちゃうことがある？", "type": "N"},
    {"question": "実際に見たり触れたりしたものを信じやすい？", "type": "S"},
    {"question": "「これって他のことにも使えそう！」とアイデアがどんどん浮かぶ方？", "type": "N"},
    {"question": "詳細や細かいことをチェックするのが得意？", "type": "S"},

    {"question": "困っている人がいても、まずはどう解決するか考えちゃう？", "type": "T"},
    {"question": "悩んでいる友達がいたら、とりあえず「大丈夫？」って声をかける？", "type": "F"},
    {"question": "何か決めるとき、感情よりも事実やデータが大事だと思う？", "type": "T"},
    {"question": "人に頼られると、「助けたい！」って思う？", "type": "F"},
    {"question": "他人の意見を聞くとき、「それって本当に正しい？」って考えちゃう？", "type": "T"},

    {"question": "旅行に行く前に、スケジュールをきっちり決めたい方？", "type": "J"},
    {"question": "予定が決まってなくても、その場のノリで何とかなるって思う？", "type": "P"},
    {"question": "宿題や仕事は、早めに終わらせたくなる？", "type": "J"},
    {"question": "締め切りギリギリでも「まあ、何とかなるでしょ！」って思う？", "type": "P"},
    {"question": "スケジュール帳やアプリで予定を管理するのが好き？", "type": "J"},
]

# MBTIのタイプ説明
#各MBTIタイプの説明を辞書形式で定義します。
mbti_descriptions = {
    "ISTJ": "責任感が強く、現実的で計画性があるタイプ。物事をコツコツと進めるのが得意で、約束やルールを守る。データ分析やプロセス改善など、効率的な仕事をこなします。",
    "ISFJ": "思いやりがあり、献身的なタイプ。他者に共感し、周囲の調和を大切にします。細やかな配慮が得意で、サポート業務やサービス提供に向いています。",
    "INFJ": "直感的で理想主義的なタイプ。深い洞察力を持ち、他者の感情やニーズを理解します。カウンセリングや執筆活動などに適性があります。",
    "INTJ": "戦略的で独立心が強いタイプ。論理的な視点で長期的な計画を立て、効率を重視します。問題解決やプロジェクト管理に強みを発揮します。",
    "ISTP": "柔軟で現実的な問題解決型。分析力に優れ、実用的な解決策を見つけるのが得意です。修理やトラブルシューティングなどで活躍します。",
    "ISFP": "温和で感性豊かなアーティストタイプ。美的センスがあり、創造的な活動を好みます。他者を受け入れながら独自の道を進みます。",
    "INFP": "夢想的で価値観を重視するタイプ。自分の信念を大切にし、理想や夢を追求します。創作活動や教育分野に向いています。",
    "INTP": "論理的で分析力が高いタイプ。知的好奇心が強く、理論や概念に興味を持ちます。プログラミングや抽象的な問題解決に優れています。",
    "ESTP": "行動力があり、冒険を好むタイプ。臨機応変に対応し、行動することで成果を出します。営業やイベント企画に適性があります。",
    "ESFP": "社交的で楽しさを重視するタイプ。周囲を楽しませるのが得意で、今この瞬間を大切にします。接客業やエンターテインメント業界で活躍します。",
    "ENFP": "情熱的で創造的な自由人タイプ。豊富なアイデアを持ち、型にはまらない発想を得意とします。広報や教育、クリエイティブな仕事に向いています。",
    "ENTP": "機知に富み、新しいアイデアを生み出すタイプ。柔軟な思考で問題解決を楽しみます。起業や戦略立案で力を発揮します。",
    "ESTJ": "組織的でリーダーシップに優れるタイプ。規律を重んじ、効率的に物事を進めます。組織管理やプロジェクト運営が得意です。",
    "ESFJ": "人をサポートし、調和を重視するタイプ。他者に寄り添い、グループの調和を保つのが得意です。教育やサービス業で活躍します。",
    "ENFJ": "カリスマ性があり、他人を導くタイプ。他者を動機づけ、可能性を引き出すのが得意です。コーチングや組織運営に向いています。",
    "ENTJ": "目的志向でリーダーシップがあるタイプ。効率的な戦略を立て、目標達成に向けて行動します。経営や大規模プロジェクト管理で活躍します。",
}

# MBTIタイプに対応する画像のパス（画像を事前に用意してください）
# 各MBTIタイプに対応する画像ファイルのパスを辞書で指定します。
mbti_images = {
    "ISTJ": "app_242124/ISTJ.png",
    "ISFJ": "app_242124/ISFJ.png",
    "INFJ": "app_242124/INFJ.png",
    "INTJ": "app_242124/INTJ.png",
    "ISTP": "app_242124/ISTP.png",
    "ISFP": "app_242124/SFP.png",
    "INFP": "app_242124/INFP.png",
    "INTP": "app_242124/INTP.png",
    "ESTP": "app_242124/ESTP.png",
    "ESFP": "app_242124/ESFP.png",
    "ENFP": "app_242124/ENFP.png",
    "ENTP": "app_242124/ENTP.png",
    "ESTJ": "app_242124/ESTJ.png",
    "ESFJ": "app_242124/ESFJ.png",
    "ENFJ": "app_242124/ENFJ.png",
    "ENTJ": "app_242124/ENTJ.png",
}

def main():#アプリのメイン処理を実行する
    # ここから記述
    st.markdown('<h1 class="title">🌟 かんたん！MBTI診断！ 🌟</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">楽しく質問に答えて、あなたの性格をチェックしてみよう！</p>', unsafe_allow_html=True)
    st.write('直感で答えてくださいね！')

    # スコアを記録する辞書
    # 各性格タイプのスコアを記録する辞書を初期化します。
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    # 質問をループで表示
    # 質問を1つずつ表示し、「はい」と答えた場合に対応するスコアを増やします。
    for question in questions:
        answer = st.radio(f"💡 {question['question']}", ["はい", "いいえ"], key=question["question"])
        if answer == "はい":
            scores[question["type"]] += 1

    result = None

    # 診断ボタン
    if st.button("診断する 🚀"):
        # タイプを判定
        result = (
            ("E" if scores["E"] > scores["I"] else "I") +
            ("S" if scores["S"] > scores["N"] else "N") +
            ("T" if scores["T"] > scores["F"] else "F") +
            ("J" if scores["J"] > scores["P"] else "P")
        )

        # 結果を表示
        st.markdown(f'<p class="result">🎉 あなたのMBTIタイプは【{result}】です！ 🎉</p>', unsafe_allow_html=True)
        st.write(f"特徴: {mbti_descriptions.get(result, '説明が見つかりませんでした。')}")

        # 結果に対応する画像を表示
        if result in mbti_images:
            st.image(
                mbti_images[result], 
                caption=f"あなたのタイプ: {result}", 
                use_container_width=False,  # ページ幅に合わせない
                width=300  # 画像幅を500pxに指定
            )

# アプリを起動
if __name__ == "__main__":
    main()