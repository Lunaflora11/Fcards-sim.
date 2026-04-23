import streamlit as st
import random
import time

st.set_page_config(page_title="محاكي البطاقات التفاعلي", layout="wide")

st.title("🃏 نظام محاكاة سحب البطاقات وتحديث الاحتمالات")

# 1. إعداد النظام (Session State)
if 'deck' not in st.session_state:
    suits = ['♥ القلوب', '♠ السباتي', '♦ الديمون', '♣ الشيريا']
    st.session_state.deck = [suit for suit in suits for _ in range(13)]
    st.session_state.history = []  # سجل السحب

total = len(st.session_state.deck)
counts = {s: st.session_state.deck.count(s) for s in ['♥ القلوب', '♠ السباتي', '♦ الديمون', '♣ الشيريا']}

# 2. عرض الاحتمالات بشكل مرئي
st.subheader("📊 تحديث الاحتمالات الفوري")
cols = st.columns(4)
for i, (suit, count) in enumerate(counts.items()):
    prob = (count / total * 100) if total > 0 else 0
    cols[i].metric(label=suit, value=f"{prob:.1f}%")
    cols[i].progress(prob / 100)

st.divider()

# 3. منطقة المحاكاة والسحب
col1, col2 = st.columns([1, 2])

with col1:
    if st.button('🎴 اضغط للسحب', use_container_width=True):
        if total > 0:
            # محاكاة السحب (تأثير بصري بسيط)
            with st.spinner('جاري سحب بطاقة...'):
                time.sleep(0.5) 
                card = random.choice(st.session_state.deck)
                st.session_state.deck.remove(card)
                st.session_state.history.insert(0, card) # إضافة للسجل
                st.rerun()
        else:
            st.error("انتهت البطاقات!")

with col2:
    if st.session_state.history:
        st.markdown(f"### 🃏 البطاقة الحالية: **{st.session_state.history[0]}**")
    else:
        st.write("اضغط على الزر لبدء المحاكاة")

# 4. سجل السحب (History)
st.divider()
st.subheader("📜 سجل السحب السابق")
if st.session_state.history:
    # عرض السجل على شكل صف من البطاقات
    st.write(" | ".join(st.session_state.history))
else:
    st.write("السجل فارغ حالياً.")

# معلومات إضافية
st.sidebar.write(f"🔢 متبقي في المجموعة: {total}")
if st.sidebar.button("إعادة ضبط اللعبة"):
    del st.session_state.deck
    del st.session_state.history
    st.rerun()
