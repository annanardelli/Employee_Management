# Files are named after their functionality here for viewing convenience, normally they would all be named lambda_function.py
# Also the dependency files aren't included here, but are necessary for AWS deployment
# This Lambda gets the employee objects from the database, takes the user's email as a param in the URL
from pymongo import MongoClient
import os, json

client = MongoClient(host=os.environ.get("ATLAS_URI"))

def lambda_handler(event, context):
    # Extract email from query string params
    email = event.get('queryStringParameters', {}).get('email', '')
    # Now fetch only the employees that were added by this user
    employees = fetch_employees_from_db(email)
    return {
        'statusCode': 200,
        'body': json.dumps(employees)
    }

def fetch_employees_from_db(email):
    # Assuming you're using PyMongo or similar
    db = client.EmployeeManagement
    employees_collection = db.Employees
    employees = list(employees_collection.find({"user_email": email}))
    return employees