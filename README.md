# Browser Memory Exfiltration

This repository demonstrates a proof of concept for exploiting **CWE-316**: Cleartext Storage of Sensitive Information in Memory. It showcases how an attacker can extract sensitive data stored in browser memory and provides mitigation techniques to secure sensitive data in memory.

---

## Repository Overview

The project is divided into the following sections:

1. **Exploit**: A PowerShell script (`exploit.ps1`) that dumps the memory of the browser process from a victim's device.
2. **Server**: Python scripts to receive the memory dump and analyze it for sensitive information.
3. **Mitigation**: Sample C programs implementing secure memory handling to mitigate the vulnerability.

---

### Requirements
- A system running **Windows** for the exploit.
- Python 3.9+ with necessary dependencies (for server-side analysis).
- C Compiler (`cl.exe`) from Visual Studio for compiling mitigation examples.

Navigate to the mitigation folder and compile the programs using cl.exe

This proof of concept is for educational purposes only. It demonstrates the issue of cleartext storage of sensitive information in memory but does not provide a comprehensive solution for all scenarios. Implementation of mitigation techniques in real-world applications may require adjustments for performance and platform-specific constraints.
