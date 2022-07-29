import json


def test_json(n):
    result = ""
    s = {
        "pathRewriteId": "rewrite-opy57pa4",
        "gatewayGroupId": "group-qevjbqab",
        "regex": "/jin2-echo/(.*)",
        "replacement": "/jin-test002/test/provider-demo/echo/$1",
        "blocked": "N",
        "order": 1
    }
    for i in range(n):
        s["regex"] = "/jin2-echo-" + str(i) + "/(.*)"
        result = result + json.dumps(s) + ","
    result = result[0:-1]
    return result


if __name__ == '__main__':
    value = test_json(2000)
    fo = open(r"D:\Jin\太保项目\test.json", "w")
    fo.write("[" + value + "]")
    fo.close()
