import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

class GeminiBrowser:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None

    def start_browser(self):
        print("🌍 Launching Browser (Undetected Chrome)...")
        options = uc.ChromeOptions()
        # options.add_argument('--headless') # Keep visible for login
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            self.driver = uc.Chrome(options=options, use_subprocess=True)
        except Exception as e:
            print(f"⚠️ Failed to start with use_subprocess=True, trying default: {e}")
            self.driver = uc.Chrome(options=options)
    
    def login(self):
        print("🔑 Logging into Google...")
        self.driver.get("https://accounts.google.com/ServiceLogin")
        
        try:
            # Email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_field.send_keys(self.email)
            email_field.send_keys(Keys.RETURN)
            
            # Password
            pwd_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            time.sleep(2) # Wait for animation
            pwd_field.send_keys(self.password)
            pwd_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete (Check URL or Element)
            print("⏳ Waiting for login to complete (Please approve 2FA on phone if needed)...")
            time.sleep(20) # Give ample time for 2FA or 'Switch to Pro' modals
            return True
        except Exception as e:
            print(f"❌ Login Error: {e}")
            return False

    def ensure_session(self):
        if not self.driver:
            self.start_browser()
            return self.login()
        return True

    def generate_content(self):
        if not self.ensure_session():
            return None
        
        print("🤖 Navigating to Gemini...")
        self.driver.get("https://gemini.google.com/app")
        time.sleep(5)
        
        prompt = """
        ACT AS A VIRAL CONTENT STRATEGIST.
        Your goal is to create a concept for an Instagram Reel that STOPS THE SCROLL instantly for men and women aged 40-50.
        
        THEME: "Forgotten knowledge", "Ancient health hacks", or "The truth about aging they don't tell you".
        
        REQUIREMENTS:
        1. **The Hook (0-3s)**: Must be provocative. Example: "Stop throwing this away," or "Your doctor isn't telling you this."
        2. **The Content**: A specific, tangible, unique fact or object. NOT generic advice like "drink water". It must be something obscure but "useful".
        3. **Retention**: Structure the script to hold attention. Use phrases like "But here is the catch..."
        4. **Visual**: The description should be for a TALKING OBJECT - an inanimate object that appears to speak directly to camera. Think of viral "talking food" or "talking tools" videos.
        
        OUTPUT FORMAT (JSON ONLY):
        {
            "object_description": "What object is talking (e.g., 'A purple onion', 'An old wooden spoon', 'A jar of honey')",
            "video_prompt": "Detailed prompt for generating a short video of this object 'talking' - describe the object, dramatic lighting, close-up, cinematic, hyperrealistic. Mention that it should look like the object is speaking to camera.",
            "video_script": "Full spoken script (75-100 words). First person perspective AS THE OBJECT. Start with a powerful hook. Include 3 detailed facts. End with a call to action. Target 30-40 seconds when spoken.",
            "hashtags": ["list", "of", "5", "viral", "hashtags"]
        }
        """
        
        try:
            # Find Chat Box (Rich text editor)
            # Depending on Gemini UI updates, this selector might change.
            # Usually: div[contenteditable="true"]
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            chat_box.send_keys(prompt)
            time.sleep(1)
            chat_box.send_keys(Keys.RETURN)
            
            print("⏳ Waiting for generation...")
            time.sleep(15) # Wait for generation
            
            # Scrape Result
            # Finding the last response
            response_elements = self.driver.find_elements(By.CSS_SELECTOR, ".model-response-text") # Generic heuristic
            if not response_elements:
                 response_elements = self.driver.find_elements(By.TAG_NAME, "message-content") # Another possibility

            if response_elements:
                text = response_elements[-1].text
                print(f"📝 Raw response text (first 200 chars): {text[:200]}...")
                
                # CLEAN JSON
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "{" in text:
                    start = text.find("{")
                    end = text.rfind("}") + 1
                    text = text[start:end]
                else:
                    print("⚠️ No JSON found in response. Using demo content.")
                    return self.get_demo_content()
                
                print(f"🔧 Cleaned JSON text (first 200 chars): {text[:200]}...")
                
                try:
                    return json.loads(text)
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parse error: {e}")
                    print("Using demo content instead.")
                    return self.get_demo_content()
            else:
                print("❌ Could not find response element.")
                return self.get_demo_content()
                
        except Exception as e:
            print(f"❌ Interaction Error: {e}")
            return self.get_demo_content()

    def get_demo_content(self):
        """Return demo talking object content for testing"""
        print("🎭 Using DEMO talking object content...")
        time.sleep(2)
        return {
            "object_description": "An ancient, gnarled ginger root",
            "video_prompt": "A hyperrealistic, cinematic close-up of an ancient ginger root with deep wrinkles and golden-brown skin, dramatic side lighting creating deep shadows, the root appears to be 'speaking' to camera, 8k quality, macro photography",
            "video_script": "Listen up. I'm a piece of ginger root, and I've been healing people for over 5000 years. But here's what Big Pharma doesn't want you to know. Every single morning, millions of people over 40 are making one critical mistake. They're reaching for pills when they should be reaching for me. Here's why. First, I reduce inflammation 10 times better than ibuprofen, without destroying your stomach lining. Second, I boost your immune system naturally by increasing white blood cell production. Third, and this is the big one, I reverse joint pain. Studies show that after just 6 weeks of daily use, people report feeling 20 years younger. But here's the secret they're hiding. My peel contains three times more antioxidants than my flesh. The ancient Chinese healers knew this. They never peeled me. They used everything. Modern doctors are just catching up now. And here's the kicker. I cost less than 50 cents, while those arthritis medications? Over 200 dollars a month. The pharmaceutical industry makes billions keeping you sick. I make you healthy for pennies. Want to know the exact method the Okinawan centenarians use? The ones living past 100 with zero joint pain? Comment GINGER right now and I'll share their secret recipe.",
            "hashtags": ["#antiaging", "#naturalhealth", "#ginger", "#over40", "#ancientwisdom"]
        }

    def generate_image_in_chat(self, image_prompt):
        if not self.ensure_session():
            return None
        
        # Ensure we are on the app page
        if "gemini.google.com/app" not in self.driver.current_url:
            self.driver.get("https://gemini.google.com/app")
            time.sleep(5)

        print(f"🎨 Asking Gemini to generate image: {image_prompt[:30]}...")
        try:
            # 1. Send Prompt
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            chat_box.send_keys(f"Generate a hyper-realistic, 8k image of: {image_prompt}")
            time.sleep(1)
            chat_box.send_keys(Keys.RETURN)
            
            # 2. Wait for Image
            print("⏳ Waiting for image generation (30s)... Please be patient.")
            time.sleep(30) # Increased wait time for Gemini to generate
            
            print("🔍 Scanning page for generated images...")
            # 3. Find Image
            # Gemini images are usually large and generated recently.
            # We look for img tags and filter by size or position.
            images = self.driver.find_elements(By.TAG_NAME, "img")
            print(f"   Found {len(images)} total img elements on page")
            
            # Simplified: Just find ANY image that looks like content (not tiny icons)
            # Trust that Gemini generated correctly
            # Simplified: Just find ANY image that looks like content. 
            # Per user request: Don't validate, just take it.
            for img in reversed(images):
                try:
                    src = img.get_attribute("src")
                    if src and src.startswith("http"):
                        print(f"   ✅ Taking first available image: {src[:60]}...")
                        
                        # Download immediately
                        import requests
                        response = requests.get(src, timeout=10)
                        if response.status_code == 200:
                            output_path = "assets/viral_image.jpg"
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            print(f"✅ Image saved to {output_path} ({len(response.content)//1024} KB)")
                            return output_path
                except Exception as e:
                    continue
            
            print("❌ No images found in chat.")
            return None
                
        except Exception as e:
            print(f"❌ Image Generation Error: {e}")
            return None

    def upload_image_and_generate_video(self, image_path, video_prompt):
        """Upload an image to Gemini and ask it to create a video from it"""
        print(f"📤 Uploading image to Gemini for Video Labs: {image_path}...")
        try:
            if not self.ensure_session():
                return None
            
            # Ensure we are on the app page
            if "gemini.google.com/app" not in self.driver.current_url:
                self.driver.get("https://gemini.google.com/app")
                time.sleep(5)

            # 1. Find Upload Input
            # Gemini usually has a hidden file input or a button that triggers it.
            # Common selector for the hidden file input:
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if not file_inputs:
                print("❌ Could not find upload input.")
                return None
            
            # Use the first file input
            abs_image_path = os.path.abspath(image_path)
            file_inputs[0].send_keys(abs_image_path)
            print("   Image uploaded. Waiting for processing...")
            time.sleep(5) # Wait for upload/thumbnail to appear

            # 2. Send Prompt for Video
            chat_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            
            full_prompt = f"Create a high-quality, cinematic video (5-10 seconds) based on this uploaded image. {video_prompt}. It should look like the object is talking to the camera."
            
            chat_box.send_keys(full_prompt)
            time.sleep(1)
            chat_box.send_keys(Keys.RETURN)
            
            # 3. Wait for Video Generation
            print("⏳ Waiting for Google Labs video generation (90s)...")
            time.sleep(90)
            
            print("🔍 Scanning page for generated video...")
            
            # Look for video element
            videos = self.driver.find_elements(By.TAG_NAME, "video")
            print(f"   Found {len(videos)} video elements")
            
            for vid in reversed(videos):
                try:
                    src = vid.get_attribute("src")
                    if src and src.startswith("http"):
                        print(f"   ✅ Found video: {src[:60]}...")
                        
                        import requests
                        response = requests.get(src, timeout=30)
                        if response.status_code == 200:
                            output_path = "assets/talking_object.mp4"
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            print(f"✅ Video saved to {output_path}")
                            return output_path
                except Exception:
                    continue
            
            print("❌ No video found.")
            return None
                
        except Exception as e:
            print(f"❌ Video Generation Upload Error: {e}")
            return None

    def generate_video_in_chat(self, video_prompt, image_path=None):
        """Wrapper to decide whether to upload image or just prompt"""
        if image_path and os.path.exists(image_path):
            return self.upload_image_and_generate_video(image_path, video_prompt)
        
        # Fallback to text-only if no image provided
        print("⚠️ No image provided for video generation. Falling back to text prompt...")
        # ... (rest of old generate_video_in_chat logic if needed, but we want the upload)
        return None

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    gb = GeminiBrowser("test@gmail.com", "pass")
    # gb.start_browser()
