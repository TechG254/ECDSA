#imports
from socket import*

Host = '127.0.0.1'
Port = 8080
Buffer_size = 1024


def start_server():
    """create, bind and start the server socket"""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((Host, Port))
    server_socket.listen(1)
    print(f"listening at http://{Host}:{Port}/")
    return server_socket

#handle client request

def handle_client(connection_socket):
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