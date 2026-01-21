# Automatic Notes Maker - Hugging Face Spaces

🎙️ **Live Demo**: Record, transcribe, translate, and analyze audio in 28+ languages!

## Features

- 🎙️ **Live Audio Recording**: Record directly in your browser
- 📂 **File Upload**: Support for MP3 and WAV files
- 🌍 **28+ Languages**: Translate to Hindi, Spanish, French, German, Japanese, and more
- 🗣️ **Text-to-Speech**: Listen to translations in any language
- 🧠 **Smart Analysis**: Extract keywords and generate summaries
- 💾 **Export Options**: Save as TXT, PDF, Word, or Markdown

## How to Use

### 🎙️ Live Recording Tab
1. Click the microphone icon to record or upload an audio file
2. Select your target language (default: Hindi)
3. Enable "Auto-translate" for real-time translation
4. Click "Process Audio" to transcribe and translate
5. Click "Speak Translation" to hear the result

### 🌍 Translation Tab
1. Enter or paste text to translate
2. Select target language
3. Click "Translate" to see the translation and hear it spoken

### 🧠 Analysis Tab
1. Paste text to analyze
2. Adjust number of keywords and summary sentences
3. Click "Analyze" to extract insights

### 💾 Export Tab
1. Paste your text
2. Choose your preferred format (TXT, PDF, Word, Markdown)
3. Download the file

## Supported Languages

English • Spanish • French • German • Italian • Portuguese • Russian • Japanese • Korean • Chinese (Simplified) • Hindi • Arabic • Dutch • Greek • Turkish • Vietnamese • Thai • Polish • Danish • Finnish • Czech • Romanian • Hungarian • Swedish • Indonesian • Hebrew • Bengali • Kannada

## Technical Details

- **Framework**: Gradio
- **Speech Recognition**: Google Speech Recognition API
- **Translation**: Google Translate
- **TTS**: Google Text-to-Speech (gTTS)
- **NLP**: NLTK for analysis

## Local Development

```bash
pip install -r requirements_hf.txt
python app.py
```

## License

MIT License

---

**Made with ❤️ using Gradio and Python**
