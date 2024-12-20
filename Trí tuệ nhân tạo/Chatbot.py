import nltk
from chatterbot_py import ChatBot
from chatterbot_py.trainers import ListTrainer
import spacy
# Tải tài nguyên NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Tạo chatbot
chatbot = ChatBot('Demo')

# Huấn luyện chatbot với dữ liệu tùy chỉnh
trainer = ListTrainer(chatbot)

# Đọc dữ liệu huấn luyện từ tệp
training_data = []
with open('tranining_data.txt','r',encoding='utf-8') as file:
    for line in file:
        # Kiểm tra xem dòng có phải là rỗng không
        if line.strip():
            # Thêm từng dòng vào tập training_data
            training_data.append(line.strip())
trainer.train(training_data)