import redis


class RedisClientManager:
    def __init__(self, host, port, username, password):
        self.client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            ssl=True,
            ssl_cert_reqs=None
        )
    def add_request(self, request_id, request_data):
        # Check if the request ID already exists
        print("request id is {}".format(request_id))
        if self.client.exists(request_id):
            return False  # Request ID already exists

        # Store the request data with the request ID as the key
        # and set an expiration time of 30 days (30 days * 24 hours/day * 60 minutes/hour * 60 seconds/minute)
        self.client.setex(request_id, 30 * 24 * 60 * 60, request_data)
        print("set success {}".format(request_id))
        return True  # Request added successfully




