from flask import Flask, request, jsonify
from model import classify_complaint
from datetime import datetime

app = Flask(__name__)

# use list to temp store complaints
complaints = []
complaint_id_counter = 1  # use counter for auto increment ID

# To check if system is running 
@app.route("/")
def home():
    return "<h2>Welcome to Complaint Report Management System !!!</h2>", 200


# Post new complaint
@app.route("/complaints", methods=["POST"])
def create_complaint():
    global complaint_id_counter
    data = request.json

    # Error handling
    # check title and description not null
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Both 'title' and 'description' are required."}), 400

    # Use AI to categorize complaint based on description
    category = classify_complaint(data["description"])

    # create new complaint
    complaint = {
        "id": complaint_id_counter,
        "title": data["title"],
        "description": data["description"],
        "category": category,
        "timestamp": datetime.utcnow().isoformat()  # ISO format timestamp
    }

    complaints.append(complaint)  # store complaint in list
    complaint_id_counter += 1

    return jsonify({"message": "Complaint submitted successfully.", "complaint": complaint}), 201


# get all complaints
@app.route("/complaints", methods=["GET"])
def get_complaints():
    return jsonify(complaints), 200


# use ID to get existing complaint 
@app.route("/complaints/<int:complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    complaint = next((c for c in complaints if c["id"] == complaint_id), None)
    if complaint:
        return jsonify(complaint), 200
    return jsonify({"error": "Complaint not found."}), 404


# Update existing complaint
@app.route("/complaints/<int:complaint_id>", methods=["PUT"])
def update_complaint(complaint_id):
    complaint = next((c for c in complaints if c["id"] == complaint_id), None)
    if not complaint:
        return jsonify({"error": "Complaint not found."}), 404
    data = request.json
    if "title" in data:
        complaint["title"] = data["title"] # update title
    if "description" in data:
        complaint["description"] = data["description"] # update description 
        complaint["category"] = classify_complaint(data["description"]) # update category
    return jsonify({"message": "Complaint updated.", "complaint": complaint}), 200


# Use ID to delete complaint
@app.route("/complaints/<int:complaint_id>", methods=["DELETE"])
def delete_complaint(complaint_id):
    global complaints
    if any(c["id"] == complaint_id for c in complaints):
        complaints = [c for c in complaints if c["id"] != complaint_id]
        return jsonify({"message": "Complaint deleted."}), 200
    return jsonify({"error": "Complaint not found."}), 404


# Running the Flask app in debug mode for easier development
if __name__ == "__main__":
    app.run(debug=True)
