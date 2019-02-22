from flask import Flask, request, jsonify
from chatbot.response import ChatBotResponse

app = Flask(__name__)
chatbot = ChatBotResponse()


@app.route('/')
def check_running():
    return 'Chatbot service is running...'


@app.route('/api/welcome', methods=['POST'])
def chatbot_welcome():
    user_id = request.form['user_id']
    username = request.form['username']
    existed = request.form['existed']
    data = chatbot.welcome(user_id, username, existed)
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)
    return resp


@app.route('/api/response', methods=['POST'])
def chatbot_response():
    user_request = request.form['request']
    user_id = request.form['user_id']
    data = chatbot.response(user_request, user_id)
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)
    return resp


@app.route('/api/username', methods=['POST'])
def get_username():
    user_id = request.form['user_id']
    data = chatbot.get_username(user_id)
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)
    return resp


@app.route('/api/remove_username', methods=['POST'])
def remove_username():
    user_id = request.form['user_id']
    chatbot.remove_username(user_id)
    resp = jsonify(status_code=200)
    return resp


if __name__ == '__main__':
    app.run()
