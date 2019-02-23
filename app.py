from flask import Flask, request, jsonify, Response
from chatbot.response import ChatBotResponse
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
chatbot = ChatBotResponse()


@app.route('/')
def check_running():
    response = jsonify({'data': 'Chatbot service is running...'})
    return response


@app.route('/api/welcome', methods=['POST'])
def chatbot_welcome():

    content = request.get_json()
    data = chatbot.welcome(content['user_id'], content['username'], content['existed'])
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)

    print(">>>>>> Response: ", resp)
    return resp


@app.route('/api/response', methods=['POST'])
def chatbot_response():

    content = request.get_json()
    data = chatbot.response(content['request'], content['user_id'])
    username = chatbot.get_username(content['user_id'])
    print(">>>>>> Username: ", username)
    if data:
        resp = jsonify(status_code=200, data=data, username=username)
    else:
        resp = jsonify(status_code=404)

    print(">>>>>> Response: ", resp)
    return resp


@app.route('/api/username', methods=['POST'])
def get_username():

    content = request.get_json()
    data = chatbot.get_username(content['user_id'])
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)
    print(">>>>>> Username: ", resp)
    return resp


@app.route('/api/remove_username', methods=['POST'])
def remove_username():
    content = request.get_json()
    chatbot.remove_username(content['user_id'])
    resp = jsonify(status_code=200)
    print(">>>>>> Remove username: ", resp)
    return resp


if __name__ == '__main__':
    app.run()
