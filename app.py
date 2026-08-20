import streamlit as st
import numpy as np

ROWS = 6
COLS = 8

st.set_page_config(page_title="사과게임 🍎", page_icon="🍎", layout="centered")
st.title("🍎 사과게임")
st.caption("숫자를 클릭해서 선택하고, 합이 10이 되면 제거하세요!")

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

# 버튼들
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 제거하기 (합이 10일 때)", use_container_width=True, type="primary"):
        if selected_sum == 10 and len(st.session_state.selected) > 0:
            count = 0
            for r, c in list(st.session_state.selected):
                if st.session_state.board[r, c] > 0:
                    st.session_state.board[r, c] = 0
                    count += 1
            st.session_state.score += count
            st.session_state.selected = set()
            st.success(f"+{count}점!")
            st.rerun()
        else:
            st.warning("합이 정확히 10이 아니에요!")

with col2:
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
            label = f"**{value}**" if is_selected else str(value)

            if cols[c].button(label, key=key):
                if is_selected:
                    st.session_state.selected.discard((r, c))
                else:
                    st.session_state.selected.add((r, c))
                st.rerun()

st.divider()
st.markdown("""
**조작법**  
1. 숫자를 클릭해서 선택/해제  
2. 합이 10이 되면 **제거하기** 버튼 누르기  
3. 최대한 많은 사과를 없애보세요!
""")
