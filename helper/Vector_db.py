import os
from dotenv import load_dotenv
from pinecone import PineconeProtocolError
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
    """
    try:
        if not documents:
            print("⚠️ No valid documents found for processing.")
            return

        # Debugging API Keys
        google_api_key = os.getenv("GOOGLE_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")

        if not google_api_key:
            print("❌ Missing GOOGLE_API_KEY. Please check your .env file.")
            return
        if not pinecone_api_key:
            print("❌ Missing PINECONE_API_KEY. Please check your .env file.")
            return

        # Debugging output
        print(f"🔹 Using GOOGLE_API_KEY: {google_api_key[:5]}... (hidden for security)")
        print(f"🔹 Using PINECONE_API_KEY: {pinecone_api_key[:5]}... (hidden for security)")

        # Initialize Embeddings and Pinecone
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )
        
        pinecone = Pinecone(api_key=pinecone_api_key)
        index_name = "rag-customer-support"
        
        print("✅ Connect with Pinecone")


        index_list = pinecone.list_indexes()
        print(f"🔹 Available indexes: {index_list}")
            
        if index_name not in index_list:
            print(f"❌ Index '{index_name}' does not exist. Create the index first.")
            return

        # Initialize Vector Store
        try:
            print("🔥 Initialize vector-store \n")
            vector_store = PineconeVectorStore(
                index_name=index_name,
                embedding=embedding_model,
                pinecone_api_key=pinecone_api_key,
                host="https://rag-customer-support-84lnu3k.svc.aped-4627-b74a.pinecone.io"
            )
        except PineconeProtocolError:
            print("⚠️ Pinecone connection timed out. Reinitializing...")
            pinecone = Pinecone(api_key=pinecone_api_key, environment="us-east-1")
            vector_store = PineconeVectorStore(
                index_name=index_name,
                embedding=embedding_model,
                pinecone_api_key=pinecone_api_key,
                host="https://rag-customer-support-84lnu3k.svc.aped-4627-b74a.pinecone.io"
            )
            vector_store.add_documents(documents=documents)
            print("✅ Successfully added new documents after retrying.")
            return


        print("🚀 Adding new documents to Pinecone...")
        vector_store.add_documents(documents=documents)
        print("✅ Successfully added new documents to Pinecone.")

    except Exception as e:
        print(f"❌ Error while adding documents to Pinecone: {e}")

