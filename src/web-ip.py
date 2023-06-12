import socket
import requests

def validate_url(url):
    # Add your own URL validation logic here
    return True

def get_ip_address(url):
    try:
        ip_addresses = socket.getaddrinfo(url, None)
        return list(set(ip[4][0] for ip in ip_addresses))
    except socket.gaierror:
        return []

def reverse_ip_lookup(ip_address):
    try:
        response = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip_address}")
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            return []
    except requests.RequestException:
        return []

def main():
    website = input("Enter the website URL: ")
    if not validate_url(website):
        print("Invalid URL format.")
        return
    
    ip_addresses = get_ip_address(website)
    
    if ip_addresses:
        print(f"The IP addresses of {website} are:")
        for ip in ip_addresses:
            print(ip)
        
        print("Performing reverse IP lookup...")
        for ip in ip_addresses:
            domain_names = set(reverse_ip_lookup(ip))  # Store domain names in a set to avoid duplicates
            if domain_names:
                print(f"\nDomain names associated with {ip}:")
                for domain in domain_names:
                    print(domain)
            else:
                print(f"No domain names found for {ip}")
    else:
        print(f"Failed to retrieve the IP address of {website}")

if __name__ == "__main__":
    main()
