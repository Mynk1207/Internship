
# AI- powered Chatbot

An AI powered chatbot that is capable of answering any queries that a user asks to it. It can take input in text as well as in voice format and can provide the answer in either format. The chatbot is powered by Google Generative AI and it's frontend is powered by Streamlit. The system is made so that the user can login or signup accordingly and can also keep the chat history in case for future reference.



## Features

- Text Chat Interface: Easy to use and ask query to the model
- Voice Chat Functionality: Voice based funtionality to understand and communicate easily with the model.
- Memory-Powered Conversations: Retain conversation history to provide contextually relevant and continuous interactions.
- Text-to-Speech (TTS): Optional feature to convert chatbot responses to audio for enhanced accessibility.
- LangSmith Integration: It can monitor and trace the model ussage
- Frontend made with Streamlit: The model' Frontend is made using streamlit for clean and simple interface.


## Requirements

The following are the packages needed for the model. (versions can be changed accordingly)

- streamlit==1.41.1
- SpeechRecognition==3.12.0
- pyttsx3==2.9
- python-dotenv==1.0.1
- langchain==0.3.10
- langchain-google-genai==2.0.6
- langsmith==0.1.147
## Installation

Follow the steps below for running the model on your system.

1. Clone the repository:
```bash
   git clone https://github.com/Mynk1207/Internship
   cd App
```

2. Set up Virtual enviornment:
```bash
python3 -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

3. Install dependencies: 
```bash
pip install -r requirements.txt
```
4. Create or generate your api keys for Google Generative AI and Langsmith and add them in place of "your api key here" :
```bash
GOOGLE_KEY=your_google_api_key_here
LANGSMITH_TRACING_V2=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your-api-key_here"
LANGSMITH_PROJECT="AI-Bot"
```
5. Run the model:
```bash
streamlit run App.py
```

    
## Usage

Text chat

- Type your queries in the input box, and the chatbot will respond in real-time.

Voice chat
- Click the "Speak" button and speak into your microphone.
- The chatbot will process your query and provide a response.




## Conclusion

An AI-powered chatbot is versatile and can be deployed across industries to enhance user experiences and operational efficiency. 
In customer support, it provides instant responses, resolves queries, and escalates complex issues to human agents. For e-commerce, it assists with product recommendations, order tracking, and personalized shopping experiences. In healthcare, it helps schedule appointments, send medication reminders, and provide initial symptom checks. Educational institutions use chatbots to guide students with course selection, deadlines, and FAQs. Businesses leverage them for lead generation, onboarding, and employee support, automating repetitive tasks and allowing teams to focus on strategic initiatives.
