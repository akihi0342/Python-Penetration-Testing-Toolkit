


# Python Penetration Testing Toolkit  

## Project Overview  
This project is dedicated to fully replicating commonly used penetration testing tools using Python 3.9. It serves as high-quality resource for learning penetration testing and Python security programming. The project adheres to the philosophy of "balancing tools and programming to achieve the most efficient penetration testing," while pursuing the goal of "achieving the highest realm of penetration testing without relying solely on tools."  

All tools and scripts can be directly used in real-world penetration testing environments, and they also serve as ideal examples for learning Python security programming. The code design emphasizes modularity and scalability, making it easy for learners to understand the integration of penetration testing principles and Python programming techniques.  

## Applicable Environment  
- **Operating System**: Kali Linux  
- **Python Version**: Python 3.9  
- **Dependent Libraries**: Dependencies required for each module of the project will be supplemented later  


## Project Structure  
### Chapter 1: Penetration Testing Frameworks  
- POC Scripts: Proof-of-Concept script framework  
- EXP Scripts: Vulnerability exploitation script framework  
- Executable File Conversion: Methods to convert Python scripts into executable files  

### Chapter 2: Information Gathering  
#### Passive Information Gathering  
- DNS Resolution Tool  
- Subdomain Mining Tool  
- Email Address Crawling Tool  

#### Active Information Gathering  
- Host Discovery Based on ICMP  
- Host Discovery Based on TCP/UDP  
- Host Discovery Based on ARP  
- Port Probing Tool  
- Service Identification Tool  
- Operating System Identification Tool  
- Sensitive Directory Probing Tool  

### Chapter 3: Vulnerability Detection and Defense  
- Unauthorized Access Vulnerabilities  
  - Redis Unauthorized Access Vulnerability Exploitation  
  - Redis Unauthorized Access Vulnerability Detection Method  
- External Entity Injection Vulnerabilities  
  - XXE Vulnerability Detection Method  
- Blind SQL Injection Vulnerabilities  
  - Boolean-Based Blind SQL Injection Detection  
  - Time-Based Blind SQL Injection Detection  
  - SQLMap Tamper Scripts  
    - Basics of Tamper Script Writing  
    - Advanced Tamper Script Writing Techniques  
- Server-Side Request Forgery (SSRF) Vulnerabilities  
  - SSRF Vulnerability Detection Method  
  - SSRF Network Proxy Tool  

### Chapter 4: Data Encryption  
- Base64 Encoding/Decoding Tool  
- DES Encryption/Decryption Implementation  
- AES Encryption/Decryption Implementation  
- MD5 Hashing Calculation Tool  

### Chapter 5: Authentication  
- Social Engineering Password Dictionary Generator  
- Web Background Weak Password Detection Script  
- SSH Password Cracking Script  
- FTP Password Cracking Script  

### Chapter 6: Fuzz Testing  
- Security Dog Bypass Techniques  
- Fuzz Testing Combined with WebShell Techniques  

### Chapter 7: Traffic Analysis  
- Traffic Sniffing Tool  
- ARP Poisoning Tool  
- Denial-of-Service (DoS) Attack Tools  
  - Data Link Layer DoS Attacks  
  - Network Layer DoS Attacks  
  - Transport Layer DoS Attacks  
  - Application Layer DoS Attacks  

### Chapter 8: Python Antivirus Evasion Techniques  
- Shellcode Generation Tool  
- Shellcode Loading and Execution Techniques  
- Implementation of Common Antivirus Evasion Methods  

### Chapter 9: Remote Control Tools  
- Socket Network Programming  
  - TCP Server/Client Implementation  
  - UDP Server/Client Implementation  
- File Transfer Server Example  
- Remote Control Tools  
  - Implementation of the Controlled End Program  
  - Implementation of the Master Control End Program  


## Usage Instructions  
- Tools and scripts in each chapter are independent modules and can be used individually as needed.  
- Ensure the required dependent libraries are installed before use (detailed installation guides will be provided later).  
- Some tools may require root privileges to run properly. Execute them with appropriate permissions in the Kali Linux environment.  


## Learning Resources  
This project is not only a practical toolset but also an excellent resource for learning Python security programming. Each module comes with detailed comments explaining the principles of penetration testing and the specifics of Python implementation.  

It is recommended to study alongside relevant security books and online tutorials for a deeper understanding.  


## Notes  
- This project is intended solely for security research and teaching. Do not use it for unauthorized penetration testing.  
- Always obtain explicit authorization from the owner of the target system before using any penetration testing tools.  
- The author assumes no responsibility for any losses caused by the use of the tools in this project.  


## Contributions  
Security researchers and Python developers are welcome to contribute code or propose improvement suggestions. Please follow the project's contribution guidelines when submitting.
