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

## 📂 Project Structure

```
leadership-transcriber/
│
├── audio/                 # put your audio files here
├── requirements.txt       # Python dependencies
├── transcribe.py          # main script (runs Whisper + Pyannote)
├── utils.py               # helper functions for merging
└── README.md              # this file
```

---

## ⚙️ Setup

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

---

## ▶️ Usage

Put your audio file in the `audio/` folder. Example: `audio/meeting1.mp3`

Run:

```bash
python transcribe.py audio/meeting1.mp3 --hf_token YOUR_HF_TOKEN --whisper_model base
```

Options:

* `--hf_token` = your Hugging Face token
* `--whisper_model` = tiny | base | small | medium | large

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

## 📝 Notes

* Whisper provides transcription only; Pyannote adds speaker diarization.
* Current merging logic is **basic** — transcript sentences are assigned to speaker turns.
* For leadership analysis, this is enough to test proof-of-concept.
* Later, you can improve with word-level alignment for higher accuracy.

---

## 📌 Roadmap

* [ ] Improve transcript-to-speaker alignment
* [ ] Add support for exporting `.srt` / `.vtt` subtitle files
* [ ] Add integration with leadership feedback AI prompts

---

👨‍💻 Built for leadership development projects.
