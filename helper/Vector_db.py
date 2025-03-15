import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

_ = load_dotenv(override=True)
def create_index(index_name: str, vect_length: int=1536):
    """
    Create an index in Pinecone for storing vectors.

    This function deletes all existing indexes and creates a new index
    if it does not already exist. The index is created with the specified
    name and vector length, using the 'cosine' similarity metric.

    Args:
        index_name (str): The name of the index to create.
        vect_length (int, optional): The dimensionality of the vectors. Defaults to 1536 (1536 for OpenAI embeddings).
                                                                                         (768 for Gemini embeddings).
    
    # Run this function to create a new index in Pinecone  
    # create_index(index_name="rag-customer-support", vect_length=768)
    """
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    try:
        print('Deleting all indexes')
        _ = [pinecone.delete_index(name=index_name['name']) for index_name in pinecone.list_indexes()]
    except Exception as e:
        print('Error In Deleting Indexes: {}'.format(e))
        
    if index_name not in pinecone.list_indexes():
        print('Creating Index: {}'.format(index_name))
        pinecone.create_index(
            name=index_name,
            dimension=vect_length,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print('Done Creating Index: {}'.format(index_name))
        

def add_documents_to_pinecone(documents: str):
    """
    Adds documents to a Pinecone vector store.

    This function processes and adds the provided documents to a specified
    Pinecone index using a Google Generative AI embedding model. If the index
    does not exist or the documents are invalid, appropriate error messages
    are displayed.

    Args:
        documents (str): The documents to be added to the Pinecone vector store.

    Raises:
        Exception: Displays an error message if any exception occurs during
                   the process.
    """
    try:
        if not documents:
            print("⚠️ No valid documents found for processing.")
            return
        
        print(os.getenv('GOOGLE_API_KEY'))
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                       google_api_key=os.getenv('GOOGLE_API_KEY'))
        pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        index_name='rag-customer-support'
        
        if index_name not in [index_info["name"] for index_info in pinecone.list_indexes()]:
            print(f"❌ Index '{index_name}' does not exist. Create the index first.")
            return
        
        print("Adding new documents to Pinecone...")
        print(os.getenv('PINECONE_API_KEY'))
        vector_store = PineconeVectorStore(index_name=index_name, embedding=embedding_model,
                                           pinecone_api_key=os.getenv('PINECONE_API_KEY'))
        print("Done Adding new documents to Pinecone...")
        vector_store.add_documents(documents=documents)
        print("✅ Successfully added new documents to Pinecone.")
    except:
        print("❌ An error occurred while adding new documents to Pinecone.")
