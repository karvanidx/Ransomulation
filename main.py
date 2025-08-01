import os
import sys
import logging
import shutil
from cryptography.fernet import Fernet
from datetime import datetime

# Configuration and logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("ransomware_simulation.log"), logging.StreamHandler(sys.stdout)]
)

class EncryptionHandler:
    """Handles encryption/decryption using Fernet symmetric encryption."""
    def __init__(self, key):
        self.key = key
        self.cipher = Fernet(key)

    def encrypt_file(self, file_path):
        """Encrypts a file in-place with Fernet encryption."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted = self.cipher.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted)
            logging.info(f"Encrypted: {file_path}")
        except Exception as e:
            logging.error(f"Encryption failed for {file_path}: {str(e)}")
            raise

    def decrypt_file(self, file_path):
        """Decrypts an encrypted file using the stored key."""
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted = self.cipher.decrypt(encrypted_data)
            with open(file_path, 'wb') as f:
                f.write(decrypted)
            logging.info(f"Decrypted: {file_path}")
        except Exception as e:
            logging.error(f"Decryption failed for {file_path}: {str(e)}")
            raise

class FileProcessor:
    """Manages file discovery and backup operations."""
    def __init__(self, directory):
        self.directory = directory
        self.target_files = []

    def find_files(self):
        """Discovers PDF and PNG files in the target directory."""
        self.target_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith(('.pdf', '.png')):
                    self.target_files.append(os.path.join(root, file))
        return self.target_files

    def create_backup(self, file_path):
        """Creates a timestamped backup of a file."""
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_name = f"{os.path.basename(file_path)}_{timestamp}.bak"
        backup_path = os.path.join(backup_dir, backup_name)
        shutil.copy2(file_path, backup_path)
        logging.info(f"Backup created: {backup_path}")
        return backup_path

def main():
    print("!!! RANSOMWARE SIMULATION FOR EDUCATIONAL PURPOSES ONLY !!!")
    print("This tool demonstrates ransomware behavior in a controlled environment.")
    print("DO NOT USE ON PRODUCTION SYSTEMS.")

    target_dir = "test_files"
    if not os.path.exists(target_dir):
        logging.error(f"Directory '{target_dir}' does not exist.")
        return

    # User confirmation steps
    confirm = input("Scan directory for PDF/PNG files? (y/n): ")
    if confirm.lower() != 'y':
        return

    processor = FileProcessor(target_dir)
    files = processor.find_files()
    print(f"Found {len(files)} files:")
    for file in files:
        print(f" - {file}")

    if not files:
        logging.warning("No target files found.")
        return

    # Generate encryption key
    key = Fernet.generate_key()
    cipher = EncryptionHandler(key)
    print(f"\nEncryption Key: {key.decode()} (Keep this safe for decryption)\n")

    # Encryption confirmation
    confirm_encrypt = input("Proceed with encryption? (y/n): ")
    if confirm_encrypt.lower() != 'y':
        return

    # Process files with encryption and backups
    for file in files:
        try:
            processor.create_backup(file)
            cipher.encrypt_file(file)
            logging.info(f"Processed: {file}")
        except Exception as e:
            logging.error(f"Error processing {file}: {str(e)}")

    print("\nEncryption complete. Backups stored in 'backups' directory.")

    # Optional decryption test
    if input("\nTest decryption of first file? (y/n): ").lower() == 'y':
        if files:
            test_file = files[0]
            try:
                cipher.decrypt_file(test_file)
                print(f"Decrypted {test_file} successfully.")
            except Exception as e:
                logging.error(f"Decryption failed: {str(e)}")
        else:
            print("No files to decrypt.")

    print("\nEDUCATIONAL WARNING:")
    print("Real ransomware is irreversible, demands payment, and uses advanced techniques.")
    print("Always practice cybersecurity best practices:")
    print("- Regularly back up critical data")
    print("- Keep systems updated")
    print("- Never pay ransom demands")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.error("Operation interrupted by user.")
    except Exception as e:
        logging.error(f"Critical error: {str(e)}")
        print("An unexpected error occurred. Check logs for details.")
