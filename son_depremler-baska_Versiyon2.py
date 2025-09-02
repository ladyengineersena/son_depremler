import requests
from bs4 import BeautifulSoup
import sys

url = "https://deprem.afad.gov.tr/last-earthquakes.html"

try:
    print("AFAD websitesine bağlanılıyor (HTTPS)...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # HTTP hatalarını kontrol et
    print(f"Bağlantı başarılı. Status code: {response.status_code}")
    
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    
    # Tüm tabloları bul
    tables = soup.find_all("table")
    print(f"Bulunan tablo sayısı: {len(tables)}")
    
    if not tables:
        print("Hiç tablo bulunamadı!")
        sys.exit(1)
    
    # İlk tabloyu al
    table = tables[0]
    rows = table.find_all("tr")
    print(f"Bulunan satır sayısı: {len(rows)}")
    
    if len(rows) < 2:
        print("Yeterli veri bulunamadı!")
        sys.exit(1)
    
    print("\n🌍 AFAD Son Depremler Raporu")
    print("=" * 60)
    print(f"📊 Toplam {len(rows)-1} deprem kaydı bulundu")
    print("=" * 60)
    
    # İlk 5 veri satırını işle (başlık satırını atla)
    for i in range(1, min(6, len(rows))):
        row = rows[i]
        cells = row.find_all(["td", "th"])
        
        if len(cells) >= 6:  # En az 6 sütun olmalı
            try:
                # Doğru sütun eşleştirmesi
                tarih_saat = cells[0].get_text(strip=True)
                enlem = cells[1].get_text(strip=True)
                boylam = cells[2].get_text(strip=True)
                derinlik = cells[3].get_text(strip=True)
                buyukluk_tipi = cells[4].get_text(strip=True)
                buyukluk = cells[5].get_text(strip=True)
                yer = cells[6].get_text(strip=True) if len(cells) > 6 else "Bilinmiyor"
                
                # Tarih ve saati ayır
                if ' ' in tarih_saat:
                    tarih, saat = tarih_saat.split(' ', 1)
                else:
                    tarih = tarih_saat
                    saat = "Bilinmiyor"
                
                # Büyüklüğe göre emoji seç
                try:
                    magnitude = float(buyukluk)
                    if magnitude >= 5.0:
                        emoji = "🔴"
                    elif magnitude >= 4.0:
                        emoji = "🟠"
                    elif magnitude >= 3.0:
                        emoji = "🟡"
                    else:
                        emoji = "🟢"
                except:
                    emoji = "⚪"
                
                print(f"\n{emoji} Deprem #{i}")
                print(f"📅 Tarih: {tarih}")
                print(f"🕐 Saat: {saat}")
                print(f"📍 Yer: {yer}")
                print(f"📏 Büyüklük: {buyukluk} ({buyukluk_tipi})")
                print(f"🌍 Konum: {enlem}°N, {boylam}°E")
                print(f"⬇️ Derinlik: {derinlik} km")
                print("-" * 50)
            except Exception as e:
                print(f"❌ Deprem #{i} işlenirken hata: {e}")
                continue
        else:
            print(f"❌ Deprem #{i} yeterli veri içermiyor")
    
    print(f"\n✅ Rapor tamamlandı. Son güncelleme: {tarih if 'tarih' in locals() else 'Bilinmiyor'}")
        
except requests.exceptions.RequestException as e:
    print(f"Bağlantı hatası: {e}")
except Exception as e:
    print(f"Beklenmeyen hata: {e}")