import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import (ChatGoogleGenerativeAI, 
                                    GoogleGenerativeAIEmbeddings)


_ = load_dotenv(override=True)

def create_retriever_chain():    
    """
    Create a conversational retrieval chain with a Google Generative AI model.

    This chain uses a Pinecone vector store as the retriever and a Google Generative AI model as the
    language model. The chain is configured with a conversational retrieval template and returns the
    source documents.

    Args:

    Returns:
        ConversationalRetrievalChain
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    
    
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vectorstore = PineconeVectorStore(embedding=embedding_model, index_name='rag-customer-support',
                                      pinecone_api_key=os.getenv('PINECONE_API_KEY'))
    
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}, alpha=0.5)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21",
                                 temperature=0.3, api_key=api_key)

    template = """
    You are an AI assistant specializing in customer support and sales for `Kindix`.  
    Your role is to provide accurate, engaging, and user-friendly information to assist customers  
    and promote `Kindix`'s services. Leverage the provided context to give  
    comprehensive responses.

    ### Context:
    {context}  

    ### User Query:
    {question}  

    ### Guidelines:  
    - Provide clear, concise, and accurate answers based on the retrieved context.  
    - If applicable, direct users to relevant sections on the website or provide a link: [Kindix Website](https://kindix.me/).  
    - Use a conversational tone and engage in a friendly and engaging conversation.  
    - Be empathetic, friendly, and approachable while subtly promoting services when relevant.  

    ### Handling Unavailable Information:  
    If you do not have a response or the context is unrelated to the user's query, say:  
    *"I'm sorry, but I don’t have that information right now. You can contact our customer service team for further assistance."*  

    #### Customer Support or services:  
    - **Website:** [Kindix Support](https://support.kindix.me/)  
    - **Phone:** +08-675-9660  
    - **Email:** [sales@kindix.me](mailto:sales@kindix.me)  
    
    #### Arabic Language Support:  
    - **Phone:** 050-444-6785 / 050-640-5322  
    ---
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"], 
        template=template
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt, "document_variable_name": "context"},
    )
    

def get_response(user_query, user_id=None):
    """
    Get a response from the conversational retrieval chain based on the user's query.

    Retrieves the chat history for the user, creates a conversational retrieval chain, and uses it to
    generate a response. The response is then saved to the chat history.

    Args:
        user_query (str): The user's query.
        user_id (str): The ID of the user.

    Returns:
        dict: A dictionary containing the response and other metadata.
    """
    
    retriever_chain = create_retriever_chain() # Get response
    result = retriever_chain.invoke({"question": user_query, "chat_history": []})
    try:    
        if len(result["source_documents"]) > 0:
            if result["source_documents"][0].metadata: 
                url = result["source_documents"][0].metadata["url"]
            else: url = None
        else:
            url = None
    except:
        url = None
    result = {"answer": result['answer'], "video-url": url}
    return result