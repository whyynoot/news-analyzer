from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from models.base_model.BaseModel import BaseModel
import pickle
import os

class LogisticRegressionModel(BaseModel):
    MODEL_BIN = "logistic_regression.sav"
    MODEL_NAME = "logistic_regression"
    VECTORIEZER_BIN = "countvectorizer.sav"
    model = None
    vectorizer = None

    def __init__(self):
        if os.path.exists(self.MODEL_BIN) and os.path.exists(self.VECTORIEZER_BIN):
            print("Model exisists, loading from bin..")
            self.model = pickle.load(open(self.MODEL_BIN, 'rb'))
            self.vectorizer = pickle.load(open(self.VECTORIEZER_BIN, 'rb'))
        else:
            print("Model bin not found, need to train")
            self.vectorizer = CountVectorizer()
            self.model = LogisticRegression()

        # if train go retrating 

    def retrain(self, text, label):
        # Unable to retrain because of last dataset unkown. just saving
        with open("suggested_dataset.csv", 'a', encoding='utf-8') as file:
            file.write(f'"{text}",{label} \n')
        
        return f'Спасибо за ваш вклад в обучении модели!\n Сохранен текст "{text[:30]}..." c параметром {label}'
        # text_vec = self.vectorizer.transform([text])

        # x_train_vec = self.vectorizer.fit_transform(text_vec)
        # self.model.fit(x_train_vec, label)

        # self.save_model()
    
    def train(self, dataset):
        X_train, X_test, y_train, y_test = train_test_split(dataset['text'], dataset['label'], test_size=0.1)

        # Преобразование текста в векторы признаков
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Обучение модели логистической регрессии
        self.model.fit(X_train_vec, y_train)

        print(f"Trained {self.MODEL_NAME}:\n Saving to {self.MODEL_BIN}...")

        self.save_model()
        
        print(f"Saved to {self.MODEL_BIN}. Tesing...")
        accuracy = self.model.score(X_test_vec, y_test)
        print(f"Testing accuracy for {self.MODEL_NAME}:", accuracy)

    def process(self, text):
        text_vec = self.vectorizer.transform([text])
        result = self.model.predict(text_vec)

        return result[0]
    
    def save_model(self):
        pickle.dump(self.model, open(self.MODEL_BIN, 'wb'))
        pickle.dump(self.vectorizer, open(self.VECTORIEZER_BIN, 'wb'))