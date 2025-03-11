import streamlit as st
import google.generativeai as genai
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
import os
sys.path.append(os.path.abspath("modules"))

# ✅ Load API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure the API key is set
if not GEMINI_API_KEY:
    st.error("❌ Google Gemini API key not found. Set GEMINI_API_KEY as an environment variable.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Import existing modules
from modules import (
    invoice_qna, multi_invoice_qna, translation, summarization,
    sentiment_analysis, grammar_correction,
    text_classification, spam_detection, speech_recognition
)

# Define AI Tools (Wrappers for existing functions)
tools = [
    Tool(name="Invoice Q&A", func=invoice_qna.answer_invoice_query, description="Answer questions based on invoice content."),
    Tool(name="Multiple Invoice Q&A", func=multi_invoice_qna.process_multiple_invoices, description="Answer questions based on multiple invoice PDFs."),
    Tool(name="Translation", func=translation.translate_text, description="Translate text into different languages."),
    Tool(name="Summarization", func=summarization.summarize_text, description="Summarize long text documents."),
    Tool(name="Sentiment Analysis", func=sentiment_analysis.analyze_sentiment, description="Analyze the sentiment of a given text."),
    Tool(name="Grammar Correction", func=grammar_correction.correct_grammar, description="Correct grammar and spelling in a given text."),
    Tool(name="Text Classification", func=text_classification.classify_text, description="Classify text into predefined categories."),
    Tool(name="Spam Detection", func=spam_detection.detect_spam, description="Detect if an email is spam or not."),
    Tool(name="Speech Recognition", func=speech_recognition.transcribe_audio, description="Transcribe speech from an audio file.")
]

# Initialize LangChain AI Agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5, google_api_key=GEMINI_API_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, memory=memory)

# Streamlit UI setup
st.set_page_config(page_title="Agentic AI Toolkit", page_icon="🤖", layout="wide")
st.sidebar.title("🤖 AI Agent")

# Show available AI agents in the sidebar
st.sidebar.subheader("Available AI Agents")
for tool in tools:
    st.sidebar.write(f"- {tool.name}")

# Display the currently used AI agent
st.sidebar.subheader("Currently Used Agent")
current_agent = st.sidebar.empty()

# User Input
st.title("AI Agent - Intelligent Query Handling")
user_input = st.text_area("💬 Enter your query:")

# File Uploaders for PDFs and Audio Files
st.sidebar.subheader("📂 Upload Files")
pdf_files = st.sidebar.file_uploader("Upload PDF Invoices", type=["pdf"], accept_multiple_files=True)
audio_file = st.sidebar.file_uploader("Upload Audio File", type=["wav", "mp3"])

if st.button("Ask AI Agent") and user_input:
    with st.spinner("Thinking..."):
        response = agent.run(user_input)
    st.success(response)
    
    # Update currently used agent in the sidebar
    current_agent.write(f"**Agent Used:** {response}")

# # Process PDFs if uploaded
# if pdf_files:
#     st.subheader("📄 Processed PDF Invoices")
#     query = st.text_input("🔍 Enter a query for the invoices:")
#     if st.button("Analyze PDFs") and query:
#         with st.spinner("Processing invoices..."):
#             results = multi_invoice_qna.process_multiple_invoices(pdf_files, query)
#         st.json(results)

# # Process PDFs if uploaded
if pdf_files:
    st.subheader("📄 Processed PDF Invoices")
    query = st.text_input("🔍 Enter a query for the invoices:")
    
    if st.button("Analyze PDFs") and query:
        with st.spinner("Processing invoices..."):
            results = multi_invoice_qna.process_multiple_invoices(pdf_files, query)
        
        # Extract text safely
        if isinstance(results, dict):
            plain_text_results = "\n\n".join(f"{key}: {value.get('answer', 'No answer found')}" for key, value in results.items())
        else:
            plain_text_results = "No valid results found."

        st.write(plain_text_results)  # Ensure plain text display


# Process Audio if uploaded
if audio_file:
    st.subheader("🎙️ Speech to Text Output")
    st.audio(audio_file, format='audio/wav')
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing audio..."):
            text_output = speech_recognition.transcribe_audio(audio_file)
        st.text_area("Transcribed Text:", text_output, height=200)
        
        # Provide a download option
        import io
        import json
        text_bytes = io.BytesIO(json.dumps(text_output, indent=2).encode("utf-8"))
        st.download_button("Download TXT", text_bytes, "transcription.txt", "text/plain")

print(os.getenv("GEMINI_API_KEY"))