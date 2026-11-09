import socket

HOST = '127.0.0.1'
PORT = 9999

def start_notification_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[Notification Server] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[Connected] {addr}")

        message = conn.recv(1024).decode()
        print(f"[Notification Received]: {message}")

        conn.close()

if __name__ == "__main__":
    start_notification_server()
