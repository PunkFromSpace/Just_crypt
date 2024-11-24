import os
from tkinter import Tk, filedialog, messagebox
from cryptography.fernet import Fernet

# Normalize file paths
def normalize_path(file_path):
    """
    Cleans up and normalizes file paths for cross-platform use.
    """
    file_path = file_path.strip().strip('"').strip("'")
    file_path = os.path.abspath(file_path)
    file_path = os.path.normpath(file_path)
    return file_path

# Validate file existence
def validate_file(file_path):
    """Checks if the file exists and is accessible."""
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"The file '{file_path}' does not exist!")
        return False
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"The path '{file_path}' is not a valid file!")
        return False
    return True

# Load the key from a specified key file
def load_key(key_filename):
    try:
        with open(key_filename, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Key file '{key_filename}' not found!")
        return None

# Decrypt the file
def decrypt_file():
    # Prompt the user to select the encrypted file
    encrypted_file = filedialog.askopenfilename(title="Select Encrypted File")
    if not encrypted_file:
        return
    encrypted_file = normalize_path(encrypted_file)
    if not validate_file(encrypted_file):
        return

    # Prompt the user to select the key file
    key_filename = filedialog.askopenfilename(title="Select Key File")
    if not key_filename:
        return
    key_filename = normalize_path(key_filename)
    if not validate_file(key_filename):
        return

    # Load the key
    key = load_key(key_filename)
    if not key:
        return
    fernet = Fernet(key)

    try:
        with open(encrypted_file, "rb") as file:
            encrypted_data = file.read()
        decrypted = fernet.decrypt(encrypted_data)
        decrypted_file = encrypted_file.replace(".enc", "")
        with open(decrypted_file, "wb") as file:
            file.write(decrypted)
        messagebox.showinfo("Success", f"File '{encrypted_file}' decrypted and saved as '{decrypted_file}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to decrypt the file.\nEnsure you are using the correct key!\n\nDetails: {e}")

# Main UI function
def main():
    # Create the main window
    root = Tk()
    root.withdraw()  # Hide the root window (we'll only use dialogs)

    # Show a welcome message
    messagebox.showinfo("Welcome", "This is the Decryption Tool!\n\nClick OK to begin.")

    # Run the decryption process
    decrypt_file()

# Run the application
if __name__ == "__main__":
    main()
