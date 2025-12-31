"""
RSÜ Algoritması Çıktıları Üretici
Algoritmanın örnek çıktılarını üretir ve kaydeder.
"""

from collatz_cipher import CollatzCipher, analyze_randomness
import datetime

def generate_algorithm_outputs():
    """
    Algoritmanın çeşitli örnek çıktılarını üretir ve dosyaya kaydeder.
    """
    outputs = []
    outputs.append("="*80)
    outputs.append("RSÜ (Rastgele Sayı Üreteci) ALGORİTMASI ÇIKTILARI")
    outputs.append("="*80)
    outputs.append(f"Üretim Tarihi: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    outputs.append("")
    
    # Test 1: Farklı anahtarlarla küçük örnekler
    outputs.append("-"*80)
    outputs.append("TEST 1: Farklı Anahtarlarla 10 Bayt Üretimi")
    outputs.append("-"*80)
    
    test_keys = ["anahtar1", "anahtar2", "test123", "farkli_anahtar"]
    for key in test_keys:
        cipher = CollatzCipher(key)
        keystream = cipher._generate_keystream(10)
        outputs.append(f"\nAnahtar: '{key}'")
        outputs.append(f"Üretilen Baytlar (hex): {keystream.hex()}")
        outputs.append(f"Üretilen Baytlar (decimal): {list(keystream)}")
    
    # Test 2: Büyük örnek ile bit dağılımı
    outputs.append("\n" + "-"*80)
    outputs.append("TEST 2: Büyük Örnek ile Bit Dağılımı Analizi (10,000 bayt)")
    outputs.append("-"*80)
    
    key = "istatistiksel_test_anahtari"
    cipher = CollatzCipher(key)
    keystream = cipher._generate_keystream(10000)
    ones, zeros = analyze_randomness(keystream)
    total_bits = ones + zeros
    ratio = ones / total_bits if total_bits > 0 else 0
    
    outputs.append(f"\nAnahtar: '{key}'")
    outputs.append(f"Toplam Bit: {total_bits:,}")
    outputs.append(f"Birler: {ones:,} ({ones/total_bits*100:.4f}%)")
    outputs.append(f"Sıfırlar: {zeros:,} ({zeros/total_bits*100:.4f}%)")
    outputs.append(f"0-1 Eşitliği Sapması: {abs(ratio - 0.5):.6f}")
    
    # Test 3: Şifreleme/Çözme örneği
    outputs.append("\n" + "-"*80)
    outputs.append("TEST 3: Şifreleme ve Çözme Örneği")
    outputs.append("-"*80)
    
    key = "sifreleme_anahtari"
    cipher = CollatzCipher(key)
    test_messages = [
        "Merhaba Dünya!",
        "RSÜ algoritması test mesajı.",
        "1234567890",
        "Özel karakterler: ğüşıöç ĞÜŞİÖÇ"
    ]
    
    for message in test_messages:
        encrypted = cipher.encrypt(message)
        decrypted = cipher.decrypt(encrypted)
        outputs.append(f"\nOrijinal Mesaj: '{message}'")
        outputs.append(f"Şifreli (hex): {encrypted.hex()}")
        outputs.append(f"Çözülen Mesaj: '{decrypted}'")
        outputs.append(f"Doğruluk: {'BASARILI' if message == decrypted else 'BASARISIZ'}")
    
    # Test 4: Deterministiklik testi (aynı anahtar, aynı çıktı)
    outputs.append("\n" + "-"*80)
    outputs.append("TEST 4: Deterministiklik Testi")
    outputs.append("-"*80)
    
    key = "deterministik_test"
    cipher1 = CollatzCipher(key)
    cipher2 = CollatzCipher(key)
    
    keystream1 = cipher1._generate_keystream(20)
    keystream2 = cipher2._generate_keystream(20)
    
    outputs.append(f"\nAnahtar: '{key}'")
    outputs.append(f"İlk Çalıştırma (hex): {keystream1.hex()}")
    outputs.append(f"İkinci Çalıştırma (hex): {keystream2.hex()}")
    outputs.append(f"Aynı Çıktı: {'EVET (Deterministik)' if keystream1 == keystream2 else 'HAYIR'}")
    
    # Test 5: Farklı anahtarlar, farklı çıktılar
    outputs.append("\n" + "-"*80)
    outputs.append("TEST 5: Farklı Anahtarlar ile Farklı Çıktılar")
    outputs.append("-"*80)
    
    keys = ["key1", "key2", "key3"]
    for key in keys:
        cipher = CollatzCipher(key)
        keystream = cipher._generate_keystream(10)
        outputs.append(f"\nAnahtar '{key}': {keystream.hex()}")
    
    # Test 6: İstatistiksel örnek (ilk 100 bayt)
    outputs.append("\n" + "-"*80)
    outputs.append("TEST 6: İstatistiksel Analiz Örneği (100 bayt)")
    outputs.append("-"*80)
    
    key = "istatistik_ornek"
    cipher = CollatzCipher(key)
    keystream = cipher._generate_keystream(100)
    
    # Bayt değerleri dağılımı
    byte_counts = {}
    for byte in keystream:
        byte_counts[byte] = byte_counts.get(byte, 0) + 1
    
    outputs.append(f"\nAnahtar: '{key}'")
    outputs.append(f"Üretilen Bayt Sayısı: {len(keystream)}")
    outputs.append(f"Benzersiz Bayt Değerleri: {len(byte_counts)}")
    outputs.append(f"En Az Görülen Bayt: {min(byte_counts.items(), key=lambda x: x[1])}")
    outputs.append(f"En Çok Görülen Bayt: {max(byte_counts.items(), key=lambda x: x[1])}")
    outputs.append(f"Ortalama Frekans: {sum(byte_counts.values())/len(byte_counts):.2f}")
    
    # Sonuç
    outputs.append("\n" + "="*80)
    outputs.append("ÇIKTI ÜRETİMİ TAMAMLANDI")
    outputs.append("="*80)
    
    # Dosyaya kaydet
    output_text = "\n".join(outputs)
    with open("algorithm_outputs.txt", "w", encoding="utf-8") as f:
        f.write(output_text)
    
    # Konsola da yazdır (Unicode karakterleri olmadan)
    try:
        print(output_text)
    except UnicodeEncodeError:
        # Windows konsol encoding sorunu varsa sadece bilgi ver
        print("Çıktılar başarıyla üretildi.")
    print(f"\nÇıktılar 'algorithm_outputs.txt' dosyasına kaydedildi.")
    
    return output_text

if __name__ == "__main__":
    generate_algorithm_outputs()

