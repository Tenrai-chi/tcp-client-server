"""
TCP-сервер: сторона сервера
"""

import socket
import threading


def get_local_ip() -> str:
    """
    Определяет локальный IP-адрес в локальной сети машины-сервера
    Можно было использовать ipconfig, но метод с подключением ко внешнему серверу проще
    """

    try:
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Используем не TCP, чтобы узнать свой ip
        socket_.connect(('77.88.8.8', 80))  # Используем внешний DNS-сервер для подключения (яндекс)
        local_ip = socket_.getsockname()[0]  # Берем из сокета ip
        return local_ip
    except Exception as _:
        print(f'Ошибка при определении локального IP: {_}')
        raise SystemExit('Не удалось определить локальный IP. Сервер не может быть запущен')


def get_free_port() -> int:
    """
    Находит свободный порт на машине-сервере
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_:  # Не могли взять порт при определении ip, так как соединение разное
        socket_.bind(('', 0))
        port = socket_.getsockname()[1]  # Берем из сокета порт
        return port


def handle_connection(connection: socket.socket, address: tuple[str, int]) -> None:
    """
    Обработка соединения с клиентом
    """

    print(f'Подключился клиент: {address}')
    try:
        while True:
            data = connection.recv(2048)
            if not data:
                break
            message = data.decode('utf-8').strip()
            print(f'{address}: {message}')

            response = input('Ответ клиенту: ')
            connection.sendall(response.encode('utf-8'))

    except Exception as _:
        print(f'Ошибка в обработке клиента {address}: {_}')
    finally:
        connection.close()
        print(f'Клиент {address} отключился')


def run_server() -> None:
    """
    Общая логика работы сервера: запуск, соединение и обработка сообщений
    """

    local_ip = get_local_ip()
    port = get_free_port()
    print(f'Сервер запущен на {local_ip}:{port}\nВведите IP и port на клиенте для связи')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_:
        socket_.bind((local_ip, port))
        socket_.listen()
        while True:  # Бесконечный цикл для приема входящих соединений
            connection, address = socket_.accept()
            # Создаем новый поток для обработки соединения с клиентом
            client_thread = threading.Thread(target=handle_connection, args=(connection, address))
            client_thread.start()


if __name__ == '__main__':
    run_server()
