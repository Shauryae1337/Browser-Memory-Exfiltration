import re
from collections import defaultdict, Counter
import urllib.parse

# Regular expressions for different patterns
email_regex = r'([a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'  # To match emails
phone_regex = r'\+91[789]\d{9}'  # Indian phone numbers with +91
ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'  # Matches IPv4 addresses
domain_regex = r'https?://([a-zA-Z0-9.-]+)'  # Matches domain names with http or https

# Function to validate if an email domain is a valid TLD and not a file extension
def is_valid_email(email):
    # Invalid extensions to check
    invalid_extensions = ['.png', '.zip', '.xpi', '.jpg', '.jpeg', '.gif', '.exe', '.pdf', '.docx']
    
    # Email should not contain underscores
    if "_" in email:
        return False
    
    # Check if the domain has a valid TLD
    tld_regex = r'\.[a-zA-Z]{2,}$'  # Matches valid TLDs like .com, .org, etc.
    if any(email.lower().endswith(ext) for ext in invalid_extensions):
        return False

    return bool(re.search(tld_regex, email))

# Function to validate if an IP address is in a valid range (excluding private and reserved ranges)
def is_valid_ip(ip):
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        try:
            if not (0 <= int(octet) <= 255):
                return False
        except ValueError:
            return False
    
    # Check for reserved IP ranges (e.g., 127.x.x.x, 10.x.x.x, etc.)
    reserved_ips = [
        (0, 0, 0, 0), (255, 255, 255, 255),  # Broadcast address
        (10, 0, 0, 0),  # Private IP range
        (172, 16, 0, 0), (172, 31, 255, 255),  # Private IP range
        (192, 168, 0, 0), (192, 168, 255, 255),  # Private IP range
        (127, 0, 0, 0),  # Loopback address
    ]
    ip_parts = tuple(map(int, octets))
    return ip_parts not in reserved_ips

# Function to extract relevant information from unstructured data in chunks
def extract_data(file_path):
    # Store results in a defaultdict for efficiency (set to remove duplicates)
    result = defaultdict(Counter)  # Using Counter to count frequency of entries

    # Read the file in chunks to save memory
    with open(file_path, 'r', encoding='utf-8') as file:
        buffer_size = 1024 * 1024  # 1 MB chunk size, can be adjusted
        buffer = file.read(buffer_size)
        
        while buffer:
            # Use re.finditer for efficient matching
            for match in re.finditer(email_regex, buffer):
                email = match.group(0)
                if is_valid_email(email):
                    email = urllib.parse.unquote(email)  # Decode %20 to spaces
                    result['emails'][email] += 1
            for match in re.finditer(phone_regex, buffer):
                phone_number = match.group(0)
                result['phone_numbers'][phone_number] += 1
            for match in re.finditer(ip_regex, buffer):
                ip = match.group(0)
                if is_valid_ip(ip):
                    result['ip_addresses'][ip] += 1
            for match in re.finditer(domain_regex, buffer):
                domain = match.group(1)
                result['domains'][domain] += 1

            # Read the next chunk of the file
            buffer = file.read(buffer_size)
    
    return result

# Function to save the extracted data to a text file
def save_to_file(result, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        # Write emails and sort by frequency
        file.write("Emails:\n")
        for email, freq in result['emails'].most_common():
            file.write(f"{email} - {freq}\n")

        file.write("\nPhone Numbers:\n")
        for phone, freq in result['phone_numbers'].most_common():
            file.write(f"{phone} - {freq}\n")

        file.write("\nIP Addresses:\n")
        for ip, freq in result['ip_addresses'].most_common():
            file.write(f"{ip} - {freq}\n")

        file.write("\nDomains:\n")
        for domain, freq in result['domains'].most_common():
            file.write(f"{domain} - {freq}\n")

# Example usage
input_file_path = 'extracted_strings.txt'  # Replace with the actual file path
output_file_path = 'extracted_data.txt'    # Replace with the desired output file path

# Extract data
result = extract_data(input_file_path)

# Save the result to the output file
save_to_file(result, output_file_path)

print(f"Extracted data saved to {output_file_path}")
