# import necessary libraries and modules
from dotenv import load_dotenv
from utils import *
import streamlit as st

# initialize environment variables from .env file
load_dotenv()

# set up the Streamlit page configuration
st.set_page_config(page_title="Multi-Media Q&A Assistant")

def chat():
    # create a header for the page
    st.header("Multi-Media Q&A Assistant")

    # allow user to upload different types of media
    pdf_files = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)
    audio_files = st.file_uploader("Upload your audios", type=["mp4", "avi", "mov", "m4a", "mp3", "webm"], accept_multiple_files=True)
    yt_video_urls = st.text_input("Enter youtube video URL(s) - separated by commas")
    urls = st.text_input("Enter a web URL(s) - separated by commas")
    
    # dictionary to store knowledge bases indexed by media sources
    knowledge_bases = {}

    # process each PDF file by extracting text and creating a knowledge base
    if pdf_files:
        for pdf in pdf_files:
            text = extract_text_from_pdf(pdf)
            chunks = text_into_chunks(text)
            knowledge_base = create_knowledge_base(chunks)
            if knowledge_base is None:
                continue
            knowledge_bases[f"PDF: {pdf.name}"] = knowledge_base
    
    # process each audio file in a similar way
    if audio_files:
        for audio in audio_files:
            text = extract_text_from_audio(audio)
            chunks = text_into_chunks(text)
            knowledge_base = create_knowledge_base(chunks)
            if knowledge_base is None:
                continue
            knowledge_bases[f"Audio: {audio.name}"] = knowledge_base

    # process each YouTube video URL
    if yt_video_urls:
        for url in yt_video_urls.split(","):
            url = url.strip()
            if url:
                text = extract_text_from_video(url)
                chunks = text_into_chunks(text)
                knowledge_base = create_knowledge_base(chunks)
                if knowledge_base is None:
                    continue
                knowledge_bases[f"Video (YouTube): {url}"] = knowledge_base

    # process each web url
    if urls:
        for url in urls.split(","):
            url = url.strip()
            if url:
                text = extract_text_from_url(url)
                chunks = text_into_chunks(text)
                knowledge_base = create_knowledge_base(chunks)
                if knowledge_base is None:
                    continue
                knowledge_bases[f"web url: {url}"] = knowledge_base

    # dropdown for user to select the media they want to query
    selected_media = st.selectbox("Select a media", list(knowledge_bases.keys()))

    # allow user to ask questions if a media is selected
    if selected_media:
        # retrieve the media's corresponding knowledge base
        knowledge_base = knowledge_bases[selected_media]

        # initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # create a container for the chat history
        chat_container = st.container()

        # show user input
        query = st.text_input("Ask a question about your selected media:")
        if query:
            # add user question to chat history
            st.session_state.chat_history.append({"is_user": True, "text": query})

            # display "Awaiting response..." message with spinner
            with st.spinner("Awaiting response..."):
                try:
                    # answer the question
                    response = answer_question(query, knowledge_base, max_tokens=900)

                    # add assistant's response to chat history
                    st.session_state.chat_history.append({"is_user": False, "text": response})
                except Exception as e:
                    # display error message if an exception occurs
                    st.error(f"Error: {str(e)}")

            # display the chat history to the UI
            with chat_container:
                for message in st.session_state.chat_history:
                    if message["is_user"]:
                        st.write(f"You: {message['text']}")
                    else:
                        st.write(f"Assistant: {message['text']}")
            

if __name__ == '__main__': 
    chat()
