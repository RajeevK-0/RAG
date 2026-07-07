import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="ML Research Assistant", page_icon="📚")
st.title("AI Research Paper Assistant")
st.caption("Powered by FastAPI, LangChain, and FAISS")

with st.sidebar:
    st.markdown("### Try asking about:")
    
    # We use session_state to hold a button click so it acts like the chat input
    if st.button("How is Attention Mechanism?"):
        st.session_state.preset_prompt = "Explain what is Attention mechanism and how is it works."
        
    if st.button("What is the math behind XGBoost?"):
        st.session_state.preset_prompt = "Explain the mathematical foundation of XGBoost and how it builds trees."
        
    if st.button("Why use Layer Norm over Batch Norm?"):
        st.session_state.preset_prompt = "Why do Transformers use Layer Normalization instead of Batch Normalization?"

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Render Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the research papers...")
if 'preset_prompt' in st.session_state:
    prompt = st.session_state.preset_prompt
    del st.session_state.preset_prompt
# 4. Handle New User Input

if prompt:
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare for the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        api_url = "http://127.0.0.1:8000/askQuery" 
        try:
            history_payload = st.session_state.messages[:-1]
            payload = {'user_query':prompt , 'history':history_payload}
            with requests.post(api_url, json=payload, stream=True) as response:
                response.raise_for_status() # Catch any 400/500 errors
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        full_response += chunk
                        # Update the placeholder with the typewriter effect and a blinking cursor
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the backend. Is your FastAPI server running?")