# Jack-offline-agent
This project is a **voice-based offline assistant** that listens, transcribes, analyzes using a local LLM, and responds via text-to-speech. It's designed to run in a local environment using tools like `Ollama`, `gTTS`, and `speech_recognition`.

## Features
- Captures system audio using loopback
- Transcribes speech to text using Google Speech Recognition
- Analyzes text with an offline LLM (LLaMA3 via Ollama)
- Responds with speech using `gTTS`
- Continuously listens until interrupted manually

## 🛠Tech Stack
- `Python 3.12+`
- [Ollama](https://ollama.com) (running a model like `llama3`)
- `speech_recognition` for audio transcription
- `soundcard` + `soundfile` for capturing and saving audio
- `gTTS` for converting response text to speech
- `cvlc` (VLC command-line player) for playback
