class Cache:
    data = {}

    def set(self, user_id, request_token):
        self.data[user_id] = request_token

    def get(self, user_id):
        print(self.data)
        return self.data[user_id]