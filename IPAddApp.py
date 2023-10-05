import requests
import tkinter as tk

def get_ip_info():
    try:
        # Use the ipinfo.io API to get IP information
        response = requests.get('https://ipinfo.io/json')

        if response.status_code == 200:
            data = response.json()

            # Retrieve IP addresses (IPv4 and IPv6)
            ipv4 = data.get('ip', 'IPv4 not available')
            ipv6 = data.get('ip6', 'IPv6 not available')

            # Retrieve location information (City, Region, Country)
            city = data.get('city', 'City not available')
            region = data.get('region', 'Region not available')
            country = data.get('country', 'Country not available')

            # Retrieve ISP information
            isp = data.get('org', 'ISP information not available')

            return ipv4, ipv6, city, region, country, isp
        else:
            return None, None, None, None, None, None

    except requests.RequestException:
        return None, None, None, None, None, None

def display_ip_info():
    ipv4, ipv6, city, region, country, isp = get_ip_info()

    if ipv4 and ipv6:
        result_label.config(
            text=f"Public IPv4 Address: {ipv4}\n"
                 f"Public IPv6 Address: {ipv6}\n"
                 f"City: {city}\n"
                 f"Region: {region}\n"
                 f"Country: {country}\n"
                 f"ISP: {isp}",
            fg="green"
        )
    else:
        result_label.config(
            text="Error: Unable to retrieve IP data",
            fg="red"
        )


window = tk.Tk()
window.title("JACKS: Network Information")  # Project Title


title_label = tk.Label(window, text="JACKS: Network Information", font=("Helvetica", 16, "bold"), pady=10)
fetch_button = tk.Button(window, text="Fetch IP Info", command=display_ip_info, padx=10, pady=5)
result_label = tk.Label(window, text="", justify="left", padx=10, pady=5, font=("Helvetica", 12))

# Widgets
title_label.pack()
fetch_button.pack(pady=10)
result_label.pack(padx=10, pady=5)

# Start App
window.mainloop()
