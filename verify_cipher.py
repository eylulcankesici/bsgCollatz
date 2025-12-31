
import unittest
from collatz_cipher import CollatzCipher, analyze_randomness

class TestCollatzCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        key = "secret_key"
        cipher = CollatzCipher(key)
        original = "Hello World! This is a test."
        encrypted = cipher.encrypt(original)
        decrypted = cipher.decrypt(encrypted)
        
        self.assertEqual(original, decrypted, "Decrypted text must match original")
        self.assertNotEqual(original.encode(), encrypted, "Ciphertext must not be plaintext")
        
    def test_distribution(self):
        key = "random_distribution_test"
        cipher = CollatzCipher(key)
        # Generate 50KB stream
        stream = cipher._generate_keystream(50000) 
        ones, zeros = analyze_randomness(stream)
        total = ones + zeros
        ratio = ones / total
        
        print(f"\nDistribution: {ratio:.4f}")
        # Allow small deviation (e.g., 0.49 to 0.51)
        self.assertTrue(0.48 <= ratio <= 0.52, f"Bit distribution {ratio} is not uniform enough")

if __name__ == '__main__':
    unittest.main()
