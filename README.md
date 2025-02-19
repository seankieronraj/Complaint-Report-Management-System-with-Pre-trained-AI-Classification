# Complaint-Report-Management-System-with-Pre-trained-AI-Classification
RESTful API that allows users to manage complaint reports. When a complaint is submitted, the system will automatically assign a category (such as Billing, Service, or Technical) using a pre-trained AI model Hugging Face

## AI Model
- **Model Used**: `distilbert-base-uncased-finetuned-sst-2-english`  
- **Mapping**:  
  - POSITIVE → Service  
  - NEGATIVE → Billing  
  - Others → Other  

## How to Run
Using Docker:
`docker build -t complaint-system`  
`docker run -p 5000:5000 complaint-system`  
Access the API at: http://localhost:5000

Without Docker:
`pip install flask transformers torch pytest`
`python app.py`

API Endpoints
- POST /complaints: Submit a new complaint
- GET /complaints: Retrieve all complaints
- GET /complaints/{id}: Get a specific complaint
- PUT /complaints/{id}: Update a complaint
- DELETE /complaints/{id}: Delete a complaint


Run Tests
`pytest test_app.py` 

