from fastapi import FastAPI

import joblib
import pandas as pd

PATH_TO_LOCAL_MODEL = 'api/model.joblib'

app = FastAPI()

# define a root `/` endpoint

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(answers):
    df_test = X_pred_transform(answers)
    print(df_test.shape)
    pipeline = joblib.load(PATH_TO_LOCAL_MODEL)
    if "best_estimator_" in dir(pipeline):
        y_pred = pipeline.best_estimator_.predict(df_test)
    else:
        y_pred = pipeline.predict(df_test)
    return {"prediction": str(y_pred[0])}

def X_pred_transform(answers):
    X_pred = pd.DataFrame({'posts': [answers]})
    return X_pred
