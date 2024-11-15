#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>

// Securely read input using Windows API to avoid buffered input
void secure_read_input(char *buffer, size_t size) {
    DWORD read_bytes;
    HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
    if (ReadFile(hStdin, buffer, (DWORD)size - 1, &read_bytes, NULL) && read_bytes > 0) {
        buffer[read_bytes - 1] = '\0';  // Null-terminate and remove newline
    }
}

int main() {
    // Allocate memory for user input
    char original_string[256] = {0};
    
    printf("Enter a sensitive string: ");
    secure_read_input(original_string, sizeof(original_string));
    
    // Encrypt the input using DPAPI
    DATA_BLOB data_in;
    DATA_BLOB data_out;

    data_in.pbData = (BYTE*)original_string;
    data_in.cbData = (DWORD)strlen(original_string) + 1;  // Include null terminator

    if (!CryptProtectData(&data_in, NULL, NULL, NULL, NULL, 0, &data_out)) {
        fprintf(stderr, "Data encryption failed. Error: %d\n", GetLastError());
        SecureZeroMemory(original_string, sizeof(original_string));
        return 1;
    }
    
    // Clear original plaintext
    SecureZeroMemory(original_string, sizeof(original_string));
    
    printf("Press Enter to decrypt and display the string...\n");
    getchar();

    // Decrypt the data using DPAPI
    DATA_BLOB decrypted_data;
    if (!CryptUnprotectData(&data_out, NULL, NULL, NULL, NULL, 0, &decrypted_data)) {
        fprintf(stderr, "Data decryption failed. Error: %d\n", GetLastError());
        LocalFree(data_out.pbData);  // Free encrypted data
        return 1;
    }

    // Display decrypted string
    printf("Decrypted string: %s\n", (char*)decrypted_data.pbData);
    
    // Securely clear sensitive data from memory
    SecureZeroMemory(decrypted_data.pbData, decrypted_data.cbData);
    LocalFree(decrypted_data.pbData);
    LocalFree(data_out.pbData);  // Free encrypted data

    return 0;
}
