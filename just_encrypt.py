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

# Generate and save a key
def generate_key(file_path):
    base_name = os.path.basename(file_path).split(".")[0]
    key_filename = f"{base_name}_key.key"

    if os.path.exists(key_filename):
        messagebox.showinfo("Key Exists", f"Key file '{key_filename}' already exists. Skipping key generation.")
        return key_filename

    try:
        key = Fernet.generate_key()
        with open(key_filename, "wb") as key_file:
            key_file.write(key)
        messagebox.showinfo("Key Generated", f"Key file '{key_filename}' generated successfully.")
        return key_filename
    except Exception as e:
        messagebox.showerror("Error", f"Error generating key for '{file_path}': {e}")
        return None

# Encrypt the file
def encrypt_file():
    # Prompt the user to select the file to encrypt
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    if not file_path:
        return
    file_path = normalize_path(file_path)
    if not validate_file(file_path):
        return

    # Generate or load the key
    key_filename = generate_key(file_path)
    if not key_filename:
        return
    try:
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load key file: {e}")
        return

    fernet = Fernet(key)

    # Encrypt the file
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted = fernet.encrypt(data)
        encrypted_file = file_path + ".enc"
        with open(encrypted_file, "wb") as file:
            file.write(encrypted)
        messagebox.showinfo("Success", f"File '{file_path}' encrypted and saved as '{encrypted_file}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to encrypt the file.\n\nDetails: {e}")

# Main UI function
def main():
    # Create the main window
    root = Tk()
    root.withdraw()  # Hide the root window (we'll only use dialogs)

    # Show a welcome message
    messagebox.showinfo("Welcome", "This is the Encryption Tool!\n\nClick OK to begin.")

    # Run the encryption process
    encrypt_file()

# Run the application
if __name__ == "__main__":
    main()
