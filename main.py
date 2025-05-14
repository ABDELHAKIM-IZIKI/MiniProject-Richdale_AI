from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from pathlib import Path
import base64

app = FastAPI()


# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Load model
model = tf.keras.models.load_model('model/mobilenet_health_leaf_model.h5')

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return Path("frontend/index.html").read_text()


# Serve predict
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

       
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes))
        img_format = img.format.lower() if img.format else 'jpeg'
        img_resized = img.resize((224, 224))  # MobileNet size
        img_array = np.array(img_resized) / 255.0 
        img_array = np.expand_dims(img_array, axis=0) 
        

        prediction = model.predict(img_array)
        confidence = float(prediction[0][0])
        
        # Convert original image to base64 for returning
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Return result with image
        if confidence > 0.5:
            return JSONResponse({
                "result": "Healthy leaf",
                "confidence": f"{confidence*100:.1f} %",
                "image": f"data:image/{img_format};base64,{img_base64}",
         
            })
        else:
            return JSONResponse({
                "result": "Diseased leaf", 
                "confidence": f"{(1-confidence)*100:.1f} %",
                "image": f"data:image/{img_format};base64,{img_base64}",
              
            })
        

@app.get("/debug")
async def debug():
    return {
        "index_exists": Path("frontend/index.html").exists(),
        "css_exists": Path("frontend/static/style.css").exists(),
        "js_exists": Path("frontend/static/script.js").exists()
    }
            
   