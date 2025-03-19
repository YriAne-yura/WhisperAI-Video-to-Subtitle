import whisper
import json
import os
import torch
import subprocess
import re

# Cấu hình đường dẫn cố định cho model
MODEL_DIR = "models"
MODEL_PATHS = {
    "tiny": os.path.join(MODEL_DIR, "tiny.pt"),
    "base": os.path.join(MODEL_DIR, "base.pt"),
    "small": os.path.join(MODEL_DIR, "small.pt"),
    "medium": os.path.join(MODEL_DIR, "medium.pt"),
    "large": os.path.join(MODEL_DIR, "large.pt")
}

def split_text_by_chars(text, max_chars):
    """Chia văn bản thành các phần có độ dài ký tự phù hợp."""
    if len(text) <= max_chars:
        return [text]
    
    # Tìm vị trí cắt phù hợp (sau dấu câu hoặc khoảng trắng)
    parts = []
    current_text = text
    
    while len(current_text) > max_chars:
        # Tìm vị trí cắt phù hợp
        cut_pos = max_chars
        for i in range(max_chars, 0, -1):
            if current_text[i] in '.,!?;: ':
                cut_pos = i + 1
                break
        
        # Nếu không tìm thấy dấu câu, cắt tại max_chars
        if cut_pos == max_chars:
            cut_pos = max_chars
        
        # Thêm phần đã cắt vào danh sách
        parts.append(current_text[:cut_pos].strip())
        current_text = current_text[cut_pos:].strip()
    
    if current_text:
        parts.append(current_text)
    
    return parts

def adjust_segment_duration(segment, min_duration, max_duration):
    """Điều chỉnh thời lượng của segment để phù hợp với giới hạn."""
    duration = segment["end"] - segment["start"]
    if duration < min_duration:
        segment["end"] = segment["start"] + min_duration
    elif duration > max_duration:
        segment["end"] = segment["start"] + max_duration
    return segment

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        print("\n⚠️ FFmpeg not found!")
        print("🔹 Please install FFmpeg:")
        print("1. Download FFmpeg from: https://github.com/BtbN/FFmpeg-Builds/releases")
        print("2. Extract the downloaded zip file")
        print("3. Add FFmpeg's bin folder to your system's PATH")
        print("4. Restart your terminal/IDE")
        print("\nOr install via package manager:")
        print("- Windows (using Chocolatey): choco install ffmpeg")
        print("- Windows (using Scoop): scoop install ffmpeg")
        print("- Windows (using Winget): winget install ffmpeg")
        return False

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def check_device():
    if device == "auto":
        if torch.cuda.is_available():
            print("🔍 Detected NVIDIA GPU, using CUDA")
            return "cuda"
        elif torch.backends.mps.is_available():
            print("🔍 Detected Apple M1/M2 GPU, using MPS")
            return "mps"
        else:
            print("🔍 No GPU detected, using CPU")
            return "cpu"
    elif device == "cuda":
        if torch.cuda.is_available():
            print("🔍 Using NVIDIA GPU as requested")
            return "cuda"
        else:
            print("⚠️ NVIDIA GPU not detected!")
            print("🔹 Please install PyTorch with CUDA support using:\n")
            print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n")
            print("Or visit: https://pytorch.org/get-started/locally/")
            exit(1)
    elif device == "mps":
        if torch.backends.mps.is_available():
            print("🔍 Using Apple M1/M2 GPU as requested")
            return "mps"
        else:
            print("⚠️ Apple M1/M2 GPU not detected!")
            return "cpu"
    else:
        print("🔍 Using CPU as requested")
        return "cpu"

# Kiểm tra FFmpeg trước khi tiếp tục
if not check_ffmpeg():
    exit(1)

# Tạo thư mục models nếu chưa tồn tại
os.makedirs(MODEL_DIR, exist_ok=True)

# Đọc cấu hình từ file config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Lấy thông tin từ config
input_file = config["input_file"]
output_format = config["output_format"]
language = config["language"]
model_name = config["model"]
device = config["device"]
translate = config.get("translate", False)
task = config.get("task", "transcribe")
initial_prompt = config.get("initial_prompt", "")

# Lấy các tùy chọn phụ đề
subtitle_options = config.get("subtitle_options", {})
max_chars = subtitle_options.get("max_chars", 80)

# Chọn thiết bị
selected_device = check_device()
print(f"✅ Using device: {selected_device}")

# Kiểm tra file đầu vào có tồn tại không
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' does not exist!")
    exit(1)

# Load mô hình Whisper
print(f"🔹 Loading Whisper model: {model_name}...")
if os.path.exists(MODEL_PATHS[model_name]):
    print(f"✅ Model already exists, loading from {MODEL_PATHS[model_name]}")
else:
    print(f"⏳ Downloading model {model_name}...")

model = whisper.load_model(model_name, device=selected_device, download_root=MODEL_DIR)

# Nhận diện giọng nói với các tùy chọn nâng cao
print(f"🎤 Transcribing audio from '{input_file}'...")
result = model.transcribe(
    input_file,
    language=language,
    task=task,
    initial_prompt=initial_prompt,
    verbose=True
)

# Lưu kết quả ra file với định dạng phù hợp
if output_format == "srt":
    output_file = "output.srt"
    subtitle_index = 1
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            # Chia văn bản thành các phần nếu cần
            if len(text) > max_chars:
                parts = split_text_by_chars(text, max_chars)
                for part in parts:
                    f.write(f"{subtitle_index}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{part}\n\n")
                    subtitle_index += 1
            else:
                f.write(f"{subtitle_index}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
                subtitle_index += 1
elif output_format == "vtt":
    output_file = "output.vtt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"]).replace(",", ".")
            end_time = format_timestamp(segment["end"]).replace(",", ".")
            text = segment["text"].strip()
            
            # Chia văn bản thành các phần nếu cần
            if len(text) > max_chars:
                parts = split_text_by_chars(text, max_chars)
                for part in parts:
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{part}\n\n")
            else:
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
else:
    output_file = "output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            # Chia văn bản thành các phần nếu cần
            if len(text) > max_chars:
                parts = split_text_by_chars(text, max_chars)
                for part in parts:
                    f.write(f"[{start_time} --> {end_time}] {part}\n")
            else:
                f.write(f"[{start_time} --> {end_time}] {text}\n")

print(f"✅ Content has been saved to '{output_file}' 🎉")
