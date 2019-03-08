from flask import request, jsonify
from datetime import datetime
from service_api import app, chatbot
from service_api.models import User, Message
from service_api import db
from service_api import database_utils as db_utils
from service_api import constant as ct
import os


@app.route('/')
def check_running():
    response = jsonify({ct.DATA: 'Chatbot service is running...'})
    return response


@app.route('/api/welcome', methods=['POST'])
def chatbot_welcome():

    content = request.get_json()
    print(">>>>>> username: " + content[ct.USERNAME])
    data, emotion = chatbot.welcome(content[ct.USER_ID], content[ct.USERNAME], content[ct.EXISTED])
    messages = ""
    if content[ct.EXISTED]:
        # Query messages from database
        messages = db_utils.get_messages(db.session, content[ct.USER_ID])
        messages.append({
            ct.CONTENT: data,
            ct.IS_USER: False,
            ct.NAME: ct.BOT_NAME
        })
    else:
        # Update messages into database
        db_utils.add_message(db.session, Message(
            user_id=content[ct.USER_ID],
            name=ct.BOT_NAME,
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
    data, emotion = chatbot.response(content[ct.REQUEST], content[ct.USER_ID])
    username = chatbot.get_username(content[ct.USER_ID])
    print(">>>>>> Username: ", username)

    # Update messages into database
    db_utils.add_message(db.session, Message(
        user_id=content[ct.USER_ID],
        name=username,
        is_user=True,
        content=content[ct.REQUEST]
    ))

    if data:
        db_utils.add_message(db.session, Message(
            user_id=content[ct.USER_ID],
            name=ct.BOT_NAME,
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
    messages = db_utils.get_messages(db.session, content[ct.USER_ID])
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
    data = chatbot.get_username(content[ct.USER_ID])
    if data:
        resp = jsonify(status_code=200, data=data)
    else:
        resp = jsonify(status_code=404)
    print(">>>>>> Username: ", resp)
    return resp


@app.route('/api/remove_username', methods=['POST'])
def remove_username():
    content = request.get_json()
    chatbot.remove_username(content[ct.USER_ID])
    resp = jsonify(status_code=200)
    print(">>>>>> Remove username: ", resp)
    return resp


@app.route('/api/feedback', methods=['POST'])
def receive_feedback():

    content = request.get_json()
    feedback_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "%s/feedback/%s-%s.txt" % (feedback_dir, content[ct.USER_ID], datetime.now().strftime('%Y-%m-%d-%H:%M'))

    with open(filename, "w+") as f:
        for key, value in content.items():
            f.write("%s: %s\n" % (key, value))

    resp = jsonify(status_code=200)
    return resp


if __name__ == '__main__':
    app.run()
