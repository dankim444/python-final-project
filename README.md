The Multi-Media Q&A Assistant is a versatile application that allows users to ask questions on content from various forms of 
media (ie. pdfs, audios, youtube videos, and web pages). It leverages OpenAI's Whisper for audio transcription, PyPDF2 for PDF text extraction, and OpenAI's language models for generating answers.

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
1. Upload PDFs, audio files, or enter YouTube video URLs and web URLs in the respective input fields.
2. Select a media source from the dropdown menu to ask questions about.
3. Enter your question in the text input field and press Enter.
4. The application will generate a response based on the content of the selected media.
5. The chat history will be displayed below the input field, showing the conversation between the user and the assistant.

## Code structure:

python-final/
├── app.py
├── utils.py
├── tests.py
├── requirements.txt
├── .env
└── test_files/
    ├── sample.pdf
    ├── empty.pdf
    └── test_audio.mp3
