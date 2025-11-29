"""
Text-to-Speech Client for The Conch using Murf API
High-quality AI voices with natural, expressive speech.
"""

import os
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ConchTTSClient:
    """Client for generating speech from text using Murf API."""

    def __init__(self):
        """Initialize the TTS client with configuration from environment."""
        self.enabled = os.getenv("TTS_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("MURF_API_KEY", "")
        self.voice_id = os.getenv("MURF_VOICE_ID", "Ryan")
        self.style = os.getenv("MURF_STYLE", "Conversational")
        self.model = os.getenv("MURF_MODEL", "Falcon")

        if self.enabled:
            if not self.api_key:
                print("❌ TTS enabled but MURF_API_KEY not set in .env")
                self.enabled = False
            else:
                print(f"✓ TTS enabled - using Murf voice: {self.voice_id} ({self.style})")

    def _clean_text_for_tts(self, text: str) -> str:
        """
        Clean text for better TTS output.

        Args:
            text: Raw text

        Returns:
            Cleaned text suitable for TTS
        """
        # Remove markdown/formatting
        cleaned = text.replace("*", "").replace("_", "").replace("`", "")

        # Remove ellipses at start/end only (not in the middle)
        cleaned = cleaned.strip()
        while cleaned.startswith("..."):
            cleaned = cleaned[3:].strip()
        while cleaned.endswith("..."):
            cleaned = cleaned[:-3].strip()

        # Join multiple lines into single text (fixes multi-line issue)
        cleaned = " ".join(line.strip() for line in cleaned.split("\n") if line.strip())

        # DON'T truncate - read the complete response
        # The responses are already short (1-2 sentences) so no need to cut off

        return cleaned

    def generate_speech(self, text: str) -> Optional[str]:
        """
        Generate speech from text using Murf API.

        Args:
            text: Text to synthesize

        Returns:
            Path to generated audio file or None
        """
        if not self.enabled:
            return None

        try:
            from murf import Murf
            import requests
            import httpx

            # Clean the text
            clean_text = self._clean_text_for_tts(text)

            if not clean_text:
                return None

            # Create httpx client with extended timeout for TTS generation
            # TTS can take 30-60 seconds for longer texts
            http_client = httpx.Client(timeout=httpx.Timeout(120.0, connect=10.0))

            # Initialize Murf client with custom timeout
            client = Murf(api_key=self.api_key, httpx_client=http_client)

            # Generate speech with Murf API
            response = client.text_to_speech.generate(
                text=clean_text,
                voice_id=self.voice_id,
                format="MP3",
                sample_rate=44100.0
            )

            # audio_file is a URL, download it
            audio_url = response.audio_file

            # Download the audio file
            audio_response = requests.get(audio_url, timeout=60)
            audio_response.raise_for_status()

            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            output_path = temp_file.name

            # Write audio data to file
            with open(output_path, 'wb') as f:
                f.write(audio_response.content)

            temp_file.close()

            # Clean up httpx client
            http_client.close()

            return output_path

        except Exception as e:
            # Only show simplified error message, not full traceback
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                print(f"⏱️  TTS generation timed out (API may be slow, continuing without voice...)")
            else:
                print(f"⚠️  TTS error: {error_msg}")

            # Clean up httpx client if it exists
            try:
                http_client.close()
            except:
                pass

            return None

    def play_audio(self, audio_path: str):
        """
        Play audio file through the system's default audio device.

        Args:
            audio_path: Path to audio file
        """
        try:
            import subprocess
            import platform

            # Use system player for reliable playback
            system = platform.system()

            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_path], check=False, stderr=subprocess.DEVNULL)
            elif system == "Linux":
                # Try multiple players
                try:
                    subprocess.run(["mpg123", audio_path], check=True, stderr=subprocess.DEVNULL)
                except:
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", audio_path], check=True, stderr=subprocess.DEVNULL)
            elif system == "Windows":
                subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{audio_path}').PlaySync()"], check=True)

            # Clean up temp file
            try:
                os.unlink(audio_path)
            except:
                pass

        except Exception as e:
            # Simplified error message without traceback
            print(f"🔇 Audio playback error: {str(e)}")
            # Try cleanup anyway
            try:
                os.unlink(audio_path)
            except:
                pass

    def speak(self, text: str) -> bool:
        """
        Generate and play speech from text (convenience method).

        Args:
            text: Text to speak

        Returns:
            True if speech was played successfully, False otherwise
        """
        if not self.enabled:
            return False

        audio_path = self.generate_speech(text)
        if not audio_path:
            return False

        self.play_audio(audio_path)
        return True


# Test function
if __name__ == "__main__":
    print("=== Testing Conch TTS with Murf API ===\n")

    tts = ConchTTSClient()

    if tts.enabled:
        test_text = """Welcome to Amphitopia. I am the Conch,
        a cultural preservation device.
        This is a multi-line test."""

        print(f"Generating speech for multi-line text...\n")
        audio_path = tts.generate_speech(test_text)

        if audio_path:
            print(f"✓ Audio generated: {audio_path}")
            print("Playing audio...")
            tts.play_audio(audio_path)
            print("Done!")
        else:
            print("✗ Failed to generate audio")
    else:
        print("TTS is disabled. Set TTS_ENABLED=true and MURF_API_KEY in .env to enable.")
