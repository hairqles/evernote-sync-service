class Cache:
    data = {}

    def set(self, user_id, request_token):
        self.data[user_id] = request_token

    def get(self, user_id):
        return self.data[user_id]

    def delete(self, user_id):
        del self.data[user_id]