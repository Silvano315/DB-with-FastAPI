from cryptography.fernet import Fernet
from typing import Optional

class DataEncryption:
    """
    Class for handling encryption and decryption of sensitive data.
    
    This class provides methods to encrypt and decrypt sensitive
    patient data before storing in or retrieving from the database.
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption handler.
        
        Args:
            encryption_key: Optional encryption key, will generate new if None
        """
        self.key = encryption_key.encode() if encryption_key else Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_data(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: The plain text data to encrypt
            
        Returns:
            str: The encrypted data as a string
        """
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data.
        
        Args:
            encrypted_data: The encrypted data to decrypt
            
        Returns:
            str: The decrypted plain text
        """
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()