"""
TCP-сервер: сторона клиента
"""

import socket


def run_client() -> None:
    """
    Запускает клиент для общения с сервером
    """

    server_ip = input('Введите IP-адрес сервера: ')
    server_port = int(input('Введите порт сервера: '))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_:
        try:
            socket_.connect((server_ip, server_port)) # Подключаемся к серверу по IP-адресу и порту
            print(f'Успешно подключились к серверу {server_ip}:{server_port}')

            while True:
                message = input('Введите сообщение для сервера (или "exit" для отключения): ')

                if message.lower() == 'exit':
                    break

                socket_.sendall(message.encode('utf-8'))
                response = socket_.recv(2048)
                response = response.decode('utf-8').strip()
                print(f'Ответ сервера: {response}')

        except ConnectionRefusedError:
            print(f'Не удалось подключиться к серверу {server_ip}:{server_port}. Проверьте, запущен ли сервер, или корректность ip-адреса и порта')
        except Exception as _:
            print(f'Произошла ошибка: {_}')


if __name__ == '__main__':
    run_client()
