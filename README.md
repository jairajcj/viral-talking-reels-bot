# Viral Reel Bot 🤖🎬


This tool automates the process of creating "Viral" Instagram Reels using AI.
It uses **Google Gemini** for creativity, **Pollinations.ai** for images, **EdgeTTS** for voiceovers, and **MoviePy** for video editing.

## Features
- 🧠 **Gemini Powered Ideas**: Generates viral hooks and scripts about "impactful old age facts".
- 🎨 **AI Image Generation**: Creates hyper-realistic images matching the script.
- 🗣️ **Neural Voiceover**: Adds a professional-grade narration.
- 🎞️ **Auto-Editing**: Compiles everything into a 9:16 vertical Reel.
- ⬆️ **Auto-Upload**: (Experimental) Can upload directly to Instagram.

## Setup
1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If you get an error with MoviePy wanting ImageMagick, install ImageMagick for Windows.*

2.  **Configuration**:
    - Open `config.py`.
    - Add your **GEMINI_API_KEY**. Get it for free at [Google AI Studio](https://aistudio.google.com/).
    - (Optional) Add your Instagram credentials if you want auto-upload.

## Usage
Run the main script:
```bash
python main.py
```

The bot will:
1.  Open Gemini (web) to show you the start.
2.  Generate a script and image idea.
3.  Create the image.
4.  Generate the voiceover and video.
5.  Save the result in `assets/final_reel.mp4`.
6.  Upload to Instagram (if configured).
