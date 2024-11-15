import re

def extract_specific_strings(file_path, output_path, min_length=4):
    """Extract and save specific patterns from a memory dump."""
    with open(file_path, 'rb') as f:
        data = f.read()

    # ASCII and Unicode string extraction
    ascii_strings = re.findall(rb'[ -~]{%d,}' % min_length, data)
    unicode_strings = re.findall(rb'(?:[\x20-\x7E]\x00){%d,}' % min_length, data)
    
    # Decode ASCII strings
    ascii_strings = [s.decode('ascii', 'ignore') for s in ascii_strings]
    # Decode Unicode strings
    unicode_strings = [s.decode('utf-16le', 'ignore') for s in unicode_strings]
    
    # Combine and save all readable strings
    all_strings = ascii_strings + unicode_strings
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_strings))
    
    print(f"Saved {len(all_strings)} readable strings to {output_path}")


def main():
    # File paths
    memory_dump_path = "firefox_dump.dmp"  # Replace with your memory dump file
    strings_output_path = "extracted_strings.txt"
    
    # Extract and analyze strings
    print("Extracting strings from the memory dump...")
    matches = extract_specific_strings(memory_dump_path, strings_output_path)
    
if __name__ == "__main__":
    main()
