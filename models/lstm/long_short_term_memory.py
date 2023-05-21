from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from models.base_model.BaseModel import BaseModel
from keras.utils import pad_sequences
import pickle
import os
from pandas import DataFrame

class LSTMModel(BaseModel):
    MODEL_BIN = "lstm.sav"
    MODEL_NAME = "lstm"
    TOKENIZER_BIN = "tokenizer.sav"
    model = None
    tokenizer = None

    def __init__(self):
        if os.path.exists(self.MODEL_BIN) and os.path.exists(self.TOKENIZER_BIN):
            print("Model exisists, loading from bin..")
            self.model = pickle.load(open(self.MODEL_BIN, 'rb'))
            self.tokenizer = pickle.load(open(self.TOKENIZER_BIN, 'rb'))
        else:
            print("Model bin not found, need to train")
            self.tokenizer = Tokenizer(num_words=10000)
            self.model = Sequential()

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
    
    def train(self, dataset: DataFrame):
        dataset['label'] = dataset['label'].replace('neutral', 0)
        dataset['label'] = dataset['label'].replace('attack', 1)
        X_train, X_test, y_train, y_test = train_test_split(dataset['text'], dataset['label'], test_size=0.11)

        # Преобразование текста в векторы признаков
        self.tokenizer.fit_on_texts(X_train)
        X_train = self.tokenizer.texts_to_sequences(X_train)
        X_test = self.tokenizer.texts_to_sequences(X_test)

        # Обучение модели логистической регрессии
        # добавление заполнения в конце последовательности для выравнивания длин
        maxlen = 100
        X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
        X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

        # создание модели LSTM
        self.model = Sequential()
        self.model.add(Embedding(input_dim=10000, output_dim=64, input_length=maxlen))
        self.model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        self.model.add(Dense(1, activation='sigmoid'))

        # компиляция модели
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # обучение модели LSTM
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=32)

        print(f"Trained {self.MODEL_NAME}:\n Saving to {self.MODEL_BIN}...")

        self.save_model()
        
        print(f"Saved to {self.MODEL_BIN}. Tesing...")
        _, accuracy = self.model.evaluate(X_test, y_test)
        print(f"Testing accuracy for {self.MODEL_NAME}:", accuracy)

    def process(self, text):
        text_seq = self.tokenizer.texts_to_sequences([text])
        text_seq = pad_sequences(text_seq, padding='post', maxlen=100)

        # получение предсказания модели
        prediction = self.model.predict(text_seq)[0][0]

        if prediction > 0.5:
            return 'attack'
        else:
            return 'neutral'
    
    def save_model(self):
        pickle.dump(self.model, open(self.MODEL_BIN, 'wb'))
        pickle.dump(self.tokenizer, open(self.TOKENIZER_BIN, 'wb'))