
This project automates the creation of viral "talking object" reels for Instagram. It finds trending topics, generates AI images of expressive objects, and automates the video generation process on platforms like Google Flow (Labs).

## Features
- **Unique Topic Generation**: Fetches a fresh trending topic from Gemini every run.
- **AI Image Generation**: Automatically requests and captures high-quality object images.
- **Workflow Automation**: Full Selenium-based automation for Google Gemini and Google Flow.
- **Context-Aware Prompts**: The final reel script is tailored to the captured trending topic.
- **Safe State Management**: Uses a dedicated Selenium user data directory to maintain sessions.

## Prerequisites
1. **Python**: Version 3.10+ recommended.
2. **Google Chrome**: Ensure Chrome is installed on your system.
3. **Accounts**: You need a logged-in Google account for Gemini and Labs.

## Installation
1. Clone the repository to your local machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the automation:
   ```bash
   python main.py
   ```
2. **First Run**: If not logged in, the script will pause. Log in manually in the opened Chrome window and press Enter in the terminal to continue.
3. **Automation**: The script will:
   - Find a trend.
   - Generate and save an image.
   - Navigate to Google Flow, upload the image, enter the prompt, and keep the browser open for generation.

## Troubleshooting
- **Logs**: Check `error_log.txt` if the script fails.
- **Screenshots**: Look at `debug_before_find.png` or `flow_final_error.png` to see where the automation stopped.
- **Selectors**: If the Google UI updates, selectors may need updating in `main.py`.
