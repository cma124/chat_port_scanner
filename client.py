import socket
import threading
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

    # hostIP_label = ttk.Label(inner_frame, text="Host IP", font=(PRIMARY_FONT, 16), bootstyle="INFO")
    # hostIP_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=36)
    # hostIP_label.grid(row=1, column=0, padx=8, pady=10)
    # hostIP_entry.grid(row=1, column=1, pady=10)

    user_label = ttk.Label(inner_frame, text="User Name", font=(PRIMARY_FONT, 16))
    user_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=36)
    join_btn = ttk.Button(inner_frame, text="Join", bootstyle="INFO", width=9, command=lambda: connectToServer())
    user_label.grid(row=1, column=0, pady=15)
    user_entry.grid(row=1, column=1, padx=8)
    join_btn.grid(row=1, column=2, padx=10)

    message_area = ttk.ScrolledText(inner_frame, font=("Arial", 12),  width=57, height=20)
    message_area.grid(row=2, column=0, columnspan=3, pady=20)    
    message_area.config(state=ttk.DISABLED)

    message_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="SUCCESS", width=58)
    message_entry.grid(row=3, column=0, columnspan=3)
    
    send_btn = ttk.Button(inner_frame, text="Send", bootstyle="SUCCESS", width=9, command=lambda: sendMessage())
    exit_btn = ttk.Button(inner_frame, text="Exit", bootstyle="WARNING", width=9)
    send_btn.grid(row=4, column=1, padx=7, pady=20, sticky="e")
    exit_btn.grid(row=4, column=2)

    message_box = ttk.dialogs.dialogs.Messagebox
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToServer():
        username = user_entry.get().strip()

        if username != '':
            try:
                user_entry.config(state=ttk.DISABLED)
                join_btn.config(state=ttk.DISABLED)

                client_socket.connect((HOST, PORT))
                client_socket.sendall(username.encode())
                threading.Thread(target=listenFromServer, args=(client_socket, )).start()
                
                global connected_status
                connected_status = True

                print("Successfully connected to server")
                message_area.config(state=ttk.NORMAL)
                message_area.insert(ttk.END, "[SERVER] Successfully connected to the server" + '\n')
                message_area.config(state=ttk.DISABLED)

            except:
                message_box.show_error("Unable to connect to server !", "Connection Error", parent=user_entry)
                user_entry.config(state=ttk.ENABLED)
                join_btn.config(state=ttk.ENABLED)

        else:
            message_box.show_warning("User name cannot be empty !", "Invalid Input", parent=user_entry)

    def sendMessage():
        message = message_entry.get()

        if connected_status:
            if message != '':
                client_socket.sendall(message.encode())

            else:
                message_box.show_warning("Message cannot be empty !", "Invalid Input", parent=user_entry)
        
        else:
            message_box.show_warning("Join to the server first !", "Warning", parent=user_entry)

        message_entry.delete(0, len(message))

    def listenFromServer(client_socket):
        while 1:
            message = client_socket.recv(2048).decode('utf-8')

            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                message_area.config(state=ttk.NORMAL)
                message_area.insert(ttk.END, f"[{username}] {content}" + '\n')
                message_area.config(state=ttk.DISABLED)

            else:
                message_box.show_warning("Message recevied from client is empty !", "Warning", parent=user_entry)