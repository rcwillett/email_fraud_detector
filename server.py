# Import Tensor Flow and keras
import tensorflow as tf
from tensorflow import keras

# Import Tensor Flow Hub and Tensor Flow Text (Required libraries for the pre-trained BERT Model)
import tensorflow_hub as hub
import tensorflow_text

# Import fast api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import uvicorn
import uvicorn

# Load trained BERT model for identification
# Load the saved model into Keras
bert_model = keras.models.load_model(
    './models/bert_model_20_relu_sig.h5',
    custom_objects={'KerasLayer':hub.KerasLayer},
    compile=False,
)

# Add the compilation parameters for the model (Note this must be done since compile has been set to False)
bert_model.compile(
    # Optimizer
    optimizer=keras.optimizers.Adam(),
    # Loss function to minimize
    loss=keras.losses.BinaryCrossentropy(),
    # Metric used to evaluate model
    metrics=[keras.metrics.BinaryAccuracy(), keras.metrics.Recall()]
)

# Initialize fast api app
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FraudBody(BaseModel):
    content: str

# Set up route for predicting results
@app.post('/identifyFraudEmail/')
def predict_sentiment(input_json: FraudBody):
    # Parse JSON from post request

    # Verify input json has correct values and throw exception if not
    if type(input_json.content) != str:
        raise Exception('The request must contain text content')

    # Put input into format model can digest
    model_input = [input_json.content]
    # Get the model's estimate for whether the email is fraud or not
    chance_fraud = bert_model.predict(model_input)[0][0]
    # Threshold the result to estimate if email is fraud or not
    is_fraud = chance_fraud >= 0.5

    return {"chance_fraud": f'{chance_fraud}', "is_fraud": f'{is_fraud}'}

@app.get('/')
def health_check():
    return { "success": True }

# Run the Flask app if this is the main file
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)