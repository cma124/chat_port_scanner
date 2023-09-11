import socket
import threading
import datetime
import ttkbootstrap as ttk

HOST = '127.0.1.1'
PORT = 1234
connected_status = False

PRIMARY_FONT = "Helvetica"

def chatClient(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=10)

    label = ttk.Label(inner_frame, text="Client Mode", font=(PRIMARY_FONT, 20))
    label.grid(row=0, column=0, columnspan=3, pady=10)

    hostIP_label = ttk.Label(inner_frame, text="Host IP", font=(PRIMARY_FONT, 16))
    hostIP_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=36)
    hostIP_label.grid(row=1, column=0, padx=8, pady=25)
    hostIP_entry.grid(row=1, column=1, pady=10)

    user_label = ttk.Label(inner_frame, text="User Name", font=(PRIMARY_FONT, 16))
    user_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=36)
    # user_entry.bind("<Return>", lambda: connectToServer())
    join_btn = ttk.Button(inner_frame, text="Join", bootstyle="INFO", width=9, command=lambda: connectToServer())
    user_label.grid(row=2, column=0, pady=15)
    user_entry.grid(row=2, column=1, padx=8)
    join_btn.grid(row=2, column=2, padx=10)

    message_area = ttk.ScrolledText(inner_frame, font=("Arial", 12),  width=57, height=20)
    message_area.grid(row=3, column=0, columnspan=3, pady=20)    
    message_area.config(state=ttk.DISABLED)

    message_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="SUCCESS", width=58)
    # message_entry.bind("<Return>", lambda: sendMessage)
    message_entry.grid(row=4, column=0, columnspan=3)
    
    send_btn = ttk.Button(inner_frame, text="Send", bootstyle="SUCCESS", width=9, command=lambda: sendMessage())
    leave_btn = ttk.Button(inner_frame, text="Leave", bootstyle="WARNING", width=9, command=lambda: leaveChat())
    send_btn.grid(row=5, column=1, padx=7, pady=20, sticky="e")
    leave_btn.grid(row=5, column=2)

    message_box = ttk.dialogs.dialogs.Messagebox
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def addMessage(message):
        message_area.config(state = ttk.NORMAL)
        message_area.insert(ttk.END, message + '\n')
        message_area.config(state = ttk.DISABLED)


    def clearMessages():
        message_area.config(state = ttk.NORMAL)
        message_area.delete(1.0, ttk.END)  # Delete from the start (1.0) to the end (ttk.END)
        message_area.config(state = ttk.DISABLED)


    def connectToServer():
        global HOST

        username = user_entry.get().strip()
        HOST = hostIP_entry.get().strip()

        if username != '' and HOST != '':
            try:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(username.encode())
                threading.Thread(target=listen_for_messages_from_server, args=(client_socket, )).start()
                
                global connected_status
                connected_status = True

                print("Successfully connected to server")
                addMessage("[SERVER] Successfully connected to the server")

                hostIP_entry.config(state = ttk.DISABLED)
                user_entry.config(state = ttk.DISABLED)
                join_btn.config(state = ttk.DISABLED)

            except:
                message_box.show_error("Unable to connect to server !", "Connection Error", parent=hostIP_entry)
                hostIP_entry.config(state = ttk.ENABLED)
                user_entry.config(state = ttk.ENABLED)
                join_btn.config(state = ttk.ENABLED)

        else:
            message_box.show_warning("Inputs cannot be empty !", "Invalid Input", parent=hostIP_entry)


    def sendMessage():
        if connected_status:
            message = message_entry.get()

            if message != '':
                client_socket.sendall(message.encode())

            else:
                message_box.show_warning("Message cannot be empty !", "Invalid Input", parent=hostIP_entry)

            message_entry.delete(0, len(message))
        
        else:
            message_box.show_warning("Join to the server first !", "Warning", parent=hostIP_entry)

    
    def listen_for_messages_from_server(client_socket):
        try:
            while 1:
                time = datetime.datetime.now().time()
                message = client_socket.recv(2048).decode('utf-8')

                if not message:
                    break  # Server closed the connection gracefully

                if message != '':
                    username = message.split("~")[0]
                    content = message.split('~')[1]

                    addMessage(f"[{time.hour}:{time.minute}:{time.second}][{username}] {content}")

                else:
                    message_box.show_warning("Message recevied from client is empty !", "Warning", parent=hostIP_entry)
                    
        except ConnectionAbortedError:
            # Handle the case where the connection is abruptly closed by the server
            print("Connection to the server was abruptly closed.")

        except Exception as e:
            print(f"Error: {str(e)}")

        finally:
            # Close the client socket when the thread exits
            client_socket.close()


    def leaveChat():
        if connected_status:
            client_socket.sendall("LEAVE".encode('utf-8'))
            
            # Close the client_socket
            client_socket.close()
            
            # Update the GUI to indicate that the user is leaving
            addMessage("[SERVER] You have left the chat")

            hostIP_entry.config(state = ttk.NORMAL)
            hostIP_entry.delete(0, len(hostIP_entry.get()))

            user_entry.config(state = ttk.NORMAL)
            user_entry.delete(0, len(user_entry.get()))

            join_btn.config(state = ttk.NORMAL)
            
            clearMessages()
        
        else:
            message_box.show_warning("Cannot leave from chat !", "Warning", parent=hostIP_entry)


    def listenFromServer(client_socket):
        while 1:
            message = client_socket.recv(2048).decode('utf-8')

            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]
                addMessage(f"[{username}] {content}")

            else:
                message_box.show_warning("Message recevied from client is empty !", "Warning", parent=hostIP_entry)