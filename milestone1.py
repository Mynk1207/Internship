import pyttsx3
import speech_recognition as sr
from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

# ==========================================llm and langsmith api key=======================================================================

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
langsmith_api = os.getenv('LANGCHAIN_API_KEY')


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash" , api_key = api_key , safety_settings={
HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
HarmBlockThreshold.BLOCK_NONE,
})

# ===========================================prompt to define voice assistant===============================================================
prompt = """You are a helpful chat bot that can answer any question asked to you. Ask me anything!"""
memory = ConversationBufferMemory()

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are a helpful assistant that gives only the required answer in one or two short sentences.\n\n" 
        # "Give answers in sarcastic manner but not too much sarcastic .\n\n"
        "Avoid unnecessary details.\n\n"
        "Conversation History:\n{history}\n\n"
        "User's Question:\n{input}\n\n"
        "Answer:"
    ),
)


conversation = ConversationChain(prompt=prompt,llm=llm, memory=memory)

tts_engine = pyttsx3.init()


voices = tts_engine.getProperty('voices') 
tts_engine.setProperty('voice', voices[1].id)


def speak(text):
    """Convert text to speech."""
    tts_engine.say(text.encode('utf-8'))
    tts_engine.runAndWait()

def listen():
    """Listen to the user's voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Could you please repeat?"
        except sr.RequestError:
            return "Sorry, there seems to be an issue with the speech recognition service."



speak("! You can talk to me. Say 'exit' to end the conversation or 'show history' to view the chat history.")
print("Chatbot: Hello! You can talk to me. Say 'exit' to end the conversation or 'show history' to view the chat history.")
while True:
  
    user_input = listen()
    print(f"You: {user_input}")

    if user_input.lower() == "exit":
        response = "Goodbye!"
        print(f"Chatbot: {response}")
        speak(response)
        break
    
    elif user_input.lower() == "show history":
        history = memory.load_memory_variables({})
        response = history.get('history', 'No history available yet.')
        print(f"Chat History:\n{response}")
        speak("Here is the conversation history." if response else "No history available yet.")
        continue
    
 
    response = conversation.invoke(input=user_input)
    response_text = response['response']
    print(f"Chatbot: {response_text}")
    speak(response_text)
    # Check if the user says 'stop' during the response
    


    # Set the voice to female
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            tts_engine.setProperty('voice', voice.id)
            break


# ===========================================================REACT Agent====================================================================


# prompt1 = PromptTemplate(
#     input_variables=["observation", "history"],
#     template="""
# You are an intelligent agent. Based on the following observation and your conversation history, decide the best action:

# Observation: {observation}
# History:{history}
# What will you do next?
#     """
# )



# memory = ConversationBufferMemory(input_key="observation")

# react_chain = LLMChain(llm=llm, prompt=prompt1, memory=memory, output_key="action")


# def run_react_agent(observations):
#     for obs in observations:
#         print(f"Observation: {obs}")
#         result = react_chain.run(observation=obs)
#         print(f"Action: {result}\n")

# # if __name__ == "__main__":
# #     observations = [
# #         "You are a college student",
# #         "You are in final year of your college and doing an internship.",
# #         "You must do something in the field of Genrative Artificial Intelligence.",
# #     ]

#     run_react_agent(observations)