from flask import Flask, render_template, request
import os
import fitz

from google import genai

client = genai.Client(api_key="AIzaSyDEPx29PZsLtITSQpPQcskvQXKzffz8KRA")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def home():
    extracted_text = None
    summary = None

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()

            extracted_text = text.strip() if text else "No text could be extracted from the PDF."

            prompt = f"summarize this passage in 2 paragraphs:\n\n{text}"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            summary = response.text
        else:
            extracted_text = "Please upload a valid PDF file."

    return render_template('home.html', summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
