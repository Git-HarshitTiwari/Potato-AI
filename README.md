# Potato AI — Voice Activated Virtual Assistant

Potato AI is a voice-activated personal assistant built entirely in Python. It listens for the wake word "Potato", acknowledges with "Ya", and then processes your spoken command. It is designed to handle everyday tasks like browsing the web, reading the news, checking weather, playing music, and answering questions — all through voice.

---

## How It Works

1. The assistant runs continuously in the background listening for the wake word.
2. Once "Potato" is detected, it responds with "Ya" and starts listening for your command.
3. The command is processed and routed to the appropriate feature — weather, news, music, web search, or OpenAI.
4. The response is spoken back to you using Google Text-to-Speech.

---

## Features

**Wake Word Activation**
Continuously listens for the word "Potato" using the SpeechRecognition library and Google's speech API. Once detected, it activates and waits for a command.

**Voice Response**
All responses are spoken aloud using gTTS (Google Text-to-Speech) combined with pygame for audio playback. This gives a natural-sounding voice without relying on offline engines that conflict with the microphone on Windows.

**Web Browsing**
Opens websites directly in your default browser by voice. Supports Google, YouTube, GitHub, Instagram, Facebook, LinkedIn, Reddit, Gmail, Google Maps, Amazon, Flipkart, Netflix, Spotify, ChatGPT, Stack Overflow, Wikipedia, and Notion. You can also open any website by saying its name.

**Music Playback**
Plays songs by name using a local music library that maps song names to YouTube links. If a song is not in the library, it automatically searches YouTube for it.

**News Headlines**
Fetches and reads the top 5 live headlines using NewsAPI. Supports the following categories:
- General
- Technology
- Sports
- Science
- Business
- Health
- Entertainment

**Weather**
Fetches real-time weather data for any city using the OpenWeatherMap API. Reports temperature, feels-like temperature, humidity, wind speed, and weather condition. You can ask for weather in any city by saying "weather in [city name]".

**OpenAI GPT-3.5-turbo**
Any command that does not match a built-in feature is sent to OpenAI's GPT-3.5-turbo model. It responds as a helpful, conversational assistant. Answers are kept short since they are spoken aloud.

**Web Search**
Performs a Google search for any query by voice and opens the results in the browser.

**Wikipedia**
Opens the Wikipedia page for any topic directly in the browser.

**Time and Date**
Reads the current time and today's full date on request.

**Jokes**
Tells a random joke from a built-in collection of programming and general jokes.

**Voice Quit**
Shut down the assistant completely by saying "goodbye", "bye", "quit", "exit", "stop", "turn off", or "close".

---

## Tech Stack

| Component | Library / Service |
|---|---|
| Voice recognition | SpeechRecognition + Google Speech API |
| Text to speech | gTTS (Google Text-to-Speech) |
| Audio playback | pygame |
| AI responses | OpenAI GPT-3.5-turbo |
| News | NewsAPI |
| Weather | OpenWeatherMap API |
| Web browsing | webbrowser (built-in) |
| HTTP requests | requests |

---

## Requirements

**Python version:** 3.10 or higher

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Dependencies:**
```
SpeechRecognition
gTTS
pygame
openai
requests
pyaudio
```

**PyAudio installation (microphone support):**

PyAudio requires a separate install step depending on your OS.

Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

macOS:
```bash
brew install portaudio
pip install pyaudio
```

Linux:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

---

## API Keys

Three free API keys are required. Sign up at the links below:

| Key | Where to get it |
|---|---|
| OpenAI API Key | https://platform.openai.com/api-keys |
| NewsAPI Key | https://newsapi.org/register |
| OpenWeatherMap Key | https://openweathermap.org/api |

Once you have them, open `potato.py` and paste them into lines 24–27:

```python
OPENAI_API_KEY  = "your-openai-key"
NEWS_API_KEY    = "your-newsapi-key"
WEATHER_API_KEY = "your-openweather-key"
DEFAULT_CITY    = "Your City"
```

Note: New OpenWeatherMap keys take around 10 minutes to activate after signup.

---

## Running the Assistant

```bash
python potato.py
```

Wait for: "Initializing Potato. Say Potato to wake me up."

Then say "Potato", wait for "Ya", and give your command.

---

## Voice Command Examples

| Command | Result |
|---|---|
| "What time is it" | Reads the current time |
| "What is today's date" | Reads today's date |
| "Tell me a joke" | Tells a random joke |
| "Weather in Pune" | Reads Pune's current weather |
| "Open YouTube" | Opens YouTube in browser |
| "Open GitHub" | Opens GitHub in browser |
| "Play believer" | Plays the song on YouTube |
| "Search Python tutorials" | Google searches the query |
| "Tech news" | Reads top technology headlines |
| "Sports news" | Reads top sports headlines |
| "What is artificial intelligence" | GPT answers the question |
| "Wikipedia quantum computing" | Opens Wikipedia page |
| "Goodbye" | Shuts Potato down |

---

## Project Structure

```
Potato-AI/
├── potato.py           Main assistant file
├── musicLibrary.py     Song name to YouTube URL mappings
├── requirements.txt    All required libraries
└── README.md           Project documentation
```

---

## Adding More Songs

Open `musicLibrary.py` and add entries in this format:

```python
music = {
    "song name": "https://www.youtube.com/watch?v=VIDEO_ID",
}
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Assistant does not hear "Potato" | Speak clearly, reduce background noise, lower `energy_threshold` in `main()` to 150 |
| No audio output | Check speaker/headphone connection, verify pygame is installed |
| News returns an error | Double check your NewsAPI key is pasted correctly |
| Weather not working | New OpenWeatherMap keys take up to 10 minutes to activate |
| OpenAI not responding | Check your API key and make sure your account has available credits |
| PyAudio fails to install | Follow the OS-specific steps in the Requirements section above |

---

## Important — Before Pushing to GitHub

Remove your API keys from `potato.py` before committing. Replace them with placeholder text like "YOUR_KEY_HERE" so they are not exposed publicly.
