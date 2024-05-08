# Posts new employees to the database
import json
from pymongo import MongoClient
import os

# MongoDB client initialization
client = MongoClient(host=os.environ.get("ATLAS_URI"))

def lambda_handler(event, context):
    print("Received event:", event)
    
    try:
        # Parse the body from event
        body = json.loads(event['body'])
        print("Parsed body:", body)
        
        # Access the data
        name = body['name']
        email = body['email']
        title = body['title']
        wage = body['wage']
        supervisor = body['supervisor']
        user_email = body['user_email']

        # Reference the database and collection
        db = client.EmployeeManagement
        collection = db.Employees

        # Insert data into MongoDB
        insertedPost = collection.insert_one({
            'name': name,
            'email': email,
            'title': title,
            'wage': wage,
            'supervisor': supervisor,
            'user_email': user_email
        })

        # Print and return the ID of the inserted document
        print("Inserted document ID:", insertedPost.inserted_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'id': str(insertedPost.inserted_id)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print("Error:", e)  # Log the exception for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }