import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))
    print("Connected to server.")
    print("Enter command (UPPER/LOWER/REVERSE/COUNT/VOWELS/TIME/DATE/QUIT):")

    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue

        client_socket.send(cmd.encode())

        if cmd.upper() == "QUIT":
            print("Connection closed.")
            break

        response = client_socket.recv(1024).decode()
        print(f"Response from server: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()
