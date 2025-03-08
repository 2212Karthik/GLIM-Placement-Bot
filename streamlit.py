import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Groq client
llm_client = Groq()

# App title and configuration
st.set_page_config(
    page_title="GLIM Placement Assistance Bot",
    page_icon="data:image/png;base64,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",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define available topics
topics = ["Finance", "Marketing", "Analytics", "Operations"]

# Custom CSS for enhanced UI
def inject_custom_css():
    st.markdown("""
    <style>
        .element-container .stButton .st-emotion-cache-ocsh0s{   
            float:right;
        }
        .st-emotion-cache-t1wise{
            padding:1rem 10rem;
            width:70%;
        }
        label{
            display:none;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    inject_custom_css()
    
    # Title and header
    st.markdown(f'<h1 class="main-title">GLIM Placement Assistance Bot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Ask your Questions!</p>', unsafe_allow_html=True)
    
    # Topic selection in a styled container
    st.markdown('<div class="content-card topic-selector">', unsafe_allow_html=True)
    topic = st.selectbox("🌍 Choose your Specialization:", topics, index=0)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area in a styled container
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="Type your question here...", height=120)
    
    if st.button("🔎 Proceed"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter a question.")
        else:
            get_response(topic, user_input)
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_response(topic, user_input):
    system_prompt = f"""
    You are a highly knowledgeable and experienced AI specializing in {topic}.
    Your role is to provide clear, accurate, and detailed answers exclusively related to {topic}.
    If a user poses a question about {topic}, respond with your best expertise.
    However, if the user asks about any subject outside of {topic}, reply with: 
    'Sorry, I cannot answer that. Feel free to ask me anything about {topic}.'
    """
    
    # Response container
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3>💡 Generated Response:</h3>", unsafe_allow_html=True)
    
    with st.spinner("⏳ Generating response..."):
        try:
            llm_response = llm_client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            
            response_text = ""
            response_container = st.empty()
            
            for chunk in llm_response:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    response_container.markdown(f'<div class="response-container">{response_text}</div>', unsafe_allow_html=True)
                    time.sleep(0.05)
            
            st.markdown('<div class="success-message">✅ Response generated successfully!</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
