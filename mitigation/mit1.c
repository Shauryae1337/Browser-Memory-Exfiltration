#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>  // For SecureZeroMemory, VirtualLock

// Simple XOR encryption/decryption function
void xor_encrypt_decrypt(char *data, const char *key, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        data[i] ^= key[i % strlen(key)];
    }
}

// Securely read input using Windows API to avoid buffered input
void secure_read_input(char *buffer, size_t size) {
    DWORD read_bytes;
    HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
    if (ReadFile(hStdin, buffer, (DWORD)size - 1, &read_bytes, NULL) && read_bytes > 0) {
        buffer[read_bytes - 1] = '\0';  // Null-terminate and remove newline
    }
}

int main() {
    // Allocate non-pageable memory for original string
    char *original_string = (char *)VirtualAlloc(NULL, 256, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (original_string == NULL) {
        fprintf(stderr, "Memory allocation failed for original_string.\n");
        return 1;
    }
    VirtualLock(original_string, 256);  // Lock memory to prevent paging

    printf("Enter a string: ");
    secure_read_input(original_string, 256);

    // Encrypt the data and store it
    size_t length = strlen(original_string);
    char *encrypted_string = (char *)VirtualAlloc(NULL, length + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (encrypted_string == NULL) {
        fprintf(stderr, "Memory allocation failed for encrypted_string.\n");
        VirtualFree(original_string, 0, MEM_RELEASE);
        return 1;
    }
    VirtualLock(encrypted_string, length + 1);

    // Copy the original string to the encrypted_string and encrypt it
    strcpy(encrypted_string, original_string);
    xor_encrypt_decrypt(encrypted_string, "samplekeyistobechanged", length);  // Encrypt in-place

    // Securely clear original string from memory
    SecureZeroMemory(original_string, length);
    VirtualUnlock(original_string, 256);
    VirtualFree(original_string, 0, MEM_RELEASE);

    // Wait for user input to decrypt
    printf("Press Enter to decrypt and display the string...\n");
    getchar();

    // Decrypt and display
    xor_encrypt_decrypt(encrypted_string, "samplekeyistobechanged", length);  // Decrypt in-place
    encrypted_string[length] = '\0';  // Ensure null-termination
    printf("Decrypted string: %s\n", encrypted_string);

    // Securely clear encrypted data from memory before exiting
    SecureZeroMemory(encrypted_string, length);
    VirtualUnlock(encrypted_string, length + 1);
    VirtualFree(encrypted_string, 0, MEM_RELEASE);

    return 0;
}
