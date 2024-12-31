import os

import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from models import db, Iris
from sklearn.datasets import load_iris

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not os.path.exists('instance/data.db'): # Initialize database with Iris dataset
        load_iris_data()

    db.init_app(app)
    return app


def load_iris_data():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        iris_dataset = load_iris()
        for feature_values, target in zip(iris_dataset['data'], iris_dataset['target']):
            iris = Iris(
                sepal_length=feature_values[0],
                sepal_width=feature_values[1],
                petal_length=feature_values[2],
                petal_width=feature_values[3],
                category=int(target) # otherwise it will be saved as hex
            )
            db.session.add(iris)
        db.session.commit()



app = create_app()
classifier = None
scaler = None

def create_iris_classifier_and_scaler():
    classifier = KNeighborsClassifier(n_neighbors=3)
    irises = Iris.query.all()
    dataset = np.array([(iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width) for iris in irises])
    categories = np.array([iris.category for iris in irises])
    scaler = StandardScaler()
    dataset = scaler.fit_transform(dataset)
    classifier.fit(dataset, categories)
    return classifier, scaler



def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
    global classifier, scaler
    if not classifier:
        classifier, scaler = create_iris_classifier_and_scaler()
    scaled_data = scaler.transform([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = classifier.predict(scaled_data)
    return prediction[0]
@app.route('/')
def home():
    irises = Iris.query.all()
    return render_template('index.html', irises=irises)

@app.route('/add', methods=['GET', 'POST'])
def add_iris():
    if request.method == 'POST':
        try:
            sepal_length = float(request.form.get('sepal_length'))
            sepal_width = float(request.form.get('sepal_width'))
            petal_length = float(request.form.get('petal_length'))
            petal_width = float(request.form.get('petal_width'))
            category = int(request.form.get('category'))
            new_iris = Iris(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length, petal_width=petal_width, category=category)
            db.session.add(new_iris)
            db.session.commit()
            return redirect(url_for('home'))
        except ValueError:
            return render_template('error.html', message="Invalid input data"), 400
    return render_template('add.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # TODO: Tu chyba je, ze kdyz uzivatel nezadá žádné hodnoty, tak se vykreslí chyba xd (alespoň tak, jak to funguje) ale mi ziutek podpowiada, že se to děje všude
    # TODO: Walidacja jescze chyba jakas
    if request.method == 'POST':
        try:
            sepal_length = float(request.form.get('sepal_length'))
            sepal_width = float(request.form.get('sepal_width'))
            petal_length = float(request.form.get('petal_length'))
            petal_width = float(request.form.get('petal_width'))
            prediction = predict_iris(sepal_length, sepal_width, petal_length, petal_width)
            return render_template('predict_result.html', prediction=prediction)
        except ValueError:
            return render_template('error.html', message="Invalid input data"), 400
    return render_template('predict.html')

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_iris(record_id):
    data_point = Iris.query.get(record_id)
    if not data_point:
        return render_template('error.html', message="Record not found"), 404
    db.session.delete(data_point)
    db.session.commit()
    return redirect(url_for('home'))


# API
@app.route('/api/data', methods=['GET'])
def get_all_irises():
    irises = Iris.query.all()
    print(irises)
    return jsonify([iris.to_dict() for iris in irises])

@app.route('/api/data', methods=['POST'])
def add_data_point_api():
    try:
        data = request.get_json()
        sepal_length = float(data['sepal_length'])
        sepal_width = float(data['sepal_width'])
        petal_length = float(data['petal_length'])
        petal_width = float(data['petal_width'])
        category = int(data['category'])
        new_iris = Iris(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length, petal_width=petal_width, category=category)
        db.session.add(new_iris)
        db.session.commit()
        return jsonify({"id": new_iris.id}), 201
    except KeyError:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_iris_api(record_id):
    iris = Iris.query.get(record_id)
    if not iris:
        return jsonify({"error": "Record not found"}), 404
    db.session.delete(iris)
    db.session.commit()
    return jsonify({"id": record_id}), 200
@app.route('/api/predictions', methods=['GET'])
def predict_api():
    print("W metodzie predict api")
    # TODO: Walidacja jescze chyba jakas
    try:
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))
        print("Dane wczytane")
        prediction = predict_iris(sepal_length, sepal_width, petal_length, petal_width)
        return jsonify({"prediction": int(prediction)}), 200
    except KeyError:
        return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
