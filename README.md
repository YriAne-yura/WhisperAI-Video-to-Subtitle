# Video to Subtitle Converter using Whisper AI

Convert video/audio files to subtitles using OpenAI's Whisper AI.

[Đọc hướng dẫn tiếng Việt](README_vi.md)

## System Requirements
- Python 3.8 or higher
- PyTorch
- OpenAI Whisper
- FFmpeg (installed and added to PATH)

## Installation
1. Install Python libraries:
   ```bash
   pip install torch torchvision torchaudio
   pip install openai-whisper
   ```

2. Install FFmpeg:
   - Windows (using Winget): `winget install ffmpeg`
   - Windows (using Chocolatey): `choco install ffmpeg`
   - Windows (using Scoop): `scoop install ffmpeg`
   - Or download from: https://github.com/BtbN/FFmpeg-Builds/releases

## Quick Start
1. Place your video file in the project directory
2. Create `config.json` with appropriate settings
3. Run: `python whisper_transcribe.py`

## Configuration (config.json)

### Vietnamese Recognition
```json
{
    "input_file": "video.mp4",
    "output_format": "srt",
    "language": "vi",
    "model": "base",
    "device": "auto",
    "translate": false,
    "task": "transcribe",
    "initial_prompt": "This is a Vietnamese video"
}
```

### English Recognition
```json
{
    "input_file": "video.mp4",
    "output_format": "srt",
    "language": "en",
    "model": "base",
    "device": "auto",
    "translate": false,
    "task": "transcribe",
    "initial_prompt": "This is an English video"
}
```

### Vietnamese to English Translation
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

## Configuration Options

### Model Types
- `tiny`: Fastest, least accurate (1GB RAM)
- `base`: Fast, good accuracy (1GB RAM)
- `small`: Balanced speed/accuracy (2GB RAM)
- `medium`: More accurate (5GB RAM)
- `large`: Most accurate, slowest (10GB RAM)

### Device Options
- `auto`: Automatically select best device
- `cuda`: Use NVIDIA GPU (requires CUDA support)
- `cpu`: Use CPU only (works on all systems)
- `mps`: Use Apple M1/M2 GPU

### Output Formats
1. SRT (SubRip Text) - `"output_format": "srt"`
   ```
   1
   00:00:01,500 --> 00:00:03,000
   Subtitle content
   ```

2. WebVTT - `"output_format": "vtt"`
   ```
   WEBVTT

   00:00:01.500 --> 00:00:03.000
   Subtitle content
   ```

3. Text with timestamps - `"output_format": "txt"`
   ```
   [00:00:01,500 --> 00:00:03,000] Subtitle content
   ```

## Best Practices

### For Vietnamese Content
1. Model Selection:
   - Use `base` or `medium` model for better accuracy
   - Use `large` model for regional accents or noisy audio
   - Avoid using `tiny` model for Vietnamese

2. Configuration:
   - Set `language` to "vi"
   - Add Vietnamese `initial_prompt` for context
   - Use `translate: false` for Vietnamese subtitles
   - Use `translate: true` to translate to English

3. Performance:
   - Same as English content
   - Consider using `medium` model for better dialect handling

### For English Content
1. Model Selection:
   - Use `base` model for most cases
   - Use `medium` model for complex audio
   - Use `large` model for professional work

2. Configuration:
   - Set `language` to "en"
   - Add appropriate `initial_prompt`
   - Use `translate: false` and `task: "transcribe"`

3. Performance:
   - Use GPU if available for faster processing
   - Close unnecessary applications
   - Ensure good audio quality

## Troubleshooting

### FFmpeg Issues
1. Not Found Error:
   - Ensure FFmpeg is installed
   - Add FFmpeg to system PATH
   - Restart terminal/IDE after installation

### CUDA/GPU Issues
1. CUDA Not Detected:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
2. GPU Memory Error:
   - Try smaller model
   - Reduce other GPU usage
   - Switch to CPU if needed

### Memory Issues
1. Out of Memory:
   - Close other applications
   - Try smaller model
   - Ensure enough RAM for model
   - Use CPU for large files

### Common Issues
1. Poor Recognition Quality:
   - Use larger model
   - Add context in `initial_prompt`
   - Ensure good audio quality
   - Set correct language

2. Slow Processing:
   - Use GPU if available
   - Try smaller model
   - Split large files
   - Close other applications 