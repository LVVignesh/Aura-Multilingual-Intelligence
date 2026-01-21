# Mic Debug Task
import speech_recognition as sr
import pyaudio

p = pyaudio.PyAudio()
print("Available Audio Devices:")
for i in range(p.get_device_count()):
    try:
        dev = p.get_device_info_by_index(i)
        # Filter for inputs
        if dev.get('maxInputChannels') > 0:
            print(f"Index {i}: {dev.get('name')} - Channels: {dev.get('maxInputChannels')}")
            # Try initializing to test
            try:
                 mic = sr.Microphone(device_index=i)
                 with mic as source:
                     print(f"  -> SUCCESS: Device {i} initialized cleanly.")
            except Exception as e:
                print(f"  -> WARNING: Device {i} failed init: {e}")
    except Exception as e:
        print(f"Error accessing device {i}: {e}")

p.terminate()
