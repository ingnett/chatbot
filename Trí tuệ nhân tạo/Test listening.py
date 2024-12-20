from pydub import AudioSegment
import speech_recognition as sr
import os
def convert_audio_to_text(file_name):
    # Khởi tạo trình nhận diện giọng nói
    recognizer = sr.Recognizer()

    # Chuyển đổi file MP3 sang WAV nếu cần thiết
    if file_name.endswith('.m4a'):
        audio = AudioSegment.from_file(file_name, format='m4a')
        wav_file = file_name.replace('.m4a', '.wav')
        audio.export(wav_file, format='wav')
    # Mở file âm thanh đã chuyển đổi
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            # Chuyển đổi âm thanh thành văn bản
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Không thể nhận diện giọng nói từ file âm thanh này."
        except sr.RequestError as e:
            return f"Yêu cầu tới dịch vụ nhận diện giọng nói gặp lỗi: {e}"


# Chuyển đổi file và in kết quả
file_name = 'Recording.m4a'  # Thay thế bằng tên file của bạn
print(convert_audio_to_text(file_name))
