import logging
from groq import Groq

logger = logging.getLogger(__name__)

class GPTTranslator:
    def __init__(self):
        self.client = Groq()
        if not self.client.api_key:
            raise Exception("GROQ_API_KEY environment variable not set")
    
    def translate_segments(self, segments, source_lang, target_lang):
        """Translate all speech segments"""
        try:
            print(f"🌍 STARTING TRANSLATION: {len(segments)} segments from {source_lang} to {target_lang}")
            logger.info(f"Starting translation of {len(segments)} segments from {source_lang} to {target_lang}")
            
            if not segments:
                print("❌ NO SEGMENTS TO TRANSLATE!")
                logger.warning("No segments to translate!")
                return []
            
            translated_segments = []
            
            for i, segment in enumerate(segments):
                print(f"🔤 TRANSLATING SEGMENT {i+1}/{len(segments)}:")
                print(f"   📥 ORIGINAL: '{segment['text']}'")
                logger.info(f"Translating segment {i+1}: '{segment['text'][:50]}...'")
                
                translated_text = self.translate_text(
                    segment['text'], 
                    source_lang, 
                    target_lang
                )
                
                print(f"   📤 TRANSLATED: '{translated_text}'")
                print(f"   ⏱️  TIMING: {segment['start_time']:.2f}s - {segment['end_time']:.2f}s")
                logger.info(f"Translation result: '{translated_text[:50]}...'")
                
                translated_segment = {
                    'start_time': segment['start_time'],
                    'end_time': segment['end_time'],
                    'original_text': segment['text'],
                    'translated_text': translated_text,
                    'text': translated_text  # Add this for compatibility with subtitle generator
                }
                translated_segments.append(translated_segment)
                print(f"   ✅ SEGMENT {i+1} COMPLETE")
            
            print(f"🎯 TRANSLATION COMPLETE: {len(translated_segments)} segments successfully translated")
            logger.info(f"Successfully translated {len(translated_segments)} segments")
            return translated_segments
            
        except Exception as e:
            print(f"💥 TRANSLATION FAILED: {str(e)}")
            logger.error(f"Translation error: {str(e)}")
            raise Exception(f"Failed to translate segments: {str(e)}")
    
    def translate_text(self, text, source_lang, target_lang):
        """Translate a single text using Groq API"""
        try:
            # Map language codes to full names for better GPT understanding
            lang_map = {
                'en': 'English',
                'es': 'Spanish',
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ru': 'Russian',
                'ja': 'Japanese',
                'ko': 'Korean',
                'zh': 'Chinese',
                'ar': 'Arabic',
                'hi': 'Hindi',
                'auto': 'auto-detect'
            }
            
            source_language = lang_map.get(source_lang, source_lang)
            target_language = lang_map.get(target_lang, target_lang)
            
            system_prompt = (
                "You are an expert translator specializing in video subtitles. "
                "Your task is to translate the user's text accurately and concisely, "
                "preserving the original meaning, tone, and context. "
                "The translation should be natural-sounding and suitable for on-screen display. "
                "Return ONLY the translated text, without any additional explanations or introductory phrases."
            )

            user_prompt = (
                f"Source Language: {source_language}\n"
                f"Target Language: {target_language}\n"
                f"Text to translate:\n\n---\n{text}\n---"
            )

            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None
            )
            
            translated_text = ""
            for chunk in response:
                translated_text += chunk.choices[0].delta.content or ""

            if translated_text:
                return translated_text.strip()
            else:
                return text
            
        except Exception as e:
            logger.error(f"Groq translation error: {str(e)}")
            # Return original text if translation fails
            return text
    
    def get_supported_languages(self):
        """Return supported language codes"""
        return {
            'auto': 'Auto-detect',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
