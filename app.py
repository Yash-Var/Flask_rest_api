from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask import Blueprint

class UserAPI:
    def __init__(self, app, db):
        self.app = app
        self.db = db



    def configure_routes(self):
        user_bp = Blueprint('user_bp', __name__)

        @user_bp.route('/users', methods=['GET'])
        def get_users():
            users_cursor = self.db.users.find()
            users_list = [user for user in users_cursor]

            for user in users_list:
                user['_id'] = str(user['_id'])

            return jsonify({'users': users_list})



        @user_bp.route('/users/<user_id>', methods=['GET'])
        def get_user(user_id):
            user = self.db.users.find_one({'_id': ObjectId(user_id)})

            if user:
                user['_id'] = str(user['_id'])
                return jsonify({'user': user})
            else:
                return jsonify({'message': 'User not found'}), 404



        @user_bp.route('/users', methods=['POST'])
        def create_user():
            data = request.json

            if 'name' in data and 'email' in data and 'password' in data:
                user_data = {
                    'name': data['name'],
                    'email': data['email'],
                    'password': data['password']
                }
                user_id = self.db.users.insert_one(user_data).inserted_id
                return jsonify({'message': 'User created', '_id': str(user_id)}), 201
            else:
                return jsonify({'message': 'Missing name, email, or password'}), 400



        @user_bp.route('/users/<user_id>', methods=['PUT'])
        def update_user(user_id):
            data = request.json

            if 'username' in data or 'email' in data:
                result = self.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': data})

                if result.modified_count > 0:
                    return jsonify({'message': 'User updated'}), 200
                else:
                    return jsonify({'message': 'User not found'}), 404
            else:
                return jsonify({'message': 'No data to update'}), 400



        @user_bp.route('/users/<user_id>', methods=['DELETE'])
        def delete_user(user_id):
            result = self.db.users.delete_one({'_id': ObjectId(user_id)})

            if result.deleted_count > 0:
                return jsonify({'message': 'User deleted'}), 200
            else:
                return jsonify({'message': 'User not found'}), 404

        
        self.app.register_blueprint(user_bp)

        

def create_app():
    app = Flask(__name__)

    
    app.config['MONGO_URI'] = 'mongodb+srv://varshney:Sj55888@cluster0.jqzobx2.mongodb.net/JWT_AUTH?retryWrites=true&w=majority'
    client = MongoClient(app.config['MONGO_URI'])
    db = client['JWT_AUTH']

    user_api = UserAPI(app, db)
    user_api.configure_routes()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
