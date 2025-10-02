# 🎙️ Leadership Transcriber

This project combines **OpenAI Whisper** (speech-to-text) with **Pyannote.audio** (speaker diarization)
to transcribe meeting recordings and label speakers.

It was designed as part of a **leadership feedback project** — transcripts generated here can be analyzed
with AI (like ChatGPT) using the **Leadership Pattern framework** (Operational Talents).

---

## 🚀 Features

* ✅ Transcribes meeting audio into text using Whisper
* ✅ Separates speakers automatically with Pyannote.audio
* ✅ Outputs a labeled transcript like:

```
[Speaker 0] Let's start the meeting by reviewing yesterday's progress.  
[Speaker 1] I think we should prioritize the budget issue.  
[Speaker 0] Agreed, let's focus on that first.  
```

---

## 🎯 Quick Start Options

**Option 1: Desktop App (Easiest)**
- Download the standalone executable (no Python required!)
- Double-click to run the GUI application
- See [Desktop App](#-desktop-application) section below

**Option 2: Command Line**
- For developers and advanced users
- See [Setup](#️-setup) and [Usage](#️-usage) sections below

## 📂 Project Structure

```
leadership-transcriber/
│
├── audio/                 # put your audio files here
├── requirements.txt       # Python dependencies
├── transcribe.py          # main script (runs Whisper + Pyannote)
├── utils.py               # helper functions for merging
├── gui.py                 # desktop GUI application
├── build_app.py           # build script for desktop app
└── README.md              # this file
```

---

## 🖥️ Desktop Application

### For End Users (No Python Required!)

1. **Download** the latest release from the [Releases page](https://github.com/sthcst/leadership-transcriber/releases)
2. **Run** the executable:
   - Windows: `Leadership-Transcriber.exe`
   - Mac: `Leadership-Transcriber.app`
3. **Enter your Hugging Face token** (get it free at [huggingface.co](https://huggingface.co/))
4. **Select your audio file** and click "Start Transcription"
5. **Save results** when complete

### For Developers (Build from Source)

```bash
# Install additional dependencies
pip install pyinstaller pillow

# Build desktop app
python build_app.py

# Your executable will be in dist/ folder
```

---

## ⚙️ Setup (Command Line)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/leadership-transcriber.git
cd leadership-transcriber
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

Whisper requires FFmpeg.

* **Windows (PowerShell):**

  ```powershell
  winget install Gyan.FFmpeg
  ```
* **macOS (Homebrew):**

  ```bash
  brew install ffmpeg
  ```
* **Ubuntu/Debian:**

  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

### 5. Hugging Face token (for Pyannote)

1. Sign up at [huggingface.co](https://huggingface.co/) (free).
2. Accept model terms for `pyannote/speaker-diarization`.
3. Copy your access token from your account settings.
4. Set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN = "your_token_here"
# Or permanently:
[System.Environment]::SetEnvironmentVariable("HF_TOKEN", "your_token_here", "User")
```

**macOS/Linux (bash/zsh):**
```bash
export HF_TOKEN="your_token_here"
# Or permanently add to ~/.bashrc or ~/.zshrc:
echo 'export HF_TOKEN="your_token_here"' >> ~/.bashrc
```

---

## ▶️ Usage

Put your audio file in the `audio/` folder. Example: `audio/meeting1.mp3`

Run:

```bash
python transcribe.py audio/meeting1.mp3 --whisper_model base
```

Options:

* `--whisper_model` = tiny | base | small | medium | large

**Note:** The script automatically detects your operating system and applies appropriate optimizations for Windows or macOS/Linux.

---

## 📊 Output

You’ll see a combined transcript + speaker diarization:

```
===== MERGED TRANSCRIPT =====

[Speaker 0] Let's start the meeting by reviewing yesterday's progress.  
[Speaker 1] I think we should prioritize the budget issue.  
[Speaker 0] Agreed, let's focus on that first.  
```

---

## � Platform Compatibility

This project works on:

* ✅ **Windows** (tested on Windows 11)
* ✅ **macOS** (Intel and Apple Silicon)
* ✅ **Linux** (Ubuntu, Debian, etc.)

The script automatically detects your operating system and applies platform-specific optimizations. No manual configuration needed!

---

## �📝 Notes

* Whisper provides transcription only; Pyannote adds speaker diarization.
* Current merging logic is **basic** — transcript sentences are assigned to speaker turns.
* For leadership analysis, this is enough to test proof-of-concept.
* Later, you can improve with word-level alignment for higher accuracy.

---

## �️ Development

### Running the GUI (Development)

```bash
python gui.py
```

### Building Desktop App

```bash
# Install build dependencies
pip install pyinstaller pillow

# Run build script
python build_app.py

# Test the executable
./dist/Leadership-Transcriber  # Linux/Mac
./dist/Leadership-Transcriber.exe  # Windows
```

## �📌 Roadmap

* [x] ✅ Desktop GUI application
* [x] ✅ Cross-platform compatibility (Windows, Mac, Linux)
* [x] ✅ Standalone executable builds
* [ ] Improve transcript-to-speaker alignment
* [ ] Add support for exporting `.srt` / `.vtt` subtitle files
* [ ] Add integration with leadership feedback AI prompts
* [ ] Add batch processing for multiple files

---

👨‍💻 Built for leadership development projects.
