import socket
import threading
import ttkbootstrap as ttk

PRIMARY_FONT = "Helvetica"

HOST = ''
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 30
active_clients = [] # List of all currently connected users

# initial_server = True
server_status = False
server_thread = None
server_socket = None

def runServer(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=20)

    label = ttk.Label(inner_frame, text="Server Mode", font=(PRIMARY_FONT, 20))
    label.grid(row=0, column=0, columnspan=2, pady=25)

    start_btn = ttk.Button(inner_frame, text="Start", bootstyle="SUCCESS", width=10, command=lambda: start_server(label))
    stop_btn = ttk.Button(inner_frame, text="Stop", bootstyle="WARNING", width=10, command=lambda: stop_server(label))
    start_btn.grid(row=1, column=0, padx=10, pady=30)
    stop_btn.grid(row=1, column=1, padx=10)

    message_box = ttk.dialogs.dialogs.Messagebox


    def start_server(parent_frame):
        # global initial_server
        global server_status
        global server_thread
        global server_socket

        try:
            if server_thread is None or not server_thread.is_alive():
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Getting Server IP Address
                # server_ip = get_local_ip()
                server_ip = "127.0.1.1"
                HOST = server_ip
                print(f"Server IP Address: {server_ip}")

                try:
                    server_socket.bind((HOST, PORT))
                    print(f"Running the server on {HOST} {PORT}")

                except:
                    print(f"Unable to bind to host {HOST} and port {PORT}")
                    
                # Set server limit
                server_socket.listen(LISTENER_LIMIT)

                server_status = True

                server_thread = threading.Thread(target=accept_connections)
                server_thread.start()

                # initial_server = False
                print("Server has started successfully")

        except:
            # initial_server = True
            message_box.show_error("Unable to connect to server !", "Connection Error", parent=parent_frame)


    def stop_server(parent_frame): 
        global active_clients
        global server_status
        global server_thread
        global server_socket
        
        if len(active_clients) == 0 and server_socket and not server_thread.is_alive():
            server_status = False

            server_socket.close()
            server_socket = None
            # server_thread.join()

            print("Server has stopped successfully")
            message_box.show_info("Server has stopped successfully", "Server Success", parent=parent_frame)

        else: 
            message_box.show_warning("Unable to stop ! Users are online", "Server Warning", parent=parent_frame)


    # Function to send message to a single client
    def send_message_to_client(client, message):

        client.sendall(message.encode()) 


    # Function to send any new message to all the clients that
    # are currently connected to this server
    def send_messages_to_all(message):
        global active_clients
        
        for user in active_clients:

            send_message_to_client(user[0], message)


    # Function to listen for upcoming messages from a client
    def listen_for_messages(client, address, username):
        global active_clients

        while server_status:
            try:
                message = client.recv(2048).decode('utf-8')

                if (not message):
                    message = ''
                    break

                if message == 'LEAVE':
                    # Remove the leaving client from the list of active clients
                    try:    
                        active_clients.remove((client, address, username))

                        # Close the client socket
                        client.close()

                        # Notify other clients that this user is leaving
                        leave_message = "SERVER~" + f"{username} on {address[0]} has left the chat"
                        send_messages_to_all(leave_message)
                        
                    except:
                        print("Error removing client from active list")

                    break

                if message != '':                    
                    final_msg = username + '~' + message
                    send_messages_to_all(final_msg)

                else:
                    print(f"The message send from client {username} is empty")
                    break

            except ConnectionResetError:
                # Handle the case where the client disconnects abruptly
                # Remove the client from the list of active clients
                active_clients.remove((client, address, username))

                # Close the client socket
                client.close()
                break


    # Function to handle client
    def client_handler(client, address):
        global active_clients
        
        # Server will listen for client message that will
        # Contain the username
        while server_status:
            try: 
                username = client.recv(2048).decode('utf-8')

                if username != '':
                    active_clients.append((client, address, username))
                    prompt_message = "SERVER~" + f"{username} has joined the chat"
                    send_messages_to_all(prompt_message)
                    # listen_for_messages(client, username)
                    break

                else:
                    print("Client username is empty")

            except:
                    active_clients.remove((client, address, username))
                    client.close()
                    break

        threading.Thread(target=listen_for_messages, args=(client, address, username, )).start()


    def accept_connections():

        # This while loop will keep listening to client connections
        while server_status:

            try:
                client, address = server_socket.accept()
                print(f"Successfully connected to client {address[0]} {address[1]}")

                threading.Thread(target=client_handler, args=(client, address, )).start()
            
            except:
                pass


    def get_local_ip():
        # Get the local IP address of the machine
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    # if not server_thread is None:
    #     server_thread.join()