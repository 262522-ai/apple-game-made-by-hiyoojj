import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

# ====================== 설정 ======================
ROWS = 6
COLS = 8
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CELL_W = CANVAS_WIDTH // COLS
CELL_H = CANVAS_HEIGHT // ROWS

st.set_page_config(page_title="사과게임 드래그 버전 🍎", page_icon="🍎", layout="centered")
st.title("🍎 사과게임 (드래그 버전)")
st.caption("마우스로 사각형을 드래그해서 합이 10이 되는 사과들을 선택하세요!")

# ====================== 세션 상태 ======================
if "board" not in st.session_state:
    st.session_state.board = np.random.randint(1, 10, size=(ROWS, COLS))
    st.session_state.score = 0
    st.session_state.last_rect = None  # 같은 사각형을 여러 번 처리하지 않기 위해

# ====================== 보드 이미지 만들기 ======================
def create_board_image(board):
    img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)

    # 글씨 크기 (기본 폰트 사용)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()

    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL_W
            y1 = r * CELL_H
            x2 = x1 + CELL_W
            y2 = y1 + CELL_H

            value = board[r, c]

            if value == 0:
                # 이미 제거된 칸
                draw.rectangle([x1, y1, x2, y2], fill=(220, 220, 220), outline=(180, 180, 180))
            else:
                # 사과 칸 (연한 초록)
                draw.rectangle([x1+2, y1+2, x2-2, y2-2], fill=(180, 230, 180), outline=(50, 120, 50), width=2)
                
                # 숫자 중앙에 그리기
                text = str(value)
                bbox = draw.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                tx = x1 + (CELL_W - tw) // 2
                ty = y1 + (CELL_H - th) // 2 - 2
                draw.text((tx, ty), text, fill=(20, 80, 20), font=font)

    return img

# ====================== 사이드바 ======================
with st.sidebar:
    st.header("게임 정보")
    st.metric("현재 점수", st.session_state.score)
    
    remaining = np.count_nonzero(st.session_state.board)
    st.metric("남은 사과", remaining)

    if st.button("🔄 새 게임", use_container_width=True):
        st.session_state.board = np.random.randint(1, 10, size=(ROWS, COLS))
        st.session_state.score = 0
        st.session_state.last_rect = None
        st.rerun()

    st.markdown("---")
    st.markdown("**조작법**")
    st.markdown("""
1. 마우스로 **사각형을 드래그**하세요  
2. 안에 들어간 숫자들의 합이 **10**이면 자동으로 제거됩니다  
3. 캔버스 위의 휴지통 아이콘으로 사각형을 지울 수 있어요
""")

# ====================== 캔버스 ======================
board_img = create_board_image(st.session_state.board)

canvas_result = st_canvas(
    fill_color="rgba(255, 80, 80, 0.3)",   # 반투명 빨간 박스
    stroke_width=3,
    stroke_color="#ff3333",
    background_image=board_img,
    update_streamlit=True,
    height=CANVAS_HEIGHT,
    width=CANVAS_WIDTH,
    drawing_mode="rect",                   # 사각형만 그리기
    key="apple_canvas",
    display_toolbar=True,
)

# ====================== 드래그한 사각형 처리 ======================
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]

    if len(objects) > 0:
        # 가장 마지막에 그린 사각형만 사용
        rect = objects[-1]

        if rect["type"] == "rect":
            left = rect["left"]
            top = rect["top"]
            width = rect["width"] * rect.get("scaleX", 1)
            height = rect["height"] * rect.get("scaleY", 1)

            # 같은 사각형을 반복 처리하지 않기 위한 체크
            rect_id = (round(left), round(top), round(width), round(height))
            
            if rect_id != st.session_state.last_rect:
                st.session_state.last_rect = rect_id

                # 사각형 안에 중심이 들어오는 칸 찾기
                selected = []
                selected_sum = 0

                for r in range(ROWS):
                    for c in range(COLS):
                        if st.session_state.board[r, c] == 0:
                            continue

                        # 칸의 중심 좌표
                        cx = c * CELL_W + CELL_W / 2
                        cy = r * CELL_H + CELL_H / 2

                        if (left <= cx <= left + width) and (top <= cy <= top + height):
                            selected.append((r, c))
                            selected_sum += st.session_state.board[r, c]

                # 합이 10이면 제거
                if selected_sum == 10 and len(selected) > 0:
                    for r, c in selected:
                        st.session_state.board[r, c] = 0
                    st.session_state.score += len(selected)
                    st.success(f"성공! +{len(selected)}점  (합: 10)")
                    st.balloons()
                    time.sleep(0.6)
                    st.rerun()
                elif len(selected) > 0:
                    st.warning(f"선택된 합: **{selected_sum}**  (10이 아니에요)")

st.markdown("---")
st.caption("사각형을 잘못 그렸으면 캔버스 오른쪽 위 휴지통 버튼을 눌러서 지우고 다시 그리세요.")
