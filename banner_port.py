import socket
import ttkbootstrap as ttk
import menus

PRIMARY_FONT = "Helvetica"

def scanBanner(right_frame):
    # Clear the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    inner_frame = ttk.Frame(right_frame)
    inner_frame.pack(pady=20)

    label = ttk.Label(inner_frame, text="Banner from Open Port of a Specific Host", font=(PRIMARY_FONT, 20))
    label.grid(row=0, column=0, columnspan=4, pady=25)

    address_label = ttk.Label(inner_frame, text="IP Address", font=(PRIMARY_FONT, 16))
    address_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=26)
    address_label.grid(row=1, column=1, padx=5, pady=20, sticky="e")
    address_entry.grid(row=1, column=2, padx=4, sticky="w")

    port_label = ttk.Label(inner_frame, text="Port Number", font=(PRIMARY_FONT, 16))
    port_entry = ttk.Entry(inner_frame, font=(PRIMARY_FONT, 16), bootstyle="INFO", width=26)
    port_label.grid(row=2, column=1, padx=5, pady=20, sticky="e")
    port_entry.grid(row=2, column=2, padx=4, sticky="w")

    btn_frame = ttk.Frame(inner_frame)
    btn_frame.grid(row=3, column=2, pady=30)
    
    scan_btn = ttk.Button(btn_frame, text="Scan", bootstyle="SUCCESS", width=7, command=lambda: banner(address_entry, port_entry, message_box, label))
    back_btn = ttk.Button(btn_frame, text="Back", bootstyle="WARNING", width=8, command=lambda: menus.chooseScanner(right_frame))
    scan_btn.grid(row=0, column=0, padx=20)
    back_btn.grid(row=0, column=1)

    message_box = ttk.dialogs.dialogs.Messagebox


def banner(address_entry, port_entry, message_box, parent_frame):
    address = address_entry.get().strip()
    port = port_entry.get().strip()

    if address != '' and port != '':
        port = int(port)
        
        try:
            sock = socket.socket()
            sock.connect((address, port))

            try:
                banner = sock.recv(1024)
                message_box.show_info(banner, 'Banner Result', parent=parent_frame)

            except:
                message_box.show_error('Cannot retrieve banner !', 'Banner Error', parent=parent_frame)
                
        except:
            message_box.show_error('Cannot make connection !', 'Banner Error', parent=parent_frame)

        sock.close()
    
    else:
        message_box.show_warning('Invalid IP Address or Port Number !', 'Invalid Input', parent=parent_frame)
