
import os
import sys
import webbrowser
import time
from config import GOOGLE_EMAIL, GOOGLE_PASSWORD, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, CHATGPT_EMAIL, CHATGPT_PASSWORD
from gemini_browser import GeminiBrowser
from chatgpt_browser import ChatGPTBrowser
from video_maker import VideoMaker
from uploader import InstagramUploader

def main():
    print("==========================================")
    print("   VIRAL REEL GENERATOR: NEW PIPELINE")
    print("   ChatGPT -> Gemini -> Google Labs (Veo)")
    print("==========================================")

    # 1. ChatGPT: Object Maker & Script
    print("\n[1/4] ChatGPT: Generating Viral Concept...")
    chatgpt = ChatGPTBrowser(CHATGPT_EMAIL, CHATGPT_PASSWORD)
    content_data = chatgpt.generate_object_content()
    chatgpt.close()
    
    if not content_data:
        print("❌ ChatGPT failed. Checking for manual override/demo...")
        # Fallback or return
        content_data = {
             "object_description": "A rusted iron key",
             "image_prompt": "A cinematic close-up of a rusted iron key, ancient, mysterious, dramatic lighting, 8k",
             "video_script": "I am the key to a forgotten door. You walk past me every day. But you never ask what I open. They say I lock away secrets. But the truth is, I lock away potential. Use me.",
             "hashtags": ["#mystery", "#unlock", "#potential"]
        }
        print("   Using Demo Data.")

    print(f"\n   -------- CONTENT PLAN --------")
    print(f"   🎭 Object: {content_data.get('object_description')}")
    print(f"   📜 Script: {content_data.get('video_script')[:50]}...")
    print(f"   ------------------------------")

    # 2. Gemini: Generate Image
    print("\n[2/4] Gemini: Generating Image...")
    if GOOGLE_EMAIL == "YOUR_GOOGLE_EMAIL":
        print("❌ ERROR: Please set GOOGLE_EMAIL in config.py")
        return

    gemini = GeminiBrowser(GOOGLE_EMAIL, GOOGLE_PASSWORD)
    
    # We keep the session open for the next step if possible, or just re-use instance
    image_path = gemini.generate_image_in_chat(content_data.get('image_prompt'))
    
    if not image_path:
        print("❌ Image generation failed.")
        return

    # 3. Google Labs (Gemini/Veo): Generate Video
    # The user asked to "send image to Google Labs". 
    # Since we are in Gemini, we will attempt to generate the video in the same session.
    # If Gemini supports Image-to-Video in the chat, this works. 
    # If not, we use the Text-to-Video (powered by Veo/Labs) with the same prompt.
    print(f"\n[3/4] Google Labs (Gemini): Creating Reel Video...")
    
    # Refined prompt for Video
    video_prompt = content_data.get('image_prompt') + " . The object is talking to the camera. Cinematic movement."
    video_path = gemini.generate_video_in_chat(video_prompt, image_path=image_path)
    
    gemini.close()

    if not video_path:
        print("⚠️  Google Labs Video generation failed. Using Static Image + Effects.")
        visual_path = image_path
    else:
        print(f"✅ Google Labs Video Acquired: {video_path}")
        visual_path = video_path

    # 4. Assemble Reel (Audio + Loop/Effects)
    print("\n[4/4] Final Assembly (Audio + 45-90s Loop)...")
    video_maker = VideoMaker()
    try:
        final_video_path = video_maker.make_video(content_data['video_script'], visual_path)
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # 5. Upload to Instagram
    print("\n[5/5] Uploading to Instagram...")
    if INSTAGRAM_USERNAME != "YOUR_USERNAME":
        uploader = InstagramUploader(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        if uploader.login():
            hashtags = content_data.get('hashtags', [])
            caption = f"{content_data.get('video_script', '')[:100]}...\n\n{' '.join(hashtags)}"
            uploader.upload_reel(final_video_path, caption)
            webbrowser.open(f"https://www.instagram.com/{INSTAGRAM_USERNAME}/")
    else:
        print(f"✅ Video saved at: {os.path.abspath(final_video_path)}")

    print("\n==========================================")
    print("   ✅ PROCESS COMPLETE")
    print("==========================================")

if __name__ == "__main__":
    main()
