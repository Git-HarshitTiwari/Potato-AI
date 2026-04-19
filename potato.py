"""
Potato AI - Voice Activated Virtual Assistant
============================================
Wake word: "Potato"
Fix log: Replaced pyttsx3 with gTTS+pygame (fixes audio conflicts on Windows)
         Improved microphone sensitivity and noise handling
"""

import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
import os
import datetime
import random
import time
from gtts import gTTS
import pygame
from openai import OpenAI

# ──────────────────────────────────────────────
#  CONFIGURATION — Fill these in
# ──────────────────────────────────────────────
OPENAI_API_KEY  = "API KEY PLEASE"
NEWS_API_KEY    = "API KEY PLEASE"
WEATHER_API_KEY = "API KEY PLEASE"
DEFAULT_CITY    = "Nagpur"

# ──────────────────────────────────────────────
#  SPEECH — gTTS + pygame
# ──────────────────────────────────────────────
pygame.mixer.init()

def speak(text: str):
    print(f"[Potato]: {text}")
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("potato_response.mp3")
        pygame.mixer.music.load("potato_response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        time.sleep(0.3)
        pygame.mixer.music.unload()
        os.remove("potato_response.mp3")
    except Exception as e:
        print(f"[Speak Error]: {e}")

# ──────────────────────────────────────────────
#  OPENAI
# ──────────────────────────────────────────────
client = OpenAI(api_key=OPENAI_API_KEY)

def aiProcess(command: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Potato, a helpful, witty, and friendly voice assistant. "
                        "Keep answers concise, 2 to 3 sentences max, since they will be spoken aloud. "
                        "Avoid bullet points, markdown, symbols, or special characters."
                    ),
                },
                {"role": "user", "content": command},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "I could not reach OpenAI right now. Please check your API key or internet connection."

# ──────────────────────────────────────────────
#  NEWS
# ──────────────────────────────────────────────
def fetchNews(category: str = "general") -> list:
    try:
        # Use country=in for India-based results, remove language param
        # (combining language+category+country can return 0 articles on free tier)
        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?country=in&category={category}&pageSize=5&apiKey={NEWS_API_KEY}"
        )
        r = requests.get(url, timeout=8)
        data = r.json()
        print(f"[News API Status]: {data.get('status')} | Total: {data.get('totalResults', 0)}")
        if data.get("status") != "ok":
            msg = data.get("message", "Unknown error")
            print(f"[News Error]: {msg}")
            return [f"News fetch failed. Reason: {msg}"]
        articles = data.get("articles", [])
        if not articles:
            # Fallback: try without category filter
            url2 = (
                f"https://newsapi.org/v2/top-headlines"
                f"?country=in&pageSize=5&apiKey={NEWS_API_KEY}"
            )
            r2 = requests.get(url2, timeout=8)
            data2 = r2.json()
            articles = data2.get("articles", [])
        if not articles:
            return ["No headlines found right now. Please try again later."]
        return [a["title"] for a in articles if a.get("title")]
    except Exception as e:
        print(f"[News Exception]: {e}")
        return ["Sorry, I could not connect to the news service. Check your NewsAPI key."]

def readNews(category: str = "general"):
    speak(f"Here are the top {category} headlines.")
    headlines = fetchNews(category)
    for i, headline in enumerate(headlines, 1):
        speak(f"Headline {i}. {headline}")

# ──────────────────────────────────────────────
#  WEATHER
# ──────────────────────────────────────────────
def extractCity(command: str) -> str:
    """Extract city name from a weather command."""
    c = command.lower()
    # Handle: "weather in Mumbai", "weather of Delhi", "weather for Pune"
    for keyword in [" in ", " of ", " for ", " at "]:
        if keyword in c:
            city = c.split(keyword)[-1].strip()
            # Remove trailing words like "today", "now", "please"
            for trailing in ["today", "now", "please", "currently"]:
                city = city.replace(trailing, "").strip()
            if city:
                return city.title()
    return DEFAULT_CITY

def fetchWeather(city: str = DEFAULT_CITY) -> str:
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        r = requests.get(url, timeout=5)
        data = r.json()
        cod = data.get("cod")
        # cod can be int 200 or string "200"
        if str(cod) != "200":
            return (
                f"Sorry, I could not find weather data for {city}. "
                f"Please check the city name and try again."
            )
        desc    = data["weather"][0]["description"]
        temp    = data["main"]["temp"]
        feels   = data["main"]["feels_like"]
        humid   = data["main"]["humidity"]
        wind    = data["wind"]["speed"]
        country = data["sys"]["country"]
        return (
            f"In {city}, {country}, it is currently {desc}. "
            f"Temperature is {temp:.1f} degrees Celsius, feels like {feels:.1f} degrees. "
            f"Humidity is {humid} percent and wind speed is {wind} meters per second."
        )
    except Exception as e:
        print(f"[Weather Error]: {e}")
        return "I could not connect to the weather service. Please check your OpenWeatherMap API key."

# ──────────────────────────────────────────────
#  JOKES
# ──────────────────────────────────────────────
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "What do you call a fake noodle? An impasta!",
    "Why did the developer go broke? Because he used up all his cache.",
    "I would tell you a construction joke, but I am still working on it.",
    "Why do Python programmers wear glasses? Because they cannot C.",
    "How many programmers does it take to change a light bulb? None, that is a hardware problem.",
    "Why was the computer cold? Because it left its Windows open.",
]

def tellJoke():
    speak(random.choice(JOKES))

# ──────────────────────────────────────────────
#  TIME & DATE
# ──────────────────────────────────────────────
def tellTime():
    now = datetime.datetime.now()
    speak(f"The current time is {now.strftime('%I:%M %p')}.")

def tellDate():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A, %B %d, %Y')}.")

# ──────────────────────────────────────────────
#  WEBSITES & NEWS CATEGORIES
# ──────────────────────────────────────────────
SITES = {
    "google":         "https://www.google.com",
    "youtube":        "https://www.youtube.com",
    "facebook":       "https://www.facebook.com",
    "linkedin":       "https://www.linkedin.com",
    "github":         "https://www.github.com",
    "instagram":      "https://www.instagram.com",
    "twitter":        "https://www.twitter.com",
    "reddit":         "https://www.reddit.com",
    "wikipedia":      "https://www.wikipedia.org",
    "stack overflow": "https://www.stackoverflow.com",
    "chatgpt":        "https://chat.openai.com",
    "gmail":          "https://mail.google.com",
    "maps":           "https://www.google.com/maps",
    "amazon":         "https://www.amazon.in",
    "flipkart":       "https://www.flipkart.com",
    "netflix":        "https://www.netflix.com",
    "spotify":        "https://www.spotify.com",
    "notion":         "https://www.notion.so",
}

NEWS_CATEGORIES = {
    "technology news":    "technology",
    "technical news":     "technology",
    "tech news":          "technology",
    "sports news":        "sports",
    "science news":       "science",
    "business news":      "business",
    "health news":        "health",
    "entertainment news": "entertainment",
    "latest news":        "general",
    "daily news":         "general",
    "top news":           "general",
    "headlines":          "general",
    "news":               "general",
}

# ──────────────────────────────────────────────
#  COMMAND PROCESSOR
# ──────────────────────────────────────────────
def processCommand(command: str):
    c = command.lower().strip()
    print(f"[Command]: {c}")

    if any(w in c for w in ["hello", "hi", "hey"]):
        speak("Hello! How can I help you today?")
        return

    if "time" in c:
        tellTime(); return

    if "date" in c or "what day" in c:
        tellDate(); return

    if "joke" in c:
        tellJoke(); return

    if "weather" in c:
        city = extractCity(c)
        speak(fetchWeather(city)); return

    for phrase in sorted(NEWS_CATEGORIES, key=len, reverse=True):
        if phrase in c:
            readNews(NEWS_CATEGORIES[phrase]); return

    if c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}.")
            webbrowser.open(link)
        else:
            speak(f"I do not have {song} in my library. Searching YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        return

    if c.startswith("open"):
        target = c.replace("open", "").strip()
        if target in SITES:
            speak(f"Opening {target}.")
            webbrowser.open(SITES[target])
        else:
            speak(f"Opening {target}.")
            webbrowser.open(f"https://www.{target}.com")
        return

    if c.startswith("search"):
        query = c.replace("search", "").strip()
        speak(f"Searching for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return

    if "wikipedia" in c:
        query = c.replace("wikipedia", "").replace("search", "").strip()
        speak(f"Opening Wikipedia for {query}.")
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
        return

    if any(w in c for w in ["stop", "exit", "quit", "goodbye", "bye", "shut down", "turn off", "close"]):
        speak("Goodbye! Shutting down Potato. Have a great day!")
        pygame.mixer.quit()
        os._exit(0)

    speak("Let me think about that.")
    response = aiProcess(command)
    speak(response)

# ──────────────────────────────────────────────
#  MICROPHONE LISTENERS
# ──────────────────────────────────────────────
def listenForWakeWord(recognizer: sr.Recognizer):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"[Wake Error]: {e}")
        return None

def listenForCommand(recognizer: sr.Recognizer):
    try:
        with sr.Microphone() as source:
            print("[Potato]: Listening for your command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        speak("I did not hear anything. Say Potato again when ready.")
        return None
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that. Please try again.")
        return None
    except Exception as e:
        print(f"[Command Error]: {e}")
        return None

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.8

    speak("Initializing Potato. Say Potato to wake me up.")
    print("\n[System]: Potato AI is running. Say 'Potato' to activate.\n")

    while True:
        word = listenForWakeWord(recognizer)

        if word and "potato" in word.lower():
            speak("Ya")
            command = listenForCommand(recognizer)
            if command:
                processCommand(command)
        elif word:
            print(f"[Heard]: {word}")

if __name__ == "__main__":
    main()
