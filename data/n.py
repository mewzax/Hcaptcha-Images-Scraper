import json
import base64
import hashlib
import math
import datetime


def n(req):
    # thank's h0nde for the following code
    x = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    req = req.split(".")

    req = {
        "header": json.loads(
            base64.b64decode(
                req[0] +
                "=======").decode("utf-8")),
        "payload": json.loads(
            base64.b64decode(
                req[1] +
                "=======").decode("utf-8")),
        "raw": {
            "header": req[0],
            "payload": req[1],
            "signature": req[2]}}

    def a(r):
        for t in range(len(r) - 1, -1, -1):
            if r[t] < len(x) - 1:
                r[t] += 1
                return True
            r[t] = 0
        return False

    def ix(r):
        t = ""
        for n in range(len(r)):
            t += x[r[n]]
        return t

    def o(r, e):
        n = e
        hashed = hashlib.sha1(e.encode())
        o = hashed.hexdigest()
        t = hashed.digest()
        e = None
        n = -1
        o = []
        for n in range(n + 1, 8 * len(t)):
            e = t[math.floor(n / 8)] >> n % 8 & 1
            o.append(e)
        a = o[:r]

        def index2(x, y):
            if y in x:
                return x.index(y)
            return -1
        return 0 == a[0] and index2(a, 1) >= r - 1 or -1 == index2(a, 1)

    def get():
        for e in range(25):
            n = [0 for i in range(e)]
            while a(n):
                u = req["payload"]["d"] + "::" + ix(n)
                if o(req["payload"]["s"], u):
                    return ix(n)

    result = get()
    hsl = ":".join([
        "1",
        str(req["payload"]["s"]),
        datetime.datetime.now().isoformat()[:19]
        .replace("T", "")
        .replace("-", "")
        .replace(":", ""),
        req["payload"]["d"],
        "",
        result
    ])
    return hsl
