import streamlit as st
from helper.Full_chain import get_response

def main():
    st.set_page_config(page_title="RAG Customer Support", page_icon=":robot_face:", layout="wide")
    st.title("RAG Customer Support :robot_face:")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    user_query = st.chat_input("Ask a question:")
    if user_query:
        response = get_response(user_query=user_query, user_id="None")
        
        st.session_state.chat_history.append({"user": user_query, 
                                              "assistant": response['answer'].replace("```markdown", "").replace("```", "").strip()})
        
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["user"])
            with st.chat_message("assistant"):
                st.write(chat["assistant"])

if __name__ == "__main__":
    main()