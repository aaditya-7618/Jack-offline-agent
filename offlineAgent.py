import ollama
import soundcard as sc
import soundfile as sf
import os
import time
import speech_recognition as sr
from gtts import gTTS

# Constants
SAMPLE_RATE = 48000
RECORD_SEC = 10
OUTPUT_FILE_NAME = "out.wav"
MP3_FILE_NAME = "output.mp3"

# prompt for llm
PROMPT_TEMPLATE = """  
I will provide you with some text, as follows: "{audioText}".
You need to analyze it and give the best possible answer.
It may include calculations, analysis, or questions.
Respond in simple English using no more than 5 lines.
Do not use asterisks, bullet points, or any opening/closing phrases.
"""

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WAV_PATH = os.path.join(BASE_DIR, OUTPUT_FILE_NAME)
MP3_PATH = os.path.join(BASE_DIR, MP3_FILE_NAME)

# Function to record audio
def record_audio():
    print("\nListening to audio...")
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
        sf.write(file=WAV_PATH, data=data[:, 0], samplerate=SAMPLE_RATE)
    print("Audio recorded and saved.")

# Function to convert audio to text
def transcribe_audio():
    print("Transcribing audio...")
    r = sr.Recognizer()
    try:
        hellow=sr.AudioFile('out.wav')
        with hellow as source:
            audio = r.record(source)
        s = r.recognize_google(audio)
        print("Text: "+s)
        return s
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return ""
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

# Function to query the offline LLM
def get_llm_response(text):
    print("Generating response using LLM...")
    formatted_prompt = PROMPT_TEMPLATE.format(audioText=text)
    response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': formatted_prompt}])
    reply = response['message']['content']
    print(f"LLM Response:\n{reply}")
    return reply

# Function to convert response to speech
def speak_text(text):
    print("Converting response to speech...")
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save(MP3_PATH)
    os.system(f"cvlc --play-and-exit {MP3_PATH}")

# Main loop which keeps the agent running
def run_agent():
    print("Personal Offline Agent Running... Press Ctrl+C to stop.")
    try:
        while True:
            record_audio()
            text = transcribe_audio()
            if text is text.strip():
                response = get_llm_response(text)
                speak_text(response)
            else:
                print("No valid audio input detected.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAgent stopped")

if __name__ == "__main__":
    run_agent()

