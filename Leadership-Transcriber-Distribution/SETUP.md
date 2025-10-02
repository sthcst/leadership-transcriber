# Leadership Transcriber - Setup Instructions

## Quick Start

1. **Install Python 3.8+** if not already installed
   - Windows: Download from https://python.org
   - Mac: `brew install python` or download from python.org
   - Linux: `sudo apt install python3 python3-pip`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (required for audio processing):
   - Windows: `winget install Gyan.FFmpeg`
   - Mac: `brew install ffmpeg`  
   - Linux: `sudo apt install ffmpeg`

4. **Get Hugging Face token** (for speaker identification):
   - Sign up at https://huggingface.co/ (free)
   - Accept terms for 'pyannote/speaker-diarization'
   - Get your token from Settings -> Access Tokens

5. **Run the app**:
   - Double-click `Leadership-Transcriber-Launcher.exe`
   - Or run: `python gui_launcher.py`

## Usage

- **Full Mode**: Transcription + Speaker identification (needs HF token)
- **Whisper Only**: Just transcription (no token needed)

Enjoy! 🎙️
