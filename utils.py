# import necessary libraries and modules
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback
from pytube import YouTube
import os
import whisper
import tempfile
from bs4 import BeautifulSoup
import requests

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def extract_text_from_pdf(pdf):
    """
    Extracts text from each page of a pdf.

    Args: 
    pdf (object): A file stream object for the pdf file.

    Returns: 
    str: A string representing the concatenated text from each page of the pdf.
    """
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_audio(audio):
    """
    Transcribes text from an audio file using OpenAI's whisper APIs.

    Args: 
    audio (object): The audio file to be transcribed.

    Returns: 
    str: A string representing the transcribed text of the audio file.
    """
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        temp_audio.write(audio.read())
        audio_path = temp_audio.name

        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        transcribed_text = result["text"]

    return transcribed_text

def extract_text_from_video(url):
    """
    Extracts and transribes audio from a youtube video url.

    Args: 
    url (object): The youtube video file to be transcribed.

    Returns: 
    str: A string representing the transcribed text from the audio of the youtube video.
    """
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, "audio.mp3")
        audio_stream.download(output_path=temp_dir, filename="audio.mp3")

        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        transcribed_text = result["text"]

    return transcribed_text

def extract_text_from_url(url):
    """
    Extracts the text from a web url using BeautifulSoup for html parsing.

    Args:
    url (object): A web url.

    Returns:
    str: A string representing the HTML content of the web page. 
    """
    with requests.get(url) as response:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text() 
    return text

def text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """
    Splits a string of text into chunks of text.

    Args:
    text (str): The text to be split into chunks.
    chunk_size (int): The size we want each chunk to be.
    chunk_overlap (int): How much overlap there is between each chunk

    Returns:
    list of str: a list of chunks.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_knowledge_base(chunks):
    """
    Embeds the chunks of text into searchable knowledge base using OpenAI embeddgins and FAISS vector store.

    Args:
    chunks (list of str): The chunks of texts to be stored in knowledge base.

    Returns:
    FAISS vector store: The knowledge base. 
    """
    if not chunks:
        return None

    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base

def answer_question(query, knowledge_base, max_tokens=900):
    """
    Generates an answer to a question by first performing a semantic search through the knowledge base (to only retrieve information 
    relevant to the query) and using an OpenAI language model to output a context-relevant response.

    Args:
    query (string): The user's question.
    knowledge_base (FAISS vector store): The knowledge base to perform semantic search over.
    max_tokens (int): threshold for length of response

    Returns:
    str: The answer to the user's question
    """
    docs = knowledge_base.similarity_search(query)
    llm = OpenAI(max_tokens=max_tokens) 
    chain = load_qa_chain(llm, chain_type="stuff") 

    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        print(cb)

    return response

