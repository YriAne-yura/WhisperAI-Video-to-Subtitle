import whisper
import json
import os
import torch
import subprocess

# Cấu hình đường dẫn cố định cho model
MODEL_DIR = "models"
MODEL_PATHS = {
    "tiny": os.path.join(MODEL_DIR, "tiny.pt"),
    "base": os.path.join(MODEL_DIR, "base.pt"),
    "small": os.path.join(MODEL_DIR, "small.pt"),
    "medium": os.path.join(MODEL_DIR, "medium.pt"),
    "large": os.path.join(MODEL_DIR, "large.pt")
}

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
    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], 1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")
elif output_format == "vtt":
    output_file = "output.vtt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"]).replace(",", ".")
            end_time = format_timestamp(segment["end"]).replace(",", ".")
            text = segment["text"].strip()
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")
else:
    output_file = "output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"[{start_time} --> {end_time}] {text}\n")

print(f"✅ Content has been saved to '{output_file}' 🎉")
