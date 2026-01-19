import requests
import os
import time

class ImageGenerator:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"
    
    def generate_image(self, prompt, output_path="assets/generated_image.jpg"):
        print(f"🎨 Generating image for prompt: {prompt[:50]}...")
        
        # Clean prompt for URL
        encoded_prompt = requests.utils.quote(prompt)
        url = f"{self.base_url}{encoded_prompt}?width=1080&height=1920&nologo=true" # Story format
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Image saved to {output_path}")
                return output_path
            else:
                print(f"❌ Failed to generate image. Status: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error downloading image: {e}")
            return None

if __name__ == "__main__":
    gen = ImageGenerator()
    gen.generate_image("A futuristic useful gadget for elderly people, hyperrealistic, 8k", "test_image.jpg")
