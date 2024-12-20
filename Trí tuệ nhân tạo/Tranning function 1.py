import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Huấn luyện mô hình hồi quy logistic
model = LogisticRegression()
model.fit(X_train, y_train)

# Sử dụng mô hình để phân loại văn bản mới
new_texts = '     - Đầu tiên, phải xác định mục tiêu: bạn muốn học tiếng anh để làm gì? (làm việc, học tập, giao tiếp cơ bản,…)\n- Đánh giá trình độ tiếng anh hiện tại: mất gốc, biết cơ bản,…\n- Lựa chọn tài liệu học tập phù hợp: tự học theo sách giáo khoa, ứng dụng, website hoặc trung tâm tiếng anh,….'
X_new = vectorizer.transform([new_texts])
pa = model.predict(X_new)

print(pa)