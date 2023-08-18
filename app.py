import streamlit as st
from LLMWrapper import LLMWrapper

model = "gpt-3.5"
def handel_user_input(user_input):
    wrapper = LLMWrapper(model)
    response = wrapper.generate_response(user_input)
    st.session_state['history'].append(user_input)
    st.session_state['history'].append(response)
    wrapper.history = st.session_state['history']
    for index, elm in enumerate(st.session_state['history']):
        if index % 2 == 0:
            st.write("You: ", elm)
        else:
            st.write("LLM: ", elm)

def main():
    st.title("LLM Chatbot", anchor="center")

    st.write("This is a chatbot powered by the LLM API. It is trained on the PersonaChat dataset.")

    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    user_input = st.text_input("You: ")
    
    if st.button("Send"):
        if user_input:
            handel_user_input(user_input)
        else:
            st.warning("Please enter a message.")

if __name__ == "__main__":
    main()