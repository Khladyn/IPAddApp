import tkinter as tk
import requests
from tkinter import ttk
from tkinter import scrolledtext
import pyperclip
from tkinter import filedialog
from datetime import datetime

# Create a list to store the history of IP information
ip_history = []

# To store the user-input of manual ip address
manual_ip = ""

# To initialize the response
response = requests.get('https://ipapi.co/json/')
data = response.json()  # Parse the JSON response into a dictionary

def initialize_api_keys():
    
    global api_keys
    api_keys = list(data.keys())  # Extract the keys from the dictionary
    # api_keys = list(response.keys())

initialize_api_keys()

import requests

def fetch_ip_info(ip_address=None):

    print(data)

    try:
        result_text.config(state=tk.NORMAL)  # Enable text widget for editing
        result_text.delete(1.0, tk.END)  # Clear existing text

        if response.status_code == 200:            
            # Extract the desired information
            ipv4 = data.get('ip', 'IPv4 not available')
            ipv6 = data.get('ip6', 'IPv6 not available')
            city = data.get('city', 'City not available')
            region = data.get('region', 'Region not available')
            country = data.get('country', 'Country not available')
            isp = data.get('org', 'ISP information not available')

            # Display the extracted information
            result_text.insert(tk.END, f"Brief IP Information:\n", "blue")
            result_text.insert(
                tk.END,
                f"Public IPv4 Address: {ipv4}\n"
                f"Public IPv6 Address: {ipv6}\n"
                f"City: {city}\n"
                f"Region: {region}\n"
                f"Country: {country}\n"
                f"ISP: {isp}",
                "green"
            )
            
            # Add fetched information to the history list
            ip_history.append(result_text.get(1.0, tk.END))  # Store the text content, not the widget
        else:
            result_text.insert(tk.END, f"Error: Unable to retrieve IP data (Status Code: {response.status_code})", "red")

    except requests.RequestException as e:
        result_text.insert(tk.END, f"Error: {e}", "red")

    result_text.config(state=tk.DISABLED)  # Disable text widget for editing

def fetch_selected_key_info(selected_key):

    if selected_key in data:
        result = f"{selected_key.capitalize()}: {data[selected_key]}"
    else:
        result = "Key not found"

    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)  # Disable text widget for editing

    # Add fetched information to the history list
    ip_history.append(result_text.get(1.0, tk.END))  # Store the text content, not the widget

def display_additional_info():
    
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear existing text

    try:
        if response.status_code == 200:
            additional_info = "\n".join([f"{key.capitalize()}: {value}" for key, value in data.items()])
            result_text.insert(tk.END, f"Additional IP Information:\n{additional_info}", "blue")

        else:
            result_text.insert(tk.END, f"Error: Unable to fetch additional details (Status Code: {response.status_code})", "red")

        # Add fetched information to the history list
        ip_history.append(result_text.get(1.0, tk.END))  # Store the text content, not the widget

    except requests.RequestException as e:
        result_text.insert(tk.END, f"Error: {e}", "red")
    
    result_text.config(state=tk.DISABLED)  # Disable text widget for editing

def clear_result():
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.config(state=tk.DISABLED)  # Disable text widget for editing

def refresh_info():
    
    # Check if additional info is currently displayed
    current_text = result_text.get(1.0, tk.END)
    if "Additional IP Information" in current_text:
        display_additional_info()  # If additional info is displayed, refresh from display_additional_info
    elif "Brief IP Information" in current_text:
        fetch_ip_info()  # Otherwise, refresh from fetch_ip_info

def copy_to_clipboard():
    # Get the current text from the result_text widget
    text_to_copy = result_text.get(1.0, tk.END)
    
    # Copy the text to the clipboard
    pyperclip.copy(text_to_copy)

def save_ip_info():
    # Get the current text from the result_text widget
    text_to_save = result_text.get(1.0, tk.END)

    # Open a file dialog for saving the text as a file with the default name
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile="MyIPInfo.txt"  # Set the default file name
    )

    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(text_to_save)
            print(f"IP information saved to {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

def history_info():
    # Create a new window for displaying history
    history_window = tk.Toplevel()
    history_window.title("History")
    
    # Create a text widget for displaying history
    history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, font=("Helvetica", 12))
    history_text.pack(fill=tk.BOTH, expand=True)
    
    # Insert the history entries into the text widget
    for entry in ip_history:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
        history_text.insert(tk.END, f"{timestamp} \n\n{entry}\n\n")  # Concatenate entry with newline
    
    # Disable editing in the history text widget
    history_text.config(state=tk.DISABLED)

def manually_assign_ip():
    global manual_ip  # Access the global manual_ip variable

    new_window = tk.Toplevel(window)
    new_window.title("Manually Assign IP Address")

    # Position the child window within the bounds of the parent window
    x = window.winfo_x() + (window.winfo_width() - new_window.winfo_reqwidth()) // 2
    y = window.winfo_y() + (window.winfo_height() - new_window.winfo_reqheight()) // 2
    new_window.geometry(f"+{x}+{y}")

    manual_ip_frame = ttk.Frame(new_window)
    manual_ip_frame.pack(pady=10, padx=(20, 10), anchor=tk.W)

    manual_ip_label = tk.Label(manual_ip_frame, text="Manually Assign IP Address:")
    manual_ip_label.pack(side=tk.LEFT)

    manual_ip_entry = tk.Entry(manual_ip_frame, width=15)
    manual_ip_entry.pack(side=tk.LEFT)

    if manual_ip:
        manual_ip_entry.insert(0, manual_ip)  # Set the entry field value

    def assign_manual_ip():
        # Access the global variables
        global manual_ip
        global response
        global data

        manual_ip = manual_ip_entry.get()  # Update the global variable with the new value
        response = requests.get(f'https://ipapi.co/{manual_ip}/json/')
        data = response.json()
        new_window.destroy()  # Close the window
        print(f"From assign_manual: {manual_ip}")

    manual_ip_button = tk.Button(manual_ip_frame, text="Assign", command=assign_manual_ip)
    manual_ip_button.pack(side=tk.LEFT)

    print(manual_ip)
        
# GUI Components
window = tk.Tk()
window.title("JACKS: Network Information")
window.geometry("720x480")

frame = tk.Frame(window)
frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)

# Buttons
button_frame = tk.Frame(frame)
button_frame.pack(pady=10, padx=(20, 10), anchor=tk.W)

button_labels = [
    "Fetch IP Information",
    "Manually Assign IP Address",
    "Clear Result",
    "Copy to Clipboard",
    "Refresh Button",
    "Save IP Information",
    "History",
    "Display Additional Info",  # Updated label
]

for label in button_labels:
    button = tk.Button(button_frame, text=label, width=30)
    if label == "Fetch IP Information":
        button.config(command=fetch_ip_info)
    elif label == "Clear Result":
        button.config(command=clear_result)
    elif label == "Copy to Clipboard":
        button.config(command=copy_to_clipboard)
    elif label == "Refresh Button":
        button.config(command=refresh_info)
    elif label == "Save IP Information":
        button.config(command=save_ip_info)  # Added command for Save IP Information button
    elif label == "Display Additional Info":
        button.config(command=display_additional_info)
    elif label == "History":
        button.config(command=history_info)  # Call history_info function
    elif label == "Manually Assign IP Address":
        button.config(command=manually_assign_ip)
    button.pack(pady=5, anchor=tk.W)

# Create a label above the dropdown
label_frame = ttk.Frame(frame)
label_frame.pack(pady=10, padx=(20, 10), anchor=tk.W)

label = tk.Label(button_frame, text="Only show:")
label.pack(side=tk.TOP, anchor=tk.W)

# Create a dropdown menu for selecting the API key
api_key_var = tk.StringVar()
api_key_var.set(api_keys[0])  # Set the initial value to an empty string
api_key_dropdown = ttk.Combobox(button_frame, textvariable=api_key_var, values=api_keys, width=33)
api_key_dropdown.pack(pady=5, anchor=tk.W)

# Bind the <<ComboboxSelected>> event to the function
api_key_dropdown.bind("<<ComboboxSelected>>",  lambda event, key_var=api_key_var: fetch_selected_key_info(api_key_var.get()))

# Result Panel
result_frame = ttk.Frame(window, padding=10, relief="ridge")
result_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=("Helvetica", 12), state=tk.DISABLED)
result_text.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(window, text="JACKS: Network Information", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, pady=(35, 0), columnspan=2, sticky="nsew")

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()
