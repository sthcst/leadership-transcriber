#!/usr/bin/env python3
"""
Build script for Leadership Transcriber Desktop App
Creates standalone executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_app():
    """Build the desktop application"""
    print("🔨 Building Leadership Transcriber Desktop App...")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller command (use python -m to ensure we use the right environment)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Leadership-Transcriber",
        "--onedir",                     # Directory bundle (better for ML libraries)
        "--windowed",                   # No console window (GUI only)
        "--icon=icon.ico",             # App icon (optional)
        "--add-data=utils.py;.",       # Include utils.py
        "--add-data=transcribe.py;.",  # Include transcribe.py
        
        # Whisper dependencies
        "--hidden-import=whisper",
        "--hidden-import=whisper.model",
        "--hidden-import=whisper.audio",
        "--hidden-import=whisper.decoding",
        "--hidden-import=whisper.tokenizer",
        "--collect-all=whisper",
        
        # PyAnnote dependencies  
        "--hidden-import=pyannote.audio",
        "--hidden-import=pyannote.core", 
        "--hidden-import=pyannote.database",
        "--hidden-import=pyannote.metrics",
        "--hidden-import=pyannote.pipeline",
        "--collect-all=pyannote",
        
        # PyTorch dependencies
        "--hidden-import=torch",
        "--hidden-import=torchaudio", 
        "--hidden-import=torchvision",
        "--collect-all=torch",
        "--collect-all=torchaudio",
        
        # SpeechBrain dependencies
        "--hidden-import=speechbrain",
        "--collect-all=speechbrain",
        
        # Other ML dependencies
        "--hidden-import=numpy",
        "--hidden-import=scipy",
        "--hidden-import=librosa",
        "--hidden-import=sklearn",
        "--hidden-import=transformers",
        "--hidden-import=huggingface_hub",
        "--collect-all=transformers",
        "--collect-all=huggingface_hub",
        
        # FFmpeg
        "--collect-all=ffmpeg",
        
        "gui.py"
    ]
    
    # Remove icon parameter if icon doesn't exist
    if not os.path.exists("icon.ico"):
        cmd = [c for c in cmd if not c.startswith("--icon")]
    
    print("Running PyInstaller...")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        print(f"📦 Application created: dist/Leadership-Transcriber/")
        print(f"   Run: dist/Leadership-Transcriber/Leadership-Transcriber{'.exe' if sys.platform == 'win32' else ''}")
        print()
        print("📋 Next steps:")
        print("1. Test the executable in dist/Leadership-Transcriber/ folder")
        print("2. The entire folder is standalone - no Python required!")
        print("3. Share the entire dist/Leadership-Transcriber/ folder with users")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Please install it:")
        print("   pip install pyinstaller")
        return False
    
    return True

def create_simple_icon():
    """Create a simple icon for the app (optional)"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
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
        return True
        
    except ImportError:
        print("ℹ️  Pillow not available - skipping icon creation")
        return False
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return False

if __name__ == "__main__":
    print("🎙️ Leadership Transcriber - Build Script")
    print("=" * 50)
    
    # Create icon (optional)
    create_simple_icon()
    
    # Build the app
    success = build_app()
    
    if success:
        print("\n🎉 Build completed! Your desktop app is ready.")
        print("\n📁 Application folder created:")
        print(f"   - dist/Leadership-Transcriber/")
        print(f"   - Main executable: Leadership-Transcriber{'.exe' if sys.platform == 'win32' else ''}")
        print("\n🚀 You can now distribute the entire Leadership-Transcriber folder to users!")
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)