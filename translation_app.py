import json
import streamlit as st
from translation import translate_korean_to_vietnamese  # Import your translate function

# Set page title and favicon
st.set_page_config(page_title="Mango🥭TOPIK", page_icon="🥭")

# Set background color
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set title style
st.title("Dịch tiếng Hàn sang tiếng Việt")
st.markdown('<div style="font-family: Noto Sans, sans-serif; font-size: 30px; color: #333333; margin-bottom: 20px;">Nhập Tiếng Hàn</div>', unsafe_allow_html=True)

# User input area
input_text = st.text_area("Korean Text", height=150)

# Initialize session state
if 'log' not in st.session_state:
    st.session_state.log = []
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# Translate button
if st.button('Translate'):
    if input_text:
        # Call your translation function
        st.session_state.translated_text = translate_korean_to_vietnamese(input_text)

# Display the translated text with Papago-like style and add margin-bottom
st.markdown(f'<div style="font-family: Noto Sans, sans-serif; font-size: 23px; color: #333333; margin-bottom: 20px;">Tiếng Việt :</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-family: Noto Sans, sans-serif; font-size: 23px; color: #007acc; border: 1px solid #007acc; padding: 10px; border-radius: 5px;">{st.session_state.translated_text}</div>', unsafe_allow_html=True)

# Add some margin-top to create space between translated text and feedback elements
st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)

# Add the usage instructions in the middle
st.markdown(
    """
    ## Hướng dẫn sử dụng

    - Chỉ có thể dịch từ Tiếng Hàn -> Tiếng Việt
    - Chỉ có thể dịch tốt tiếng Hàn hàng ngày, TẤT CẢ các câu đề thi đọc của TOPIK và KIIP
    - Nên dịch một câu một cho ra kết quả tốt nhất.
    - Nếu thấy hữu ích hãy share giúp bọn mình: [mangotopik.com](https://mangotopik.com)
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    ## Đánh giá của bạn
    """,
    unsafe_allow_html=True
)

# User feedback
like = st.checkbox('Tốt 🤗')
dislike = st.checkbox('Chưa tốt 😢')
feedback = st.text_input('Góp ý')

# Add some margin-top to create space between feedback elements and the Submit button
st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

# Write log to file
if st.button('Submit'):
    # Log user interactions
    st.session_state.log.append({
        'user_input': input_text,
        'translated_text': st.session_state.translated_text,
        'like': like,
        'dislike': dislike,
        'feedback': feedback
    })

    with open('translation_log.json', 'a') as f:
        json.dump(st.session_state.log, f, indent=2)
        f.write('\n')  # Add a newline between entries

    # Clear the session state log after writing to file
    st.session_state.log = []
