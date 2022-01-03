class Users:
    def __init__(self, chat_id, bursbot, mongodb, message):
        self.chat_id = chat_id
        self.bursbot = bursbot
        self.db = mongodb
        self.message = message

    @property
    def user(self, chat_id):
       return self.db.users.find_one({'chat.id': self.chat_id})

    @property
    def state(self, chat_id):
        return self.user.get('state')

    def update_state(self, state):
        self.db.users.update_one(
            {'chat.id': self.chat_id},
            {'$set': {'state': state}},
            upsert=True
            )
