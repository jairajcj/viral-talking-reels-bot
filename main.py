import time
import os
import requests
import datetime
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

def run_gemini_workflow(driver):
    print("Navigating to Gemini...")
    driver.get("https://gemini.google.com/")
    
    wait = WebDriverWait(driver, 60)
    
    # 1. Login Check & Auto-Login
    print("-" * 50)
    print("STEP 1: LOGIN CHECK")
    
    try:
        input_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
        print("Already logged in.")
    except:
        print("Not logged in. Attempting auto-login...")
        try:
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            print("Entering email...")
            email_input.send_keys("jairajchilukala@gmail.com")
            email_input.send_keys(Keys.ENTER)
            
            time.sleep(3) 
            pass_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
            print("Entering password...")
            pass_input.send_keys("Woxsen@9912081240")
            pass_input.send_keys(Keys.ENTER)
            
            print("Login submitted. Waiting for redirection to Gemini...")
            wait_long = WebDriverWait(driver, 120) 
            input_area = wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            print("Successfully logged in!")
            
        except Exception as e:
            print(f"Auto-login failed: {e}")
            print("Please finish logging in manually in the browser.")
            time.sleep(10)
            input("Press ENTER here once you are logged in...")
            input_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            
    def send_message(text):
        inp = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        inp.send_keys(text)
        time.sleep(1)
        inp.send_keys(Keys.ENTER)
        
    # --- Step 1: Trending Fact Topic ---
    print("Step 1: Asking for Trending Fact Topic...")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    topic_prompt = f"Give me a unique, mind-blowing, and specific 'did you know' style fact that would make a great 8-second Instagram reel. Current time reference: {now_str}. Just the fact or topic name."
    send_message(topic_prompt)
    
    time.sleep(12) 
    topic_text = "Mind-blowing Fact"
    try:
        resp_elements = driver.find_elements(By.CSS_SELECTOR, "model-response, .model-response-text, content-block, .message-content")
        if resp_elements:
            topic_text = resp_elements[-1].text.strip().split('\n')[0]
            print(f"Captured Fact/Topic: {topic_text}")
    except:
        print("Could not capture specific topic text, using default.")

    # --- Step 2: Image for the Role ---
    print("\nStep 2: Generating Image for Expressive Object...")
    img_prompt_req = f"Write a detailed image generation prompt for an expressive object that looks like it is talking about: {topic_text}. The object should be central and very expressive. Provide ONLY the prompt text."
    send_message(img_prompt_req)
    time.sleep(10)

    send_message("Generate a high-quality, realistic image based on the prompt you just provided.")
    print(f"Waiting for image generation (45s)...")
    time.sleep(45)

    # --- Step 3: Extract Image ---
    try:
        filename = "gemini_final_image.png"
        responses = driver.find_elements(By.CSS_SELECTOR, "model-response")
        target_container = responses[-1] if responses else driver
        
        images = target_container.find_elements(By.TAG_NAME, "img")
        best_image = None
        max_area = 0
        for img in images:
            try:
                w = img.rect['width']
                h = img.rect['height']
                area = w * h
                if area > max_area and w > 150 and h > 150:
                    max_area = area
                    best_image = img
            except:
                continue
        
        if best_image:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", best_image)
            time.sleep(2)
            png_data = best_image.screenshot_as_png
            if len(png_data) > 2000:
                with open(filename, "wb") as f:
                    f.write(png_data)
                print(f"SUCCESS: Saved {filename} ({len(png_data)} bytes)")
            else:
                print("Warning: Screenshot was too small.")
        else:
            print("Could not find a large image.")
    except Exception as e:
        print(f"Error extracting image: {e}")

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
        new_btn = wait_flow.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'New project') or contains(text(), 'Create')]")))
        print(f"Clicking: {new_btn.text}")
        driver.execute_script("arguments[0].click();", new_btn)
        
        time.sleep(5)

        print("Step 6: Attaching Image...")
        try:
             file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
             if file_inputs:
                 file_input = file_inputs[0]
                 file_path = os.path.abspath("gemini_final_image.png")
                 file_input.send_keys(file_path)
                 print(f"Uploaded image: {file_path}")
             else:
                 print("Could not find file input for upload.")
        except Exception as e:
            print(f"Non-fatal upload issue: {e}")

        # --- Step 7: Text Prompt ---
        print("Step 7: Entering Reel Prompt (8-sec Fact)...")
        wait_flow.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        text_areas = driver.find_elements(By.TAG_NAME, "textarea")
        if text_areas:
            prompt_input = text_areas[0]
            reel_prompt = f"A vertical viral Instagram reel of this object talking about this fact: {topic_text}. The video must be exactly 8 seconds long."
            prompt_input.clear()
            prompt_input.send_keys(reel_prompt)
            print(f"Prompt entered: {reel_prompt}")
            time.sleep(2)
            
            # --- Step 8: Click Generate ---
            # print("Step 8: Clicking Generate...")
            # try:
            #     gen_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Generate')] | //button[@aria-label='Generate']")
            #     if gen_buttons:
            #         gen_buttons[0].click()
            #         print("Clicked Generate button.")
            #     else:
            #         prompt_input.send_keys(Keys.ENTER)
            #         print("Sent Enter to trigger generation.")
            # except:
            #     prompt_input.send_keys(Keys.ENTER)
            print("Prompt entered. Stopping as requested.")
        else:
            print("Could not find prompt input.")
            
    except Exception as e:
        print(f"Error in Google Flow step: {e}")
        driver.save_screenshot("flow_final_error.png")

    print("-" * 50)
    print("WORKFLOW COMPLETE.")
    print("-" * 50)

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
        print("Workflow finished. Keeping browser open as requested.")
        # Keeping browser open by not calling driver.quit()
        while True:
            time.sleep(100)

if __name__ == "__main__":
    main()

