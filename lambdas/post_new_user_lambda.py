# This Lambda is triggered when a new user confirms their account
import os
from pymongo import MongoClient

# Environment variables for MongoDB connection
client = MongoClient(host=os.environ.get("ATLAS_URI"))
db = client.EmployeeManagement
collection = db.Users

def lambda_handler(event, context):
    # Get user attributes from the Cognito event
    user_attributes = event['request']['userAttributes']
    user_id = user_attributes['sub']  # Cognito unique identifier for the user

    # Prepare the document to insert into MongoDB
    user_document = {
        'cognito_user_id': user_id,
        'email': user_attributes.get('email'),
        'given_name': user_attributes.get('given_name'),
        'family_name': user_attributes.get('family_name') 
    }

    # Insert the document into MongoDB
    result = collection.insert_one(user_document)

    print(f"Inserted user {user_id} with result {result.inserted_id}")

    # Return to Cognito
    return event