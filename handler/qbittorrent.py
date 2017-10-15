import requests


class HandlerQBT:
    def __init__(self, base_url):
        self.BASE_URL = base_url
        self.cookie = ''

    def login(self, user, password):
        self.cookie = ''

        url = self.BASE_URL + '/login'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': user, 'password': password}
        response = requests.post(url, data=data, headers=headers)

        if response.status_code != requests.codes.ok:
            return False

        cookie = response.headers.get('Set-Cookie')
        if cookie:
            self.cookie = cookie
            return True
        else:
            return False

    def logout(self):
        url = self.BASE_URL + '/logout'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': self.cookie}
        requests.post(url, headers=headers)

    def get_torrent_list(self):
        url = self.BASE_URL + '/query/torrents'
        headers = {'Cookie': self.cookie}
        response = requests.get(url, headers=headers)

        return response.text

    def add_from_url(self, torrent_url):
        url = self.BASE_URL + '/command/download'
        headers = {'Cookie': self.cookie}
        data = {'urls': torrent_url}
        response = requests.post(url, headers=headers, data=data)

        if response.status_code != requests.codes.ok:
            return False
        else:
            return True
