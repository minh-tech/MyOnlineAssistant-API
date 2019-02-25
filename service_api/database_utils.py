from service_api.models import User, Message
from service_api import db
from datetime import datetime


def add_or_update_user(session, _user, **kwargs):
    instance = session.query(User).filter_by(user_id=_user.user_id).first()
    if instance:
        for key, value in kwargs.items():
            setattr(instance, key, value)
    else:
        session.add(_user)
    session.commit()


def add_message(session, _message):
    session.add(_message)
    session.commit()


def get_messages(session, _user_id):
    _messages = session.query(Message).filter_by(user_id=_user_id)\
                        .with_entities(Message.name, Message.is_user, Message.content, Message.created_date).all()
    array = []
    for msg in _messages:
        array.append({'name': msg.name,
                      'is_user': msg.is_user,
                      'content': msg.content,
                      'created_date': msg.created_date
                      })
    return array


if __name__ == '__main__':
    # user = User(user_id="1106", username="John", email="john@minh.com", organization="House", last_active_date=datetime.utcnow())
    # add_or_update_user(session=db.session, _user=user, username="Hoang Minh 1")
    # msg = Message(user_id='1106', name='John', is_user=True, content='How are you?')
    # add_message(db.session, msg)
    # msg = Message(user_id='1106', name='Cheri', is_user=False, content='Very excellent')
    # add_message(db.session, msg)
    # msg = Message(user_id='1106', name='Cheri', is_user=False, content='Thank you')
    # add_message(db.session, msg)
    # msg = Message(user_id='1106', name='John', is_user=True, content='Nice to see you')
    # add_message(db.session, msg)
    messages = get_messages(db.session, _user_id='1106')
    print(messages)
    # for m in messages:
    #     print(m)
