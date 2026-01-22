import gradio as gr
from huggingface_hub import InferenceClient
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
import nltk
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from docx import Document as DocxDocument
import io

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Language mapping
LANGUAGES = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Japanese': 'ja',
    'Korean': 'ko', 'Chinese (Simplified)': 'zh-cn', 'Hindi': 'hi',
    'Arabic': 'ar', 'Dutch': 'nl', 'Greek': 'el', 'Turkish': 'tr',
    'Vietnamese': 'vi', 'Thai': 'th', 'Polish': 'pl', 'Danish': 'da',
    'Finnish': 'fi', 'Czech': 'cs', 'Hungarian': 'hu',
    'Swedish': 'sv', 'Indonesian': 'id', 'Bengali': 'bn',
    'Kannada': 'kn'
}

def transcribe_audio(audio_file):
    if audio_file is None:
        return "Please upload an audio file or record audio."
    
    recognizer = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(audio_file)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
            wav_path = tmp_wav.name
            audio.export(wav_path, format='wav')
        
        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        os.remove(wav_path)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def translate_text(text, target_language):
    if not text or not text.strip():
        return "Please provide text to translate."
    try:
        target_lang = LANGUAGES.get(target_language, 'en')
        if target_lang == 'en' and target_language == 'English':
            return text
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"

def text_to_speech(text, language):
    if not text or not text.strip():
        return None
    try:
        lang_code = LANGUAGES.get(language, 'en')
        tts = gTTS(text=text, lang=lang_code, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_audio:
            audio_path = tmp_audio.name
            tts.save(audio_path)
        return audio_path
    except Exception as e:
        return None

def extract_keywords(text, num_keywords=5):
    if not text or not text.strip():
        return "Please provide text to analyze."
    try:
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]
        if not words: return "No keywords found."
        freq_dist = FreqDist(words)
        keywords = nlargest(num_keywords, freq_dist, key=freq_dist.get)
        return "\n".join([f"{i+1}. {word}" for i, word in enumerate(keywords)])
    except Exception as e:
        return f"Error: {str(e)}"

def generate_summary(text, num_sentences=3):
    if not text or not text.strip():
        return "Please provide text to summarize."
    
    # 1. Try AI Abstractive Summarization (Handles unpunctuated text better)
    try:
        # Use existing HF_TOKEN if available, otherwise anonymous (rate limited but usually fine for demos)
        client = InferenceClient(model="facebook/bart-large-cnn", token=os.getenv("HF_TOKEN"))
        # Map 'num_sentences' roughly to token length (approx 20-30 tokens per sentence)
        max_len = max(30, min(150, num_sentences * 40))
        min_len = max(10, num_sentences * 10)
        
        summary_obj = client.summarization(text, parameters={"min_length": min_len, "max_length": max_len, "truncation": "only_first"})
        
        # InferenceClient.summarization usually returns a SummarizationOutput object or list. 
        # We handle the text extraction safely.
        if hasattr(summary_obj, 'summary_text'):
            return summary_obj.summary_text
        elif isinstance(summary_obj, list) and len(summary_obj) > 0 and 'summary_text' in summary_obj[0]:
             return summary_obj[0]['summary_text']
        else:
             # Fallback if return format is unexpected (e.g. strict string)
             return str(summary_obj).strip()
             
    except Exception as e:
        print(f"AI Summary failed ({e}), falling back to NLTK...")
        
    # 2. Fallback to NLTK Extractive Summarization
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences: return text
        
        stop_words = set(stopwords.words('english'))
        words = [word for word in word_tokenize(text.lower()) if word.isalnum() and word not in stop_words]
        if not words: return text[:500] + "..."
        
        word_freq = FreqDist(words)
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]
        
        summary_sentences = nlargest(num_sentences, sentence_scores.items(), key=lambda x: x[1])
        summary_sentences.sort(key=lambda x: text.find(x[0]))
        return " ".join([s[0] for s in summary_sentences])
    except Exception as e:
        return f"Error: {str(e)}"

def save_as_txt(text):
    if not text: return None
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp:
        tmp.write(text)
        return tmp.name

def save_as_pdf(text):
    if not text: return None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("Automatic Notes Maker", styles['Heading1']), Spacer(1, 12)]
        for paragraph in text.split('\n'):
            if paragraph.strip():
                story.append(Paragraph(paragraph, styles['Normal']))
                story.append(Spacer(1, 12))
        doc.build(story)
        return pdf_path
    except Exception as e: return None

def save_as_docx(text):
    if not text: return None
    try:
        doc = DocxDocument()
        doc.add_heading('Automatic Notes Maker', 0)
        for paragraph in text.split('\n'):
            if paragraph.strip(): doc.add_paragraph(paragraph)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            doc.save(tmp.name)
            return tmp.name
    except Exception as e: return None

def process_audio_and_translate(audio, target_language, auto_translate):
    transcription = transcribe_audio(audio)
    translation = translate_text(transcription, target_language) if auto_translate else ""
    return transcription, translation

def analyze_text(text, num_keywords, num_sentences):
    return extract_keywords(text, num_keywords), generate_summary(text, num_sentences)

# Gradio Interface (Adapted for 4.x)
with gr.Blocks(theme=gr.themes.Soft(), title="Automatic Notes Maker") as demo:
    gr.Markdown("# 🎙️ Automatic Notes Maker\n### Record, Transcribe, Translate, and Analyze")
    
    with gr.Tabs():
        with gr.Tab("🎙️ Live Recording"):
            with gr.Row():
                with gr.Column():
                    audio_input = gr.Audio(label="Record or Upload Audio", type="filepath")
                    target_lang = gr.Dropdown(choices=list(LANGUAGES.keys()), value="Hindi", label="Translate to")
                    auto_translate_check = gr.Checkbox(value=True, label="Auto-translate")
                    process_btn = gr.Button("🎯 Process Audio", variant="primary")
                with gr.Column():
                    transcription_output = gr.Textbox(label="Original Text", lines=5)
                    translation_output = gr.Textbox(label="Translated Text", lines=5)
                    audio_output = gr.Audio(label="Translation Audio", type="filepath")
            
            process_btn.click(process_audio_and_translate, [audio_input, target_lang, auto_translate_check], [transcription_output, translation_output])
            translation_output.change(lambda text, lang: text_to_speech(text, lang), [translation_output, target_lang], audio_output)

        with gr.Tab("🧠 Analysis"):
            with gr.Row():
                with gr.Column():
                    analysis_input = gr.Textbox(label="Input Text", lines=10)
                    num_kw = gr.Slider(3, 15, 5, step=1, label="Keywords")
                    num_sen = gr.Slider(1, 10, 3, step=1, label="Summary Sentences")
                    analyze_btn = gr.Button("📊 Analyze", variant="primary")
                with gr.Column():
                    keywords_out = gr.Textbox(label="Keywords")
                    summary_out = gr.Textbox(label="Summary")
            analyze_btn.click(analyze_text, [analysis_input, num_kw, num_sen], [keywords_out, summary_out])

        with gr.Tab("💾 Export"):
            export_text = gr.Textbox(label="Text to Export", lines=10)
            with gr.Row():
                btn_txt = gr.Button("📄 TXT")
                btn_pdf = gr.Button("📕 PDF")
                btn_docx = gr.Button("📘 Word")
            export_file = gr.File(label="Download")
            btn_txt.click(save_as_txt, export_text, export_file)
            btn_pdf.click(save_as_pdf, export_text, export_file)
            btn_docx.click(save_as_docx, export_text, export_file)

if __name__ == "__main__":
    demo.launch()
