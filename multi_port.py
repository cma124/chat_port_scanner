import socket
import ttkbootstrap as ttk
import menus

PRIMARY_FONT = "Helvetica"

def scanMultiple(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=20)

    label = ttk.Label(inner_frame, text="     Single Host and Multiple Port     ", font=(PRIMARY_FONT, 20))
    label.grid(row=0, column=0, columnspan=4, pady=25)

    address_label = ttk.Label(inner_frame, text="IP Address", font=(PRIMARY_FONT, 16))
    address_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=26)
    address_label.grid(row=1, column=1, padx=5, pady=20, sticky="e")
    address_entry.grid(row=1, column=2, padx=4, sticky="w")

    start_port_label = ttk.Label(inner_frame, text="Start Port", font=(PRIMARY_FONT, 16))
    start_port_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=26)
    start_port_label.grid(row=2, column=1, padx=5, pady=20, sticky="e")
    start_port_entry.grid(row=2, column=2, padx=4, sticky="w")

    end_port_label = ttk.Label(inner_frame, text="End Port", font=(PRIMARY_FONT, 16))
    end_port_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=26)
    end_port_label.grid(row=3, column=1, padx=5, pady=20, sticky="e")
    end_port_entry.grid(row=3, column=2, padx=4, sticky="w")

    btn_frame = ttk.Frame(inner_frame)
    btn_frame.grid(row=4, column=2, pady=30)
    
    scan_btn = ttk.Button(btn_frame, text="Scan", bootstyle="SUCCESS", width=7, command=lambda: scan(address_entry, start_port_entry, end_port_entry, message_box, label))
    back_btn = ttk.Button(btn_frame, text="Back", bootstyle="WARNING", width=8, command=lambda: menus.chooseScanner(right_frame))
    scan_btn.grid(row=0, column=0, padx=20)
    back_btn.grid(row=0, column=1)

    message_box = ttk.dialogs.dialogs.Messagebox


def scan(address_entry, start_port_entry, end_port_entry, message_box, parent_frame):
    address = address_entry.get().strip()
    start_port = start_port_entry.get().strip()
    end_port = end_port_entry.get().strip()

    if address != '' and start_port != '' and end_port != '':
        results = ''
        start_port = int(start_port)
        end_port = int(end_port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for port in range(start_port, end_port + 1):
            if sock.connect_ex((address,port)):
                results += f'Port {port} is closed in host {address}\n'

            else :
                results += f'Port {port} is opened in host {address}\n'

        message_box.show_info(results, 'Scan Result', parent=parent_frame)
        sock.close()

    else:
        message_box.show_warning('Invalid IP Address or Port Numbers !', 'Invalid Input', parent=parent_frame)
