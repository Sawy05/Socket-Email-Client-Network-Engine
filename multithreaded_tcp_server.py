import socket
import threading
import time
from datetime import datetime

client_counter = 0


def handle_client(client_socket, client_address, client_name):
    print(f"{client_name} connected from {client_address[0]}:{client_address[1]}")

    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            # Parse command
            if ":" in data:
                command, message = data.split(":", 1)
                command = command.strip().upper()
                message = message.strip()
            else:
                command = data.upper()
                message = ""

            # Execute operations
            if command == "UPPER":
                result = message.upper()
            elif command == "LOWER":
                result = message.lower()
            elif command == "REVERSE":
                result = message[::-1]
            elif command == "COUNT":
                result = str(len(message))
            elif command == "VOWELS":
                vowels = "aeiouAEIOU"
                result = str(sum(1 for c in message if c in vowels))
            elif command == "TIME":
                # 12-hour format with AM/PM
                result = time.strftime("%I:%M:%S %p")
            elif command == "DATE":
                result = datetime.now().strftime("%Y-%m-%d")
            elif command == "QUIT":
                print(f"{client_name} disconnected.")
                client_socket.send("Connection closed".encode())
                break
            else:
                result = "ERROR: Unknown command"

            # Print EXACT format required
            print(f"{client_name} sent: {data} → {result}")

            client_socket.send(result.encode())

        except Exception:
            break

    client_socket.close()


def main():
    global client_counter

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)

    print("Server started on port 5000")

    while True:
        client_socket, client_address = server.accept()
        client_counter += 1
        client_name = f"Client{client_counter}"

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, client_name),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
