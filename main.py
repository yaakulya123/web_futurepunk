#!/usr/bin/env python3
"""
The Conch: A Cultural Preservation Experience
Main application entry point for Amphitopia's heritage archive.
"""

import sys
import time
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

from llm_client import HorrorLLMClient
from conch_character import conch
from tts_client import ConchTTSClient
from speech_to_text import SpeechToTextClient


class ConchChatApp:
    """Main application for the Amphitopia cultural preservation conch experience."""

    def __init__(self):
        """Initialize the chat application."""
        self.console = Console()
        self.llm_client: Optional[HorrorLLMClient] = None
        self.tts_client: Optional[ConchTTSClient] = None
        self.stt_client: Optional[SpeechToTextClient] = None

        # Underwater futuristic color scheme
        self.conch_color = "cyan"  # Glowing underwater artifact
        self.user_color = "white"
        self.system_color = "grey50"
        self.error_color = "red"

    def slow_print(self, text: str, delay: float = 0.04):
        """
        Print text with a slow typing effect for atmosphere.

        Args:
            text: The text to print
            delay: Delay between characters in seconds
        """
        for char in text:
            self.console.print(char, end="", style=self.conch_color)
            time.sleep(delay)
        self.console.print()  # New line at the end

    def display_welcome(self):
        """Display the welcome message with atmospheric styling."""
        self.console.clear()
        self.console.print()

        # Title with minimal styling
        title = Text("THE CONCH", style=f"bold {self.conch_color}")
        self.console.print(Panel(
            title,
            border_style=self.system_color,
            padding=(1, 2)
        ))

        self.console.print()
        time.sleep(0.5)

        # Get welcome message (don't clean it - we want the full welcome text including the question)
        welcome_message = conch.get_welcome_message()

        # Generate voice for welcome message
        self.display_conch_response(welcome_message)

        self.console.print(
            f"[{self.system_color}](Type 'exit' to leave)[/{self.system_color}]"
        )
        self.console.print()

    def display_goodbye(self, skip_voice: bool = False):
        """
        Display the goodbye message.

        Args:
            skip_voice: If True, skip TTS generation (useful for forced exits)
        """
        self.console.print()
        time.sleep(0.5)

        # Get goodbye message
        goodbye_message = conch.get_goodbye_message()
        goodbye_message = self.clean_response(goodbye_message)

        # Display with or without voice depending on how we're exiting
        if skip_voice:
            # Just display text without TTS
            self.console.print(goodbye_message, style=self.conch_color)
        else:
            # Normal display with TTS
            self.display_conch_response(goodbye_message)

        self.console.print()
        time.sleep(0.5)

    def get_user_input(self) -> Optional[str]:
        """
        Get input from the user with styled prompt.
        Supports both text input and speech-to-text.

        Returns:
            User input string or None if user wants to exit
        """
        try:
            # Check if speech-to-text is enabled
            if self.stt_client and self.stt_client.enabled:
                prompt_text = f"[{self.user_color}]You[/{self.user_color}] (press Enter to type, or 's' + Enter to speak)"
            else:
                prompt_text = f"[{self.user_color}]You[/{self.user_color}]"

            user_input = Prompt.ask(prompt_text, console=self.console).strip()

            # Check if user wants to use speech-to-text
            if user_input.lower() == 's' and self.stt_client and self.stt_client.enabled:
                transcribed_text = self.stt_client.listen_and_transcribe(duration=5)

                if transcribed_text:
                    self.console.print(
                        f"[{self.conch_color}]💬 You said: \"{transcribed_text}\"[/{self.conch_color}]\n"
                    )
                    user_input = transcribed_text
                else:
                    self.console.print(
                        f"[{self.error_color}]❌ Could not understand speech. Please try typing instead.[/{self.error_color}]\n"
                    )
                    return ""

            if not user_input:
                return ""

            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                return None

            return user_input

        except (KeyboardInterrupt, EOFError):
            return None

    def clean_response(self, response: str) -> str:
        """
        Clean the LLM response to enforce formatting rules.

        Args:
            response: Raw response from LLM

        Returns:
            Cleaned response
        """
        import re

        # Remove anything between asterisks (stage directions)
        response = re.sub(r'\*[^*]+\*', '', response)

        # Remove standalone asterisks
        response = response.replace('*', '')

        # Remove ellipses
        response = response.replace('...', '')

        # Clean up whitespace
        response = ' '.join(response.split())
        response = response.strip()

        # Limit to first 3 sentences maximum (definition + follow-up question)
        sentences = re.split(r'(?<=[.!?])\s+', response)
        if len(sentences) > 3:
            response = ' '.join(sentences[:3])

        # If still no ending punctuation, add period
        if response and response[-1] not in '.!?':
            response += '.'

        return response

    def display_conch_response(self, response: str):
        """
        Display the conch's response with styling and optional voice.

        Args:
            response: The response text from the conch
        """
        self.console.print()

        # Generate voice audio FIRST (while user waits)
        audio_path = None
        if self.tts_client and self.tts_client.enabled:
            try:
                audio_path = self.tts_client.generate_speech(response)
            except Exception as e:
                print(f"Voice generation error: {e}")
                audio_path = None

        # Start playing audio in background if available
        import threading
        audio_thread = None
        if audio_path:
            try:
                # Play audio in separate thread so text can display simultaneously
                audio_thread = threading.Thread(
                    target=self.tts_client.play_audio,
                    args=(audio_path,),
                    daemon=True
                )
                audio_thread.start()
            except Exception as e:
                print(f"Voice playback error: {e}")
                audio_thread = None

        # Show response with slow typing effect (plays while audio speaks)
        lines = response.split('\n')
        for line in lines:
            if line.strip():
                self.slow_print(line, delay=0.04)
            else:
                self.console.print()
            time.sleep(0.2)

        self.console.print()

        # Wait for audio to finish if it's still playing
        if audio_thread:
            try:
                audio_thread.join(timeout=15)  # Max 15 seconds
            except:
                pass

    def chat_loop(self):
        """Main chat loop."""
        while True:
            # Get user input
            user_message = self.get_user_input()

            if user_message is None:
                # User wants to exit
                break

            if not user_message:
                # Empty input, skip
                continue

            # Show thinking indicator
            with self.console.status(
                f"[{self.system_color}]... processing ...[/{self.system_color}]",
                spinner="dots"
            ):
                # Generate response
                response = self.llm_client.generate_response(
                    user_message=user_message,
                    system_prompt=conch.system_prompt
                )

            # Display response
            if response:
                # Clean the response to remove asterisks and keep it short
                response = self.clean_response(response)
                self.display_conch_response(response)
            else:
                self.console.print(
                    f"[{self.error_color}]... no response ...[/{self.error_color}]",
                    style="italic"
                )
                self.console.print()

    def run(self):
        """Run the main application."""
        try:
            # Initialize LLM client
            try:
                self.llm_client = HorrorLLMClient()
            except ValueError as e:
                self.console.print(f"\n[{self.error_color}]Error: {e}[/{self.error_color}]\n")
                self.console.print(
                    f"[{self.system_color}]Please follow the setup instructions in README.md[/{self.system_color}]\n"
                )
                sys.exit(1)
            except Exception as e:
                self.console.print(f"\n[{self.error_color}]Unexpected error: {e}[/{self.error_color}]\n")
                sys.exit(1)

            # Initialize TTS client (optional)
            try:
                self.tts_client = ConchTTSClient()
            except Exception as e:
                self.console.print(
                    f"[{self.system_color}]Note: Voice features unavailable ({str(e)})[/{self.system_color}]\n"
                )

            # Initialize STT client (optional)
            try:
                self.stt_client = SpeechToTextClient()
                if self.stt_client.enabled:
                    self.console.print(
                        f"[{self.system_color}]✓ Speech-to-text enabled (press 's' + Enter to speak)[/{self.system_color}]\n"
                    )
            except Exception as e:
                self.console.print(
                    f"[{self.system_color}]Note: Speech-to-text unavailable ({str(e)})[/{self.system_color}]\n"
                )

            # Display welcome
            self.display_welcome()

            # Run chat loop
            self.chat_loop()

            # Display goodbye
            self.display_goodbye()

        except KeyboardInterrupt:
            self.console.print("\n")
            # Skip voice on forced exit to avoid timeout delays
            self.display_goodbye(skip_voice=True)

        except Exception as e:
            self.console.print(f"\n[{self.error_color}]Fatal error: {e}[/{self.error_color}]\n")
            sys.exit(1)


def main():
    """Entry point for the application."""
    app = ConchChatApp()
    app.run()


if __name__ == "__main__":
    main()
