from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import mindspore as ms
from mindspore import Tensor
from mindspore.train.serialization import load_checkpoint, load_param_into_net
import json
import base64
from PIL import Image
import numpy as np
import io
import mobilenet_ms as mn


app = FastAPI()

# Load the MindSpore model
param_dict = load_checkpoint(r"C:\Users\gobotinjr1\CPE178P_E01_2T2526\LocalRepo\Lab04\ckpt\checkpoint_net_1-1_1875.ckpt")
  # check if file exists
num_class = 5
net = mn.mobilenet_v2(num_class)

# Load model parameters
ms.load_param_into_net(net, param_dict)
model = ms.Model(net)

# Preprocessing function
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = img.transpose(2, 0, 1)
    img = img[np.newaxis, ...]
    return Tensor(img, ms.float32)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_data = preprocess_image(image_bytes)
    output = net(input_data)
    predicted_class = np.argmax(output.asnumpy())
    predicted_class = int(predicted_class)
    probs = np.exp(output) / np.sum(np.exp(output), axis=-1, keepdims=True)
    s_np = probs[0, :]
    probs_label = np.argmax(s_np)
    prob_score = probs[0, probs_label] * 100
    return {"class": predicted_class, "score": prob_score}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            class_name = {0: 'daisy', 1: 'dandelion', 2: 'roses', 3: 'sunflowers', 4: 'tulips'}
            
            # --- Prediction logic ---
            image_data = base64.b64decode(json.loads(data)["data"])
            input_data = preprocess_image(image_data)
            output = net(input_data)
            predicted_class = np.argmax(output.asnumpy())
            predicted_class_int = int(predicted_class)
            predicted_class_str = class_name[predicted_class_int]
            
            probs = np.exp(output) / np.sum(np.exp(output), axis=-1, keepdims=True)
            print(probs)  # show score in the terminal
            s_np = probs[0, :]
            probs_label = np.argmax(s_np)
            prob_score = float(probs[0, probs_label] * 100)
            print("prob score: {}".format(prob_score))
            
            await websocket.send_text(json.dumps({
                "type": "prediction",
                "class": predicted_class_str,
                "score": prob_score
            }))
    except WebSocketDisconnect:
        pass
