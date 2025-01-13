from flask import Flask, request, jsonify, render_template
import boto3
import json
from botocore.exceptions import NoCredentialsError, NoRegionError

app = Flask(__name__)

# Initialize AWS client with dynamic profile name and region
def get_client(profile_name="default", region_name="us-east-1"):
    try:
        session = boto3.Session(profile_name=profile_name)
        return session.client('secretsmanager', region_name=region_name)
    except NoRegionError:
        raise Exception("No AWS region specified. Please provide a valid region.")

@app.route('/')
def index():
    return render_template('index.html')  # The main UI page

# List all secrets
@app.route('/list', methods=['GET'])
def list_secrets():
    profile_name = request.args.get('profile_name', 'default')  # Default profile
    region_name = request.args.get('region_name', 'us-east-1')  # Default region
    client = get_client(profile_name, region_name)
    try:
        secrets = client.list_secrets()["SecretList"]
        return jsonify({"message": "Secrets listed successfully", "data": secrets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create a new secret
@app.route('/create', methods=['POST'])
def create_secret():
    data = request.json
    profile_name = data.get('profile_name', 'default')  # Default profile if not provided
    region_name = data.get('region_name', 'us-east-1')  # Default region if not provided
    client = get_client(profile_name, region_name)
    try:
        response = client.create_secret(
            Name=data['name'],
            SecretString=json.dumps(data['value']),
            Description=data.get('description', "Managed by Flask UI")
        )
        return jsonify({"message": "Secret created successfully", "data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/get/<name>', methods=['GET'])
def get_secret(name):
    profile_name = request.args.get('profile_name', 'default')  # Default profile
    region_name = request.args.get('region_name', 'us-east-1')  # Default region
    client = get_client(profile_name, region_name)
    try:
        response = client.get_secret_value(SecretId=name)
        secret_value = json.loads(response['SecretString'])
        return jsonify({"message": "Secret retrieved successfully", "data": secret_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
