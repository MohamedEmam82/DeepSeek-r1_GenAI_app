import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate,
                                    AIMessagePromptTemplate,
                                    ChatPromptTemplate)


### add css styling
st.markdown("""
<style>
        /* Existing styles */
            
    .main{
            background-color: #1a1a1a;
            color: #ffffff;
        }
    
    .sidebar .sidebar-content{
                background-color: #2d2d2d;
        }
    
    .stTextInput textarea{
            color: #ffffff !importatnt;
        }
            

    
    /* styles for selecting boxes */
            
        .stSelectbox div[data-baseweb="select"]{
            background-color: #2d2d2d !important;
            color: white !importamt;
            }
        
        .stSelectbox svg{
            fill: white !important;
            }

        .stSelectbox option{
            background-color: #2d2d2d !important;
            color: white !importamt;
            }

    
    /* styles for dropdown menue items */
            
        div[role="listbox"] div{
            background-color: #2d2d2d !important;
            color: white !importamt;
            }
</style>

""", unsafe_allow_html=True)

# stremlit emojis code link
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
st.title("🧠 Hamada Coding Companion")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

###### sidebar config #######
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(label="Choose Model",
                                  options=["deepseek-r1:1.5b", "deepseek-r1:1.3b"],
                                  index=0)
                                
                                    
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
                - 🐍 Python Expert
                - 🐞 Debugging Assistant
                - 📝 Code Documentation
                - 💡 Solution Design
                """)
    st.divider()
    st.markdown("Built by: Mohamed Emam")


####### Initiate chat engine #######

llm_engine = ChatOllama(model=selected_model,
                        base_url="http://localhost:11434",
                        temprature=0.3)
                    
    

### system prompt config
# dectate the role of this llm, or how this llm will act.
system_prompt = SystemMessagePromptTemplate.from_template(template=[""" You are expert AI coding assistant. 
                                                                        Provide concise, correct solutions with 
                                                                        stratigic print statements for debugging. 
                                                                        Always respond in English."""])
                                                            

### session state management
# to manage chat history
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role":"ai", "content":"Hi!, I'm Hamada. How can I assist you to code today?"}]


### chat container
chat_container = st.container()

### display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

### chat input and processing
user_query = st.chat_input(placeholder="Type your coding questions here...")

def generate_ai_reponse(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)


if user_query:
    # add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    # generate ai reponse
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_reponse(prompt_chain)

    # add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    # return to update the chat display
    st.rerun()