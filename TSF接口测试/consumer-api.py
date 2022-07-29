import time
import requests


class TestUrl:

    def __init__(self, host, port, run_speed_times_limit, run_speed_unit_time, run_time):
        """
        run_time:运行时间, 秒
        run_speed_times_limit: 限流请求数
        run_speed_unit_time: 单位时间
        """
        self.host = host
        self.port = port
        self.run_speed_times_limit = run_speed_times_limit
        self.run_speed_unit_time = run_speed_unit_time
        self.run_time = run_time

    def ping_url(self):
        tag_params = {'tagName': 'user', 'tagValue': 'test'}
        re = requests.get(url='http://{}:{}/echo-rest/hello'.format(self.host, self.port), params=tag_params)
        print(re.text)

    def loop_ping(self):
        count = 0
        sleep_time = self.run_speed_unit_time / self.run_speed_times_limit
        start_time = time.time()
        end_time = start_time + self.run_time
        while time.time() < end_time:
            count += 1
            self.ping_url()
            stop_time = time.time()
            print('已ping {} 次, 共使用 {} 秒'.format(count, stop_time - start_time))
            time.sleep(sleep_time)


if __name__ == '__main__':
    host = '192.168.22.16'
    port = '31441'
    run_speed_times_limit = 120
    run_speed_unit_time = 10
    run_time = 300
    test_url = TestUrl(host, port, run_speed_times_limit, run_speed_unit_time, run_time)
    test_url.loop_ping()
