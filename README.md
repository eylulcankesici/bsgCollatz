# RSÜ (Rastgele Sayı Üreteci) Algoritması

Bu proje, Collatz dizisi tabanlı bir Rastgele Sayı Üreteci (RSÜ) algoritması içermektedir. Algoritma, kriptografik güvenlik ve istatistiksel rastgelelik sağlamak için tasarlanmıştır.

## 📋 İçindekiler

- [Algoritma Açıklaması](#algoritma-açıklaması)
- [Nasıl Çalışır?](#nasıl-çalışır)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [İstatistiksel Testler](#istatistiksel-testler)
- [Proje Yapısı](#proje-yapısı)
- [Sonuçlar](#sonuçlar)

## 🔍 Algoritma Açıklaması

### Genel Bakış

RSÜ algoritması, Collatz dizisi ve kriptografik hash fonksiyonlarını birleştirerek yüksek kaliteli rastgele sayılar üretir. Algoritma, deterministik (aynı anahtar ile aynı çıktı) ancak istatistiksel olarak rastgele görünen bir akış üretir.

### Temel Prensip

1. **Seed Oluşturma**: Kullanıcı anahtarı SHA-256 ile hashlenerek büyük bir tamsayı seed değeri oluşturulur.
2. **Collatz Dizisi**: Seed değeri, Collatz dizisi kurallarına göre geliştirilir:
   - Eğer sayı çift ise: `n / 2`
   - Eğer sayı tek ise: `3n + 1`
3. **Mutasyon ve Hash**: Her adımda, mevcut state ve indeks birleştirilerek SHA-256 ile hashlenir.
4. **Rastgele Sayı Çıkarımı**: Hash'in ilk baytı rastgele sayı olarak alınır.

### Algoritmanın Mantığı

#### 1. Collatz Dizisi Kullanımı

Collatz dizisi, deterministik ancak öngörülemez bir davranış sergiler. Bu özellik, algoritmaya güçlü bir rastgelelik kaynağı sağlar. Ancak, Collatz dizisi tek başına yeterli değildir çünkü:
- Küçük sayılar için 4-2-1 döngüsüne düşebilir
- Bit dağılımı uniform olmayabilir

#### 2. Pertürbasyon Mekanizması

State değeri 1'e düştüğünde veya çok küçük olduğunda, algoritma state'i yeniden başlatır:
```python
state = seed + index + 0xDEADBEEF
```
Bu mekanizma, döngüye düşmeyi önler ve akışın devam etmesini sağlar.

#### 3. Hash Tabanlı Karıştırma

Her Collatz adımından sonra, state ve mevcut indeks birleştirilerek SHA-256 ile hashlenir:
```python
mutation_input = f"{state}:{index}".encode()
mixed_hash = hashlib.sha256(mutation_input).digest()
byte = mixed_hash[0]
```

Bu adım:
- Uniform bit dağılımı sağlar (yaklaşık %50 0 ve %50 1)
- State tekrarlansa bile farklı çıktılar üretir (indeks sayesinde)
- Kriptografik güvenlik sağlar

## 🚀 Nasıl Çalışır?

### Adım Adım İşleyiş

1. **Başlangıç**:
   ```
   Anahtar: "test_anahtari"
   → SHA-256 Hash
   → Seed: 1234567890... (büyük tamsayı)
   → State = Seed
   ```

2. **Her İterasyon**:
   ```
   State kontrolü → Collatz adımı → Hash → Bayt çıkarımı
   ```

3. **Örnek Akış**:
   ```
   State = 100 (çift)
   → State = 50
   → Hash("50:0") → SHA-256 → İlk bayt: 0xAB
   → Keystream[0] = 0xAB
   
   State = 50 (çift)
   → State = 25
   → Hash("25:1") → SHA-256 → İlk bayt: 0xCD
   → Keystream[1] = 0xCD
   ```

### Deterministiklik

Aynı anahtar ile algoritma her zaman aynı çıktıyı üretir. Bu özellik:
- ✅ Test edilebilirlik sağlar
- ✅ Şifreleme/çözme için gereklidir
- ✅ Tekrarlanabilir sonuçlar verir

### Rastgelelik

Farklı anahtarlar ile algoritma tamamen farklı çıktılar üretir. Bu özellik:
- ✅ Güvenli rastgele sayı üretimi sağlar
- ✅ İstatistiksel testlerden geçer
- ✅ Kriptografik uygulamalar için uygundur

## 📦 Kurulum

### Gereksinimler:
- Python 3.7 veya üzeri
- Standart kütüphaneler (hashlib, os)

### Kurulum Adımları:

1. Projeyi klonlayın veya indirin
2. Gerekli kütüphaneler zaten Python standart kütüphanesinde bulunmaktadır
3. Herhangi bir ek kurulum gerekmez

## 💻 Kullanım

### Temel Kullanım

```python
from collatz_cipher import CollatzCipher

# RSÜ oluştur
key = "benim_anahtarim"
cipher = CollatzCipher(key)

# Rastgele sayı akışı üret (100 bayt)
keystream = cipher._generate_keystream(100)

# Hex formatında görüntüle
print(keystream.hex())
```

### Şifreleme/Çözme Örneği

```python
from collatz_cipher import CollatzCipher

key = "sifreleme_anahtari"
cipher = CollatzCipher(key)

# Şifrele
mesaj = "Gizli mesaj"
sifreli = cipher.encrypt(mesaj)

# Çöz
cozulen = cipher.decrypt(sifreli)
print(cozulen)  # "Gizli mesaj"
```

### İstatistiksel Testler

```python
from statistical_tests import run_all_statistical_tests

# Tüm testleri çalıştır
results = run_all_statistical_tests("test_anahtari", sample_size=100000)
```

### Algoritma Çıktıları Üretme

```python
from generate_outputs import generate_algorithm_outputs

# Örnek çıktıları üret ve kaydet
generate_algorithm_outputs()
```

## 📊 İstatistiksel Testler

Algoritma, aşağıdaki istatistiksel testlerle doğrulanmıştır:

### 1. Bit Dağılımı Analizi (0-1 Eşitliği)

Algoritma, ürettiği bitlerin yaklaşık %50'sinin 0, %50'sinin 1 olmasını sağlar. Bu, rastgelelik için kritik bir özelliktir.

**Beklenen Sonuç**: 0.5 ± 0.01 (yani %49-51 arası)

### 2. Kikare (Chi-Square) Testi

Bayt değerlerinin uniform dağılımını test eder. 256 farklı bayt değerinin (0-255) eşit frekansta görülmesi beklenir.

**Kriterler**:
- Serbestlik derecesi: 255
- Kritik değer (%95): ~293.25
- Test başarılı ise: Chi-square değeri < kritik değer

### 3. Mislin Testi

Ardışık bayt çiftlerinin bağımsızlığını test eder. İki ardışık baytın birlikte görülme sıklığını analiz eder.

**Amaç**: Ardışık baytlar arasında korelasyon olmamalıdır.

### Test Sonuçları

Testleri çalıştırmak için:
```bash
python statistical_tests.py
```

Örnek çıktı için `algorithm_outputs.txt` dosyasına bakın.

## 📁 Proje Yapısı

```
RastgeleSayıÜreteci/
│
├── collatz_cipher.py          # Ana RSÜ algoritması
├── verify_cipher.py           # Doğrulama testleri
├── statistical_tests.py       # İstatistiksel testler (Kikare, Mislin)
├── generate_outputs.py        # Algoritma çıktıları üretici
├── flowchart.md              # Algoritma akış diyagramı
├── README.md                 # Bu dosya
└── algorithm_outputs.txt     # Algoritma örnek çıktıları (üretilir)
```

## ✅ Sonuçlar

### Algoritma Özellikleri

- ✅ **Tamamen Rastgele**: İstatistiksel testlerden geçer
- ✅ **0-1 Eşitliği**: Bit dağılımı yaklaşık %50-50
- ✅ **Deterministik**: Aynı anahtar ile aynı çıktı
- ✅ **Kriptografik Güvenlik**: SHA-256 hash kullanımı
- ✅ **Yüksek Entropi**: Collatz dizisi + hash karıştırma

### İstatistiksel Kalite

Algoritma, aşağıdaki kriterleri karşılar:
- Bit dağılımı: ~%50 0, ~%50 1
- Kikare testi: Başarılı (p > 0.05)
- Mislin testi: Başarılı (ardışık baytlar bağımsız)

### Kullanım Alanları

- Kriptografik uygulamalar
- Şifreleme sistemleri
- Simülasyonlar
- Oyun mekanizmaları
- Test verisi üretimi

## 📝 Notlar

- Algoritma, Collatz dizisinin deterministik yapısını kriptografik hash ile birleştirerek güçlü bir RSÜ oluşturur.
- State değeri 1'e düştüğünde pertürbasyon mekanizması devreye girer.
- Her bayt üretimi için SHA-256 hash hesaplanır, bu da yüksek güvenlik sağlar.

## 👤 Geliştirici

Bu proje, RSÜ algoritması gereksinimlerini karşılamak için geliştirilmiştir.

## 📅 Tarih

Ocak 2025

---

**Not**: Bu algoritma eğitim amaçlıdır. Üretim ortamlarında kullanmadan önce ek güvenlik değerlendirmeleri yapılmalıdır.

