import streamlit as st
import numpy as np

ROWS = 6
COLS = 8

st.set_page_config(page_title="사과게임 🍎", page_icon="🍎", layout="centered")
st.title("🍎 사과게임")
st.caption("숫자를 클릭해서 선택하세요. 합이 10이 되면 자동으로 제거됩니다!")

# 세션 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = np.random.randint(1, 10, size=(ROWS, COLS))
    st.session_state.score = 0
    st.session_state.selected = set()

# 사이드바
with st.sidebar:
    st.header("게임 정보")
    st.metric("점수", st.session_state.score)
    remaining = np.count_nonzero(st.session_state.board)
    st.metric("남은 사과", remaining)

    if st.button("🔄 새 게임", use_container_width=True):
        st.session_state.board = np.random.randint(1, 10, size=(ROWS, COLS))
        st.session_state.score = 0
        st.session_state.selected = set()
        st.rerun()

# 선택된 합 계산
selected_sum = 0
for r, c in st.session_state.selected:
    if st.session_state.board[r, c] > 0:
        selected_sum += st.session_state.board[r, c]

st.write(f"**현재 선택된 합:** `{selected_sum}`")

# 합이 10이면 자동 제거
if selected_sum == 10 and len(st.session_state.selected) > 0:
    count = 0
    for r, c in list(st.session_state.selected):
        if st.session_state.board[r, c] > 0:
            st.session_state.board[r, c] = 0
            count += 1
    st.session_state.score += count
    st.session_state.selected = set()
    st.success(f"+{count}점! 자동 제거되었습니다")
    st.rerun()

# 선택 취소 버튼
if st.button("선택 취소", use_container_width=True):
    st.session_state.selected = set()
    st.rerun()

st.divider()

# 보드 그리기
for r in range(ROWS):
    cols = st.columns(COLS)
    for c in range(COLS):
        value = st.session_state.board[r, c]
        key = f"btn_{r}_{c}"

        if value == 0:
            cols[c].button(" ", key=key, disabled=True)
        else:
            is_selected = (r, c) in st.session_state.selected

            if is_selected:
                label = f"✅\n🍎\n**{value}**"
            else:
                label = f"🍎\n{value}"

            if cols[c].button(label, key=key):
                if is_selected:
                    st.session_state.selected.discard((r, c))
                else:
                    st.session_state.selected.add((r, c))
                st.rerun()

st.divider()
st.markdown("""
**조작법**  
1. 사과를 클릭해서 선택/해제  
2. 합이 **정확히 10**이 되면 자동으로 사라집니다  
3. 최대한 빨리 많은 점수를 내보세요!
""")
