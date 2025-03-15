# Kindix Customer Support Chatbot

## Overview
The **Kindix Customer Support Chatbot** is an AI-powered chatbot designed to provide efficient customer service and support. The chatbot is built using **FastAPI**, **FAISS Vector Database**, and **Google Generative AI**, leveraging **RAG (Retrieval-Augmented Generation)** to process and retrieve information from documents and video transcripts.

## Features
- Extracts text from **documents (PDF, DOCX, TXT)** and **YouTube videos**.
- Stores processed data in **FAISS Vector Database** for efficient retrieval.
- Utilizes **Google Generative AI** for intelligent conversational responses.
- Provides a **FastAPI-based REST API** for adding data and interacting with the chatbot.
- Supports **multilingual customer interactions**, including **English and Arabic**.
- Integrate with **MySQL** to Save Chat-history.
- Integrates with **WhatsApp** for direct customer communication.

---

## Installation & Setup

### 1. Prerequisites
Ensure you have the following installed:
- **Python 3.10+**
- **pip** (Python package manager)
- **Docker** (optional, for containerized deployment)

### 2. Clone Repository
```bash
# Clone the repository
git clone https://github.com/kindix/+++++++++.git # Note support
cd +++++++++
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file based on `.env.example` and set the required API keys.
```bash
cp .env.example .env
```
Ensure the following keys are set:
- `GOOGLE_API_KEY` (for Google Generative AI)
- `DB_HOST` 
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DB_PORT`

### 5. Create MySQL-DB.
* Create Database --> rag-customer-support
* Create Table
```sql
CREATE TABLE chat_history (
    id INT(11) NOT NULL AUTO_INCREMENT,
    user_query TEXT NOT NULL,
    chatbot_answer TEXT NOT NULL,
    user_id VARCHAR(255) DEFAULT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```
### 5. Run the Application
```bash
uvicorn backend:app --reload
```

---

## API Endpoints

### 1. Add Data (Documents / YouTube Transcripts)
**Endpoint:** `POST /add_data`

#### Request (Upload Document)
```python
import requests
url = "http://127.0.0.1:8000/add_data"
# url = "http://localhost:8000/add_data" # Docker
files = {"files_data": ("1page.pdf", open(r"1page.pdf", "rb"), "application/pdf")}
data = {"url": "", "case": "Document"}
response = requests.post(url, files=files, data=data, headers={"accept": "application/json"})
print(response.json())
```

#### Request (Process YouTube URL)
```python
import requests
url = "http://127.0.0.1:8000/add_data"
# url = "http://localhost:8000/add_data" # Docker
data = {
    "url": "https://www.youtube.com/watch?v=Rjw1319nwrQ&ab_channel=NewMediaAcademyLife", "case": "URL"}
headers = {"accept": "application/json"}
response = requests.post(url, data=data, headers=headers)
print(response.json())
```

### 2. Chat with the AI
**Endpoint:** `POST /get_response`

#### Request
```python
import requests
url = "http://127.0.0.1:8000/get_response"
# url = "http://localhost:8000/get_response" # Docker
data = {
    "user_query": "Hi", # User-query
    "user_id": "none" # User-ID from WhatsAPP
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}
response = requests.post(url, data=data, headers=headers)
print(response.json())
```

#### Response:
```python
{"messege": {"answer": chat-bot-answer, "video-url": url}}
```

---

## Architecture
![RAG-Customer-support](./img/RAG%20-%20customer%20support.jpg)
### 1. **Backend**
- **FastAPI**: Lightweight and fast backend framework.
- **FAISS**: Used for storing and retrieving vector embeddings of processed documents.
- **Google Generative AI**: Provides intelligent responses.

### 2. **Data Processing**
- `Load_data.py`: Handles document and YouTube transcript extraction.
- `Vector_db.py`: Manages FAISS database operations.
- `Full_chain.py`: Implements the chatbot’s conversational retrieval mechanism.
- `MySQL_DB.py`: Implements the connection for MySQL Database.

---

## Deployment

### Docker Setup
```bash
# Build and run Docker container
# Before you run this in local need to host DB and change host.
docker build -t kindix-chatbot .
docker run -p 8000:8000 --env-file .env kindix-chatbot
# docker run -p 8000:8000 kindix-chatbot
```

---

## Contact & Support
- **Website:** [Kindix](https://kindix.me/)
- **Email:** [sales@kindix.me](mailto:sales@kindix.me)
- **Phone:** +08-675-9660 (English), 050-444-6785 (Arabic)

---

## License
This project is proprietary and maintained by **Kindix**. Unauthorized distribution is prohibited.