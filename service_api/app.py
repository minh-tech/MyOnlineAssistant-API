from flask import request, jsonify
from service_api import app, chatbot
from service_api.models import User, Message
from datetime import datetime
from service_api import db
from service_api import database_utils as db_utils


@app.route('/')
def check_running():
    response = jsonify({'data': 'Chatbot service is running...'})
    return response


@app.route('/api/welcome', methods=['POST'])
def chatbot_welcome():

    content = request.get_json()

    data, emotion = chatbot.welcome(content['user_id'], content['username'], content['existed'])
    messages = ""
    if content['existed']:
        # Query messages from database
        messages = db_utils.get_messages(db.session, content['user_id'])
        messages.append({
            "content": data,
            "is_user": False,
            "name": "Cheri"
        })
    else:
        # Update messages into database
        db_utils.add_message(db.session, Message(
            user_id=content['user_id'],
            name='Cheri',
            is_user=False,
            content=data
        ))
    if data:
        resp = jsonify(status_code=200, data=messages, emotion=emotion)
    else:
        resp = jsonify(status_code=404)

    print(">>>>>> Response: ", resp)
    return resp


@app.route('/api/response', methods=['POST'])
def chatbot_response():

    content = request.get_json()
    data, emotion = chatbot.response(content['request'], content['user_id'])
    username = chatbot.get_username(content['user_id'])
    print(">>>>>> Username: ", username)

    # Update messages into database
    db_utils.add_message(db.session, Message(
        user_id=content['user_id'],
        name=username,
        is_user=True,
        content=content['request']
    ))

    if data:
        db_utils.add_message(db.session, Message(
            user_id=content['user_id'],
            name='Cheri',
            is_user=False,
            content=data
        ))

        resp = jsonify(status_code=200, data=data, username=username, emotion=emotion)
    else:
        resp = jsonify(status_code=404)

    print(">>>>>> Response: ", resp.status_code)
    return resp


@app.route('/api/messages', methods=['POST'])
def get_all_messages():
    content = request.get_json()
    messages = db_utils.get_messages(db.session, content['user_id'])
    print(">>>>>> messages: ", messages)
    if messages:
        resp = jsonify(status_code=200, data=messages)
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
