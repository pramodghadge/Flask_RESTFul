class MessageModel(object):
    def __init__(self, message, duration, creation_date, message_category):
        self.idx  = 0
        self.message = message
        self.duration = duration
        self.creation_date = creation_date
        self.message_category = message_category
        self.printed_times = 0
        self.printed_once = False

    def __repr__(self):
        return 'Model:idx['+str(self.idx)+'],message:['+str(self.message) + '], message category:['+ str(self.message_category)+']'