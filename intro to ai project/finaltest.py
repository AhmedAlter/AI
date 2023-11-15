import streamlit as st
from typing import Literal
from dataclasses import dataclass
import base64
import time

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:", layout="wide")
st.markdown('<style>' + open(r'C:\Users\ahmed\OneDrive\Desktop\Uni\Fall 2023\CSAI 350\AI Project\static\styles.css').read() + '</style>', unsafe_allow_html=True)

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0    # Don't worry about this im just testing it smth
    if "conversation" not in st.session_state:
        st.session_state.conversation = []  # Initialize the conversation history

def on_click_callback():
    human_prompt = st.session_state.human_prompt

    # Hardcoded responses for testing
    responses = {
        "how are you": "I'm doing well!",
        "hello": "Hi there!",
    }

    # Get response
    response = responses.get(human_prompt.lower(), "I didn't understand that.")

    # Add the user input and bot response to the conversation history
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", response))

initialize_session_state()

# Sidebar
st.sidebar.title("CSCI 350 Project - Chatbot 🤖")

# About section
st.sidebar.markdown("### About")
st.sidebar.markdown("This is a chatbot designed for the Intro to AI Project. It can respond to specific prompts and engage in conversations with users that has been made using the following:")

# Used Technologies section
st.sidebar.markdown("### Used Technologies")
st.sidebar.markdown("- [Streamlit](https://streamlit.io/)\n - [Ghaleb's Killer Knowledge, Super Strength, and Integrity](https://www.shutterstock.com/shutterstock/photos/1552486565/display_1500/stock-photo-muscled-male-model-in-studio-1552486565.jpg)")

st.sidebar.markdown("&nbsp;")
st.sidebar.markdown("---")


if st.sidebar.button("New Conversation"):
    # Save the current conversation
    st.session_state.conversation.append(st.session_state.history.copy())
    # Reset the current conversation history
    st.session_state.history = []

# Display old conversations in the sidebar
selected_conversation = st.sidebar.selectbox("Select Conversation", ["None"] + [f"Conversation {i}" for i in range(1, len(st.session_state.conversation) + 1)])
if selected_conversation != "None":
    # Load the selected conversation
    st.session_state.history = st.session_state.conversation[int(selected_conversation.split()[-1]) - 1]


chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

with chat_placeholder:
    for chat in st.session_state.history:
        image_path = r'C:/Users/ahmed/OneDrive/Desktop/Uni/Fall 2023/CSAI 350/AI Project/static/ai_icon.png' if chat.origin == 'ai' else r'C:/Users/ahmed/OneDrive/Desktop/Uni/Fall 2023/CSAI 350/AI Project/static/user_icon.png'
        div = f"""
        <div class="chat-row
            {'' if chat.origin == 'ai' else 'row-reverse'}">
            <img class="chat-icon" src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}"
                width=32 height=32>
            <div class="chat-bubble
            {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                &#8203;{chat.message}
            </div>
        </div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")


with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        value="Hello",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit",
        type="primary",
        on_click=on_click_callback,
    )

st.caption(f"""
Used {st.session_state.token_count} tokens
""")