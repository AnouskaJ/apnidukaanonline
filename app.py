# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.applications import DenseNet121
from keras.preprocessing import image
from keras.applications.densenet import preprocess_input
from sklearn.metrics.pairwise import linear_kernel
import pathlib

app = Flask(__name__)
CORS(app) 

model = keras.models.load_model('keras_model.h5')
df_embeddings = pd.read_csv('embeddings_data.csv')
df = pd.read_csv('fashion-dataset/styles.csv', nrows=6000)


# Compute cosine similarity between embeddings
cosine_sim = linear_kernel(df_embeddings, df_embeddings)

# Function to recommend products based on an image
def recommend_products(image_path):
    # Preprocess the input image to match the model's requirements
    img = image.load_img(image_path, target_size=(200, 200))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # Get the image embedding from your pre-trained model
    image_embedding = model.predict(img).reshape(-1)

    # Compute similarity scores between the input image and all products
    sim_scores = cosine_sim.dot(image_embedding)

    # Sort products by similarity scores and get the top 5 most similar
    top_indices = np.argsort(sim_scores)[::-1][:5]

    # Return the recommended products
    recommendations = df.iloc[top_indices].to_dict(orient='records')
    return recommendations

# API endpoint to receive an image and get product recommendations
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        # Get the image file from the request
        image_file = request.files['image']

        # Save the image temporarily
        image_path = 'temp_image.jpg'
        image_file.save(image_path)

        # Call the recommendation function
        recommendations = recommend_products(image_path)

        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
