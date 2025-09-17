"""
YouTube Transcript Generator for AI Baba Admin System
Integrates with existing text processing pipeline for automatic wisdom extraction
Updated with pytubefix and improved error handling
"""

import torch
from transformers import pipeline
import os
import tempfile
import textwrap
from typing import Tuple, Optional
from datetime import datetime

# Import pytubefix instead of pytube
try:
    from pytubefix import YouTube
except ImportError:
    print("Installing pytubefix...")
    os.system("pip install pytubefix")
    from pytubefix import YouTube

class YouTubeTranscriber:
    """YouTube video transcription service for AI Baba"""
    
    def __init__(self):
        self.transcriber = None
        # Updated model name - use the latest stable version
        self.model_name = "openai/whisper-large-v3"  # More reliable than distil-whisper
        # Alternative: "distil-whisper/distil-large-v3" if you prefer speed over accuracy
        self.device = 0 if torch.cuda.is_available() else -1
        
    def _initialize_model(self) -> bool:
        """Initialize the transcription model with better error handling"""
        try:
            if self.transcriber is None:
                print("Loading transcription model...")
                self.transcriber = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_name,
                    device=self.device,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    model_kwargs={"use_safetensors": True}  # Added for stability
                )
                print("✅ Model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Model initialization failed: {e}")
            # Fallback to a smaller, more reliable model
            try:
                print("Trying fallback model...")
                self.model_name = "openai/whisper-base"
                self.transcriber = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_name,
                    device=self.device,
                    torch_dtype=torch.float32
                )
                print("✅ Fallback model loaded")
                return True
            except Exception as fallback_error:
                print(f"❌ Fallback model also failed: {fallback_error}")
                return False

    def get_video_info(self, video_url: str) -> Tuple[bool, str, Optional[dict]]:
        """Get basic video information without downloading"""
        try:
            cleaned_url = self._clean_youtube_url(video_url)
            
            # Use pytubefix with better error handling
            yt = YouTube(
                cleaned_url,
                use_oauth=False,
                allow_oauth_cache=True
            )
            
            # Force connection to validate
            yt.check_availability()
            
            video_info = {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'description': yt.description[:200] + "..." if yt.description and len(yt.description) > 200 else (yt.description or ""),
                'thumbnail_url': yt.thumbnail_url,
                'publish_date': yt.publish_date.isoformat() if yt.publish_date else None
            }
            
            return True, "Video information retrieved successfully", video_info
            
        except Exception as e:
            error_msg = str(e)
            if "unavailable" in error_msg.lower():
                return False, "Video is unavailable, private, or doesn't exist", None
            elif "age" in error_msg.lower():
                return False, "Video is age-restricted and cannot be accessed", None
            else:
                return False, f"Failed to get video info: {error_msg}", None

    def generate_transcript(self, video_url: str, progress_callback=None) -> Tuple[bool, str, Optional[str]]:
        """Generate transcript from YouTube video with improved error handling"""
        temp_file = None
        
        def update_progress(message: str):
            if progress_callback:
                progress_callback(message)
            else:
                print(message)
        
        try:
            # Step 1: Validate URL
            update_progress("🔍 Validating video URL...")
            cleaned_url = self._clean_youtube_url(video_url)
            
            # Use pytubefix with better configuration
            yt = YouTube(
                cleaned_url,
                use_oauth=False,
                allow_oauth_cache=True
            )
            
            # Check availability
            yt.check_availability()
            
            # Check video length (limit to reasonable duration)
            if yt.length and yt.length > 7200:  # 2 hour limit
                return False, "Video is too long (max 2 hours supported)", None
                
            update_progress(f"📹 Video: {yt.title} ({yt.length//60}:{yt.length%60:02d})")
            
            # Step 2: Download audio with better stream selection
            update_progress("📥 Downloading audio stream...")
            
            # Try multiple audio stream options
            audio_stream = None
            stream_options = [
                yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first(),
                yt.streams.filter(only_audio=True, file_extension='webm').order_by('abr').desc().first(),
                yt.streams.filter(only_audio=True).first(),
                yt.streams.filter(adaptive=True, file_extension='mp4').order_by('abr').desc().first()
            ]
            
            for stream in stream_options:
                if stream:
                    audio_stream = stream
                    break
            
            if not audio_stream:
                return False, "No suitable audio stream found", None
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                temp_file = tmp.name
            
            # Download with progress tracking
            try:
                audio_stream.download(filename=temp_file)
                update_progress("✅ Audio downloaded successfully")
            except Exception as download_error:
                return False, f"Audio download failed: {str(download_error)}", None
            
            # Verify file was downloaded
            if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                return False, "Downloaded file is empty or corrupted", None
            
            # Step 3: Initialize transcription model
            update_progress("🤖 Loading transcription model...")
            if not self._initialize_model():
                return False, "Failed to initialize transcription model", None
            
            # Step 4: Transcribe with better parameters
            update_progress("💬 Transcribing audio... (this may take several minutes)")
            
            try:
                # Use optimized parameters for better results
                result = self.transcriber(
                    temp_file,
                    chunk_length_s=30,
                    stride_length_s=5,
                    return_timestamps=False,  # Set to True if you want timestamps
                    generate_kwargs={
                        "task": "transcribe",
                        "language": "en"  # Specify language for better accuracy
                    }
                )
                
                transcript = result["text"].strip() if isinstance(result, dict) else str(result).strip()
                update_progress("✅ Transcription completed!")
                
                if not transcript:
                    return False, "Transcription produced empty result", None
                
                return True, f"Successfully transcribed {len(transcript)} characters", transcript
                
            except Exception as transcription_error:
                return False, f"Transcription failed: {str(transcription_error)}", None
            
        except Exception as e:
            error_msg = f"Transcription error: {str(e)}"
            update_progress(f"❌ {error_msg}")
            return False, error_msg, None
            
        finally:
            # Cleanup temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    update_progress("🧹 Cleaned up temporary files")
                except Exception as cleanup_error:
                    print(f"Warning: Could not clean up temp file: {cleanup_error}")

    def format_transcript_for_processing(self, transcript: str, video_info: dict) -> str:
        """Format transcript with video metadata for better processing"""
        formatted_text = f"""YouTube Video Transcript
========================
Video Title: {video_info.get('title', 'Unknown')}
Author: {video_info.get('author', 'Unknown')}
Duration: {video_info.get('length', 0)//60}:{video_info.get('length', 0)%60:02d}
Views: {video_info.get('views', 'Unknown'):,} 
Published: {video_info.get('publish_date', 'Unknown')}
Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Transcript Content:
==================
{transcript}
"""
        return formatted_text.strip()

    def _clean_youtube_url(self, url: str) -> str:
        """Clean YouTube URL - improved version"""
        import re
        
        if not url:
            return url
        
        # Remove any extra whitespace
        url = url.strip()
        
        # Extract video ID using comprehensive regex
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'(?:m\.youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
        
        # If no pattern matches, return original URL
        return url

    def validate_youtube_url(self, url: str) -> Tuple[bool, str]:
        """Validate YouTube URL with improved error handling"""
        if not url:
            return False, "URL cannot be empty"
        
        cleaned_url = self._clean_youtube_url(url)
        
        # Basic URL pattern check
        youtube_patterns = [
            'youtube.com/watch?v=',
            'youtu.be/',
            'm.youtube.com/watch?v=',
            'www.youtube.com/watch?v='
        ]
        
        if not any(pattern in cleaned_url.lower() for pattern in youtube_patterns):
            return False, "URL does not appear to be a valid YouTube URL"
        
        try:
            # Test with pytubefix
            yt = YouTube(cleaned_url, use_oauth=False, allow_oauth_cache=True)
            yt.check_availability()
            return True, f"Valid YouTube URL: {yt.title}"
            
        except Exception as e:
            error_msg = str(e)
            if "unavailable" in error_msg.lower():
                return False, "YouTube video is unavailable or private"
            elif "age" in error_msg.lower():
                return False, "Video is age-restricted"
            else:
                return False, f"Invalid YouTube URL: {error_msg}"

# Legacy function for backward compatibility
def get_youtube_transcript(video_url: str) -> str:
    """Legacy function for backward compatibility"""
    transcriber = YouTubeTranscriber()
    success, message, transcript = transcriber.generate_transcript(video_url)
    if success:
        return transcript
    else:
        return f"An error occurred: {message}"

# Example usage and testing
if __name__ == "__main__":
    # Test the transcriber
    transcriber = YouTubeTranscriber()
    
    # Test URL - replace with your URL
    test_url = "https://www.youtube.com/watch?v=N-N2psoS8pQ"
    print("Testing Improved YouTube Transcriber...")
    print(f"URL: {test_url}")
    
    # Validate URL
    valid, msg = transcriber.validate_youtube_url(test_url)
    print(f"URL Validation: {msg}")
    
    if valid:
        # Get video info
        success, message, info = transcriber.get_video_info(test_url)
        if success:
            print(f"Video Info: {info['title']} by {info['author']}")
            
            # Generate transcript (uncomment to test)
            print("Starting transcription...")
            success, message, transcript = transcriber.generate_transcript(test_url)
            if success:
                print(f"✅ Success! Transcript length: {len(transcript)} characters")
                print(f"Preview: {transcript[:200]}...")
            else:
                print(f"❌ Transcription failed: {message}")
        else:
            print(f"❌ Failed to get video info: {message}")
# """
# YouTube Transcript Generator for AI Baba Admin System
# Integrates with existing text processing pipeline for automatic wisdom extraction
# """
# import torch
# from transformers import pipeline
# from pytube import YouTube
# import os
# import tempfile
# import textwrap
# from typing import Tuple, Optional
# from datetime import datetime


# class YouTubeTranscriber:
#     """YouTube video transcription service for AI Baba"""
    
#     def __init__(self):
#         self.transcriber = None
#         self.model_name = "distil-whisper/distil-large-v2"
#         self.device = 0 if torch.cuda.is_available() else -1
        
#     def _initialize_model(self) -> bool:
#         """Initialize the transcription model"""
#         try:
#             if self.transcriber is None:
#                 self.transcriber = pipeline(
#                     "automatic-speech-recognition", 
#                     model=self.model_name,
#                     device=self.device,
#                     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
#                 )
#             return True
#         except Exception as e:
#             print(f"Model initialization failed: {e}")
#             return False
    
#     def get_video_info(self, video_url: str) -> Tuple[bool, str, Optional[dict]]:
#         """
#         Get basic video information without downloading
        
#         Args:
#             video_url (str): YouTube video URL
            
#         Returns:
#             Tuple[bool, str, Optional[dict]]: (success, message, video_info)
#         """
#         try:
#             # Clean the URL and create YouTube object
#             cleaned_url = self._clean_youtube_url(video_url)
#             yt = YouTube(cleaned_url)
            
#             # Get video info
#             video_info = {
#                 'title': yt.title,
#                 'author': yt.author,
#                 'length': yt.length,  # seconds
#                 'views': yt.views,
#                 'description': yt.description[:200] + "..." if len(yt.description) > 200 else yt.description,
#                 'thumbnail_url': yt.thumbnail_url,
#                 'publish_date': yt.publish_date.isoformat() if yt.publish_date else None
#             }
            
#             return True, "Video information retrieved successfully", video_info
            
#         except Exception as e:
#             return False, f"Failed to get video info: {str(e)}", None
    
#     def generate_transcript(self, video_url: str, progress_callback=None) -> Tuple[bool, str, Optional[str]]:
#         """
#         Generate transcript from YouTube video
        
#         Args:
#             video_url (str): YouTube video URL
#             progress_callback: Optional callback function to report progress
            
#         Returns:
#             Tuple[bool, str, Optional[str]]: (success, message, transcript)
#         """
#         temp_file = None
        
#         def update_progress(message: str):
#             if progress_callback:
#                 progress_callback(message)
#             else:
#                 print(message)
        
#         try:
#             # Step 1: Clean the URL and validate
#             update_progress("🔍 Validating video URL...")
            
#             # Clean the URL using the dedicated method
#             cleaned_url = self._clean_youtube_url(video_url)
            
#             yt = YouTube(cleaned_url)
            
#             # Check video length (limit to reasonable duration)
#             if yt.length and yt.length > 3600:  # 1 hour limit
#                 return False, "Video is too long (max 1 hour supported)", None
            
#             update_progress(f"📹 Video: {yt.title} ({yt.length//60}:{yt.length%60:02d})")
            
#             # Step 2: Download audio
#             update_progress("📥 Downloading audio stream...")
#             audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            
#             if not audio_stream:
#                 return False, "No suitable audio stream found", None
            
#             # Create temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
#                 temp_file = tmp.name
            
#             # Download audio
#             audio_stream.download(filename=temp_file)
#             update_progress("✅ Audio downloaded successfully")
            
#             # Step 3: Initialize transcription model
#             update_progress("🤖 Loading transcription model...")
#             if not self._initialize_model():
#                 return False, "Failed to initialize transcription model", None
            
#             update_progress("✅ Model loaded")
            
#             # Step 4: Transcribe
#             update_progress("💬 Transcribing audio... (this may take several minutes)")
            
#             # Process the audio file
#             result = self.transcriber(temp_file, chunk_length_s=30, stride_length_s=5)
#             transcript = result["text"].strip()
            
#             update_progress("✅ Transcription completed!")
            
#             if not transcript:
#                 return False, "Transcription produced empty result", None
            
#             return True, f"Successfully transcribed {len(transcript)} characters", transcript
            
#         except Exception as e:
#             error_msg = f"Transcription error: {str(e)}"
#             update_progress(f"❌ {error_msg}")
#             return False, error_msg, None
        
#         finally:
#             # Cleanup temporary file
#             if temp_file and os.path.exists(temp_file):
#                 try:
#                     os.remove(temp_file)
#                     update_progress("🧹 Cleaned up temporary files")
#                 except:
#                     pass
    
#     def format_transcript_for_processing(self, transcript: str, video_info: dict) -> str:
#         """
#         Format transcript with video metadata for better processing
        
#         Args:
#             transcript (str): Raw transcript text
#             video_info (dict): Video metadata
            
#         Returns:
#             str: Formatted transcript with metadata
#         """
#         formatted_text = f"""
# YouTube Video Transcript
# ========================

# Video Title: {video_info.get('title', 'Unknown')}
# Author: {video_info.get('author', 'Unknown')}
# Duration: {video_info.get('length', 0)//60}:{video_info.get('length', 0)%60:02d}
# Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Transcript Content:
# ==================

# {transcript}
# """
#         return formatted_text.strip()
    
#     def _clean_youtube_url(self, url: str) -> str:
#         """
#         Clean YouTube URL by extracting only the video ID and constructing a standard URL
#         This handles various YouTube URL formats and removes problematic parameters
        
#         Args:
#             url (str): YouTube URL to clean
            
#         Returns:
#             str: Cleaned YouTube URL with only the video ID
#         """
#         import re
        
#         if not url:
#             return url
            
#         # Try to extract video ID using regex patterns
#         # Pattern for youtu.be URLs
#         youtu_be_pattern = r'youtu\.be\/([a-zA-Z0-9_-]{11})'
#         # Pattern for youtube.com URLs with v parameter - more permissive pattern
#         youtube_pattern = r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})'
#         # Direct pattern for the specific URL format in the example
#         direct_pattern = r'www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
#         # Fallback pattern for other YouTube URL formats
#         youtube_fallback_pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})'
        
#         # First try the specific youtu.be pattern
#         match = re.search(youtu_be_pattern, url)
#         if match:
#             video_id = match.group(1)
#             return f"https://www.youtube.com/watch?v={video_id}"
            
#         # Try the direct pattern for the specific URL format in the example
#         match = re.search(direct_pattern, url)
#         if match:
#             video_id = match.group(1)
#             return f"https://www.youtube.com/watch?v={video_id}"
            
#         # Then try the direct youtube.com/watch?v= pattern
#         match = re.search(youtube_pattern, url)
#         if match:
#             video_id = match.group(1)
#             return f"https://www.youtube.com/watch?v={video_id}"
            
#         # Try the fallback pattern for other YouTube URL formats
#         match = re.search(youtube_fallback_pattern, url)
#         if match:
#             video_id = match.group(1)
#             return f"https://www.youtube.com/watch?v={video_id}"
        
#         # If we couldn't extract the ID with regex, try the old method
#         video_id = None
        
#         # Handle youtu.be format
#         if 'youtu.be' in url.lower():
#             # Extract ID from path component
#             path = url.split('/')[-1]
#             if '?' in path:
#                 video_id = path.split('?')[0]
#             else:
#                 video_id = path
        
#         # Handle youtube.com format
#         elif 'youtube.com' in url.lower() or 'www.youtube.com' in url.lower():
#             if '?' in url:
#                 # Extract v parameter
#                 params = url.split('?')[1].split('&')
#                 for param in params:
#                     if param.startswith('v='):
#                         video_id = param.split('=')[1]
#                         break
                        
#             # Direct extraction for the specific URL format
#             if not video_id and 'watch?v=' in url:
#                 try:
#                     video_id = url.split('watch?v=')[1]
#                     if '&' in video_id:
#                         video_id = video_id.split('&')[0]
#                 except:
#                     pass
        
#         # If we found a video ID, construct a clean URL
#         if video_id:
#             return f"https://www.youtube.com/watch?v={video_id}"
        
#         # If we couldn't extract the ID, return the original URL
#         return url
    
# def validate_youtube_url(self, url: str) -> Tuple[bool, str]:
#     """
#     Validate if the provided URL is a valid YouTube URL
#     """
#     if not url:
#         return False, "URL cannot be empty"
    
#     # Extract video ID using regex
#     import re
#     video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
#     video_id_match = re.search(video_id_pattern, url)
    
#     if not video_id_match:
#         return False, "Could not extract video ID from URL"
        
#     video_id = video_id_match.group(1)
#     cleaned_url = f"https://www.youtube.com/watch?v={video_id}"
    
#     try:
#         yt = YouTube(cleaned_url)
#         # Force a connection to verify the video exists
#         yt.check_availability()
#         return True, f"Valid YouTube URL: {yt.title}"
#     except Exception as e:
#         error_msg = str(e)
#         if "HTTP Error 400" in error_msg:
#             return False, "Invalid YouTube URL: Video not found"
#         elif "Video unavailable" in error_msg:
#             return False, "YouTube video is unavailable or private"
#         else:
#             return False, f"Invalid YouTube URL: {error_msg}"


# def get_youtube_transcript(video_url: str) -> str:
#     """
#     Legacy function for backward compatibility
    
#     Args:
#         video_url (str): YouTube video URL
        
#     Returns:
#         str: Transcript text or error message
#     """
#     transcriber = YouTubeTranscriber()
#     success, message, transcript = transcriber.generate_transcript(video_url)
    
#     if success:
#         return transcript
#     else:
#         return f"An error occurred: {message}"


# # Example usage and testing
# if __name__ == "__main__":
#     # Test the transcriber
#     transcriber = YouTubeTranscriber()
    
#     # Test URL validation
#     test_url = "https://www.youtube.com/watch?v=N-N2psoS8pQ"
    
#     print("Testing YouTube Transcriber...")
#     print(f"URL: {test_url}")
    
#     # Validate URL
#     valid, msg = transcriber.validate_youtube_url(test_url)
#     print(f"URL Validation: {msg}")
    
#     if valid:
#         # Get video info
#         success, message, info = transcriber.get_video_info(test_url)
#         if success:
#             print(f"Video Info: {info}")
            
#             # Generate transcript (uncomment to test)
#             # success, message, transcript = transcriber.generate_transcript(test_url)
#             # if success:
#             #     print(f"Transcript ({len(transcript)} chars): {transcript[:200]}...")
#             # else:
#             #     print(f"Transcription failed: {message}")
