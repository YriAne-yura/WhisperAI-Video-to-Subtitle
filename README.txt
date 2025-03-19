Whisper AI Video to Subtitle Converter
====================================

A Python tool that uses OpenAI's Whisper to convert video/audio files to subtitles in various formats.

System Requirements
-----------------
- Python 3.8 or higher
- PyTorch
- OpenAI Whisper
- FFmpeg (installed and added to PATH)

Installation
-----------
1. Install Python dependencies:
   ```
   pip install torch torchvision torchaudio
   pip install openai-whisper
   ```

2. Install FFmpeg:
   - Windows (using Winget): `winget install ffmpeg`
   - Windows (using Chocolatey): `choco install ffmpeg`
   - Windows (using Scoop): `scoop install ffmpeg`
   - Or download from: https://github.com/BtbN/FFmpeg-Builds/releases

Usage
-----
1. Place your video file in the same directory as the script
2. Configure settings in config.json
3. Run: `python whisper_transcribe.py`

Configuration (config.json)
-------------------------
{
    "input_file": "video.mp4",      // Your video/audio file
    "output_format": "srt",         // Output format: "srt", "vtt", or "txt"
    "language": "vi",               // Language code (see Language Codes below)
    "model": "base",                // Model size (see Model Types below)
    "device": "auto",               // Device: "auto", "cuda", "cpu", or "mps"
    "translate": false,             // true: translate to English, false: transcribe only
    "task": "transcribe",           // "transcribe" or "translate"
    "initial_prompt": ""            // Optional context hint for better recognition
}

Language Codes
-------------
Common languages:
- "vi" : Vietnamese
- "en" : English
- "ja" : Japanese
- "ko" : Korean
- "zh" : Chinese
- "fr" : French
- "de" : German
- "auto": Auto-detect language

Model Types
----------
Available models (smaller to larger):
- "tiny"   : Fastest, least accurate (1GB RAM)
- "base"   : Fast, good accuracy (1GB RAM)
- "small"  : Balanced speed/accuracy (2GB RAM)
- "medium" : More accurate (5GB RAM)
- "large"  : Most accurate, slowest (10GB RAM)

Device Options
-------------
- "auto" : Automatically select best available device
- "cuda" : Use NVIDIA GPU (requires CUDA support)
- "cpu"  : Use CPU only (works on all systems)
- "mps"  : Use Apple M1/M2 GPU

Output Formats
-------------
1. SRT (SubRip Text) - "output_format": "srt"
   ```
   1
   00:00:01,500 --> 00:00:03,000
   Subtitle text
   ```

2. WebVTT - "output_format": "vtt"
   ```
   WEBVTT

   00:00:01.500 --> 00:00:03.000
   Subtitle text
   ```

3. Text with Timestamps - "output_format": "txt"
   ```
   [00:00:01,500 --> 00:00:03,000] Subtitle text
   ```

Examples
--------
1. Basic Vietnamese transcription:
   ```json
   {
       "input_file": "video.mp4",
       "output_format": "srt",
       "language": "vi",
       "model": "base",
       "device": "auto"
   }
   ```

2. English transcription with high accuracy:
   ```json
   {
       "input_file": "video.mp4",
       "output_format": "srt",
       "language": "en",
       "model": "medium",
       "device": "auto"
   }
   ```

3. Vietnamese to English translation:
   ```json
   {
       "input_file": "video.mp4",
       "output_format": "srt",
       "language": "vi",
       "model": "base",
       "device": "auto",
       "translate": true,
       "task": "translate"
   }
   ```

Tips
----
1. For Vietnamese content:
   - Use "base" or "medium" model for better accuracy
   - Add context with initial_prompt: "Đây là video tiếng Việt"
   - Set language explicitly to "vi"

2. For English content:
   - "base" model is usually sufficient
   - For complex audio, use "medium" model
   - Set language to "en"

3. Performance:
   - Use GPU if available (CUDA/MPS) for faster processing
   - Larger models are slower but more accurate
   - Processing time depends on video length and model size

Troubleshooting
--------------
1. FFmpeg not found:
   - Ensure FFmpeg is installed and added to PATH
   - Restart terminal/IDE after installation

2. CUDA errors:
   - Install PyTorch with CUDA support:
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

3. Memory issues:
   - Try a smaller model
   - Close other applications
   - Ensure sufficient RAM for chosen model
