# Automatic Notes Maker 📝🎙️

A professional desktop application for recording, transcribing, translating, and analyzing audio content. Built with Python and CustomTkinter with a modern dark theme UI.

![App Screenshot](https://via.placeholder.com/800x500?text=Automatic+Notes+Maker+UI)

## ✨ Key Features

### 🎙️ Live Recording Tab
- **Real-time Speech-to-Text**: Transcribe microphone input as you speak
- **Auto-Translate**: Automatic real-time translation (enabled by default)
- **28+ Languages**: Translate to Hindi, Spanish, French, German, Japanese, Korean, Chinese, Arabic, and more
- **Multi-Language TTS**: Speak translations in any language using Google AI voices
- **Ambient Noise Adjustment**: Automatically adjusts for background noise

### 📂 File Processing Tab
- **Audio Format Support**: Process both **MP3** and **WAV** files
- **Long Audio Handling**: Automatic chunking for files longer than 60 seconds
- **Audio Cleaning**: Normalize audio for better transcription accuracy
- **Batch Processing**: Load, clean, transcribe, and translate audio files

### 🧠 Analysis Tab
- **Keyword Extraction**: Extract top N keywords from transcribed text using NLP
- **Smart Summarization**: Generate concise summaries from long transcripts
- **Frequency Analysis**: Identify most important words and phrases
- **Import from Live/File**: Easily import text from other tabs for analysis
- **Customizable Output**: Choose number of keywords and summary sentences

### 🗣️ Text-to-Speech (TTS)
- **Multi-Language Support**: Speak text in 28+ languages
- **Google AI Voices**: Natural-sounding speech using gTTS
- **Playback Control**: Start/stop speech playback
- **Works on All Tabs**: Available in both Live Recording and File Processing

### 💾 Professional Export Options
- **TXT**: Plain text format
- **PDF**: Professional formatted documents with ReportLab
- **Word (.docx)**: Microsoft Word compatible documents
- **Markdown**: Notion-ready markdown format

### 🎨 Modern UI
- **Dark Theme**: Comfortable cyberpunk-inspired dark mode
- **Tabbed Interface**: Organized workflow with 3 main tabs
- **Status Updates**: Real-time feedback on all operations
- **Responsive Design**: Smooth threading for non-blocking UI

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for translation and Google TTS)
- Microphone (for live recording)

### Setup Steps

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/yourusername/automatic-notes-maker.git
   cd automatic-notes-maker
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (automatic on first run):
   The app will automatically download required NLTK packages (punkt, stopwords) on first launch.

## 🏃 Usage

### Running the Application
```bash
python main.py
```

### Live Recording Workflow
1. **Select target language** from dropdown (default: Hindi)
2. **Enable "Auto-translate"** checkbox (enabled by default)
3. **Click "Start Recording"** and speak clearly in English
4. Watch your speech appear in "Original Text"
5. See automatic translation in "Translated Text" in real-time
6. **Click "Stop"** when finished
7. **Optional**: Click "Speak Translation" to hear the translated text
8. **Save** your work in your preferred format

### File Processing Workflow
1. **Click "Load Audio"** and select an MP3 or WAV file
2. Wait for transcription (long files are automatically chunked)
3. **Select target language** from dropdown
4. **Click "Translate"** to translate the transcribed text
5. **Optional**: Click "Speak Translation" to hear it
6. **Save** your work

### Analysis Workflow
1. **Import text** from Live or File tab (or paste directly)
2. **Set number of keywords** (default: 5)
3. **Set summary sentences** (default: 3)
4. **Click "Extract Keywords"** to see most important words
5. **Click "Generate Summary"** to create a concise summary
6. **Save Results** to export analysis

## 🌍 Supported Languages

English • Spanish • French • German • Italian • Portuguese • Russian • Japanese • Korean • Chinese (Simplified) • Hindi • Arabic • Dutch • Greek • Turkish • Vietnamese • Thai • Polish • Danish • Finnish • Czech • Romanian • Hungarian • Swedish • Indonesian • Hebrew • Bengali • Kannada

## 📦 Dependencies

```
customtkinter>=5.0.0
SpeechRecognition>=3.10.0
googletrans==4.0.0-rc1
gTTS>=2.3.0
pygame>=2.5.0
pyttsx3>=2.90
pydub>=0.25.1
nltk>=3.8
reportlab>=4.0.0
python-docx>=0.8.11
CTkMessagebox>=2.5
```

## ❓ Troubleshooting

### Microphone Not Working
**Windows**: Microphone access is restricted by default.
1. Go to **Settings** → **Privacy & Security** → **Microphone**
2. Enable **"Microphone access"**
3. Enable **"Let desktop apps access your microphone"**

### Translation Not Working
- **Check internet connection** (Google Translate API requires internet)
- Ensure `googletrans==4.0.0-rc1` is installed correctly
- Try reinstalling: `pip install --upgrade googletrans==4.0.0-rc1`

### TTS Audio Device Error
If you see "Invalid audio device ID":
- This is a pygame warning and can be safely ignored
- TTS will still work correctly
- The warning appears during pygame initialization

### MP3 Files Not Processing
- Ensure `ffmpeg` is in the same directory as `main.py`
- Or install ffmpeg system-wide and add to PATH
- Alternatively, convert MP3 to WAV using an online converter

### NLTK Data Missing
The app automatically downloads required NLTK data on first run. If you encounter errors:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

## 🎯 Use Cases

- **Students**: Record lectures and get automatic summaries with keywords
- **Journalists**: Transcribe interviews and translate to multiple languages
- **Content Creators**: Generate subtitles and translations for videos
- **Researchers**: Analyze long audio recordings and extract key insights
- **Language Learners**: Practice pronunciation with TTS in target language
- **Meeting Notes**: Record meetings and get actionable summaries

## 🔧 Technical Details

### Architecture
- **GUI Framework**: CustomTkinter (modern CTk widgets)
- **Speech Recognition**: Google Speech Recognition API
- **Translation**: Google Translate via googletrans
- **TTS Engine**: gTTS (Google Text-to-Speech) + pygame for playback
- **NLP**: NLTK for tokenization, stopwords, and frequency analysis
- **Audio Processing**: pydub with ffmpeg backend

### Threading Model
All long-running operations (recording, translation, TTS, file processing) run in background threads to keep the UI responsive.

## 📝 License

[MIT License](https://choosealicense.com/licenses/mit/)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ using Python and CustomTkinter**

