import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

class ChatGPTBrowser:
    def __init__(self, email=None, password=None):
        self.driver = None
        self.email = email
        self.password = password

    def start_browser(self):
        print("🌍 Launching Browser (Undetected Chrome) for ChatGPT...")
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            # use_subprocess=True can cause Handle Invalid errors in some envs
            self.driver = uc.Chrome(options=options)
        except Exception as e:
            print(f"⚠️ Failed to start Chrome: {e}")
            self.driver = None # Handle this?
    
    def login(self):
        print("🔑 Checking for Login...")
        try:
            # Check if we are on login page or need to click login
            if "login" in self.driver.current_url or self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]"):
                print("   Logging in...")
                
                # If "Log in" button exists on landing page
                login_btns = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
                if login_btns:
                    login_btns[0].click()
                    time.sleep(3)

                # Email
                try:
                    email_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "username")) # Auth0 usually uses 'username' or 'email'
                    )
                except:
                     email_field = self.driver.find_element(By.ID, "email-input")

                email_field.send_keys(self.email)
                email_field.send_keys(Keys.RETURN)
                time.sleep(2)

                # Password
                pwd_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                pwd_field.send_keys(self.password)
                pwd_field.send_keys(Keys.RETURN)
                
                print("⏳ Waiting for login to complete...")
                time.sleep(10)
                
                # Check for "Stay logged in" or other prompts if needed
                return True
        except Exception as e:
            print(f"⚠️ Login attempt failed or not needed: {e}")
            return False

    def generate_object_content(self):
        if not self.driver:
            self.start_browser()
        
        print("🤖 Navigating to ChatGPT...")
        self.driver.get("https://chatgpt.com/")
        time.sleep(5)
        
        # Attempt Login if credentials provided
        if self.email and self.password:
            self.login()
        
        # Wait for input area
        print("⏳ Waiting for ChatGPT to load...")
        
        try:
            # Try to find the text area
            prompt_area = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "prompt-textarea"))
            )
        except Exception:
            print("❌ Could not find ChatGPT input. Please log in manually.")
            # Give user time to log in
            time.sleep(30)
            try:
                prompt_area = self.driver.find_element(By.ID, "prompt-textarea")
            except:
                return None

        prompt = """
        You are an 'Object Maker' for viral reels.
        I need a concept for a "Talking Object" viral video (40-50s).
        
        Target Audience: Men/Women 40-50.
        Topic: Ancient health hacks or Forgotten Wisdom.
        
        OUTPUT JSON ONLY:
        {
            "object_description": "Description of the object (e.g., 'A dusty old book', 'A cracked clay pot')",
            "image_prompt": "Detailed prompt to generate a hyper-realistic image of this object, cinematic lighting, 8k",
            "video_script": "A 150-word script in first person AS THE OBJECT. Powerful hook. Insightful content. Call to action. Must be between 45 and 90 seconds when spoken.",
            "hashtags": ["#tag1", "#tag2"]
        }
        """
        
        print("📤 Sending Prompt to ChatGPT...")
        prompt_area.send_keys(prompt)
        time.sleep(1)
        prompt_area.send_keys(Keys.RETURN)
        
        print("⏳ Waiting for response...")
        time.sleep(15)
        
        # Scrape response
        try:
            # Find all assistant messages
            responses = self.driver.find_elements(By.CSS_SELECTOR, "div[data-message-author-role='assistant']")
            if not responses:
                # Fallback selector
                responses = self.driver.find_elements(By.CSS_SELECTOR, ".markdown")
            
            if responses:
                last_response = responses[-1].text
                return self.parse_json(last_response)
        except Exception as e:
            print(f"❌ Error scraping ChatGPT: {e}")
            
        return None

    def parse_json(self, text):
        try:
            print(f"📝 Raw ChatGPT Response: {text[:100]}...")
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "{" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                text = text[start:end]
            return json.loads(text)
        except Exception:
            print("⚠️ Failed to parse JSON from ChatGPT.")
            return None

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"⚠️ Error closing ChatGPT browser: {e}")
            except OSError:
                pass # Ignore handle errors on exit
