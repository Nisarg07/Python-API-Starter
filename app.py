from typing import List, Optional
from flask import Flask, jsonify, request
from user_model import User
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore


__firebase_config = '{}' 
__app_id = 'default-app-id'
__initial_auth_token = ''

db = None
user_id = "anonymous"
app_id = __app_id

try:
    firebase_config = json.loads(__firebase_config)

    if firebase_config and len(firebase_config) > 0:

        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

    if __initial_auth_token:
        try:
            decodeed_token = auth.verify_id_token(__initial_auth_token)
            user_id = decodeed_token['uid']
        except Exception:
            user_id = "default-user-id"
    
        print("INFO: Firebase Admin SDK initialized successfully.")
    else:
        # Config is empty (placeholder), skip Admin SDK initialization
        db = None
        user_id = "local-test-id" # Use a consistent ID for local testing
        print("WARNING: Firebase Admin SDK initialization skipped. __firebase_config is empty. Database calls will fail until configuration is provided.")

except Exception as e:
    print(f"FATAL ERROR initializing Firebase: {e}")
    db = None
    app_id = 'error-app-id'
    user_id = 'error-user-id'

USER_COLLECTION_PATH = f"artifacts/{app_id}/users/{user_id}/profiles"

def add_document(collection_path: str, data: dict) -> str:
    if db is None:
        raise ConnectionError("Firestore is not initialized. Can not add document.")
    
    doc_ref = db.collection(collection_path).document()
    doc_ref.set(data)
    return doc_ref.id

def get_documents(collection_path: str) -> List[dict]:
    if db is None:
        raise ConnectionError("Firestore not initialized. Cannot fetch documents. Check console for configuration warning.")

    docs = db.collection(collection_path).stream()
    return [{**doc.to_dict(), 'id': doc.id} for doc in docs]

def get_documents_by_id(collection_path: str, doc_id: str) -> Optional[dict]:
    if db is None:
        raise ConnectionError("Firestore not initialized. Cannot fetch documents.Check console for confuguration warning.")
    doc_ref = db.collection(collection_path).document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        return{**doc.to_dict(), 'id': doc.id}
    return None


app = Flask(__name__)

def serialize_users(users: List[User]) -> List[dict]:
    return [u.to_dict() for u in users]

    


@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Fetching documents from Firestore
        user_dicts = get_documents(USER_COLLECTION_PATH)
        return jsonify(user_dicts)
    except ConnectionError as e:
        # This occurs if db is None (i.e., Firebase init failed due to empty config)
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Failed to fetch users: {e}"}), 500
#     users_storage = [
#     User(1, "Alice", "alice@example.com", "Junior"),
#         User(2, "Bob", "bob@example.com", "Mid"),
# ]
#     user_dicts = serialize_users(users_storage) 
    
#     return jsonify(user_dicts)

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    try:
        # Fetching documents from Firestore
        user_dict = get_documents_by_id(USER_COLLECTION_PATH, id)
        if user_dict is None:
            return jsonify({"error": f"User with ID '{id}' not found."}), 404

        return jsonify(user_dict)
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Failed to fetch user: {e}"}), 500

@app.route('/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error":"Missing required fields (username, email)"}), 400
    
    new_user = User(
        id = None,
        username = data['username'],
        email = data['email'],
        level = data.get('level','Junior')
    )
    user_data = new_user.to_dict()

    try:
        new_id = add_document(USER_COLLECTION_PATH, user_data)

        return jsonify({
            "message": "User created successfully",
            "id": new_id,
            "collection_path": USER_COLLECTION_PATH
        }), 201
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Database save failed: {e}"}), 500

if __name__ == '__main__':
    print(f"--- FLASK APP STARTING ---")
    print(f"APP ID: {app_id}, USER ID: {user_id}")
    print(f"USER COLLECTION PATH: {USER_COLLECTION_PATH}")

    app.run(debug = True)
