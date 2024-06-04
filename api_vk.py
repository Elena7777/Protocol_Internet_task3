import requests
from requests import HTTPError


def help():
    print('Данная программа предоставляет некоторую информацию о пользователе.')
    print('Чтобы узнать какие-то данные нужно сначала ввести id пользователя и')
    print('следующим сообщением нужный запрос из перечисленных:')
    print('friends - выводит всех друзей пользователя')
    print('photo - выведет все названия фотоальбомов')
    print('groups - выведет названия всех сообществ, в которые вступил пользователь')
    print('user - выведет имя, фамилию пользователя, статус')
    print('ВНИМАНИЕ: перед началом работы программы нужно ввести ваш access_token в VK')
    print('Например: vk1.a.sOV...')


class VkApi(object):
    def __init__(self, id_user, request):
        self.token = 'Your token'
        self.id_user = id_user
        self.request = request
        self.friends = ''
        self.photo_album = ''
        self.groups = ''
        self.url = 'https://api.vk.com/method/'
        if self.token is None:
            print("Введите свой токен API VK в программу")
            return

        self.flag_request = 0
        self.collect_data()

    def collect_data(self):
        try:
            if self.request == 'user':
                user = requests.get(f'{self.url}users.get?user_ids={self.id_user}&fields=status&access_token={self.token}&v=5.131').json()
                if 'response' in user:
                    info_user = user['response'][0]
                    print('Пользователь:')
                    print(' Фамилия:', info_user.get('last_name', 'Нет данных'))
                    print(' Имя:', info_user.get('first_name', 'Нет данных'))
                    print(' Статус:', info_user.get('status', 'Нет данных'))
                    open_profile = 'Нет' if info_user['is_closed'] else 'Да'
                    print(' Отрытый профиль:', open_profile)
                else:
                    print('Пользователь не найден')

            elif self.request == 'friends':
                friends = requests.get(f"{self.url}friends.get", params={
                    'user_id': self.id_user,
                    'order': 'name',
                    'fields': 'nickname',
                    'access_token': self.token,
                    'v': 5.131
                }).json()
                if 'response' in friends:
                    print('Всего друзей: ', friends['response']['count'])
                    info_friends = friends['response']['items']
                    for friend in info_friends:
                        print('Друг:', friend['last_name'], friend['first_name'], friend['id'])
                else:
                    print('Пользователь не найден')

            elif self.request == 'photo':
                photo = requests.get(f'{self.url}photos.getAlbums', params={
                    'owner_id': self.id_user,
                    'need_system': 1,
                    'access_token': self.token,
                    'v': 5.131
                }).json()
                if 'response' in photo:
                    print('Всего альбомов: ', photo['response']['count'])
                    info_photos = photo['response']['items']
                    for photo in info_photos:
                        size = 'Нет фотографий' if photo['size'] == 0 else photo['size']
                        print('Альбом:', photo['title'])
                        print('Количество фотографий:', size)
                        print()
                else:
                    print('Пользователь не найден')

            elif self.request == 'groups':
                groups = requests.get(f'{self.url}groups.get', params={
                    'user_id': self.id_user,
                    'access_token': self.token,
                    'extended': 1,
                    'v': 5.131
                }).json()
                if 'response' in groups:
                    print('Всего групп:', groups['response']['count'])
                    info_groups = groups['response']['items']
                    for group in info_groups:
                        print('Группа:', group['name'])
                        if group['is_admin']:
                            print('Является админом')
                else:
                    print('Пользователь не найден')
            else:
                print('Введён неправильный запрос')
                print('Введите запрос')
                self.flag_request += 1
                self.request = input()
                if self.flag_request > 3:
                    help()
                    return
                self.collect_data()

        except HTTPError as e:
            print(e)


def main():
    print('Введите id пользователя (цифрами, без id) или --h, -help для справки по использованию программы')
    id_user = input()
    if id_user == '--h' or id_user == '-help':
        help()
        return
    print('Введите интересующий запрос')
    request = input()
    VkApi(id_user, request)


if __name__ == '__main__':
    main()
