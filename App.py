import pyttsx3
import speech_recognition as sr
from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import streamlit as st
import threading
import hashlib

# ========================================== Load API Keys ====================================================================
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
langsmith_api = os.getenv('LANGCHAIN_API_KEY')

# ========================================== Initialize LLM ===================================================================
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

# ========================================== Prompt and Memory Setup ==========================================================
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are a helpful assistant that gives only the required answer in one or two short sentences.\n\n"
        "Avoid unnecessary details.\n\n"
        "Conversation History:\n{history}\n\n"
        "User's Question:\n{input}\n\n"
        "Answer:"
    ),
)

memory = ConversationBufferMemory()
conversation = ConversationChain(prompt=prompt, llm=llm, memory=memory)

# ========================================== Initialize TTS Engine ===========================================================
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[1].id)


def speak(text):
    """Convert text to speech in a separate thread."""
    def run_tts():
        tts_engine = pyttsx3.init()
        voices = tts_engine.getProperty('voices')
        tts_engine.setProperty('voice', voices[1].id)  # Adjust voice if needed
        tts_engine.say(text)
        tts_engine.runAndWait()
    
    tts_thread = threading.Thread(target=run_tts)
    tts_thread.start()

def listen():
    """Listen to the user's voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Could you please repeat?"
        except sr.RequestError:
            return "Sorry, there seems to be an issue with the speech recognition service."

# ========================================== Streamlit Interface ==============================================================

if "users" not in st.session_state:
    st.session_state["users"] = {}


# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to validate login credentials
def validate_login(username, password):
    hashed_password = hash_password(password)
    return st.session_state["users"].get(username) == hashed_password


# Function to handle signup
def signup_user(username, password):
    if username in st.session_state["users"]:
        return False     # Username already exists
    st.session_state["users"][username] = hash_password(password)
    return True


# Function to switch pages
def switch_page(page_name):
    st.session_state["current_page"] = page_name


# Main Function for Pages
def login_page():
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_login(username, password):
            st.success(f"Welcome back, {username}!")
            st.session_state["authenticated"] = True
            switch_page("Chatbot")
        else:
            st.error("Invalid username or password. Please try again.")
    
    st.button("New User? Signup Here", on_click=lambda: switch_page("Signup")) 



def signup_page():
    st.title("🔒 Signup")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif signup_user(new_username, new_password):
            st.success("Account created successfully! Please log in.")
            switch_page("Login")               # Switch to login after successful signup
        else:
            st.error("Username already exists. Please choose a different one.")
    
    st.button("Already have an account? Login Here", on_click=lambda: switch_page("Login"))

def chatbot_page():
    st.title("🤖 Chatbot Assistant")
    st.write("Hi there! I’m your AI assistant. You can type or speak your questions, and I’ll respond.")
    st.markdown("---")


    
    # Conversation History Display
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = ""

    
    # Input Method Selection
    input_method = st.radio("Select Input Method:", ("Text", "Voice"))

    
    # Chat Interface
    if input_method == "Text":
        user_input = st.text_input("Type your message:", key="user_input")
    else:
        user_input = ""
        if st.button("Speak"):
            user_input = listen()
            st.text_area("Your Voice Input:", user_input, height=100, disabled=True)  # Increased height to 100px

    if user_input:
        if user_input.lower() == "exit":
            st.write("Chatbot: Goodbye!")
            speak("Goodbye!")
            switch_page("Login")  
            return  

        elif user_input.lower() == "show history":
            history = memory.load_memory_variables({})
            conversation_history = history.get("history", "No history available yet.")
            st.write("Chat History:")
            st.text_area("", conversation_history, height=300)
            speak("Here is the conversation history." if conversation_history else "No history available yet.")
        else:
            response = conversation.invoke(input=user_input)
            response_text = response["response"]
            st.session_state["conversation_history"] += f"**User**: {user_input}\n**Chatbot**: {response_text}\n\n"
            st.write(f"**Chatbot**: {response_text}")
            speak(response_text)

    
    # Display Conversation History
    st.markdown("### Conversation History")
    st.text_area("Conversation Log", st.session_state["conversation_history"], height=300, disabled=True)

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        switch_page("Login")

# ========================================== Page Navigation ==================================================================

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Login"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["current_page"] == "Login":
    login_page()
elif st.session_state["current_page"] == "Signup":
    signup_page()
elif st.session_state["current_page"] == "Chatbot" and st.session_state["authenticated"]:
    chatbot_page()
else:
    st.session_state["current_page"] = "Login"
    login_page()

