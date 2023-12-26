import requests


headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': None,
}

cookies = {'csrftoken': None}
client = requests.session()

def set_csrf_token() -> None:
    res = client.get('http://127.0.0.1:8000/users/token')
    if not res.ok:
        RuntimeError("res is not getting the right csrf")
    csrf_token = res.json()['csrfToken']
    headers['X-CSRFToken'] = csrf_token
    cookies['csrftoken'] = csrf_token


def register(username, email, password) -> None:
    registration_data = dict(username=username, email=email, password=password)
    res = client.post(url='http://127.0.0.1:8000/users/register', json=registration_data, cookies=cookies, headers=headers)
    if not res.ok:
        RuntimeError(f"cannot register: {res.text}")


def login(username, password) -> None:
    user_data = dict(username=username, password=password)
    res = client.post(url='http://127.0.0.1:8000/users/login', json=user_data, cookies=cookies, headers=headers)
    if not res.ok:
        RuntimeError(f"cannot login: {res.text}")


def logout() -> None:
    res = client.post(url='http://127.0.0.1:8000/users/logout', cookies=cookies, headers=headers)
    if not res.ok:
        RuntimeError(f"cannot logout: {res.text}")


def write_message(receiver_id, body, subject) -> int:
    write_message_data = dict(receiver_id=receiver_id, body=body, subject=subject)
    res = client.post(url='http://127.0.0.1:8000/messages/write_message', json=write_message_data, cookies=cookies, headers=headers)
    if not res.ok:
        RuntimeError(f"cannot write_message: {res.text}")
    return res.json()["message_id"]


def read_message(message_id) -> dict:
    read_message_data = {"message_id": message_id}
    res = client.get(url='http://127.0.0.1:8000/messages/read_message', json=read_message_data, headers=headers, cookies=cookies)
    if not res.ok:
        RuntimeError(f"cannot write_message: {res.text}")
    return res.json()


def get_messages_id() -> list:
    res = client.get(url='http://127.0.0.1:8000/messages/messages_per_receiver', headers=headers, cookies=cookies)
    if not res.ok:
        RuntimeError(f"cannot get messages id: {res.text}")
    return res.json()["messages_id"]


def get_unread_messages_id() -> list:
    res = client.get(url='http://127.0.0.1:8000/messages/unread_per_receiver', headers=headers, cookies=cookies)
    if not res.ok:
        RuntimeError(f"cannot get messages id: {res.text}")
    return res.json()["messages_id"]


def delete_message(message_id) -> None:
    delete_message_data = dict(message_id=message_id)
    res = client.delete(url='http://127.0.0.1:8000/messages/delete_message', json=delete_message_data, headers=headers, cookies=cookies)
    if not res.ok:
        RuntimeError(f"cannot get messages id: {res.text}")


if __name__ == '__main__':
    # set csrf
    set_csrf_token()

    # details for this program
    username = 'Noam'
    password = 'MyExamplePass1577@!'
    email = "example@gmail.com"

    # register the user -> ! put this statement in comment after you register !
    register(username=username, password=password, email=email)

    # login this user
    login(username=username, password=password)

    # write here your functions

    # logout
    logout()