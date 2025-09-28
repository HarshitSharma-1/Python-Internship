from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {}
user_id_counter = 1

@app.route('/')
def home():
    return jsonify({
        "message": "User Management API",
        "endpoints": {
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create new user",
            "PUT /users/<id>": "Update user by ID",
            "DELETE /users/<id>": "Delete user by ID"
        }
    })

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "users": users,
        "total": len(users)
    })

# GET single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# CREATE new user
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    
    data = request.get_json()
    
    # Validation
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and email are required"}), 400
    
    # Check if email already exists
    if any(user['email'] == data['email'] for user in users.values()):
        return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age'),
        "city": data.get('city')
    }
    
    users[user_id_counter] = user
    user_id_counter += 1
    
    return jsonify(user), 201

# UPDATE user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user = users[user_id]
    
    # Update fields if provided
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        # Check if email already exists for other users
        if any(u['email'] == data['email'] for uid, u in users.items() if uid != user_id):
            return jsonify({"error": "Email already exists"}), 400
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']
    if 'city' in data:
        user['city'] = data['city']
    
    users[user_id] = user
    return jsonify(user)

# DELETE user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    deleted_user = users.pop(user_id)
    return jsonify({
        "message": "User deleted successfully",
        "deleted_user": deleted_user
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)