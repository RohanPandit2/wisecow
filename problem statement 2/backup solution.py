import paramiko
from scp import SCPClient
import os
import datetime

def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def backup_directory(local_directory, remote_directory, server, port, user, password):
    try:
        ssh_client = create_ssh_client(server, port, user, password)
        scp = SCPClient(ssh_client.get_transport())

        # Create remote directory if it does not exist
        stdin, stdout, stderr = ssh_client.exec_command(f'mkdir -p {remote_directory}')
        stdout.channel.recv_exit_status()  # Wait for mkdir to complete

        # Transfer the files
        scp.put(local_directory, recursive=True, remote_path=remote_directory)
        scp.close()

        report_success(local_directory, remote_directory, server)
    except Exception as e:
        report_failure(local_directory, remote_directory, server, str(e))
    finally:
        ssh_client.close()

def report_success(local_directory, remote_directory, server):
    report = f"Backup Success\nTime: {datetime.datetime.now()}\nLocal Directory: {local_directory}\nRemote Directory: {remote_directory}\nServer: {server}\n"
    print(report)
    with open("backup_report.log", "a") as log_file:
        log_file.write(report)

def report_failure(local_directory, remote_directory, server, error):
    report = f"Backup Failure\nTime: {datetime.datetime.now()}\nLocal Directory: {local_directory}\nRemote Directory: {remote_directory}\nServer: {server}\nError: {error}\n"
    print(report)
    with open("backup_report.log", "a") as log_file:
        log_file.write(report)

if __name__ == "__main__":
    # Configuration   Add your own path 
    LOCAL_DIRECTORY = "/path/to/local/directory"
    REMOTE_DIRECTORY = "/path/to/remote/directory"
    SERVER = "your.remote.server"
    PORT = 22
    USER = "your_username"  #set username password accordingly
    PASSWORD = "your_password"  #set password accordingly

    # Perform backup
    backup_directory(LOCAL_DIRECTORY, REMOTE_DIRECTORY, SERVER, PORT, USER, PASSWORD)
