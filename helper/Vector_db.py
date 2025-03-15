import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv(".env")

# Function Load Vector-DB
def load_vector_db():
    """
    Load Vector-DB from local file.

    The Vector-DB is a local file that stores the embedded data.
    If the file exists, it will be loaded and returned as a FAISS vectorstore.
    If not, it will return None.

    Returns:
        FAISS: A FAISS vectorstore containing the embedded data.
    """
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                    google_api_key="AIzaSyCHQdYdiHjAf910XztOLYFxvDJW58OrKMA")
    save_path = f'vector_db'
    try:
        if os.path.exists(save_path):
                vectorstore = FAISS.load_local(save_path, embeddings=embedding_model,
                                            allow_dangerous_deserialization=True)
                return vectorstore
        else: print("❌ Vector-DB not found.")
    except:
        print("❌ An error occurred while loading Vector-DB.")
        
# Function to update vector store
def update_vector_store(documents: str):
    """
    Update the FAISS vector store with new documents.

    This function updates an existing FAISS vectorstore by adding new documents
    with their embeddings. If the vectorstore file does not exist, it creates a new
    one using the provided documents.

    Args:
        documents (str): The documents to be embedded and added to the vector store.

    Raises:
        Exception: If an error occurs while loading or updating the vector store, 
                   an error message is printed.
    """
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                    google_api_key="AIzaSyCHQdYdiHjAf910XztOLYFxvDJW58OrKMA")
    save_path = f'vector_db'
    
    try:  
        if os.path.exists(save_path):
            vectorstore = FAISS.load_local(save_path, embeddings=embedding_model,
                                        allow_dangerous_deserialization=True)
            
            # Add new products
            if documents:
                vectorstore.add_documents(documents, embedding=embedding_model)
        
        else:
            os.makedirs(save_path, exist_ok=True)
            vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)

        # Save updated vector store
        vectorstore.save_local(save_path)
        print("Vector store has been updated with new documents.")
    except:
        print("❌ An error occurred while adding / Create Vector-DB.")