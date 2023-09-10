import ttkbootstrap as ttk
import menus
import client

PRIMARY_FONT = "Helvetica"

# Create the main window
root = ttk.Window(title="LAN Chat and Port Scanner", themename="solar", size=(900, 600), resizable=(False, False), iconphoto="icon.png")
root.place_window_center()

# For all buttons
my_style = ttk.Style()
my_style.configure("TButton", font=(PRIMARY_FONT, 16))

# Create a left frame for the side menu
left_frame = ttk.Frame(root, bootstyle="DARK")
left_frame.pack(side="left", fill="y")

# Create a right frame for the content
right_frame = ttk.Frame(root)
right_frame.pack(fill="both", expand=True, padx=8)

# Create buttons in the side menu
chat_menu_btn = ttk.Button(left_frame, text="LAN Chat", bootstyle="SUCCESS", width=13, command=lambda: menus.chooseClientServer(right_frame))
scanner_menu_btn = ttk.Button(left_frame, text="Port Scanners", bootstyle="SUCCESS", width=13, command=lambda: menus.chooseScanner(right_frame))

chat_menu_btn.pack(padx=30, pady=47)
scanner_menu_btn.pack(padx=30)

# Initially page for right frame
inner_frame = ttk.Frame(right_frame)
inner_frame.pack(pady=33)

label = ttk.Label(inner_frame, text="LAN Chat", font=(PRIMARY_FONT, 32))

client_btn = ttk.Button(inner_frame, text="Client Mode", bootstyle="INFO", width=25, command=lambda: client.chatClient(right_frame))
server_btn = ttk.Button(inner_frame, text="Server Mode", bootstyle="INFO", width=25, command=lambda: menus.executeServer(inner_frame))

label.pack(pady=12)
client_btn.pack(pady=25)
server_btn.pack(pady=25)

# Start the Tkinter main loop
root.mainloop()