import streamlit as st
import streamlit.components.v1 as components
import os

# --- 페이지 설정 ---
st.set_page_config(
    page_title="게임: 사라지는 얼음",
    page_icon="🧊",
    layout="wide",
)

# --- 폰트 적용 ---
# (이전과 동일하게 Pretendard-Bold.ttf 폰트를 적용하는 함수, 필요시 추가)
def apply_custom_font():
    FONT_PATH = "/fonts/Pretendard-Bold.ttf"
    if os.path.exists(FONT_PATH):
        # 폰트 적용 CSS 코드 (이전 답변 내용과 동일)
        pass # 여기에 이전 폰트 적용 코드를 붙여넣으세요.
apply_custom_font()


# --- 메인 앱 ---
st.title("🧊 GUI 게임: 사라지는 얼음")
st.markdown("""
**조작법:** 스페이스 바 또는 마우스 클릭으로 점프하세요!

점점 빠르게 사라지는 얼음들을 피해 북극곰이 최대한 멀리 갈 수 있도록 도와주세요. 얼음이 사라지는 속도가 빨라지는 것은 **지구 온난화가 가속화되는 현실**을 의미합니다.
""")

# game.html 파일을 읽어와서 삽입
try:
    with open('game.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
    components.html(html_code, height=610)
except FileNotFoundError:
    st.error("게임 파일을 찾을 수 없습니다. 'game.html' 파일이 streamlit_app.py와 같은 폴더에 있는지 확인해주세요.")