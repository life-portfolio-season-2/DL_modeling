from flask import Flask, render_template, request
import joblib
import numpy as np
import mysql.connector
import os

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": "irisDB"
}

db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# 저장된 XGBoost 모델 불러오기
model_filename = './app/model/iris_xgboost_model.joblib'
loaded_model = joblib.load(model_filename)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # HTML 폼에서 입력한 값 가져오기
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    # 모델에 입력값 전달하여 예측 수행
    input_data = np.array(
        [[sepal_length, sepal_width, petal_length, petal_width]])
    predicted_class = loaded_model.predict(input_data)[0]

    class_names = ["Setosa", "Versicolor", "Virginica"]

    # 예측 결과를 숫자로 변환
    prediction_result = class_names[predicted_class]

    # MySQL에 예측 결과 저장
    sql_query = "INSERT INTO iris_data (sepal_length, sepal_width, petal_length, petal_width, class) VALUES (%s, %s, %s, %s, %s)"
    values = (sepal_length, sepal_width, petal_length,
              petal_width, int(predicted_class))

    db_cursor.execute(sql_query, values)
    db_connection.commit()

    return render_template('index.html', prediction_result=prediction_result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
