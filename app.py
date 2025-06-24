from flask import Flask, render_template, request
import os
from face_utils import detect_faces, recognize_face

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
STATIC_UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    # Face detection
    detected_img_path, face_count = detect_faces(img_path)

    # Face recognition
    matches = recognize_face(img_path)

    return render_template("result.html",
                           detected_img=os.path.basename(detected_img_path),
                           face_count=face_count,
                           matches=matches)

if __name__ == "__main__":
    app.run(debug=True)
