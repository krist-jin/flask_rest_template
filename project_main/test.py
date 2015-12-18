import requests

for i in xrange(10000):
    print i
    # res = requests.get("http://127.0.0.1/ad")
    # print res.content
    requests.post("http://127.0.0.1/impression",data={'aid': 2, 'timestamp': 3})

