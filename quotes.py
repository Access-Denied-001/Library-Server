import requests


def quotes():
    res = requests.get("https://quotes.rest/qod")
    data = dict(res.json())
    if list(data.keys())[0] == "error":
        return "error"
    c = ((data["contents"])["quotes"])[0]["quote"]
    d = ((data["contents"])["quotes"])[0]["author"]
    l = [c, d]
    return l


quotes = quotes()