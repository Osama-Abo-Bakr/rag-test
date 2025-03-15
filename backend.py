import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, HTTPException
from helper.Load_data import load_data
from helper.Vector_db import add_documents_to_pinecone
from helper.Full_chain import get_response

_ = load_dotenv(override=True)

app = FastAPI(
    debug=True,
    title="Customer Support Chatbot",
    description="A chatbot for E-Commerce websites.",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add_data")
async def Add_Data_Pinecone(files_data: Optional[UploadFile]=None,
                            url: Optional[str] = Form(None),
                            case: str=Form(..., description='Case', enum=['URL', 'Document'])):
    """
    Endpoint to upload and process documents or YouTube video transcripts.

    - If a file is uploaded, it will be processed and stored in Pinecone.
    - If a YouTube URL is provided, the transcript will be extracted and stored.
    """
    try:
        # if files_data and files_data.filename:
        if case == 'Document':
            if not files_data or not files_data.filename:
                raise HTTPException(status_code=400, detail="No file uploaded for Document case")
            if url:
                raise HTTPException(status_code=400, detail="URL should not be provided for Document case")
            
            temp_file_path = os.path.join(os.getcwd(), files_data.filename)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(await files_data.read())
            
            data = load_data(file_paths=[temp_file_path])
            add_documents_to_pinecone(data)
            _ = os.remove(temp_file_path)
            return {"message": "✅ Files uploaded and processed successfully. 📁"}
        
        # elif url:
        elif case == 'URL':
            if not url:
                raise HTTPException(status_code=400, detail="No URL provided for URL case")
            if files_data:
                raise HTTPException(status_code=400, detail="File should not be provided for URL case")
            
            data = load_data(url=url)
            add_documents_to_pinecone(data)
            return {"message": "✅ URL processed successfully. 🔗"}
        
        else:
            return HTTPException(status_code=400, detail="Please provide either file or url.")
    
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    

@app.post("/get_response")
async def Get_Response(user_query: str = Form(...), user_id: str = Form(None)):
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
    try:
        return {"message": get_response(user_query=user_query, user_id=user_id)}
    
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))