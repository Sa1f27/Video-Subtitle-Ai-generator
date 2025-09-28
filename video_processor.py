import os
import logging
import subprocess
import json
from pydub import AudioSegment
from pydub.silence import split_on_silence
import yt_dlp
from groq import Groq
import re

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        pass

    def download_video(self, url, output_dir, job_id):
        """Download video from URL using yt-dlp"""
        try:
            output_path = os.path.join(output_dir, f"{job_id}_downloaded.%(ext)s")

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': output_path,
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find the downloaded file
            for file in os.listdir(output_dir):
                if file.startswith(f"{job_id}_downloaded"):
                    return os.path.join(output_dir, file)

            raise Exception("Downloaded file not found")

        except Exception as e:
            logger.error(f"Video download error: {str(e)}")
            raise Exception(f"Failed to download video: {str(e)}")

    def get_video_duration(self, video_path):
        """Get video duration in seconds using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries',
                'format=duration', '-of', 'csv=p=0', video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception as e:
            logger.error(f"Duration check error: {str(e)}")
            raise Exception(f"Failed to get video duration: {str(e)}")

    def extract_audio(self, video_path, audio_folder, job_id):
        """Extract audio from video using ffmpeg"""
        try:
            audio_filename = f"{job_id}_audio.wav"
            audio_path = os.path.join(audio_folder, audio_filename)

            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg', '-y', '-i', video_path,
                '-ac', '1', '-ar', '16000', '-f', 'wav', audio_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)

            return audio_path

        except Exception as e:
            logger.error(f"Audio extraction error: {str(e)}")
            raise Exception(f"Failed to extract audio: {str(e)}")

    def extract_speech_segments(self, audio_path):
        """Extract speech segments using Groq Whisper API with verbose JSON response"""
        try:
            print(f"🎤 STARTING GROQ WHISPER TRANSCRIPTION FROM: {audio_path}")
            logger.info(f"Starting Groq Whisper transcription on: {audio_path}")

            client = Groq()
            if not client.api_key:
                raise Exception("GROQ_API_KEY environment variable not set")

            print("🤖 SENDING AUDIO TO GROQ API...")

            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json",
                )

            print(f"✅ GROQ TRANSCRIPTION SUCCESS!")

            # Process segments from verbose JSON
            speech_segments = []
            for segment in transcription.segments:
                speech_segments.append({
                    'start_time': segment['start'],
                    'end_time': segment['end'],
                    'text': segment['text']
                })

            if speech_segments:
                print(f"📊 CREATED {len(speech_segments)} SEGMENTS:")
                for i, segment in enumerate(speech_segments):
                    print(f"   🎬 SEGMENT {i+1}: {segment['start_time']:.2f}s-{segment['end_time']:.2f}s")
                    print(f"       💬 TEXT: '{segment['text']}'")
            else:
                # Fallback to single segment with full text
                duration = transcription.duration
                speech_segments = [{
                    'start_time': 0.0,
                    'end_time': duration,
                    'text': transcription.text.strip()
                }]

            return speech_segments

        except Exception as e:
            print(f"💥 GROQ TRANSCRIPTION FAILED: {str(e)}")
            logger.error(f"Groq transcription error: {str(e)}")

            # Final fallback
            try:
                audio_segment = AudioSegment.from_wav(audio_path)
                duration = len(audio_segment) / 1000

                fallback_segments = [{
                    'start_time': 0.0,
                    'end_time': duration,
                    'text': "Audio content detected - Transcription failed"
                }]

                return fallback_segments
            except:
                return [{
                    'start_time': 0.0,
                    'end_time': 30.0,
                    'text': "Audio processing completed"
                }]
