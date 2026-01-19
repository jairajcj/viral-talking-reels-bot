import google.generativeai as genai
import json
import os
import time

class ContentEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE" and api_key != "dummy_key":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def generate_viral_content(self):
        print("🤖 Asking Gemini for a viral concept...")
        
        prompt = """
        ACT AS A VIRAL CONTENT STRATEGIST.
        Your goal is to create a concept for an Instagram Reel that STOPS THE SCROLL instantly for men and women aged 40-50.
        
        THEME: "Forgotten knowledge", "Ancient health hacks", or "The truth about aging they don't tell you".
        
        REQUIREMENTS:
        1. **The Hook (0-3s)**: Must be provocative. Example: "Stop throwing this away," or "Your doctor isn't telling you this."
        2. **The Content**: A specific, tangible, unique fact or object. NOT generic advice like "drink water". It must be something obscure but "useful".
        3. **Retention**: Structure the script to hold attention. Use phrases like "But here is the catch..."
        4. **Visual**: The image description must be weird, high-contrast, or visually confusing to incite curiosity.
        
        OUTPUT FORMAT (JSON ONLY):
        {
            "image_prompt": "Detailed description of a single, hyper-realistic, high-contrast object/scene. Lighting should be dramatic. Mention specific colors and textures to look premium.",
            "video_script": "Full spoken script (approx 40-60 words). Start with the Hook. End with a question or call to action.",
            "hashtags": ["list", "of", "5", "viral", "hashtags"]
        }
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleanup json string if wraps with markdown
            text = response.text
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "")
            
            data = json.loads(text)
            return data
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

    def mock_content(self):
        print("⚠️  Using MOCK data for demonstration (No API Key found)...")
        time.sleep(2)
        return {
            "image_prompt": "A secret ancient wooden tool used by centenarians in Okinawa, glowing with soft blue light, hyperrealistic, cinematic lighting",
            "video_script": "Did you know there is a simple tool that people in the blue zones use to live over 100 years old? It's not magic. It's science. And almost nobody knows about it. Watch this until the end.",
            "hashtags": ["#longevity", "#secret", "#health", "#viral", "#unknown"]
        }

if __name__ == "__main__":
    # Test
    from config import GEMINI_API_KEY
    if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        engine = ContentEngine(GEMINI_API_KEY)
        print(engine.generate_viral_content())
    else:
        print("Set API Key in config to test")
