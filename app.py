from flask import Flask, jsonify, request  
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://varshney:Sj55888@cluster0.jqzobx2.mongodb.net/JWT_AUTH?retryWrites=true&w=majority'
client = MongoClient(app.config['MONGO_URI'])
db = client['JWT_AUTH'] 

@app.route('/users')
def get_users():
    users_cursor = db.users.find()
    users_list = [user for user in users_cursor]

    
    for user in users_list:
        user['_id'] = str(user['_id'])

    return jsonify({'users': users_list})



@app.route('/users/<string:id>')
def get_user(id):
    try:
        print("Received ID:", id)  
        user_id = ObjectId(id)
        print("Converted to ObjectId:", user_id)  
        
        user = db.users.find_one({'_id': user_id})

        if user:
            
            user['_id'] = str(user['_id'])
            return jsonify({'user': user})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400 


 

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json  
    user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    db.users.insert_one(user)
    return jsonify({'message': 'User created'})



@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.json
        user_id = ObjectId(id)  
        update_result = db.users.update_one({'_id': user_id}, {'$set': data})

        if update_result.modified_count > 0:
            return jsonify({'message': 'User updated'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400



@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user_id = ObjectId(id) 
        delete_result = db.users.delete_one({'_id': user_id})

        if delete_result.deleted_count > 0:
            return jsonify({'message': 'User deleted'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        if isinstance(e, Timestamp):
            return jsonify({'message': 'User deleted'}), 200  
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
