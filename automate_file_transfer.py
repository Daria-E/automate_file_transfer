''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''


import ftplib
import os
import shutil
import schedule

def automatic_file_transfer():
    # Initialize FTP, list files in remnote directory.
    ftp = ftplib.FTP('ftp.halifax.rwth-aachen.de')
    ftp.login()
    ftp.cwd('/ubuntu-releases/releases/jammy')
    files = ftp.nlst()
    print("Files in remote directory:" , *files, sep = "\n")

    # Check for existence of local directory, to store files.
    local_dir = "local_dir"
    if not os.path.isdir(local_dir):
        print("Local directory to store files does not exist. \n Creating local dir.")
        os.makedirs(local_dir)

    # Download all remote files to local directory.
    if not os.path.exists('log.txt'):
        open('log.txt', 'w')
    for remote_file in files:
        print(f"Downloading {remote_file}...")
        try:
            with open(os.path.join(local_dir,remote_file), 'wb') as file:
                ftp.retrbinary(f"RETR {remote_file}", file.write)
        except Exception as e:
            msg = f"Error downloading {remote_file}: {e} \n"
            with open("log.txt", "a") as log:
                log.write(msg)

    # Move all files from local directory to internal network. Sample names.
    internal_net_dir = "internal_net_dir/"
    shutil.copytree(local_dir, internal_net_dir, dirs_exist_ok=True)

    # Close FTP server
    ftp.close()

def main():
    schedule.every().day.at("00:00").do(automatic_file_transfer)

if __name__ == "__main__":
	main()