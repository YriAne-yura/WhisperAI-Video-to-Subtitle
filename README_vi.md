# Công cụ chuyển đổi Video sang Phụ đề sử dụng Whisper AI

Chuyển đổi file video/audio thành phụ đề sử dụng OpenAI's Whisper AI.

[Read English guide](README.md)

## Example
Terminal - Ví dụ khi chuyển đổi video 30 giây

![image](https://github.com/user-attachments/assets/207f927e-9d91-4b51-be94-d116cd47c08b)


## Yêu cầu hệ thống
- Python 3.8 trở lên
- PyTorch
- OpenAI Whisper
- FFmpeg (đã cài đặt và thêm vào PATH)

## Cài đặt
1. Cài đặt các thư viện Python:
   ```bash
   pip install torch torchvision torchaudio
   pip install openai-whisper
   ```

2. Cài đặt FFmpeg:
   - Windows (sử dụng Winget): `winget install ffmpeg`
   - Windows (sử dụng Chocolatey): `choco install ffmpeg`
   - Windows (sử dụng Scoop): `scoop install ffmpeg`
   - Hoặc tải từ: https://github.com/BtbN/FFmpeg-Builds/releases

## Bắt đầu nhanh
1. Đặt file video của bạn vào thư mục dự án
2. Tạo file `config.json` với cấu hình phù hợp
3. Chạy: `python whisper_transcribe.py`

## Cấu hình (config.json)

### Nhận dạng tiếng Việt
```json
{
    "input_file": "video.mp4",
    "output_format": "srt",
    "language": "vi",
    "model": "base",
    "device": "auto",
    "translate": false,
    "task": "transcribe",
    "initial_prompt": "Đây là video tiếng Việt",
    "subtitle_options": {
        "max_chars": 80
    }
}
```

### Nhận dạng tiếng Anh
```json
{
    "input_file": "video.mp4",
    "output_format": "srt",
    "language": "en",
    "model": "base",
    "device": "auto",
    "translate": false,
    "task": "transcribe",
    "initial_prompt": "This is an English video",
    "subtitle_options": {
        "max_chars": 80
    }
}
```

### Dịch từ tiếng Việt sang tiếng Anh
```json
{
    "input_file": "video.mp4",
    "output_format": "srt",
    "language": "vi",
    "model": "base",
    "device": "auto",
    "translate": true,
    "task": "translate",
    "subtitle_options": {
        "max_chars": 80
    }
}
```

## Tùy chọn cấu hình

### Các loại Model
- `tiny`: Nhanh nhất, độ chính xác thấp nhất (1GB RAM)
- `base`: Nhanh, độ chính xác tốt (1GB RAM)
- `small`: Cân bằng tốc độ/độ chính xác (2GB RAM)
- `medium`: Chính xác hơn (5GB RAM)
- `large`: Chính xác nhất, chậm nhất (10GB RAM)

### Tùy chọn thiết bị
- `auto`: Tự động chọn thiết bị tốt nhất
- `cuda`: Sử dụng GPU NVIDIA (yêu cầu hỗ trợ CUDA)
- `cpu`: Chỉ sử dụng CPU (hoạt động trên mọi hệ thống)
- `mps`: Sử dụng GPU Apple M1/M2

### Định dạng đầu ra
1. SRT (SubRip Text) - `"output_format": "srt"`
   ```
   1
   00:00:01,500 --> 00:00:03,000
   Nội dung phụ đề
   ```

2. WebVTT - `"output_format": "vtt"`
   ```
   WEBVTT

   00:00:01.500 --> 00:00:03.000
   Nội dung phụ đề
   ```

3. Text với thời gian - `"output_format": "txt"`
   ```
   [00:00:01,500 --> 00:00:03,000] Nội dung phụ đề
   ```

## Thực hành tốt nhất

### Cho nội dung tiếng Việt
1. Lựa chọn Model:
   - Sử dụng model `base` hoặc `medium` để có độ chính xác tốt hơn
   - Sử dụng model `large` cho giọng địa phương hoặc có tiếng ồn
   - Tránh sử dụng model `tiny` cho tiếng Việt

2. Cấu hình:
   - Đặt `language` thành "vi"
   - Thêm `initial_prompt` bằng tiếng Việt để có ngữ cảnh
   - Sử dụng `translate: false` cho phụ đề tiếng Việt
   - Sử dụng `translate: true` để dịch sang tiếng Anh

3. Hiệu suất:
   - Giống như nội dung tiếng Anh
   - Nên sử dụng model `medium` để xử lý giọng địa phương tốt hơn

### Cho nội dung tiếng Anh
1. Lựa chọn Model:
   - Sử dụng model `base` cho hầu hết trường hợp
   - Sử dụng model `medium` cho âm thanh phức tạp
   - Sử dụng model `large` cho công việc chuyên nghiệp

2. Cấu hình:
   - Đặt `language` thành "en"
   - Thêm `initial_prompt` phù hợp
   - Sử dụng `translate: false` và `task: "transcribe"`
   - Có thể thêm `max_line_length` trong config để kiểm soát độ dài phụ đề

3. Hiệu suất:
   - Sử dụng GPU nếu có để xử lý nhanh hơn
   - Đóng các ứng dụng không cần thiết
   - Đảm bảo chất lượng âm thanh tốt
   - Chia phụ đề dài thành nhiều dòng (tối đa 80 ký tự mỗi dòng)
   - Giữ phụ đề trên màn hình ít nhất 2-3 giây để dễ đọc

## Xử lý sự cố

### Vấn đề FFmpeg
1. Lỗi không tìm thấy:
   - Đảm bảo FFmpeg đã được cài đặt
   - Thêm FFmpeg vào PATH hệ thống
   - Khởi động lại terminal/IDE sau khi cài đặt

### Vấn đề CUDA/GPU
1. Không phát hiện CUDA:
   ```bash
   # Cài đặt PyTorch với hỗ trợ CUDA
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   
   # Cài đặt các thư viện phụ thuộc NVIDIA
   pip install nvidia-cuda-runtime-cu11 nvidia-cuda-nvrtc-cu11 nvidia-cuda-cupti-cu11 nvidia-cudnn-cu11
   pip install nvidia-cublas-cu11 nvidia-cufft-cu11 nvidia-curand-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11
   ```

2. Yêu cầu bổ sung:
   - GPU NVIDIA có hỗ trợ CUDA
   - Đã cài đặt driver NVIDIA GPU
   - CUDA Toolkit 11.8 hoặc phiên bản tương thích
   - Thư viện cuDNN (để có hiệu suất tốt hơn)

3. Lỗi bộ nhớ GPU:
   - Thử model nhỏ hơn
   - Giảm sử dụng GPU khác
   - Chuyển sang CPU nếu cần
   - Theo dõi sử dụng bộ nhớ GPU với lệnh `nvidia-smi`

### Vấn đề bộ nhớ
1. Hết bộ nhớ:
   - Đóng các ứng dụng khác
   - Thử model nhỏ hơn
   - Đảm bảo đủ RAM cho model
   - Sử dụng CPU cho file lớn

### Vấn đề thường gặp
1. Chất lượng nhận dạng kém:
   - Sử dụng model lớn hơn
   - Thêm ngữ cảnh trong `initial_prompt`
   - Đảm bảo chất lượng âm thanh tốt
   - Đặt đúng ngôn ngữ

2. Xử lý chậm:
   - Sử dụng GPU nếu có
   - Thử model nhỏ hơn
   - Chia file lớn thành nhiều phần
   - Đóng các ứng dụng khác 
