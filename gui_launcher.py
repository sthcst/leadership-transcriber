#!/usr/bin/env python3
"""
Leadership Transcriber - Lightweight Desktop Launcher
This version creates a simple desktop app that launches the existing Python scripts
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
from pathlib import Path

class TranscriberLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Leadership Transcriber")
        self.root.geometry("800x600")
        
        # Variables
        self.selected_file = tk.StringVar()
        self.whisper_model = tk.StringVar(value="base")
        self.hf_token = tk.StringVar()
        self.mode = tk.StringVar(value="full")  # "full" or "whisper-only"
        
        # Check for existing HF_TOKEN
        existing_token = os.getenv("HF_TOKEN")
        if existing_token:
            self.hf_token.set(existing_token)
        
        self.setup_ui()
        self.check_ready_state()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎙️ Leadership Transcriber", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Mode selection
        ttk.Label(main_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W, pady=5)
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Radiobutton(mode_frame, text="Full (Transcription + Speaker ID)", 
                       variable=self.mode, value="full", command=self.on_mode_change).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Whisper Only (Transcription only)", 
                       variable=self.mode, value="whisper-only", command=self.on_mode_change).grid(row=1, column=0, sticky=tk.W)
        
        # HF Token section (only for full mode)
        self.token_label = ttk.Label(main_frame, text="Hugging Face Token:")
        self.token_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.hf_entry = ttk.Entry(main_frame, textvariable=self.hf_token, show="*", width=50)
        self.hf_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.help_btn = ttk.Button(main_frame, text="?", command=self.show_token_help, width=3)
        self.help_btn.grid(row=2, column=2, padx=(5, 0))
        
        # File selection
        ttk.Label(main_frame, text="Audio File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, state="readonly")
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=0, column=1, padx=(5, 0))
        
        # Model selection
        ttk.Label(main_frame, text="Whisper Model:").grid(row=4, column=0, sticky=tk.W, pady=5)
        model_combo = ttk.Combobox(main_frame, textvariable=self.whisper_model, 
                                  values=["tiny", "base", "small", "medium", "large"],
                                  state="readonly", width=15)
        model_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to transcribe")
        ttk.Label(main_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.status_label.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Transcribe button
        self.transcribe_btn = ttk.Button(main_frame, text="🎙️ Start Transcription", 
                                        command=self.start_transcription)
        self.transcribe_btn.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Results area
        ttk.Label(main_frame, text="Results:", font=("Arial", 12, "bold")).grid(row=8, column=0, sticky=tk.W, pady=(20, 5))
        
        # Results text with scrollbar
        self.results_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.results_text.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(9, weight=1)
        
        # Save button
        self.save_btn = ttk.Button(main_frame, text="💾 Save Results", 
                                  command=self.save_results, state="disabled")
        self.save_btn.grid(row=10, column=0, columnspan=3, pady=10)
    
    def on_mode_change(self):
        """Handle mode change between full and whisper-only"""
        if self.mode.get() == "whisper-only":
            self.token_label.grid_remove()
            self.hf_entry.grid_remove()
            self.help_btn.grid_remove()
        else:
            self.token_label.grid()
            self.hf_entry.grid()
            self.help_btn.grid()
        
        self.check_ready_state()
    
    def check_ready_state(self):
        """Check if ready to transcribe and update UI"""
        if self.mode.get() == "full" and not self.hf_token.get():
            self.progress_var.set("⚠️  Please enter your Hugging Face token for speaker identification")
            self.transcribe_btn.config(state="disabled")
        elif not self.selected_file.get():
            self.progress_var.set("⚠️  Please select an audio file")
            self.transcribe_btn.config(state="disabled")
        else:
            mode_text = "Full transcription + speaker ID" if self.mode.get() == "full" else "Whisper-only transcription"
            self.progress_var.set(f"Ready for {mode_text}")
            self.transcribe_btn.config(state="normal")
    
    def show_token_help(self):
        """Show help dialog for HF token"""
        help_text = """Hugging Face Token (for Speaker Identification):

FULL MODE requires a token:
1. Sign up at https://huggingface.co/ (free)
2. Accept model terms for 'pyannote/speaker-diarization'
3. Go to Settings → Access Tokens
4. Create a new token and copy it here

WHISPER-ONLY MODE doesn't need a token:
- Just transcribes speech to text
- No speaker identification
- Select "Whisper Only" mode above"""
        
        messagebox.showinfo("Hugging Face Token Help", help_text)
    
    def browse_file(self):
        """Open file dialog to select audio file"""
        filetypes = [
            ("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file.set(filename)
            self.check_ready_state()
    
    def start_transcription(self):
        """Start transcription by calling the appropriate Python script"""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select an audio file")
            return
        
        if self.mode.get() == "full" and not self.hf_token.get():
            messagebox.showerror("Error", "Please enter your Hugging Face token for full mode")
            return
        
        # Disable UI during transcription
        self.transcribe_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.results_text.delete(1.0, tk.END)
        
        # Start progress bar
        self.progress_bar.start()
        mode_text = "Full transcription (this may take several minutes)" if self.mode.get() == "full" else "Whisper-only transcription"
        self.progress_var.set(f"Running {mode_text}...")
        
        # Run transcription in separate thread
        thread = threading.Thread(target=self.run_transcription, daemon=True)
        thread.start()
    
    def run_transcription(self):
        """Run the actual transcription using subprocess"""
        try:
            audio_file = self.selected_file.get()
            model_size = self.whisper_model.get()
            
            # Prepare environment
            env = os.environ.copy()
            if self.mode.get() == "full" and self.hf_token.get():
                env["HF_TOKEN"] = self.hf_token.get()
            
            # Choose which script to run
            if self.mode.get() == "full":
                cmd = [sys.executable, "transcribe.py", audio_file, "--whisper_model", model_size]
            else:
                # Use whisper directly for whisper-only mode
                cmd = [sys.executable, "-c", f"""
import whisper
import sys

try:
    print("Loading Whisper model ({model_size})...")
    model = whisper.load_model("{model_size}")
    print("Transcribing audio...")
    result = model.transcribe("{audio_file}")
    
    print()
    print("===== TRANSCRIPTION =====")
    print()
    print(result["text"])
    
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
"""]
            
            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                env=env
            )
            
            if result.returncode == 0:
                output = result.stdout
                if result.stderr:
                    output += "\n\nWarnings:\n" + result.stderr
                self.root.after(0, lambda: self.transcription_completed(output))
            else:
                error_msg = f"Command failed (exit code {result.returncode}):\n\n"
                error_msg += f"STDOUT:\n{result.stdout}\n\n"
                error_msg += f"STDERR:\n{result.stderr}"
                self.root.after(0, lambda: self.transcription_error(error_msg))
                
        except Exception as e:
            error_msg = f"Error running transcription:\n{str(e)}"
            self.root.after(0, lambda: self.transcription_error(error_msg))
    
    def transcription_completed(self, results):
        """Handle successful transcription completion"""
        self.progress_bar.stop()
        self.progress_var.set("✅ Transcription completed successfully!")
        
        # Display results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
        
        # Re-enable UI
        self.transcribe_btn.config(state="normal")
        self.save_btn.config(state="normal")
    
    def transcription_error(self, error_msg):
        """Handle transcription error"""
        self.progress_bar.stop()
        self.progress_var.set("❌ Transcription failed")
        
        # Show error in results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, error_msg)
        
        # Re-enable transcribe button
        self.transcribe_btn.config(state="normal")
        
        # Show error dialog
        messagebox.showerror("Transcription Error", 
                           "Transcription failed. Check the results area for details.")
    
    def save_results(self):
        """Save transcription results to file"""
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save transcription results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

def main():
    """Main entry point for GUI application"""
    root = tk.Tk()
    app = TranscriberLauncher(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()