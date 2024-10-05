The Multi-Media Q&A Assistant is a versatile application that allows users to ask questions on content from various forms of 
media (ie. pdfs, audios, youtube videos, and web pages). It leverages OpenAI's Whisper for audio transcription, PyPDF2 for PDF text extraction, and OpenAI's language models for generating answers.

## Features
- **Transcription & Extraction:** Transcribe audio files or extract text from PDFs.
- **Question and answering:** Ask questions about content from different media types.
- **Interactive Chat:** View the conversation between the user and the assistant with the chat history feature.

## Installation instructions:
1. Create a virtual environment: 
python3 -m venv venv
source venv/bin/activate

2. Install the required dependencies via this command:
pip install -r requirements.txt

3. Create a .env file in the project root directory. Add the following line to the .env file, replacing YOUR_API_KEY with your actual OpenAI API key:
OPENAI_API_KEY=YOUR_API_KEY

4. Run the application by typing 'streamlit run app.py' into your terminal.

## Usage:
1. **Upload media:** Upload a PDF, audio file, or provide a YouTube video URL or web URL in the respective input field.
2. **Select media source:** Choose a media source from the dropdown menu to ask questions about.
3. **Ask your question:** Enter your question in the text input field and press enter.
4. **View response:** The app will analyze the selected media and generate a response.
5. **Chat history:** The conversation between the user and the assistant will be displayed below the input field.

## Code structure:
```
root/
├── app.py
├── utils.py
├── tests.py
├── requirements.txt
├── .env
└── test_files/
    ├── sample.pdf
    ├── empty.pdf
    └── test_audio.mp3
```
