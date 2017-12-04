from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, abort, fields, marshal
from flask01.models import MessageModel

import datetime


class MessageManager(object):
    last_id = 0

    def __init__(self):
        self.messages = {}

    def insert_message(self, message):
        MessageManager.last_id += 1
        # print MessageManager.last_id
        message.idx = MessageManager.last_id
        self.messages[MessageManager.last_id] = message
        # print self.messages

    def get_message(self, idx):
        return self.messages[idx]

    def delete_message(self, idx):
        del self.messages[idx]


message_fields = dict(
    idx = fields.Integer,
    uri = fields.Url('message_endpoint'),
    message = fields.String,
    duration = fields.Integer,
    creation_date = fields.DateTime,
    message_category = fields.String,
    printed_times  = fields.Integer,
    printed_once = fields.Boolean
)


message_manager = MessageManager()

class Message(Resource):

    def abort_if_message_doesnt_exist(self, idx):
        if idx not in message_manager.messages:
            abort(
                404,
                message = "Message {0} doesn't exist".format(idx)
            )

    @marshal_with(message_fields)
    def get(self, idx):
        self.abort_if_message_doesnt_exist(idx)

        return message_manager.get_message(idx)

    def delete(self, idx):
        self.abort_if_message_doesnt_exist(idx)

        message_manager.delete_message(idx)
        return '', 204


    @marshal_with(message_fields)
    def patch(self, idx):
        self.abort_if_message_doesnt_exist(idx)

        message = message_manager.get_message(idx)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('duration', type=int)
        parser.add_argument('printed_times', type=int)
        parser.add_argument('printed_once', type=bool)

        args = parser.parse_args()

        if 'message' in args:
            message.message = args['message']

        if 'duration' in args:
            message.duration = args['duration']

        if 'printed_times' in args:
            message.printed_times = args['printed_times']

        if 'printed_once' in args:
            message.printed_once = args['printed_once']

        return message
        #alternate way with marshal
        # return marshal(message, message_fields), 200

class MessageList(Resource):

    @marshal_with(message_fields)
    def get(self):
        return [v for v in message_manager.messages.values()]

    @marshal_with(message_fields)
    def post(self):
        parser =reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True, help='message cannot be blank')
        parser.add_argument('duration', type=int, required=True, help='duration cannot be blank')
        parser.add_argument('message_category', type=str, required=True, help='message category cannot be blank')
        args = parser.parse_args()
        message = MessageModel(
            message= args['message'],
            duration = args['duration'],
            message_category = args['message_category'],
            creation_date = datetime.datetime.utcnow()
        )

        print message
        message_manager.insert_message(message)
        return message, 201

app = Flask(__name__)
api = Api(app)

api.add_resource(MessageList, '/api/messages/')
api.add_resource(Message, '/api/messages/<int:idx>', endpoint='message_endpoint')

if __name__ == '__main__':
    app.run(debug=True)


