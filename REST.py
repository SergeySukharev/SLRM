import requests
import json

def main():
    session = requests.Session()
    base_url = "https://httpbin.org" + "/get"
    headers = {
        'X-Shop-Token': 'vfhnsirf',
        'User-Agent': 'Mega-Browser'
    }
    params = {
        'order': 'votes',
        'sort': 'desc'
    }
    r = session.get(base_url, params=params,headers=headers)
    jsonified_response_2 = json.loads(r.text)
    print(jsonified_response_2)


if __name__ == '__main__':
    main()
