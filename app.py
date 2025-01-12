from flask import Flask, request, jsonify, render_template
import boto3
import json
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Initialize AWS client
def get_client():
    session = boto3.Session(profile_name="default")  # Adjust profile_name as needed for SSO
    return session.client('secretsmanager')

@app.route('/')
def index():
    return render_template('index.html')  # A simple UI

@app.route('/create', methods=['POST'])
def create_secret():
    data = request.json
    client = get_client()
    try:
        response = client.create_secret(
            Name=data['name'],
            SecretString=json.dumps(data['value']),
            Description=data.get('description', "Managed by Flask UI")
        )
        return jsonify({"message": "Secret created successfully", "data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve/<name>', methods=['GET'])
def retrieve_secret(name):
    client = get_client()
    try:
        response = client.get_secret_value(SecretId=name)
        secret_value = json.loads(response['SecretString'])
        return jsonify({"message": "Secret retrieved successfully", "data": secret_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update', methods=['PUT'])
def update_secret():
    data = request.json
    client = get_client()
    try:
        response = client.update_secret(
            SecretId=data['name'],
            SecretString=json.dumps(data['value'])
        )
        return jsonify({"message": "Secret updated successfully", "data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<name>', methods=['DELETE'])
def delete_secret(name):
    client = get_client()
    try:
        response = client.delete_secret(
            SecretId=name,
            ForceDeleteWithoutRecovery=True
        )
        return jsonify({"message": "Secret deleted successfully", "data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
