from flask import Flask, jsonify
from user_model import User

app = Flask(__name__)

    
users_storage = [
    User("Alice","Smith","alice@example.com", True),
    User("BOb","Johnson","bob@example.com"),
    User("Charlie","Brown","charli@example.com")
]

@app.route('/users', methods=['GET'])
def get_users():
    user_data_list = []

    for user in users_storage:
        user_data_list.append({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "initials": user.get_initials()
        })
    
    return jsonify(user_data_list)

@app.route('/')
def home():
    return "<h1>Welcome to the Python/Flask Project API</h1>"

if __name__ == '__main__':
    app.run(debug=True)
