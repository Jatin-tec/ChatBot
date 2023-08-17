import os
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ConversationEntityMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from openai.error import RateLimitError

def get_conversation_chain():
    llm= OpenAI(max_tokens=1000, temperature=0.8,)

    if 'entity_memory' not in st.session_state:
        # handling token limit 
        st.session_state.entity_memory = ConversationEntityMemory(
            llm=llm,
            k=3,
        )

    conversation_chain = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory,
    )

    return conversation_chain

def handel_userinput(user_question):
    try:
        conversation= st.session_state.conversation.run(input=user_question)
    except RateLimitError:
        st.error("Rate limit exceeded. Please try again later.")
        return
    
    st.session_state.history.append(user_question)
    st.session_state.generated.append(conversation)

    with st.expander("Conversation"):
        for i in range(len(st.session_state.history)):
            st.info("Human: " + st.session_state.history[i])
            st.success("AI: " + st.session_state.generated[i])

def main():
    load_dotenv()
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    if 'generated' not in st.session_state:
        st.session_state.generated = []
    
    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'input' not in st.session_state:
        st.session_state.input = ""

    if 'stored_session' not in st.session_state:
        st.session_state.stored_session = []


    st.set_page_config(page_title="Streamlit App", page_icon=":shark:")

    st.header("Streamlit App")

    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                        placeholder="Type your message here...")
    
    if st.button("Ask 🤔"):
        #create conversation chain
        st.session_state.conversation = get_conversation_chain()
        if input_text:
            handel_userinput(input_text)

if __name__ == "__main__":
    main()