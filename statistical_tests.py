"""
RSÜ Algoritması İstatistiksel Test Modülü
Kikare (Chi-Square) ve Mislin Testlerini içerir.
"""

import math
from collections import Counter
from collatz_cipher import CollatzCipher

def chi_square_test(data: bytes, num_bins: int = 256) -> dict:
    """
    Kikare (Chi-Square) testi: Bayt değerlerinin uniform dağılımını test eder.
    
    Args:
        data: Test edilecek bayt verisi
        num_bins: Beklenen kategori sayısı (bayt için 256)
    
    Returns:
        Test sonuçlarını içeren dictionary
    """
    n = len(data)
    if n == 0:
        return {"error": "Boş veri"}
    
    # Her bayt değerinin frekansını say
    frequency = Counter(data)
    
    # Beklenen frekans (her bayt değeri için eşit dağılım)
    expected_freq = n / num_bins
    
    # Kikare istatistiğini hesapla
    chi_square = 0.0
    for byte_value in range(num_bins):
        observed = frequency.get(byte_value, 0)
        chi_square += ((observed - expected_freq) ** 2) / expected_freq
    
    # Serbestlik derecesi (256 - 1 = 255)
    degrees_of_freedom = num_bins - 1
    
    # Kritik değer (α=0.05 için, yaklaşık 293.25)
    # Daha kesin hesaplama için scipy kullanılabilir, ama basit yaklaşım:
    critical_value_95 = 293.25  # df=255 için %95 güven seviyesi
    critical_value_99 = 310.46  # df=255 için %99 güven seviyesi
    
    # Test sonucu
    passed_95 = chi_square < critical_value_95
    passed_99 = chi_square < critical_value_99
    
    return {
        "test_name": "Kikare (Chi-Square) Testi",
        "chi_square_value": chi_square,
        "degrees_of_freedom": degrees_of_freedom,
        "critical_value_95": critical_value_95,
        "critical_value_99": critical_value_99,
        "passed_95": passed_95,
        "passed_99": passed_99,
        "sample_size": n,
        "expected_frequency": expected_freq,
        "min_frequency": min(frequency.values()) if frequency else 0,
        "max_frequency": max(frequency.values()) if frequency else 0,
    }


def mislin_test(data: bytes) -> dict:
    """
    Mislin Testi: Ardışık bayt çiftlerinin bağımsızlığını test eder.
    İki ardışık baytın birlikte görülme sıklığını analiz eder.
    
    Args:
        data: Test edilecek bayt verisi
    
    Returns:
        Test sonuçlarını içeren dictionary
    """
    n = len(data)
    if n < 2:
        return {"error": "Yeterli veri yok (en az 2 bayt gerekli)"}
    
    # Ardışık bayt çiftlerini say
    pairs = {}
    for i in range(n - 1):
        pair = (data[i], data[i + 1])
        pairs[pair] = pairs.get(pair, 0) + 1
    
    # Toplam çift sayısı
    total_pairs = n - 1
    
    # Her bayt değerinin frekansını hesapla
    byte_freq = Counter(data)
    
    # Beklenen çift frekansı (bağımsızlık varsayımı altında)
    # P(byte1, byte2) = P(byte1) * P(byte2) * total_pairs
    chi_square = 0.0
    total_expected = 0
    total_observed = 0
    
    # Tüm olası çiftler için (256x256 = 65536 çift)
    # Pratik olarak sadece gözlemlenen çiftleri kontrol edelim
    for pair, observed in pairs.items():
        byte1, byte2 = pair
        freq1 = byte_freq.get(byte1, 0)
        freq2 = byte_freq.get(byte2, 0)
        
        # Beklenen frekans
        if freq1 > 0 and freq2 > 0:
            expected = (freq1 / n) * (freq2 / n) * total_pairs
        else:
            expected = 0
        
        if expected > 0:
            chi_square += ((observed - expected) ** 2) / expected
        
        total_observed += observed
        total_expected += expected
    
    # Gözlemlenmeyen çiftler için de katkı ekle (basitleştirilmiş)
    # Pratikte bu çok büyük olabilir, bu yüzden sadece gözlemlenen çiftlere odaklanıyoruz
    
    # Serbestlik derecesi (gözlemlenen çift sayısı - 1)
    # Daha doğru hesaplama için: (256-1) * (256-1) = 65025
    degrees_of_freedom = len(pairs) - 1 if len(pairs) > 1 else 1
    
    # Kritik değerler (yaklaşık)
    # df çok büyük olduğu için normal dağılıma yaklaşır
    # Basit yaklaşım: df kadar kritik değer
    if degrees_of_freedom > 100:
        critical_value_95 = degrees_of_freedom + 1.96 * math.sqrt(2 * degrees_of_freedom)
        critical_value_99 = degrees_of_freedom + 2.58 * math.sqrt(2 * degrees_of_freedom)
    else:
        # Küçük df için tablo değerleri (yaklaşık)
        critical_value_95 = degrees_of_freedom * 1.5
        critical_value_99 = degrees_of_freedom * 2.0
    
    passed_95 = chi_square < critical_value_95
    passed_99 = chi_square < critical_value_99
    
    return {
        "test_name": "Mislin Testi (Ardışık Bayt Çiftleri)",
        "chi_square_value": chi_square,
        "degrees_of_freedom": degrees_of_freedom,
        "critical_value_95": critical_value_95,
        "critical_value_99": critical_value_99,
        "passed_95": passed_95,
        "passed_99": passed_99,
        "total_pairs": total_pairs,
        "unique_pairs": len(pairs),
        "sample_size": n,
    }


def run_all_statistical_tests(key: str, sample_size: int = 100000) -> dict:
    """
    Tüm istatistiksel testleri çalıştırır.
    
    Args:
        key: RSÜ algoritması için anahtar
        sample_size: Üretilecek bayt sayısı
    
    Returns:
        Tüm test sonuçlarını içeren dictionary
    """
    print(f"\n{'='*60}")
    print(f"İSTATİSTİKSEL TESTLER - Örnek Boyutu: {sample_size:,} bayt")
    print(f"{'='*60}\n")
    
    # RSÜ algoritması ile rastgele veri üret
    cipher = CollatzCipher(key)
    random_data = cipher._generate_keystream(sample_size)
    
    # Bit dağılımı analizi
    from collatz_cipher import analyze_randomness
    ones, zeros = analyze_randomness(random_data)
    total_bits = ones + zeros
    bit_ratio = ones / total_bits if total_bits > 0 else 0
    
    print(f"\n{'='*60}")
    print("BİT DAĞILIMI ANALİZİ")
    print(f"{'='*60}")
    print(f"0-1 Eşitliği: {abs(bit_ratio - 0.5):.6f} (0.5'e ne kadar yakın)")
    print(f"İdeal: 0.5, Mevcut: {bit_ratio:.6f}")
    
    # Kikare testi
    print(f"\n{'='*60}")
    print("KİKARE (CHI-SQUARE) TESTİ")
    print(f"{'='*60}")
    chi_result = chi_square_test(random_data)
    if "error" not in chi_result:
        print(f"Kikare Değeri: {chi_result['chi_square_value']:.4f}")
        print(f"Serbestlik Derecesi: {chi_result['degrees_of_freedom']}")
        print(f"Kritik Değer (%95): {chi_result['critical_value_95']:.4f}")
        print(f"Kritik Değer (%99): {chi_result['critical_value_99']:.4f}")
        print(f"Sonuç (%95): {'BAŞARILI' if chi_result['passed_95'] else 'BAŞARISIZ'}")
        print(f"Sonuç (%99): {'BAŞARILI' if chi_result['passed_99'] else 'BAŞARISIZ'}")
        print(f"Beklenen Frekans: {chi_result['expected_frequency']:.2f}")
        print(f"Min Frekans: {chi_result['min_frequency']}")
        print(f"Max Frekans: {chi_result['max_frequency']}")
    else:
        print(f"Hata: {chi_result['error']}")
    
    # Mislin testi
    print(f"\n{'='*60}")
    print("MİSLİN TESTİ (Ardışık Bayt Çiftleri)")
    print(f"{'='*60}")
    mislin_result = mislin_test(random_data)
    if "error" not in mislin_result:
        print(f"Kikare Değeri: {mislin_result['chi_square_value']:.4f}")
        print(f"Serbestlik Derecesi: {mislin_result['degrees_of_freedom']}")
        print(f"Kritik Değer (%95): {mislin_result['critical_value_95']:.4f}")
        print(f"Kritik Değer (%99): {mislin_result['critical_value_99']:.4f}")
        print(f"Sonuç (%95): {'BAŞARILI' if mislin_result['passed_95'] else 'BAŞARISIZ'}")
        print(f"Sonuç (%99): {'BAŞARILI' if mislin_result['passed_99'] else 'BAŞARISIZ'}")
        print(f"Toplam Çift Sayısı: {mislin_result['total_pairs']:,}")
        print(f"Benzersiz Çift Sayısı: {mislin_result['unique_pairs']:,}")
    else:
        print(f"Hata: {mislin_result['error']}")
    
    print(f"\n{'='*60}\n")
    
    return {
        "bit_distribution": {
            "ones": ones,
            "zeros": zeros,
            "ratio": bit_ratio,
            "deviation_from_ideal": abs(bit_ratio - 0.5)
        },
        "chi_square": chi_result,
        "mislin": mislin_result
    }


if __name__ == "__main__":
    # Test çalıştır
    key = "test_anahtari_12345"
    results = run_all_statistical_tests(key, sample_size=100000)

