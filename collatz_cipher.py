import hashlib
import os

class CollatzCipher:
    def __init__(self, key: str):
        """
        Şifreyi bir dize anahtarı ile başlatır.
        Anahtar, Collatz dizisi için büyük bir tamsayı tohumu oluşturmak üzere hashlenir.
        """
        # Güçlü bir başlangıç noktası (seed) elde etmek için kullanıcı anahtarını hashle
        self.seed = int(hashlib.sha256(key.encode()).hexdigest(), 16)
        self.state = self.seed

    def _collatz_step(self, n: int) -> int:
        """
        Collatz dizisindeki bir sonraki sayıyı hesaplar.
        Eğer n çift ise: n / 2
        Eğer n tek ise: 3n + 1
        """
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1

    def _generate_keystream(self, length: int) -> bytes:
        """
        'length' uzunluğunda bir anahtar akışı (keystream) üretir.
        Collatz durumunu geliştirir ve yüksek entropili baytlar (yaklaşık %50 0 ve 1 dağılımı simüle edilerek)
        üretmek için bir karıştırma fonksiyonu kullanır.
        """
        keystream = bytearray()
        
        for _ in range(length):
            # 1. Collatz ile durumu geliştir
            # Küçük sayılar için 4-2-1 döngüsüne sıkışmayı önlemek veya tohum bozulursa,
            # 1'e ulaşırsak bir pertürbasyon ekleriz.
            if self.state <= 1:
                # Akışı devam ettirmek için durumu deterministik bir mutasyonla yeniden başlat
                self.state = (self.seed + len(keystream) + 0xDEADBEEF) 
            
            self.state = self._collatz_step(self.state)
            
            # 2. Yüksek Entropi için Karıştırma Adımı ("%50 dağılım" mantığı)
            # Sadece ham Collatz değerlerini kullanmak düzgün bit dağılımını garanti etmez.
            # Düzgün rastgele bir bayt elde etmek için mevcut durumu (indeks ile tuzlayarak) hashliyoruz.
            # Collatz üzerindeki bu "diğer şifreleme mantığı" gücü sağlar.
            
            # Durum tekrarlansa bile benzersizliği sağlamak için mevcut durum ve indeksi birleştir
            mutation_input = f"{self.state}:{len(keystream)}".encode()
            mixed_hash = hashlib.sha256(mutation_input).digest()
            
            # Hash'in ilk baytını akış baytımız olarak al
            byte = mixed_hash[0]
            keystream.append(byte)
            
        return bytes(keystream)

    def encrypt(self, plaintext: str) -> tuple[bytes, bytes]:
        """
        Düz metin dizesini şifreler. (sifreli_baytlar, orijinal_uzunluk) döndürür.
        """
        plaintext_bytes = plaintext.encode('utf-8')
        length = len(plaintext_bytes)
        
        # Gerekirse tekrarlanabilir akış için durumu sıfırla,
        # veya durumlu (stateful) yapabiliriz. Burada aynı mesajın deterministik şifrelemesi 
        # için anahtara göre sıfırlıyoruz (akış şifresi stili).
        # İdeal olarak, güvenlik için bir nonce kullanılmalıdır.
        # Bu demo için, kendi kendine yeten doğruluğu sağlamak adına her seferinde yeniden tohumluyoruz.
        self.state = self.seed 
        
        keystream = self._generate_keystream(length)
        
        ciphertext = bytearray()
        for p, k in zip(plaintext_bytes, keystream):
            ciphertext.append(p ^ k)
            
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> str:
        """
        Şifreli metin baytlarını tekrar dizeye çözer.
        """
        length = len(ciphertext)
        
        # Aynı anahtar akışını üretmek için durumu sıfırla
        self.state = self.seed
        
        keystream = self._generate_keystream(length)
        
        plaintext_bytes = bytearray()
        for c, k in zip(ciphertext, keystream):
            plaintext_bytes.append(c ^ k)
            
        return plaintext_bytes.decode('utf-8')

def analyze_randomness(data: bytes):
    """
    Verinin bit dağılımını analiz eder.
    0'ların ve 1'lerin yüzdesini yazdırır.
    """
    total_bits = len(data) * 8
    ones = 0
    for byte in data:
        ones += bin(byte).count('1')
    
    zeros = total_bits - ones
    
    print(f"Toplam Bit: {total_bits}")
    print(f"Birler:  {ones} ({ones/total_bits*100:.2f}%)")
    print(f"Sıfırlar: {zeros} ({zeros/total_bits*100:.2f}%)")
    
    return ones, zeros

if __name__ == "__main__":
    
    key = "anahtar"
    cipher = CollatzCipher(key)
    
    original_text = "BSG odevi basariyla yapildi."
    print(f"Orijinal: {original_text}")
    
    encrypted = cipher.encrypt(original_text)
    print(f"Şifreli (hex): {encrypted.hex()}")
    
    decrypted = cipher.decrypt(encrypted)
    print(f"Çözülen: {decrypted}")
