from socket import *


HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024


def start_server():
    """Create, bind, and start the server socket."""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server running at http://{HOST}:{PORT}/")
    return server_socket


def handle_client(connection_socket):
    """Handle a single client request."""
    try:
        request = receive_request(connection_socket)
        filename = parse_request(request)
        content = read_file(filename)
        response = build_response(200, content)
    except FileNotFoundError:
        response = build_404_response()
    except Exception as e:
        print("Server error:", e)
        response = build_500_response()

    connection_socket.sendall(response)
    connection_socket.close()


def receive_request(connection_socket):
    """Receive HTTP request from the client."""
    request = connection_socket.recv(BUFFER_SIZE).decode()
    print("HTTP Request:")
    print(request)
    return request


def parse_request(request):
    """Extract requested filename from HTTP request."""
    request_line = request.splitlines()[0]
    filename = request_line.split()[1]

    if filename == '/':
        filename = '/index.html'

    return filename[1:]  # remove leading '/'


def read_file(filename):
    """Read requested file from disk."""
    with open(filename, 'rb') as file:
        return file.read()


def build_response(status_code, content):
    """Build HTTP response message."""
    if status_code == 200:
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
        )
        return header.encode() + content


def build_404_response():
    """Build 404 Not Found response."""
    body = "<html><body><h1>404 Not Found</h1></body></html>"
    header = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    )
    return header.encode() + body.encode()


def build_500_response():
    """Build 500 Internal Server Error response."""
    body = "<html><body><h1>500 Internal Server Error</h1></body></html>"
    header = (
        "HTTP/1.1 500 Internal Server Error\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    )
    return header.encode() + body.encode()


def main():
    server_socket = start_server()

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        handle_client(connection_socket)


if __name__ == "__main__":
    main()
