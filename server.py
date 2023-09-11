import socket
import threading
import ttkbootstrap as ttk

PRIMARY_FONT = "Helvetica"

HOST = ''
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users
server_status = True

server_thread = None

def runServer(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=20)

    label = ttk.Label(inner_frame, text="Server Mode", font=(PRIMARY_FONT, 20))
    label.grid(row=0, column=0, columnspan=2, pady=25)

    start_btn = ttk.Button(inner_frame, text="Start", bootstyle="SUCCESS", width=10, command=lambda: main())
    stop_btn = ttk.Button(inner_frame, text="Stop", bootstyle="WARNING", width=10, command=lambda: stop_server(label))
    start_btn.grid(row=1, column=0, padx=10, pady=30)
    stop_btn.grid(row=1, column=1, padx=10)

    # Function to listen for upcoming messages from a client
    def listen_for_messages(client, username):
        while server_status:

            message = client.recv(2048).decode('utf-8')
            if message != '':
                
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)

            else:
                print(f"The message send from client {username} is empty")


    # Function to send message to a single client
    def send_message_to_client(client, message):

        client.sendall(message.encode())


    # Function to send any new message to all the clients that
    # are currently connected to this server
    def send_messages_to_all(message):
        
        for user in active_clients:

            send_message_to_client(user[1], message)


    # Function to handle client
    def client_handler(client):
        
        # Server will listen for client message that will
        # Contain the username
        while server_status:

            try: 
                username = client.recv(2048).decode('utf-8')
                if username != '':
                    active_clients.append((username, client))
                    prompt_message = "SERVER~" + f"{username} added to the chat"
                    send_messages_to_all(prompt_message)
                    listen_for_messages(client, username)
                    break
                else:
                    print("Client username is empty")

            except:
                    active_clients.remove(client)
                    client.close()
                    break

        threading.Thread(target=listen_for_messages, args=(client, username, )).start()


    # Main function
    def main():
        global server_thread

        # Getting Local IP Address
        # local_ip = get_local_ip()
        local_ip = "172.20.2.53"
        HOST = local_ip
        print(f"Local IP Address: {local_ip}")
        # Creating the socket class object
        # AF_INET: we are going to use IPv4 addresses
        # SOCK_STREAM: we are using TCP packets for communication
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Creating a try catch block
        try:
            # Provide the server with an address in the form of
            # host IP and port
            server.bind((HOST, PORT))
            print(f"Running the server on {HOST} {PORT}")
        except:
            print(f"Unable to bind to host {HOST} and port {PORT}")

        # Set server limit
        server.listen(LISTENER_LIMIT)

        # This while loop will keep listening to client connections
        while server_status:

            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")

            server_thread = threading.Thread(target=client_handler, args=(client, ))
            server_thread.start()


    def stop_server(parent_frame): 
        global server_status
        
        if len(active_clients) != 0:
            server_status = False

        else: 
            ttk.dialogs.dialogs.Messagebox.show_warning("Unable to stop ! Users are online", "Server Warning", parent=parent_frame)


    def get_local_ip():
        # Get the local IP address of the machine
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip



# if __name__ == '__main__':
#     main()