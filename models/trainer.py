import models.logistic_regression.LogisticRegression as lg
import models.lstm.long_short_term_memory as lstm
import models.convd.convd as convd
import pandas as pd

models = {
    'lg': lg.LogisticRegressionModel(),
    'lstm': lstm.LSTMModel(),
    'conv1d': convd.Conv1DModel(),
}

def train(path):
    dataset = pd.read_csv(path)

    for model in models.values():
        print(model)
        model.train(dataset)

def get_models():
    return models