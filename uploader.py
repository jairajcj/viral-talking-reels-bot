from instagrapi import Client
import os

class InstagramUploader:
    def __init__(self, username, password):
        self.client = Client()
        self.username = username
        self.password = password
        
    def login(self):
        print("📸 Logging into Instagram...")
        try:
            self.client.login(self.username, self.password)
            print("✅ Login Successful")
            return True
        except Exception as e:
            print(f"❌ Login Failed: {e}")
            print("Tip: Try logging in cleanly or check 2FA/Challenge requirements.")
            return False

    def upload_reel(self, video_path, caption):
        print("🚀 Uploading to Instagram...")
        try:
            media = self.client.clip_upload(
                video_path,
                caption=caption
            )
            print(f"✅ Uploaded! Media ID: {media.pk}")
            return True
        except Exception as e:
            print(f"❌ Upload Failed: {e}")
            return False
