import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  // Function to handle image upload and recommendations
  const handleUpload = (event) => {
    const formData = new FormData();
    const selectedImage = event.target.files[0]; // Get the selected image

    // Set the selected image in the state
    setSelectedImage(selectedImage);

    formData.append('image', selectedImage);

    axios.post('http://localhost:5000/recommend', formData)
      .then((response) => {
        // Update the recommendations state with the received recommendations
        setRecommendations(response.data.recommendations);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div>
      <h1>Upload an Image</h1>
      <input type="file" accept=".jpg, .jpeg, .png" onChange={handleUpload} />

      {/* Display the selected image */}
      {selectedImage && (
        <div>
          <h2>Selected Image</h2>
          <img
            src={URL.createObjectURL(selectedImage)}
            alt="Selected"
            style={{ maxWidth: '100%', maxHeight: '300px' }} // Adjust image size as needed
          />
        </div>
      )}
    
      {/* Display recommendations */}
      <div className="recommendations">
      {Array.isArray(recommendations) && recommendations.map((product, index) => (
          <div key={index}>
            <img src={product.image} alt={product.name} />
            <p>{product.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
