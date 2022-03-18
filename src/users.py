class Users:
    def __init__(self, chat_id, bursbot, mongodb):
        self.chat_id = chat_id
        self.bursbot = bursbot
        self.db = mongodb

    @property
    def user(self):
       return self.db.users.find_one({'chat.id': self.chat_id})

    @property
    def state(self):
        return self.user.get('state')

    @property
    def portfolio(self):
        return self.user.get('portfolio') or {}

    @property
    def current_symbol(self):
        return self.user.get('current_symbol') or {}

    def update_state(self, state):
        self.db.users.update_one(
            {'chat.id': self.chat_id},
            {'$set': {'state': state}},
            upsert=True
            )

    def update_portfolio(self, portfolio):
        self.db.users.update_one(
            {'chat.id': self.chat_id},
            {'$set': {'portfolio': portfolio}},
            upsert=True
            )

    def update_current_symbol(self, current_symbol):
        self.db.users.update_one(
            {'chat.id': self.chat_id},
            {'$set': {'current_symbol': current_symbol}},
            upsert=True
            )
