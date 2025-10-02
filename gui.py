#!/usr/bin/env python3
"""
Leadership Transcriber - Desktop GUI Application
A user-friendly desktop interface for the Leadership Transcriber
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import traceback

# We'll import transcription functionality when needed (lazy loading)
# This prevents slow startup due to heavy ML library imports

class TranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Leadership Transcriber")
        self.root.geometry("800x600")
        
        # Variables
        self.selected_file = tk.StringVar()
        self.whisper_model = tk.StringVar(value="base")
        self.hf_token = tk.StringVar()
        
        # Check for existing HF_TOKEN
        existing_token = os.getenv("HF_TOKEN")
        if existing_token:
            self.hf_token.set(existing_token)
        
        self.setup_ui()
        self.check_hf_token()
    
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
        
        # HF Token section
        ttk.Label(main_frame, text="Hugging Face Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        hf_entry = ttk.Entry(main_frame, textvariable=self.hf_token, show="*", width=50)
        hf_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        ttk.Button(main_frame, text="?", command=self.show_token_help, width=3).grid(row=1, column=2, padx=(5, 0))
        
        # File selection
        ttk.Label(main_frame, text="Audio File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, state="readonly")
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=0, column=1, padx=(5, 0))
        
        # Model selection
        ttk.Label(main_frame, text="Whisper Model:").grid(row=3, column=0, sticky=tk.W, pady=5)
        model_combo = ttk.Combobox(main_frame, textvariable=self.whisper_model, 
                                  values=["tiny", "base", "small", "medium", "large"],
                                  state="readonly", width=15)
        model_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to transcribe")
        ttk.Label(main_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.status_label.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Transcribe button
        self.transcribe_btn = ttk.Button(main_frame, text="🎙️ Start Transcription", 
                                        command=self.start_transcription)
        self.transcribe_btn.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Results area
        ttk.Label(main_frame, text="Results:", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        
        # Results text with scrollbar
        self.results_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.results_text.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(8, weight=1)
        
        # Save button
        self.save_btn = ttk.Button(main_frame, text="💾 Save Results", 
                                  command=self.save_results, state="disabled")
        self.save_btn.grid(row=9, column=0, columnspan=3, pady=10)
    
    def check_hf_token(self):
        """Check if HF token is available and show warning if not"""
        if not self.hf_token.get():
            self.progress_var.set("⚠️  Please enter your Hugging Face token to continue")
            self.transcribe_btn.config(state="disabled")
        else:
            self.progress_var.set("Ready to transcribe")
            self.transcribe_btn.config(state="normal")
    
    def show_token_help(self):
        """Show help dialog for HF token"""
        help_text = """Hugging Face Token Required:

1. Sign up at https://huggingface.co/ (free)
2. Accept model terms for 'pyannote/speaker-diarization'
3. Go to Settings → Access Tokens
4. Create a new token and copy it here

This token is needed for speaker diarization functionality."""
        
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
    
    def check_ready_state(self):
        """Check if ready to transcribe and update UI"""
        if not self.hf_token.get():
            self.progress_var.set("⚠️  Please enter your Hugging Face token")
            self.transcribe_btn.config(state="disabled")
        elif not self.selected_file.get():
            self.progress_var.set("⚠️  Please select an audio file")
            self.transcribe_btn.config(state="disabled")
        else:
            self.progress_var.set("Ready to transcribe")
            self.transcribe_btn.config(state="normal")
    
    def start_transcription(self):
        """Start transcription in a separate thread"""
        if not self.hf_token.get():
            messagebox.showerror("Error", "Please enter your Hugging Face token")
            return
        
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select an audio file")
            return
        
        # Set HF_TOKEN environment variable
        os.environ["HF_TOKEN"] = self.hf_token.get()
        
        # Disable UI during transcription
        self.transcribe_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.results_text.delete(1.0, tk.END)
        
        # Start progress bar
        self.progress_bar.start()
        self.progress_var.set("Transcribing... This may take several minutes")
        
        # Run transcription in separate thread
        thread = threading.Thread(target=self.run_transcription, daemon=True)
        thread.start()
    
    def run_transcription(self):
        """Run the actual transcription (in separate thread)"""
        try:
            # Capture the output by redirecting stdout temporarily
            import io
            import contextlib
            
            # Create string buffer to capture output
            output_buffer = io.StringIO()
            
            # Custom progress callback
            def update_progress(message):
                self.root.after(0, lambda: self.progress_var.set(message))
            
            # Update status
            self.root.after(0, lambda: update_progress("Loading Whisper model..."))
            
            # Import and run transcription (we'll modify transcribe.py to accept a callback)
            audio_file = self.selected_file.get()
            model_size = self.whisper_model.get()
            
            # Import transcription functionality (lazy loading to avoid slow startup)
            try:
                from transcribe import main as transcribe_main
                
                # Call the existing main function and capture output
                with contextlib.redirect_stdout(output_buffer):
                    with contextlib.redirect_stderr(output_buffer):
                        transcribe_main(audio_file, model_size)
            except ImportError as e:
                raise Exception(f"Failed to import transcription modules: {e}")
            except Exception as e:
                raise Exception(f"Transcription failed: {e}")
            
            # Get the results
            results = output_buffer.getvalue()
            
            # Update UI in main thread
            self.root.after(0, lambda: self.transcription_completed(results))
            
        except Exception as e:
            error_msg = f"Error during transcription:\n{str(e)}\n\n{traceback.format_exc()}"
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
    app = TranscriberGUI(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()