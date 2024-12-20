
from flask import Flask, render_template, request, jsonify
from chatterbot_py import ChatBot
import speech_recognition as sr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from pydub import AudioSegment


app = Flask(__name__)

# Tạo chatbot
chatbot = ChatBot('Demo')

@app.route("/")
def home():
    return render_template("haha.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json['message'].strip()
    try:
        if user_input =='':
            return jsonify(response = str("Bạn không nhập gì cả vui lòng nhập lại"))
        else:
            if classify(user_input)=='question':
                response = chatbot.get_response(user_input)
                clean_response = response.text.replace("\\n", "\n").replace("\n","<br>")
            else:
                return jsonify(response =str("Đây không là dạng câu hỏi"))
    except KeyError as e:
        clean_response = "Đã xảy ra lỗi"
    return jsonify(response=str(clean_response))

@app.route("/speech_recognize",methods = ["GET"])
def speech_recognize():
    ear = sr.Recognizer()
    with sr.Microphone() as mic:
        audio = ear.listen(mic)
        text = ear.recognize_google(audio,language = 'vi-VN')
        return jsonify({'text':text})

@app.route("/convert_file_mp3",methods = ["POST"])
def convert_file_mp3():
    file_name = request.json['file']
    ear = sr.Recognizer()
    if file_name.endswith('.m4a'):
        audio = AudioSegment.from_file(file_name, format='m4a')
        wav_file = file_name.replace('.m4a', '.wav')
        audio.export(wav_file, format='wav')
    if file_name.endswith('.mp3'):
        audio = AudioSegment.from_file(file_name, format='mp3')
        wav_file = file_name.replace('.mp3', '.wav')
        audio.export(wav_file, format='wav')
    with sr.AudioFile(wav_file) as source:
        audio_data = ear.record(source)
        try:
            # Chuyển đổi âm thanh thành văn bản
            text = ear.recognize_google(audio_data,language ="vi-VN")
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'text':"Loi ko nhan dc giong noi"})
def classify(text):
# Đọc tệp CSV
    df = pd.read_csv('training_ques_ans.csv', encoding='utf-8')

    # Chuẩn bị dữ liệu cho câu hỏi (ques) và câu trả lời (ans)
    ques = df['question']
    ans = df['answer']

    # Tạo nhãn cho câu hỏi và câu trả lời
    # Tập này ở dạng list
    ques_label = ['question'] * len(ques)
    ans_label = ['answer'] * len(ans)

    # Kết hợp câu hỏi và câu trả lời
    # Kết hợp câu hỏi va câu trả lời ở dạng các DataFrame
    texts = pd.concat([ques, ans])
    # Kết hợp nhãn của câu hỏi và câu trả lời thành dạng DataFrame 1 chiều
    labels = pd.concat([pd.Series(ques_label), pd.Series(ans_label)])


    # Chuyển đổi văn bản thành vector
    # Dữ liệu dạng text nên cần chuyển đổi thành dạng số
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    # Y là kết quả dự đoán sau cùng nên ko cần phải chuyển đổi
    y = labels

    # Chia tập dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # Huấn luyện mô hình hồi quy logistic
    model = LogisticRegression()
    model.fit(X_train, y_train)

    X_new = vectorizer.transform([text])
    return model.predict(X_new)

if __name__ == "__main__":
    app.run(debug=True)


