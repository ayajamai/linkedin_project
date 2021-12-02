from sklearn.compose import make_column_transformer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from termcolor import colored
from xgboost import XGBClassifier

from linkedin_project.encoders import links_counts, SentimentAnalysis, TextCleaner
from linkedin_project.data import get_data_from_gcp
from linkedin_project.gcp import storage_upload

import pandas as pd
import joblib

class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        function_transform = make_pipeline(FunctionTransformer(links_counts),
                                           StandardScaler())

        transformer = make_column_transformer(
            (SentimentAnalysis('posts'), ['posts']),
            (function_transform, ['posts']),
            (TextCleaner('posts'), ['posts']))

        self.pipeline = make_pipeline(transformer,
                                      XGBClassifier(max_depth=3,
                                                    n_estimators=300,
                                                    learning_rate=0.05))

    def set_random_search(self):
        """defines the pipeline as a class attribute"""

        params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
        }

        xgb = XGBClassifier(gpu_id=0,
                    tree_method='gpu_hist',
                    max_depth=5,
                    n_estimators=50,
                    learning_rate=0.1,
                    objective='binary:logistic',
                    silent=True,
                    nthread=1)

        skf = StratifiedKFold(n_splits=5, shuffle = True, random_state = 42)


        function_transform = make_pipeline(FunctionTransformer(links_counts),
                                           StandardScaler())

        transformer = make_column_transformer(
            (SentimentAnalysis('posts'), ['posts']),
            (function_transform, ['posts']), (TextCleaner('posts'), ['posts']))

        random_search = make_pipeline(
            transformer,
            RandomizedSearchCV(xgb,
                               param_distributions=params,
                               n_iter=5,
                               scoring='roc_auc',
                               n_jobs=4,
                               cv=skf.split(X_train, y_train),
                               verbose=3,
                               random_state=1001))

        search = random_search.fit(self.X, self.y)
        return search.best_params_

    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the accuracy"""
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_pred, y_test) * 100
        return accuracy

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))


if __name__ == "__main__":
    # Get and clean data
    N = 100
    df = get_data_from_gcp(nrows=N)
    df = clean_data(df)
    y = df["type"]
    X = df.drop("type", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.run()
    acc = trainer.evaluate(X_test, y_test)
    print(f"Accuracy: {acc}")
    trainer.save_model_locally()
    storage_upload()
