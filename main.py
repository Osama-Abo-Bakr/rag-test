import os
import streamlit as st
from helper.Load_data import load_data
from helper.Vector_db import add_documents_to_pinecone

def main():
    st.set_page_config(page_title="RAG Customer Support", page_icon=":robot_face:", layout="wide")
    st.title("RAG Customer Support :robot_face:")
    
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf", "docx", "txt"])
    url = st.text_input("Enter a YouTube URL:", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    if uploaded_files:
        file_paths = []
        for path in uploaded_files:
            temp_file_path = os.path.join(os.getcwd(), path.name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(path.read())
            file_paths.append(temp_file.name)
        
        with st.spinner("Processing files...", show_time=True):
            data = load_data(file_paths=file_paths)
            add_documents_to_pinecone(data)
            _ = [os.remove(file_path) for file_path in file_paths]
        st.success("✅ Files uploaded and processed successfully. 📁")
    
    elif url:
        with st.spinner("Processing Video URL...", show_time=True):
            data = load_data(url=url)
            add_documents_to_pinecone(data)
        st.write("✅ URL processed successfully. 🔗")
        
    else:
        st.write("Please upload files or provide a YouTube URL.")
        
        

if __name__ == "__main__":
    main()