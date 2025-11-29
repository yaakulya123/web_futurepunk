"""
Speech-to-Text Module for The Conch
Converts spoken audio input to text using multiple backend options.
"""

import os
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SpeechToTextClient:
    """Client for converting speech to text with multiple backend options."""

    def __init__(self):
        """Initialize the speech-to-text client."""
        self.enabled = os.getenv("STT_ENABLED", "false").lower() == "true"
        self.backend = os.getenv("STT_BACKEND", "whisper").lower()

        if not self.enabled:
            return

        # Initialize based on backend choice
        if self.backend == "whisper":
            self._init_whisper()
        elif self.backend == "google":
            self._init_google()
        else:
            print(f"Unknown STT backend: {self.backend}. Speech-to-text disabled.")
            self.enabled = False

    def _init_whisper(self):
        """Initialize OpenAI Whisper (local) for speech recognition."""
        try:
            import whisper
            import sounddevice
            import soundfile
            import ssl
            import certifi

            # Fix SSL certificate verification for macOS
            ssl._create_default_https_context = ssl._create_unverified_context

            # Load the model (tiny, base, small, medium, large)
            model_size = os.getenv("WHISPER_MODEL", "base")
            print(f"Loading Whisper model: {model_size}...")
            print("(First time may take a few minutes to download the model...)")
            self.whisper_model = whisper.load_model(model_size)
            print(f"✓ Whisper ({model_size}) ready for speech-to-text")

        except ImportError as e:
            print(f"Warning: Could not initialize Whisper. Missing dependencies: {e}")
            print("Install with: pip install openai-whisper sounddevice soundfile")
            self.enabled = False
        except Exception as e:
            print(f"Warning: Could not initialize Whisper: {e}")
            print("Try running: pip install --upgrade openai-whisper")
            self.enabled = False

    def _init_google(self):
        """Initialize Google Speech Recognition."""
        try:
            import speech_recognition
            self.recognizer = speech_recognition.Recognizer()
            print("✓ Google Speech Recognition ready for speech-to-text")
        except ImportError:
            print("Warning: Could not initialize Google Speech Recognition.")
            print("Install with: pip install SpeechRecognition pyaudio")
            self.enabled = False
        except Exception as e:
            print(f"Warning: Could not initialize Google Speech Recognition: {e}")
            self.enabled = False

    def record_audio(self, duration: int = 5, sample_rate: int = 16000) -> Optional[str]:
        """
        Record audio from microphone and save to temporary file.

        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate (16000 Hz is standard for speech)

        Returns:
            Path to temporary audio file or None if recording failed
        """
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np
            import sys
            import time

            print(f"\n🎤 Recording for {duration} seconds... SPEAK NOW!\n")

            # Show countdown with progress
            start_time = time.time()

            # Start recording in background
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype=np.float32
            )

            # Show progress while recording
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                remaining = duration - elapsed

                # Progress bar
                progress = int((elapsed / duration) * 20)
                bar = "█" * progress + "░" * (20 - progress)

                # Display with countdown
                sys.stdout.write(f"\r[{bar}] {remaining:.1f}s remaining ")
                sys.stdout.flush()
                time.sleep(0.1)

            # Ensure recording is complete
            sd.wait()

            print("\n✓ Recording complete! Processing...\n")

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            sf.write(temp_file.name, audio_data, sample_rate)

            return temp_file.name

        except Exception as e:
            print(f"\n❌ Error recording audio: {e}")
            print("Make sure your microphone is connected and accessible.\n")
            return None

    def transcribe_whisper(self, audio_file: str) -> Optional[str]:
        """
        Transcribe audio using Whisper.

        Args:
            audio_file: Path to audio file

        Returns:
            Transcribed text or None if transcription failed
        """
        try:
            result = self.whisper_model.transcribe(audio_file, language="en")
            return result["text"].strip()
        except Exception as e:
            print(f"Error transcribing with Whisper: {e}")
            return None

    def transcribe_google(self, audio_file: str) -> Optional[str]:
        """
        Transcribe audio using Google Speech Recognition.

        Args:
            audio_file: Path to audio file

        Returns:
            Transcribed text or None if transcription failed
        """
        try:
            import speech_recognition as sr

            # Load audio file
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)

            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            return text.strip()

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            print(f"Error transcribing with Google: {e}")
            return None

    def listen_and_transcribe(self, duration: int = 5) -> Optional[str]:
        """
        Record audio and transcribe it to text.

        Args:
            duration: Recording duration in seconds

        Returns:
            Transcribed text or None if failed
        """
        if not self.enabled:
            return None

        # Record audio
        audio_file = self.record_audio(duration)
        if not audio_file:
            return None

        # Transcribe based on backend
        try:
            if self.backend == "whisper":
                text = self.transcribe_whisper(audio_file)
            elif self.backend == "google":
                text = self.transcribe_google(audio_file)
            else:
                text = None

            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except:
                pass

            return text

        except Exception as e:
            print(f"Error during transcription: {e}")
            return None


# Test function
if __name__ == "__main__":
    print("=== Testing Speech-to-Text ===\n")

    # Test with Whisper
    client = SpeechToTextClient()

    if client.enabled:
        print("\nReady to test! Press Enter to start recording...")
        input()

        text = client.listen_and_transcribe(duration=5)

        if text:
            print(f"\n✓ Transcription: {text}")
        else:
            print("\n✗ Transcription failed")
    else:
        print("Speech-to-text is not enabled.")
