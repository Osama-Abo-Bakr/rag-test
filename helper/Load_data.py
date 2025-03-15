import os
import yt_dlp
from groq import Groq
from typing import List
from langchain_community.document_loaders import (TextLoader, PyPDFLoader, Docx2txtLoader)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Get the FFmpeg path dynamically
FFMPEG_PATH = "./ffmpeg/bin/ffmpeg.exe"
# FFMPEG_PATH = r"D:\Pycharm\RAG-Project\RAG (Customer Services)\V3\ffmpeg\bin\ffmpeg.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

# import shutil

# # Automatically find FFmpeg in the system
# FFMPEG_PATH = shutil.which("ffmpeg")

# if not FFMPEG_PATH:
#     raise EnvironmentError("FFmpeg is not installed or not found in PATH. Install it in Docker.")

# os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)


def loading_documents(file_paths: List[str]):
    """
    Load text from documents in the given file paths.

    Supported file formats: .txt, .pdf, .docx.

    :param file_paths: A list of paths to the files to load
    :return: A list containing a single Document object with all text concatenated
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


def download_audio(url, output_folder="audio"):
    """
    Downloads the audio from a YouTube video using yt-dlp.

    :param url: The URL of the YouTube video
    :param output_folder: Folder to save the downloaded audio
    :return: Path to the downloaded audio file
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Ensure the folder exists

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_folder}/%(title)s.%(ext)s",  # Proper filename format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_PATH,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")  # Ensure correct file format

    return filename  # Return full filename


def loading_youtube_transcript(url):
    """
    Downloads and transcribes a YouTube video.

    :param url: The YouTube video URL
    :return: Transcribed text as a Document object
    """
    try:
        audio_path = download_audio(url)
        print(f"Downloaded audio path: {audio_path}")

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        client = Groq(api_key="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")
        
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3-turbo",
                prompt="Specify context or spelling",
                response_format="json",
                language="en",
                temperature=0.0
            )

        transcript_text = transcription.text

        # Remove the downloaded audio file
        os.remove(audio_path)
        print(f"Deleted audio file: {audio_path}")

        return [Document(page_content=f"video-URL: {url} \n{transcript_text}", metadata={"url": url})]

    except Exception as e:
        raise ValueError(f"Error processing video: {str(e)}")


def load_data(file_paths: List[str] = None, url: str = None):
    """
    Load data from either a list of file paths or a YouTube URL.

    Args:
        file_paths (List[str]): A list of file paths to load data from.
        url (str): A YouTube URL to load transcript from.

    Returns:
        List[Document]: A list of Document objects, each containing text chunks.
    """
    if url and url.strip():
        data = loading_youtube_transcript(url)
    elif file_paths or file_paths == []:
        data = loading_documents(file_paths)
    else:
        raise ValueError("Either file_paths or url must be provided.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    final_data = splitter.split_documents(documents=data)

    return final_data



# # url = "https://www.youtube.com/watch?v=dzoL2n8HweE"
# url="https://www.youtube.com/watch?v=dzoL2n8HweE&t=3s&ab_channel=%D7%A7%D7%99%D7%A0%D7%93%D7%A7%D7%A1%D7%9B%D7%9C%D7%99%D7%A0%D7%99%D7%94%D7%95%D7%9C%D7%9E%D7%AA%D7%A7%D7%93%D7%9E%D7%99%D7%9D%D7%9C%D7%91%D7%AA%D7%99%D7%A1%D7%A4%D7%A8"
# try:
#     results = load_data(url=url)
#     print(results)
# except Exception as err:
#     print(f"Error: {err}")
