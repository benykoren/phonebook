import requests

BASE_URL = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    response = requests.post(f'{BASE_URL}/contacts', json={
        'first_name': 'b',
        'last_name': 'b',
        'phone': 1,
        'address': 'b'
    })
    print(response.json())

    response = requests.get(f'{BASE_URL}/contacts', params={'page': 0})
    print(response.json())

    for i in range(0, 3):
        response = requests.delete(f'{BASE_URL}/contacts/{i}')
        print(response.json())

    response = requests.get(f'{BASE_URL}/contacts', params={'page': 1})
    print(response.json())

    response = requests.put(f'{BASE_URL}/contacts/5', json={
        'last_name': 'pp',
        'address': 'pp'
    })
    print(response.json())

    response = requests.get(f'{BASE_URL}/contacts', params={'page': 1})
    print(response.json())

    response = requests.get(f'{BASE_URL}/contacts/search', params={'query': 'a'})
    print(response.json())

    response = requests.get(f'{BASE_URL}/contacts', params={'page': 1})
    print(response.json())
