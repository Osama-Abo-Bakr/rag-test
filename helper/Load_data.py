import re
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.document_loaders import (TextLoader, PyPDFLoader, Docx2txtLoader)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def loading_documents(file_paths: List[str]):
    """
    Load text from documents in the given file paths.

    Supported file formats are .txt, .pdf, .docx.

    :param file_paths: A list of paths to the files to load
    :return: A single string containing all the text from the files, with each file's text
             separated by a line containing "----"
    """
    full_text = ""
    for path in file_paths:
        try:
            if path.endswith(".txt"):
                loader = TextLoader(path)
            elif path.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.endswith(".docx"):
                loader = Docx2txtLoader(path)
            else:
                print(f"Unsupported file format: {path}")
                continue
            
            documents = loader.load()
            extracted_text = "\n".join([doc.page_content for doc in documents])
            full_text += extracted_text + "\n---\n"
        
        except Exception as e:
            print(f"Error processing file {path}: {e}")
            continue
    
    return [Document(page_content=full_text)]

def extract_video_id(url):
    if len(url) == 11 and re.match(r'^[A-Za-z0-9_-]{11}$', url):
        return url
    
    # Try to extract from various URL formats
    patterns = [
        r'youtube\.com/watch\?v=([A-Za-z0-9_-]{11})',
        r'youtu\.be/([A-Za-z0-9_-]{11})',
        r'youtube\.com/embed/([A-Za-z0-9_-]{11})',
        r'youtube\.com/v/([A-Za-z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def loading_youtube_transcript(url):
    """
    Downloads the transcript of a YouTube video given its URL.

    :param url: The URL of the YouTube video
    :return: The transcript of the video as a string
    :raises ValueError: if the transcript could not be retrieved
    """
    try:
        # Extract video ID from the URL
        video_id = extract_video_id(url)
        if not video_id:
            raise print("Invalid YouTube URL or video ID")
        
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
        transcript_text = f"video-URL: {url} \n" + ' '.join([item['text'] for item in transcript_list])
        
        return [Document(page_content=transcript_text, metadata={"url": url})]
    
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript: {str(e)}")
    

def load_data(file_paths: List[str]=None, url: str=None):
    """
    Load data from either a list of file paths or a YouTube URL.

    Args:
        file_paths (List[str]): A list of file paths to load data from.
        url (str): A YouTube URL to load transcript from.

    Returns:
        List[str]: A list of strings, where each string is a chunk of text from
            the loaded data. The chunks are determined by the
            RecursiveCharacterTextSplitter.
    """
    if url and url.strip():
        data = loading_youtube_transcript(url)
    elif file_paths or file_paths == []:
        data = loading_documents(file_paths)
    else: 
        raise ValueError("Either file_paths or url must be provided.")
        
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, 
                                              chunk_overlap=200)
    
    final_data = splitter.split_documents(documents=data)
    return final_data