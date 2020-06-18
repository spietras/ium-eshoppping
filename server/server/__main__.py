import pandas as pd
from flask import Flask, jsonify, request, abort, render_template

from server import loaders

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/users', methods=['GET'])
def users():
    return jsonify({
        "users": users_df.to_dict(orient="records")
    })


@app.route('/categories', methods=['GET'])
def categories():
    return jsonify({
        'categories': categories_df.to_dict(orient="records")
    })


@app.route('/products', methods=['GET'])
def products():
    category = request.args.get("category")
    if not category:
        abort(400, "Parameter \"category\" not passed")
    return jsonify({
        'products': products_df[products_df["category"] == category].to_dict(orient="records")
    })


@app.route('/predict', methods=['GET'])
def predict():
    user_id = request.args.get("user")
    product_id = request.args.get("product")
    if not user_id:
        abort(400, "Parameter \"user\" not passed")
    if not product_id:
        abort(400, "Parameter \"product\" not passed")
    return jsonify({
        'prediction': 0.5
    })


def load_dataset(base_path, file):
    if base_path[-1] != '/':
        base_path += '/'

    return pd.read_json(base_path + file, lines=True)


if __name__ == '__main__':
    print("Loading server. It may take a while...")
    data_base_path = "data/"

    try:
        users_df = loaders.get_api_users(data_base_path)
        categories_df = loaders.get_api_categories(data_base_path)
        products_df = loaders.get_api_products(data_base_path)
        aggregated_df = loaders.get_aggregated(data_base_path)
    except IOError as e:
        print("Can't load server. Error occurred: ", e)
        exit(1)

    app.run(port=8080)