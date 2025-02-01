import os
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
from fuzzywuzzy import fuzz, process
from pymongo import MongoClient

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["faq_assistant_db"]
logs_collection = db["logs"]

# Load FAQs from JSON file
def load_faqs():
    try:
        with open('faq_assistant/faq_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save FAQs to JSON file
def save_faqs(faq_data):
    try:
        with open("faq_assistant/faq_data.json", "w") as file:
            json.dump(faq_data, file, indent=4)
    except Exception as e:
        print(f"Error saving FAQs: {e}")

# Search for the best-matching FAQ
def search_faq(question, faqs):
    faq_questions = [faq['question'] for faq in faqs]
    best_match = process.extractOne(question, faq_questions, scorer=fuzz.ratio)
    
    if best_match and best_match[1] > 80:
        best_faq = next(faq for faq in faqs if faq['question'] == best_match[0])
        return best_faq['answer']
    return None

# Generate response using Gemini API or fallback to FAQs
def get_gemini_response(question):
    faqs = load_faqs()
    response = search_faq(question, faqs)
    
    if response:
        return response
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        return response.text if response else "Sorry, I couldn't find an answer."
    except Exception as e:
        return f"Error: {str(e)}"

# Homepage route
@app.route("/")
def index():
    return render_template("index.html")

# Handle user queries
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    
    if not question:
        return jsonify({"answer": "Please ask a valid question."})
    
    answer = get_gemini_response(question)
    return jsonify({"answer": answer})

# Admin route to update FAQs
@app.route("/admin/update_faq", methods=["POST"])
def admin_update_faq():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    
    if not question or not answer:
        return jsonify({"message": "Question and answer are required."}), 400
    
    faq_data = load_faqs()
    faq_data.append({"question": question, "answer": answer})
    save_faqs(faq_data)
    
    logs_collection.insert_one({
        "action": "FAQ updated",
        "question": question,
        "answer": answer
    })
    
    return jsonify({"message": "FAQ added/updated successfully!"})

# Admin panel route
@app.route("/admin")
def admin():
    return render_template("admin.html")

# Retrieve logs from MongoDB
def get_logs_from_db():
    return list(logs_collection.find({}, {'_id': 0}))

# Admin route to view logs
@app.route("/admin/view_logs", methods=["GET"])
def view_logs():
    logs = get_logs_from_db()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
