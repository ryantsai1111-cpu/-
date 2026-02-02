import streamlit as st
import pandas as pd
import time
import random

# --- 1. 初始化遊戲狀態 (Session State) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "Lv.0 五十音道場"
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# 設定頁面
st.set_page_config(page_title="日本語大冒險", page_icon="🎌", layout="centered")

# --- 2. 側邊欄：玩家狀態 ---
st.sidebar.title("👤 冒險者狀態")
st.sidebar.write(f"**等級**: {st.session_state.level}")
# 經驗值條
xp_progress = min(st.session_state.xp % 100 / 100, 1.0)
st.sidebar.progress(xp_progress, text=f"XP: {st.session_state.xp}/100 (下一級)")
st.sidebar.metric("🔥 連續答對", f"{st.session_state.streak} 題")

st.sidebar.divider()
st.sidebar.markdown("### 🗺️ 冒險地圖")
stage_selection = st.sidebar.radio(
    "選擇關卡",
    ["Lv.0 五十音道場", "Lv.1 新手村糾錯", "Lv.2 動詞變形森林", "Lv.3 JLPT 試煉場"]
)

# --- 共用函數：檢查答案 ---
def check_answer(user_answer, correct_answer, explanation):
    if user_answer == correct_answer:
        st.session_state.xp += 10
        st.session_state.streak += 1
        st.success(f"✅ 正確！經驗值 +10")
        st.balloons() # Duolingo 風格的獎勵動畫
        
        # 升級機制
        if st.session_state.xp > 0 and st.session_state.xp % 100 == 0:
            st.session_state.level += 1
            st.toast(f"🎉 恭喜升級！現在是 Lv.{st.session_state.level}！")
            
    else:
        st.session_state.streak = 0
        st.error(f"❌ 哎呀！正確答案是：{correct_answer}")
    
    with st.expander("📖 查看詳解", expanded=True):
        st.info(explanation)
    
    time.sleep(1) # 稍作暫停讓使用者看結果

# --- 3. 關卡內容設計 ---

# === Lv.0 五十音道場 (資料來源：維基百科) ===
if stage_selection == "Lv.0 五十音道場":
    st.header("Lv.0 五十音道場")
    st.markdown("從零開始！這是日語的地基。根據資料，平假名源自漢字草書 [cite: 246]。")
    
    tab1, tab2 = st.tabs(["📚 學習模式", "⚔️ 挑戰模式"])
    
    with tab1:
        st.subheader("平假名記憶卡")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("あ (a)", help="安 - 記憶法：阿")
            st.button("い (i)", help="以 - 記憶法：椅")
        with col2:
            st.button("う (u)", help="宇 - 記憶法：屋")
            st.button("え (e)", help="衣 - 記憶法：埃")
        with col3:
            st.button("お (o)", help="於 - 記憶法：喔")
    
    with tab2:
        st.subheader("快速測驗")
        # 簡單的題庫
        questions = [
            {"q": "「あ」的發音是？", "options": ["a", "i", "u", "e"], "ans": "a", "exp": "「あ」是五十音的第一個字，讀作 a。"},
            {"q": "哪一個是「u」的平假名？", "options": ["あ", "う", "お", "え"], "ans": "う", "exp": "「う」源自漢字「宇」[cite: 256]。"},
            {"q": "「K」行加上「a」變什麼？", "options": ["ka (か)", "sa (さ)", "ta (た)"], "ans": "ka (か)", "exp": "K行：ka, ki, ku, ke, ko [cite: 153]。"}
        ]
        
        # 隨機選題 (或是固定順序)
        q = questions[st.session_state.xp % len(questions)] # 根據 XP 輪播題目
        
        st.markdown(f"**問題：{q['q']}**")
        ans = st.radio("請選擇：", q['options'], key=f"q_lv0_{st.session_state.xp}")
        
        if st.button("送出答案", key="btn_lv0"):
            check_answer(ans, q['ans'], q['exp'])

# === Lv.1 新手村糾錯 (資料來源：常見錯誤 Reddit) ===
elif stage_selection == "Lv.1 新手村糾錯":
    st.header("Lv.1 新手村糾錯")
    st.markdown("這裡有很多新手常犯的陷阱。把錯誤修正過來，就能變強！")
    
    st.info("💡 提示：形容詞接名詞時，不需要加「の」 。")
    
    questions = [
        {
            "q": "想稱讚「可愛的女生」，哪句是對的？",
            "options": ["かわいいの女性", "かわいい女性"],
            "ans": "かわいい女性",
            "exp": "形容詞可以直接修飾名詞，不需要加「の」。例如：赤い服 (紅色的衣服) 。"
        },
        {
            "q": "想說「很有趣（過去式）」，哪句是對的？",
            "options": ["楽しいでした", "楽しかったです"],
            "ans": "楽しかったです",
            "exp": "去 i 形容詞的過去式是將詞尾的「い」改成「かった」+ です 。"
        },
        {
            "q": "如何說「大家」？",
            "options": ["みんなさん", "みなさん"],
            "ans": "みなさん",
            "exp": "雖然漢字寫「皆さん」，但讀音是「みなさん (Mina-san)」而不是 Minna-san 。"
        }
    ]
    
    q_index = st.session_state.xp % len(questions)
    q = questions[q_index]
    
    st.markdown(f"### 挑戰 {q_index + 1}")
    st.write(q['q'])
    ans = st.radio("你的選擇是？", q['options'], key="q_lv1")
    
    if st.button("送出答案", key="btn_lv1"):
        check_answer(ans, q['ans'], q['exp'])

# === Lv.2 動詞變形森林 (資料來源：巨匠日語) ===
elif stage_selection == "Lv.2 動詞變形森林":
    st.header("Lv.2 動詞變形森林")
    st.markdown("動詞變化是 N5 的大魔王！只要掌握規則，就能輕鬆過關。")
    
    st.markdown("""
    **📜 魔法卷軸 (規則)**：
    1. **第一類 (五段)**：把語尾的 u 段音改成 i 段音 + ます [cite: 262]。
    2. **第二類 (一段)**：把語尾的 る 去掉 + ます [cite: 262]。
    3. **第三類 (不規則)**：死記！来る (kuru) -> 来ます (kimasu) 。
    """)
    
    # 互動式練習
    verb_q = [
        {"q": "「書く (kaku)」的禮貌形 (Masu形) 是？", "options": ["書きます (kakimasu)", "書くます (kakumasu)"], "ans": "書きます (kakimasu)", "exp": "這是第一類動詞。ku -> ki + masu [cite: 262]。"},
        {"q": "「食べる (taberu)」的禮貌形 (Masu形) 是？", "options": ["食べります (taberimasu)", "食べます (tabemasu)"], "ans": "食べます (tabemasu)", "exp": "這是第二類動詞。直接去掉 る + ます [cite: 262]。"},
        {"q": "「する (suru)」的禮貌形 (Masu形) 是？", "options": ["します (shimasu)", "すります (surimasu)"], "ans": "します (shimasu)", "exp": "這是第三類動詞，屬於不規則變化 。"}
    ]
    
    # 讓使用者選擇要練習的動詞類型
    type_filter = st.selectbox("選擇修煉對象", ["全部混合", "第一類 (五段)", "第二類 (一段)"])
    
    # 這裡簡化邏輯，實際可根據 filter 過濾題目
    q = verb_q[st.session_state.xp % len(verb_q)]
    
    st.markdown("---")
    st.subheader(f"⚔️ 遭遇魔物：{q['q']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(q['options'][0]):
            check_answer(q['options'][0], q['ans'], q['exp'])
    with col2:
        if st.button(q['options'][1]):
            check_answer(q['options'][1], q['ans'], q['exp'])

# === Lv.3 JLPT 試煉場 (資料來源：JLPT攻略) ===
elif stage_selection == "Lv.3 JLPT 試煉場":
    st.header("Lv.3 JLPT 試煉場")
    st.markdown("你準備好參加檢定了嗎？這裡模擬真實考試的知識點。")
    
    st.info("JLPT N5 要求：能理解基本的詞彙、句型與片語，例如自我介紹 [cite: 233]。")
    
    st.write("📝 **模擬試題**")
    st.markdown("**題目：田中さんは　毎日　新聞を　_____。**")
    
    options = ["読みます (讀)", "見ます (看)", "聞きます (聽)"]
    ans = st.radio("請填入正確動詞：", options)
    
    if st.button("提交試卷"):
        if ans == "読みます (讀)":
            st.session_state.xp += 20
            st.success("⭕ 正確！看報紙在日文中習慣用「読む (讀)」。")
            st.balloons()
        else:
            st.error("❌ 錯誤。雖然眼睛看，但在日文看報紙是用「讀」。")

st.divider()
st.caption("Designed for Japanese Learners | Source: User Uploaded Documents")
