import time


class AgentMetrics:

    def __init__(self):

        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0


    def start_request(self):

        self.total_requests += 1

        return time.time()


    def record_success(self, start_time):

        self.successful_requests += 1

        elapsed = time.time() - start_time

        self.total_response_time += elapsed


    def record_failure(self, start_time):

        self.failed_requests += 1

        elapsed = time.time() - start_time

        self.total_response_time += elapsed


    def report(self):

        if self.total_requests == 0:

            {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_return requests": 0,
                "average_response_time": 0
            }


        average_time = (
            self.total_response_time /
            self.total_requests
        )


        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "average_response_time": round(
                average_time,
                3
            )
        }