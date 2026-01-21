import speech_recognition as sr
try:
    print("PyAudio version:", sr.pyaudio.__version__ if hasattr(sr, 'pyaudio') else "Unknown")
    print("Mics found:", sr.Microphone.list_microphone_names())
except Exception as e:
    print("Error:", e)
