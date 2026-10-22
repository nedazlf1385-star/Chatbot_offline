'''
import streamlit as st

prompt = st.chat_input('Enter you prompt')
if prompt:
    st.write(f'Prompt: {prompt}')

st.chat_message('ai').write('How can I help You ?')
st.chat_message('user').write('Tell me about football.')

st.write(st.session_state)
if 'count' not in st.session_state:
    st.session_state['count'] = 0

if st.button('ADD'):
    st.session_state['count'] += 1
    st.write(f'Count: {st.session_state['count']}')

import time 
with st.spinner('Generating...'):
    time.sleep(3)
'''
# import streamlit as st

# prompt = st.chat_input('Enter you prompt')
# if prompt:
#     st.write(f'Prompt: {prompt}')

# st.chat_message('ai').write('How can I help You ?')
# st.chat_message('user').write('Tell me about football.')

# # role --> ai / user
# # content --> message

# st.write(st.session_state)
# if 'count' not in st.session_state:
#     st.session_state['count'] = 0

# if st.button('ADD'):
#     st.session_state['count'] += 1
#     st.write(f'Count: {st.session_state['count']}')

# import time
# with st.spinner('Generating ...'):
#     time.sleep(3)
#--------------------------------------------------------------------

import streamlit as st
import utils
from pathlib import Path
from datetime import datetime

st.title('STREAMLIT CHATBOT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role':'ai', 'content':'How Can I Help You?'}]

for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])


prompt = st.chat_input('Enter Your Question')
model = 'gemma3:1b'

if prompt:
    new_prompt = prompt +'Descride your answer with detail and imagens'
    st.chat_message('user').write(prompt)
    st.session_state['messages'].append({'role':'user', 'content':'prompt'})

    with st.spinner('Generating Response ...'):
        response = utils.call_ollama_model(new_prompt, model)

    st.chat_message('ai').write(response)
    st.session_state['messages'].append({'role':'ai','content':response})
    
# Stop Model and Clear History Buttons

col1, col2 = st.columns(2)

with col1:
    if st.button("Stop Model"):
        st.session_state["stop_model"] = True
        st.warning("Model stopped!")

with col2:
    if st.button("Clear History"):
        st.session_state["messages"] = []
        st.success("Chat history cleared!")
        st.rerun()


# ذخیره و خلاصه‌سازی مکالمه
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

def get_chat_text():
    return "\n\n".join(
        f"{'کاربر' if m['role'] == 'user' else 'چت‌بات'}: {m['content']}"
        for m in st.session_state["messages"]
    )

st.divider()
st.subheader("مدیریت مکالمه")

if st.button("ذخیره کل مکالمه"):
    (PROJECT_DIR / "chat_history.txt").write_text(
        get_chat_text(), encoding="utf-8"
    )
    st.success("مکالمه ذخیره شد.")

if st.button("خلاصه‌سازی کل مکالمه"):
    prompt_summary = f"""
    متن زیر را به فارسی خلاصه کن.
    نکات مهم، راه‌حل‌ها و کارهای باقی‌مانده را حفظ کن.
    اطلاعات جدید اضافه نکن و مطالب تکراری را حذف کن.

    متن مکالمه:
    {get_chat_text()}
    """

    with st.spinner("در حال خلاصه‌سازی..."):
        summary = utils.call_ollama_model(prompt_summary, model)

    if summary == "ERROR" or summary.startswith("خطا:"):
        st.error(summary)
    else:
        st.subheader("خلاصه مکالمه")
        st.write(summary)
        (PROJECT_DIR / "chat_summary.txt").write_text(
            summary, encoding="utf-8"
        )
        st.success("خلاصه ذخیره شد.")
        st.download_button(
            "دانلود خلاصه",
            summary,
            file_name="chat_summary.txt"
        )
