import requests

# for i in xrange(5):
#     print i
#     requests.post("http://127.0.0.1/ad",data={'content': "ebay ad 333", 'category_id': 3})

for i in xrange(10000):
    print i
    # res = requests.get("http://127.0.0.1/ad")
    # print res.content
    requests.post("http://127.0.0.1/impression",data={'aid': 2, 'timestamp': 3})

# for i in xrange(100):
#     print i
#     res = requests.get("http://127.0.0.1/ad")
#     requests.post("http://127.0.0.1/click",data={'aid': int(res.content), 'timestamp': 3})

