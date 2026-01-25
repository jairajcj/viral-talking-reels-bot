import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_DATA_DIR = os.path.abspath("selenium_user_data")

def setup_driver():
    print("Setting up Chrome Driver...")
    options = Options()
    options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def wait_for_gemini_response(driver, wait_obj, previous_response_count=0):
    """
    Waits for a new response to appear in the chat.
    This is tricky in Gemini as dynamic classes change. 
    We often look for the 'model-response' containers or similar.
    """
    print("Waiting for Gemini response...")
    time.sleep(3) # Initial buffer
    
    # Wait until the number of response containers increases
    try:
        def response_count_increased(d):
            # General selector for user/model turns. 
            # Note: Selectors for Gemini are unstable. 
            # We'll rely on time + checking for new text blocks.
            current_responses = d.find_elements(By.CSS_SELECTOR, ".model-response-text, content-block") 
            # If that selector fails, we might just sleep.
            return True if len(current_responses) > 0 else False
        
        # Simple wait strat: Just wait a fixed time + check for stop button disappearance if possible
        # Or just wait sufficiently long.
        time.sleep(8) 
        return True
    except:
        return False

def get_last_response_text(driver):
    # Try to grab the last text block from the model
    # This selector is a best-guess based on recent Gemini DOM
    # It might need adjustment if Gemini updates
    try:
        # Look for the last paragraph or content block
        responses = driver.find_elements(By.CSS_SELECTOR, "div[data-message-id]") # message container
        if not responses:
            # Fallback for other structures
            responses = driver.find_elements(By.TAG_NAME, "message-content")
            
        if responses:
            return responses[-1].text
        
        # Fallback: just grab all body text and split? No.
        # Let's try getting the active element or standard text
        return None
    except:
        return None

def run_gemini_workflow(driver):
    print("Navigating to Gemini...")
    driver.get("https://gemini.google.com/")
    
    wait = WebDriverWait(driver, 60)
    
    # 1. Login Check & Auto-Login
    print("-" * 50)
    print("STEP 1: LOGIN CHECK")
    
    # Check if already logged in first
    try:
        input_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
        print("Already logged in.")
    except:
        print("Not logged in. Attempting auto-login...")
        try:
            # Click "Sign in" if present (Gemini landing page often has a specific button)
            # Sometimes it redirects directly to accounts.google.com
            # Let's try navigating to the login URL directly if not found
            # But usually gemini.google.com redirects to login if no session.
            
            # Wait for email input
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            print("Entering email...")
            email_input.send_keys("jairajchilukala@gmail.com")
            email_input.send_keys(Keys.ENTER)
            
            # Wait for password input
            # This is where it gets tricky. Sometimes there's a "Next" transition
            print("Waiting for password field...")
            # Increased wait for animation
            time.sleep(3) 
            pass_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
            print("Entering password...")
            pass_input.send_keys("Woxsen@9912081240")
            pass_input.send_keys(Keys.ENTER)
            
    
            # Wait for the chat input now.
            print("Login submitted. Waiting for redirection to Gemini...")
            # Increased timeout to 120 seconds for redirection/loading
            wait_long = WebDriverWait(driver, 120) 
            input_area = wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            print("Successfully logged in!")
            
        except Exception as e:
            print(f"Auto-login failed: {e}")
            print("Please finish logging in manually in the browser.")
            # Give user ample time to rescue the login
            time.sleep(10)
            input("Press ENTER here once you are logged in...")
            # Re-verify
            input_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            
    # --- Start Workflow ---
    # Once logged in, we proceed.

    
    # helper to send message
    def send_message(text):
        # Refresh element reference
        inp = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        inp.send_keys(text)
        time.sleep(1)
        inp.send_keys(Keys.ENTER)
        
    # --- Step 1: Trending Topic ---
    print("Step 1: Asking for Unique Trending Topic...")
    import datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    topic_prompt = f"Give me a unique, specific, and helpful trending topic for an Instagram reel that is different from common generic ones. Current time reference: {now_str}. Just the topic name."
    send_message(topic_prompt)
    
    time.sleep(10) 
    # Try to grab the topic text for later use
    topic_text = "Instagram Trends" # Default
    try:
        topic_element = driver.find_elements(By.CSS_SELECTOR, ".model-response-text, content-block, .message-content")
        if topic_element:
            topic_text = topic_element[-1].text
            print(f"Captured Topic: {topic_text[:50]}...")
    except:
        print("Could not capture specific topic text, using default.")

    # --- Step 2: Image Prompt ---
    print("Step 2: Asking for Image Prompt...")
    send_message("Give me a detailed image prompt for an AI generator. It should feature an object that looks like it is talking about that topic. The object should be central and expressive. Provide ONLY the prompt text.")
    
    time.sleep(10)
    
    # --- Step 3: Generate Image ---
    print("Step 3: Generating Image...")
    send_message("Generate a realistic image based on the prompt you just wrote.")
    
    print("Waiting for image generation (30s)...")
    time.sleep(30)
    
    # --- Step 4: Download Image ---
    print("Step 4: Finding and Downloading Image...")
    try:
        # Save a debug screenshot
        driver.save_screenshot("debug_before_find.png")
        
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(images)} images.")
        
        # Find the largest image by area
        best_image = None
        max_area = 0
        
        for img in images:
            try:
                w = img.rect['width']
                h = img.rect['height']
                area = w * h
                # Filter small icons
                if area > max_area and w > 200 and h > 200:
                    max_area = area
                    best_image = img
            except:
                continue
        
        if best_image:
            print(f"Found best image ({max_area} px). Saving via screenshot...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", best_image)
            time.sleep(2)
            
            png_data = best_image.screenshot_as_png
            if len(png_data) > 2000: # Check for reasonable file size
                with open("gemini_final_image.png", "wb") as f:
                    f.write(png_data)
                print(f"SUCCESS: Image saved to gemini_final_image.png ({len(png_data)} bytes)")
            else:
                print("Warning: Image screenshot too small.")
        else:
            print("Could not identify a large generated image. Saving page backup.")
            driver.save_screenshot("gemini_workflow_screenshot.png")
            
    except Exception as e:
        print(f"Error during image extraction: {e}")

    # --- Step 5: Google Flow ---
    print("-" * 50)
    print("STEP 5: GOOGLE FLOW")
    flow_url = "https://labs.google/fx/tools/flow" 
    print(f"Navigating to {flow_url}...")
    driver.get(flow_url)
    
    time.sleep(15) 

    try:
        print("Looking for 'New project' or 'Create' button...")
        wait_flow = WebDriverWait(driver, 20)
        # Search for the New Project button
        new_btn = wait_flow.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'New project') or contains(text(), 'Create')]")))
        print(f"Clicking: {new_btn.text}")
        driver.execute_script("arguments[0].click();", new_btn)
        
        # --- USER REQUEST: 5 SEC LAG ---
        print("Action: 5-second lag for project to load...")
        time.sleep(5)
        # -------------------------------

        print("Step 6: Attaching Image...")
        # Attempt to upload image directly to the visible file input
        try:
             # Find file input - using a broadcast search
             file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
             if file_inputs:
                 file_input = file_inputs[0]
                 file_path = os.path.abspath("gemini_final_image.png")
                 file_input.send_keys(file_path)
                 print(f"Uploaded image: {file_path}")
             else:
                 # Fallback: find any button that might look like an upload/add image button
                 clickable_els = driver.find_elements(By.XPATH, "//button | //div[@role='button']")
                 for el in clickable_els:
                     if "image" in el.text.lower() or "upload" in el.text.lower() or "+" in el.text:
                         print(f"Clicking potential upload button: {el.text}")
                         el.click()
                         time.sleep(2)
                         # Then try to find input again
                         driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(os.path.abspath("gemini_final_image.png"))
                         break
        except Exception as e:
            print(f"Non-fatal upload issue: {e}")

        # --- Step 7: Text Prompt ---
        print("Step 7: Entering Reel Prompt...")
        # Find prompt area - often a textarea or contenteditable div
        wait_flow.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        text_areas = driver.find_elements(By.TAG_NAME, "textarea")
        if text_areas:
            prompt_input = text_areas[0]
            reel_prompt = f"A vertical viral instagram reel of this object talking about {topic_text}. Format: Educational and engaging."
            prompt_input.clear()
            prompt_input.send_keys(reel_prompt)
            print(f"Prompt entered: {reel_prompt}")
            time.sleep(1)
            
            # --- Step 8: Click Generate ---
            print("Step 8: Clicking Generate...")
            # Look for a generate button or just press Enter
            try:
                # Find button with text Generate or an arrow icon
                gen_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Generate')] | //button[@aria-label='Generate']")
                if gen_buttons:
                    gen_buttons[0].click()
                    print("Clicked Generate button.")
                else:
                    prompt_input.send_keys(Keys.ENTER)
                    print("Sent Enter to trigger generation.")
            except:
                prompt_input.send_keys(Keys.ENTER)
        else:
            print("Could not find prompt input.")
            
    except Exception as e:
        print(f"Error in Google Flow step: {e}")
        driver.save_screenshot("flow_final_error.png")

    print("-" * 50)
    print("WORKFLOW COMPLETE.")
    print("-" * 50)
    
    time.sleep(600) # Keep open



def main():
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        
    driver = setup_driver()
    try:
        run_gemini_workflow(driver)
    except Exception as e:
        print(f"Workflow Error: {e}")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Workflow Error: {e}\n")
    finally:
        print("Done. Closing in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
i m p o r t   o s  
 i m p o r t   t i m e  
 #   A d d e d   c o m m e n t s  
 #   S t e p   1  
 #   S t e p   2  
 #   S t e p   3  
 #   S t e p   4  
 #   S t e p   5  
 #   S t e p   6  
 