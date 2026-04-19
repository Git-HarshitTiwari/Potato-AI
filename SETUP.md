# 🥔 Potato AI — Complete Setup Guide

## Project Structure

```
potato_ai/
│
├── potato.py          ← Main assistant (run this)
├── musicLibrary.py    ← Song name → URL mapping
├── requirements.txt   ← All dependencies
└── SETUP.md           ← This file
```

---

## Step 1 — Install Python

Make sure you have **Python 3.10 or higher**.

```bash
python --version
```

---

## Step 2 — Install PyAudio (Microphone Support)

PyAudio is tricky. Follow your OS:

### Windows
```bash
pip install pipwin
pipwin install pyaudio
```
If that fails, download the right `.whl` from:
👉 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

Then install it:
```bash
pip install PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl
```

### macOS
```bash
brew install portaudio
pip install pyaudio
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

## Step 3 — Install All Other Libraries

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install SpeechRecognition pyttsx3 openai requests gTTS pygame
```

---

## Step 4 — Get Your API Keys

### 1. OpenAI API Key
- Go to: https://platform.openai.com/api-keys
- Click **"Create new secret key"**
- Copy the key (starts with `sk-...`)

### 2. NewsAPI Key (Free)
- Go to: https://newsapi.org/register
- Sign up for free
- Copy your API key from the dashboard

### 3. OpenWeatherMap Key (Free)
- Go to: https://home.openweathermap.org/users/sign_up
- Sign up and verify email
- Go to **API keys** tab and copy your default key
- Note: New keys take ~10 minutes to activate

---

## Step 5 — Configure potato.py

Open `potato.py` and fill in these lines at the top:

```python
OPENAI_API_KEY   = "sk-..."                    # Your OpenAI key
NEWS_API_KEY     = "abc123..."                 # Your NewsAPI key
WEATHER_API_KEY  = "xyz789..."                 # Your OpenWeatherMap key
DEFAULT_CITY     = "Mumbai"                    # Your city
```

---

## Step 6 — VS Code Setup

### Install Python Extension
- Open VS Code
- Press `Ctrl+Shift+X` → Search `Python` → Install Microsoft's Python extension

### Select the Right Interpreter
- Press `Ctrl+Shift+P`
- Type: `Python: Select Interpreter`
- Choose the Python version where you installed all libraries (usually the default one)

### Open the Project Folder
```
File → Open Folder → select your potato_ai folder
```

### Run the Assistant
- Open `potato.py`
- Press `F5` or click the ▶ Run button
- OR open Terminal (`Ctrl+`) and run:

```bash
python potato.py
```

---

## Step 7 — Test It

1. Run `potato.py`
2. Wait for: **"Initializing Potato. Say Potato to activate me."**
3. Say **"Potato"** clearly
4. Potato replies **"Ya"** — now give a command!

---

## Example Commands

| Say this | What happens |
|---|---|
| `Potato` | Wakes up, says "Ya" |
| `What time is it` | Reads current time |
| `Tell me today's date` | Reads today's date |
| `Open YouTube` | Opens YouTube in browser |
| `Open GitHub` | Opens GitHub |
| `Play believer` | Plays Imagine Dragons on YouTube |
| `Search Python tutorials` | Googles the query |
| `What's the weather` | Reads your city's weather |
| `Weather in Delhi` | Reads Delhi's weather |
| `Tell me the news` | Reads top general headlines |
| `Tech news` | Reads technology headlines |
| `Sports news` | Reads sports headlines |
| `Tell me a joke` | Tells a random joke |
| `What is machine learning` | Asks GPT, reads answer |
| `Goodbye` | Shuts Potato down |

---

## Why "Ya" Wasn't Working — The Fix Explained

Your original code had this issue:

```python
# ❌ PROBLEM: phrase_time_limit=1 — only 1 second to hear "potato"
audio = r.listen(source, timeout=2, phrase_time_limit=1)
```

One second is too short to recognize a two-syllable word reliably. The fix:

```python
# ✅ FIX: Give 3 seconds, adjust for ambient noise
recognizer.adjust_for_ambient_noise(source, duration=0.3)
audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
```

Also, `processCommand()` was called **without** passing `command` — that would crash:
```python
# ❌ Bug: missing argument
processCommand()

# ✅ Fixed:
processCommand(command)
```

---

## Add More Songs

Edit `musicLibrary.py`:

```python
music = {
    "your song name": "https://www.youtube.com/watch?v=VIDEO_ID",
    # add more...
}
```

---

## Add More Websites

In `potato.py`, add to the `SITES` dictionary:

```python
SITES = {
    "netflix": "https://www.netflix.com",
    "notion":  "https://www.notion.so",
    # ...
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'pyaudio'` | Follow Step 2 above |
| Potato doesn't hear "Potato" | Speak louder, reduce background noise, try lowering `energy_threshold` to `200` |
| "Ya" plays but cuts off | Your speaker/headphone setup. Try gTTS instead (see commented code in `potato.py`) |
| GPT not working | Check your OpenAI key and account credits |
| News returns error | Verify your NewsAPI key is pasted correctly |

---

## Optional: Better Voice with gTTS

If `pyttsx3` sounds robotic, switch to gTTS. In `potato.py`, comment out the pyttsx3 `speak()` function and uncomment the gTTS one. You'll also need:

```bash
pip install gtts pygame
```

gTTS requires internet but sounds much more natural.
