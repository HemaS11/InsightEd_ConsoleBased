# InsightEd – Console-Based Academic Feedback Analyzer

InsightEd is a Python-based console application that helps analyze student feedback about courses and instructors.

## Features
- Submit course feedback
- View all submitted feedback
- Dashboard analytics
- Course-wise analytics
- Sentiment analysis (Positive, Negative, Neutral)
- Topic insights
- Course improvement recommendations
- Generate CSV feedback reports

## Technologies Used
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Sentiment Analysis
- Requests

## How to Run

1. Clone the repository.
2. Activate your Python virtual environment.
3. Install dependencies:
   `pip install -r Backend/requirements.txt`
4. Start the backend:
   `cd Backend`
   `uvicorn main:app --reload --host 127.0.0.1 --port 8000`
5. Open another terminal in the project root and run:
   `python console_app.py`

## Project Type
Console-based application.
