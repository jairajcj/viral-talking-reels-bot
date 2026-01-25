# AI Trend & Image Automation

This project automates the process of finding a trending Instagram topic using ChatGPT, generating an image prompt for it, and then using Gemini to generate the image.

## Prerequisites

1.  **Python**: Ensure Python is installed.
2.  **Browsers**: Google Chrome should be installed.
3.  **Accounts**: You must have accounts for [ChatGPT](https://chatgpt.com) and [Google Gemini](https://gemini.google.com).

## Installation

1.  Open a terminal in this folder.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

## Usage

1.  Run the script:
    ```bash
    python main.py
    ```

2.  **First Run / Login**:
    *   The browser will open (NOT in headless mode).
    *   If you are not logged in to ChatGPT or Gemini, the script will pause and ask you to log in manually in the browser window.
    *   Once logged in, verify the prompt in the terminal asking you to press **Enter** to continue.
    *   The browser session is saved in the `user_data` folder, so you shouldn't need to log in every time.

## workflow

1.  **ChatGPT**: Asks for a trending, knowledgeable Instagram topic.
2.  **ChatGPT**: Asks for an image prompt of an object talking about that topic.
3.  **Gemini**: Pastes the prompt to generate an image.

## Troubleshooting

*   **Selectors**: Web automation is fragile. If ChatGPT or Gemini change their website layout (class names, IDs), the script might timeout waiting for a selector.
*   **Captchas**: If a captcha appears, solve it manually in the browser window.
