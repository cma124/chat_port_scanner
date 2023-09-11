import os
import ttkbootstrap as ttk
import client
import server
import single_port
import multi_port
import banner_port

PRIMARY_FONT = "Helvetica"

def executeServer(parent_frame):
    ttk.dialogs.dialogs.Messagebox.show_info("Server is Running", "Server", parent=parent_frame)
    os.system('python server.py')


def chooseClientServer(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=33)

    label = ttk.Label(inner_frame, text="LAN Chat", font=(PRIMARY_FONT, 32))

    client_btn = ttk.Button(inner_frame, text="Client Mode", bootstyle="INFO", width=25, command=lambda: client.chatClient(right_frame))
    server_btn = ttk.Button(inner_frame, text="Server Mode", bootstyle="INFO", width=25, command=lambda: server.runServer(right_frame))

    label.pack(pady=12)
    client_btn.pack(pady=25)
    server_btn.pack(pady=25)


def chooseScanner(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=33)

    label = ttk.Label(inner_frame, text="Port Scanners", font=(PRIMARY_FONT, 32))

    singleport_btn = ttk.Button(inner_frame, text="Single Host and Single Port", bootstyle="INFO", width=42, command=lambda: single_port.scanSingle(right_frame))
    multiport_btn = ttk.Button(inner_frame, text="Single Host and Multiple Ports", bootstyle="INFO", width=42, command=lambda: multi_port.scanMultiple(right_frame))
    banner_btn = ttk.Button(inner_frame, text="Banner from Open Port of a Specific Host", bootstyle="INFO", width=42, command=lambda: banner_port.scanBanner(right_frame)) 

    label.pack(pady=12)
    singleport_btn.pack(pady=25)
    multiport_btn.pack(pady=25)
    banner_btn.pack(pady=25)
