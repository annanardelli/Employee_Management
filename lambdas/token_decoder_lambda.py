# Decodes id tokens obtained from the cognito sign-in process, takes the token as a query string param
import jwt
import json

def lambda_handler(event, context):
    # Get the token from the query string parameters
    token = event.get('queryStringParameters', {}).get('token', '')
    
    print("token", token)
    
    try:
        # Attempt to decode the token
        decoded = jwt.decode(token, options={"verify_signature": False})
        print("Decoded token:", decoded)
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
        },
        # Ensure the body is a JSON string
            'body': json.dumps(decoded)
        }
    # Handle exceptions
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error decoding token: {str(e)}'})
        }