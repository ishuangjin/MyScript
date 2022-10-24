# 每unit_time秒运行count次
count = 105
unit_time = 60
# 运行run_time秒
run_time = 6000

all_url = r"http://192.168.45.29:26435/group-jin/demo2/shenliufei-consumer-demo1/echo-rest/hello"
# all_url = r"http://192.168.45.29:44980/echo-rest/hello"
headers = r"x-mg-traceid: 55b00164-4880-11ed-83f0-2811a82fb6cd"

tag_params = {'tagName': 'user', 'tagValue': 'test'}
test_url = "testUrl"
test_url.loop_ping()


def testUrl(count, unit_time, run_time, all_url, *args):
    print(count, unit_time, run_time, all_url, tag_params, headers)


testUrl(count, unit_time, run_time, all_url, tag_params, headers)