from flask import Flask, request, jsonify, send_file, render_template
from openai import OpenAI
import os
import base64
import json

app = Flask(__name__)

client = OpenAI(
    api_key=''
)

UPLOAD_FOLDER = 'uploads'
TRANSCRIPT_FOLDER = 'transcripts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

allowed_versions = ['gpt-4o', 'gpt-4o-mini',
                    'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list_files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'files': files})


@app.route('/process', methods=['POST'])
def process_file():
    upload_option = request.form.get('upload_option', 'upload')

    if upload_option == 'upload':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_to_process = file_path
    elif upload_option == 'choose':
        selected_file = request.form.get('existing_file')
        file_to_process = os.path.join(UPLOAD_FOLDER, selected_file)
        if not os.path.isfile(file_to_process):
            return jsonify({"error": "Selected file does not exist"}), 400
    else:
        return jsonify({"error": "Invalid option selected"}), 400

    gpt_version = request.form.get('gpt_version', 'gpt-4o')
    if gpt_version not in allowed_versions:
        gpt_version = 'gpt-4o'

    # Open the local image file in binary mode
    with open(file_to_process, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Send the image to OpenAI for processing
    response = client.chat.completions.create(
        model=gpt_version,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Provide JSON file that represents extracted text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    # Process the response
    if response.choices and response.choices[0].message:
        json_data = json.loads(response.choices[0].message['content'])
        filename_without_extension = os.path.splitext(
            os.path.basename(file_to_process))[0]
        json_filename = os.path.join(
            TRANSCRIPT_FOLDER, f"{filename_without_extension}.json")

        with open(json_filename, 'w') as file:
            json.dump(json_data, file, indent=4)

        return send_file(json_filename, as_attachment=True)
    else:
        return jsonify({"error": "Failed to process the image"}), 500


if __name__ == '__main__':
    app.run(debug=True)
