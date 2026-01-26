import asyncio
import edge_tts
from moviepy.editor import *
import os
import re

class VideoMaker:
    def __init__(self):
        self.voice = "en-US-ChristopherNeural" # Deep male voice, good for "impactful" content
        
    async def generate_audio(self, text, output_file="assets/audio.mp3"):
        print("🗣️ Generating Voiceover...")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)
        return output_file

    def create_subtitles(self, script_text, duration):
        """Generate word-by-word subtitle clips for professional look"""
        # Split into phrases for better readability
        phrases = re.split(r'[.!?]\s+', script_text)
        clips = []
        
        time_per_phrase = duration / max(len(phrases), 1)
        
        for i, phrase in enumerate(phrases):
            if not phrase.strip():
                continue
                
            start_time = i * time_per_phrase
            end_time = min((i + 1) * time_per_phrase, duration)
            
            try:
                # Create subtitle with professional styling
                txt = TextClip(
                    phrase.strip().upper(),
                    fontsize=60,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=3,
                    size=(1000, None),
                    method='caption',
                    align='center'
                )
                txt = txt.set_position(('center', 'bottom')).set_start(start_time).set_duration(end_time - start_time)
                clips.append(txt)
            except Exception as e:
                print(f"⚠️ Subtitle creation failed: {e}")
                return None
        
        return clips

    def create_reel(self, visual_path, audio_path, script_text, output_file="assets/final_reel.mp4"):
        print("🎬 Assembling Reel...")
        
        # Load Audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Determine if input is Image or Video
        if visual_path.endswith(('.mp4', '.mov', '.avi')):
            print("   Using Video Input (Looping to match audio)...")
            video_clip = VideoFileClip(visual_path)
            # Loop video to fill duration
            video_clip = video_clip.loop(duration=duration)
            # Resize/Crop to 9:16 if needed
            w, h = video_clip.size
            if w > h: # Landscape, likely need crop
                video_clip = video_clip.resize(height=1920)
                video_clip = video_clip.crop(x1=video_clip.w//2-540, y1=0, x2=video_clip.w//2+540, y2=1920)
            else:
                 video_clip = video_clip.resize(newsize=(1080, 1920))
            
            final_clip = video_clip.set_audio(audio)
        else:
            print("   Using Image Input...")
            # Load Image
            image_clip = ImageClip(visual_path).set_duration(duration)
            image_clip = image_clip.resize(height=1920)
            
            # Center crop to 9:16 (1080x1920)
            w, h = image_clip.size
            x_center = w // 2
            image_clip = image_clip.crop(x1=x_center-540, y1=0, x2=x_center+540, y2=1920)
            
            # Apply Ken Burns zoom effect
            image_clip = image_clip.resize(lambda t : 1 + 0.05*t)
            final_clip = image_clip.set_audio(audio)
        
        # Add Subtitles
        print("   Adding Subtitles...")
        subtitles = self.create_subtitles(script_text, duration)
        if subtitles:
             final_clip = CompositeVideoClip([final_clip] + subtitles)
        
        # Export
        print("📼 Rendering video (Fast Mode)...")
        final_clip.write_videofile(
            output_file, 
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset='ultrafast',
            threads=4
        )
        
        print(f"✅ Video created: {output_file}")
        return output_file

    def make_video(self, script, image_path):
        audio_path = asyncio.run(self.generate_audio(script))
        return self.create_reel(image_path, audio_path, script)

if __name__ == "__main__":
    # Test
    vm = VideoMaker()
    # Mock files need to exist to test
    pass
