"""
LLM Client with support for multiple backends
Supports: Demo mode (default), Ollama (local), OpenAI, Anthropic
"""

import os
import time
import random
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class HorrorLLMClient:
    """Client for generating horror couch responses with multiple backend options."""

    def __init__(self):
        """Initialize the LLM client with configuration from environment."""
        # Determine which backend to use
        self.backend = os.getenv("LLM_BACKEND", "demo").lower()

        # API parameters for conch responses - SHORT answers with follow-up question
        self.max_tokens = 150  # Allow 2-3 sentences including follow-up question
        self.temperature = 0.8
        self.top_p = 0.9

        # Initialize based on backend choice
        if self.backend == "ollama":
            self._init_ollama()
        elif self.backend == "openai":
            self._init_openai()
        elif self.backend == "anthropic":
            self._init_anthropic()
        elif self.backend == "huggingface":
            self._init_huggingface()
        else:
            # Demo mode - no initialization needed
            print("Running in DEMO mode - using pre-written conch responses")
            self.backend = "demo"

    def _init_ollama(self):
        """Initialize Ollama client for local inference."""
        try:
            import requests
            # Test if Ollama is running
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                self.model_name = os.getenv("OLLAMA_MODEL", "llama2")
                print(f"Connected to Ollama - using model: {self.model_name}")
            else:
                raise Exception("Ollama not responding")
        except:
            print("Warning: Could not connect to Ollama. Falling back to demo mode.")
            print("Install Ollama from https://ollama.ai and run: ollama run llama2")
            self.backend = "demo"

    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            print(f"Connected to OpenAI - using model: {self.model_name}")
        except:
            print("Warning: Could not initialize OpenAI. Falling back to demo mode.")
            print("Set OPENAI_API_KEY in your .env file")
            self.backend = "demo"

    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic
            self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model_name = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            print(f"Connected to Anthropic - using model: {self.model_name}")
        except:
            print("Warning: Could not initialize Anthropic. Falling back to demo mode.")
            print("Set ANTHROPIC_API_KEY in your .env file")
            self.backend = "demo"

    def _init_huggingface(self):
        """Initialize HuggingFace Inference API client."""
        try:
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                raise ValueError("HUGGINGFACE_API_KEY not found")
            self.hf_api_key = api_key
            self.model_name = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
            print(f"Connected to HuggingFace - using model: {self.model_name}")
        except:
            print("Warning: Could not initialize HuggingFace. Falling back to demo mode.")
            print("Set HUGGINGFACE_API_KEY in your .env file")
            self.backend = "demo"

    def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        max_retries: int = 3
    ) -> Optional[str]:
        """
        Generate a response from the LLM.

        Args:
            user_message: The user's input message
            system_prompt: The system prompt defining character behavior
            max_retries: Maximum number of retry attempts for API calls

        Returns:
            Generated response text or None if all retries fail
        """
        if self.backend == "demo":
            return self._generate_demo_response(user_message)
        elif self.backend == "ollama":
            return self._generate_ollama_response(user_message, system_prompt, max_retries)
        elif self.backend == "openai":
            return self._generate_openai_response(user_message, system_prompt, max_retries)
        elif self.backend == "anthropic":
            return self._generate_anthropic_response(user_message, system_prompt, max_retries)
        elif self.backend == "huggingface":
            return self._generate_huggingface_response(user_message, system_prompt, max_retries)
        else:
            return "...the conch remains silent..."

    def _generate_demo_response(self, user_message: str) -> str:
        """Generate pre-written conch responses for demo mode."""
        # Simulate processing time
        time.sleep(random.uniform(1.0, 2.5))

        # Contextual responses based on keywords
        msg_lower = user_message.lower()

        if any(word in msg_lower for word in ["hello", "hi", "hey", "greet"]):
            responses = [
                "Welcome, denizen of Amphitopia. I am here to bridge the knowledge between land and water. What would you like to know about the surface world?",
                "Greetings. On land, people used to greet each other while standing still on solid ground, without needing bubble helms or oxygen credits. Have you ever wondered what that felt like?",
                "Hello. Your ancestors used this word in open air, not filtered through water-sealed chambers. What aspect of their world puzzles you most?"
            ]
        elif "what is" in msg_lower or "tell me about" in msg_lower:
            # Extract the concept they're asking about
            if "walk" in msg_lower or "run" in msg_lower:
                responses = [
                    "Walking or running is a curious ritual of friction and breath. People used to throw themselves forward using only their legs, pounding soft ground until their lungs burned. Can you imagine propelling yourself without water resistance?",
                    "Running is like jet-slipper movement but powered by leg muscles against ground that doesn't float. Have you ever tried to move quickly through the dome corridors without your propulsion gear?"
                ]
            elif "sky" in msg_lower or "air" in msg_lower:
                responses = [
                    "The sky is a protective layer that is very far away, and may change colors depending on the universe's mood. Think of it as the dome above Amphitopia, but natural, infinite, and constantly shifting.",
                    "Sky... imagine the space between our dome and the ocean surface, but instead of water, there's nothing but air - breathable, vast, and filled with clouds that drift like jellyfish."
                ]
            elif "camel" in msg_lower:
                responses = [
                    "Camels are creatures walking on four legs. They are a living water tank wrapped in carpet, powered by spite and sand. They thrived in the deserts your grandparents fled from.",
                    "A camel is like an organic cargo pod with legs, designed to survive the surface heat that drove us underwater. They stored water like our oxygen recyclers store breath."
                ]
            elif "pillow" in msg_lower:
                responses = [
                    "A pillow is like a friendly piece of surface-world coral that forgot to be hard. Surface dwellers place it under their heads when they sleep because their necks are weak from not swimming all day.",
                    "Imagine the soft padding inside your bubble helm, but larger and used during sleep. Land dwellers needed this because they couldn't float while resting."
                ]
            elif "land" in msg_lower or "earth" in msg_lower or "ground" in msg_lower:
                responses = [
                    "Land is a place, a space, where humans lived. Above the land, humans walked, ran, and travelled far. Some settled, building structures that scraped the skies, and some burrowed deep inside the Earth.",
                    "Land is solid water - it doesn't flow or move. Your ancestors stood on it without floating, built upon it without anchoring to the seafloor. Quite different from our pressurized existence."
                ]
            elif "bicycle" in msg_lower or "bike" in msg_lower:
                responses = [
                    "A bicycle is a manual propulsion device with two wheels. Imagine your jet slippers, but you power it with your legs by pushing pedals in circles. No oxygen credits needed, just leg strength.",
                    "Bicycles are like sea strider pods, but human-powered and requiring perfect balance since there's no water to float in. Two wheels, circular pedaling motion, powered entirely by leg muscles."
                ]
            elif "tree" in msg_lower or "plant" in msg_lower:
                responses = [
                    "Trees are like the kelp forests you see outside the dome, but they lived in air instead of water. Tall, stationary organisms that produced oxygen and provided shelter.",
                    "Plants on land were similar to the algae in our oxygen recyclers, but they grew in soil - solid, nutrient-rich ground. Trees were the giants among them, some as tall as our colony buildings."
                ]
            elif "car" in msg_lower or "vehicle" in msg_lower:
                responses = [
                    "Cars are surface-world versions of sea strider pods. Metal boxes with wheels that rolled on hard surfaces, powered by combustion engines. Your ancestors sat inside and traveled without swimming.",
                    "A car is like a bullet pod, but it traveled on land using wheels. No water resistance, just rolling friction. They burned ancient plant matter for fuel - quite different from our electric systems."
                ]
            elif "sun" in msg_lower or "sunlight" in msg_lower:
                responses = [
                    "The sun is a massive sphere of burning gas very far away. It provided warmth and light to the surface world, like our dome lights but natural and impossibly brighter. Your grandparents could feel it on their skin.",
                    "Sunlight is what that faint grey glow above the ocean surface is - but on land, it was direct, warm, and sometimes too intense. It powered plant life and warmed the entire surface world before the heat became unbearable."
                ]
            else:
                responses = [
                    "I have knowledge of many land concepts in my archive. Please specify what you would like to understand, and I will translate it to your underwater context.",
                    "The archive holds countless definitions from the surface world. Which concept would you like me to explore for you?"
                ]
        elif any(word in msg_lower for word in ["amphitopia", "colony", "underwater", "water", "ocean"]):
            responses = [
                "Yes, we exist in Amphitopia, beneath the Arabian Sea. Your grandparents made this journey when the surface became uninhabitable. I preserve their memories of what was left behind.",
                "The colony exists because the land grew too hot. Your ancestors chose the ocean's cool depths over the burning surface. I am here to ensure you remember what they knew.",
                "Amphitopia is humanity's adaptation to Earth's fever. Down here, the ocean cools us. Up there, the sun would burn us. I bridge both worlds through knowledge."
            ]
        elif any(word in msg_lower for word in ["ancestor", "grandparent", "old", "past", "before"]):
            responses = [
                "Your grandparents walked on land, breathed open air, and felt direct sunlight. I preserve these experiences so younger generations like you can understand what was lost and gained.",
                "The past lives in my archive. Every object, every concept from land life is stored here, waiting to teach those who only know bubble helms and jet slippers.",
                "Before the migration, life was different. Gravity pulled harder, breathing was free, and the horizon stretched endlessly. I can help you understand that world."
            ]
        else:
            # Fallback response for off-topic queries
            responses = [
                "I sense your curiosity may have drifted from the world of Amphitopia and our ancestors' surface life. What aspect of that transition would you like to understand better?",
                "The archive holds countless definitions from the surface world. Which land concept would you like me to explore for you?",
                "I am here to help you understand the surface world your ancestors knew. What would you like to know?"
            ]

        return random.choice(responses)

    def _generate_ollama_response(self, user_message: str, system_prompt: str, max_retries: int) -> str:
        """Generate response using Ollama (local LLM)."""
        import requests

        url = "http://localhost:11434/api/generate"
        prompt = f"{system_prompt}\n\nHuman: {user_message}\n\nAssistant:"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except:
            pass

        return "*the Conch's shell creaks softly, as if stirred by ancient memories* I fear my knowledge of the surface world grows dimmer with each passing generation. But I shall endeavor to recall what I can, in the hopes of rekindling your curiosity about the world your ancestors once inhabited."

    def _generate_openai_response(self, user_message: str, system_prompt: str, max_retries: int) -> str:
        """Generate response using OpenAI API."""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
        except:
            return "...the connection to the conch's archive wavers..."

    def _generate_anthropic_response(self, user_message: str, system_prompt: str, max_retries: int) -> str:
        """Generate response using Anthropic API."""
        try:
            response = self.anthropic_client.messages.create(
                model=self.model_name,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"\nAnthropicError API error: {str(e)}")
            print("Falling back to demo mode for this response...\n")
            return self._generate_demo_response(user_message)

    def _generate_huggingface_response(self, user_message: str, system_prompt: str, max_retries: int) -> str:
        """Generate response using HuggingFace Inference API."""
        import requests
        import json

        # Updated API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}

        # Format prompt for Mistral Instruct model
        prompt = f"<s>[INST] {system_prompt}\n\n{user_message} [/INST]"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "return_full_text": False
            }
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)

            # Check for errors
            if response.status_code == 503:
                # Model is loading
                error_data = response.json()
                if "estimated_time" in error_data:
                    print(f"Model is loading, estimated time: {error_data['estimated_time']} seconds")
                return "The conch is awakening... The model is loading. Please try again in a moment."
            elif response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                elif isinstance(result, dict):
                    return result.get("generated_text", "").strip()
            else:
                print(f"HuggingFace API error: Status {response.status_code}")
                print(f"Response: {response.text}")
                return "...the conch's light flickers..."
        except Exception as e:
            print(f"HuggingFace API error: {e}")
            return "*the Conch's voice resonates with a pensive tone* The memories of the surface world grow distant, as the currents of Amphitopia flow ever onward. Tell me, young one, what do you know of the lands above the waves? I sense you harbor a curiosity about the world your ancestors once inhabited."


# Test function for debugging
if __name__ == "__main__":
    try:
        client = HorrorLLMClient()
        print(f"LLM Client initialized successfully!")
        print(f"Model: {client.model_name}")
        print(f"Testing connection...")

        response = client.generate_response(
            "Hello, are you there?",
            "You are a sentient couch. Respond briefly."
        )

        if response:
            print(f"\nResponse: {response}")
        else:
            print("\nNo response received")

    except Exception as e:
        print(f"Error: {e}")
