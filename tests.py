# import necessary libraries and modules
import unittest
from unittest.mock import patch, MagicMock
from utils import *

"""
Unit tests functions in utils.py
"""
class TestUtils(unittest.TestCase):
    # test extract_text_from_pdf on valid pdf
    def test_extract_text_valid_pdf(self):
        with open("test_files/sample.pdf", "rb") as file:
            text = extract_text_from_pdf(file)
        self.assertIn("This is a sample PDF for testing.", text)

    # test extract_text_from_pdf on an empty pdf (no content)
    def test_extract_text_empty_pdf(self):
        with open("test_files/empty.pdf", "rb") as file:
            text = extract_text_from_pdf(file)
        self.assertEqual("", text)
    
    # test extract_text_from_audio on a valid audio file
    @patch('utils.whisper') 
    def test_extract_text_valid_audio(self, mock_whisper):
        mock_model = MagicMock()
        mock_whisper.load_model.return_value = mock_model 
        mock_model.transcribe.return_value = {"text": "expected transcribed text"} # simulates transcribing audio file without actually processing one
        with open("test_files/test_audio.mp3", "rb") as file:
            text = extract_text_from_audio(file)
        self.assertEqual("expected transcribed text", text)
    
    # test extract_text_from_video on a valid youtube url
    @patch('utils.YouTube')
    @patch('utils.whisper')
    def test_extract_text_valid_video(self, mock_whisper, mock_youtube):
        mock_model = MagicMock()
        mock_whisper.load_model.return_value = mock_model
        mock_model.transcribe.return_value = {"text": "expected video text"} # sets the expected transcribed text 
        mock_youtube.return_value.streams.filter.return_value.first.return_value.download.return_value = "downloaded path"
        text = extract_text_from_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual("expected video text", text)

    # test extract_text_from_url on a valid webpage
    @patch('utils.requests.get')
    def test_extract_text_from_url(self, mock_get):
        mock_get.return_value.__enter__.return_value.text = "<html><body>Sample Text</body></html>"
        text = extract_text_from_url("https://en.wikipedia.org/wiki/Chess")
        self.assertIn("Sample Text", text)

    def test_text_into_chunks(self):
        text = "this is a test text " * 20  
        chunks = text_into_chunks(text, chunk_size=50, chunk_overlap=10)
        self.assertIsNotNone(chunks) 

    @patch('utils.FAISS.from_texts')
    @patch('utils.OpenAIEmbeddings')
    def test_create_knowledge_base(self, mock_embeddings, mock_fais):
        chunks = ["chunk1", "chunk2"]
        knowledge_base = create_knowledge_base(chunks)
        self.assertIsNotNone(knowledge_base)

if __name__ == '__main__':
    unittest.main()

