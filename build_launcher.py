#!/usr/bin/env python3
"""
Build script for Leadership Transcriber Launcher
Creates a lightweight desktop app that uses the local Python environment
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_launcher():
    """Build the lightweight desktop launcher"""
    print("🔨 Building Leadership Transcriber Launcher...")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller command for lightweight launcher
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Leadership-Transcriber-Launcher",
        "--onefile",                   # Single executable (lightweight)
        "--windowed",                  # No console window (GUI only)
        "--icon=icon.ico",            # App icon (optional)
        "gui_launcher.py"
    ]
    
    # Remove icon parameter if icon doesn't exist
    if not os.path.exists("icon.ico"):
        cmd = [c for c in cmd if not c.startswith("--icon")]
    
    print("Running PyInstaller...")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        print(f"📦 Launcher created: dist/Leadership-Transcriber-Launcher{'.exe' if sys.platform == 'win32' else ''}")
        print()
        print("📋 How it works:")
        print("1. The launcher is a lightweight GUI (few MB)")
        print("2. It calls your existing Python scripts for transcription")
        print("3. Users need Python + your requirements installed")
        print("4. But they get a user-friendly interface!")
        print()
        print("📋 Distribution:")
        print("1. Share the launcher executable")
        print("2. Include instructions for installing Python dependencies")
        print("3. Much easier than sharing command-line instructions!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Please install it:")
        print("   pip install pyinstaller")
        return False
    
    return True

def create_distribution_package():
    """Create a complete distribution package"""
    print("\n📦 Creating distribution package...")
    
    # Create distribution folder
    dist_folder = Path("Leadership-Transcriber-Distribution")
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    # Copy launcher
    launcher_name = f"Leadership-Transcriber-Launcher{'.exe' if sys.platform == 'win32' else ''}"
    launcher_path = Path("dist") / launcher_name
    
    if launcher_path.exists():
        shutil.copy2(launcher_path, dist_folder / launcher_name)
        print(f"✅ Copied launcher to {dist_folder}")
    
    # Copy Python files
    python_files = ["transcribe.py", "utils.py", "requirements.txt", "README.md"]
    for file in python_files:
        if Path(file).exists():
            shutil.copy2(file, dist_folder / file)
    
    # Create setup instructions
    setup_instructions = """# Leadership Transcriber - Setup Instructions

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
"""
    
    with open(dist_folder / "SETUP.md", "w", encoding="utf-8") as f:
        f.write(setup_instructions)
    
    print(f"✅ Created complete distribution package in {dist_folder}")
    print(f"📁 Package contents:")
    for item in dist_folder.iterdir():
        print(f"   - {item.name}")
    
    return dist_folder

if __name__ == "__main__":
    print("🎙️ Leadership Transcriber - Launcher Build Script")
    print("=" * 60)
    
    # Create icon (optional)
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple 256x256 icon
        size = 256
        img = Image.new('RGBA', (size, size), (70, 130, 180, 255))  # Steel blue background
        draw = ImageDraw.Draw(img)
        
        # Draw microphone shape
        mic_color = (255, 255, 255, 255)  # White
        
        # Microphone body
        draw.ellipse([size//4, size//6, 3*size//4, 2*size//3], fill=mic_color)
        
        # Microphone stand
        draw.rectangle([size//2-10, 2*size//3, size//2+10, 5*size//6], fill=mic_color)
        draw.rectangle([size//3, 5*size//6-5, 2*size//3, 5*size//6+5], fill=mic_color)
        
        # Save as ICO
        img.save("icon.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("✅ Created app icon: icon.ico")
        
    except ImportError:
        print("ℹ️  Pillow not available - skipping icon creation")
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
    
    # Build the launcher
    success = build_launcher()
    
    if success:
        # Create distribution package
        dist_folder = create_distribution_package()
        
        print(f"\n🎉 Build completed successfully!")
        print(f"\n📦 Ready to distribute:")
        print(f"   - Lightweight launcher: dist/Leadership-Transcriber-Launcher.exe")
        print(f"   - Complete package: {dist_folder}/")
        print(f"\n🚀 Users can now easily use your transcription tool!")
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)