import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

#  Excel'den veriyi al
veri = pd.read_excel("D:/PHD/ALL_koordinatli.xlsx")

#  Konum servisinden veri çekmek için başlatılıyor
arama_motoru = Nominatim(user_agent="Turkiye_uygulamam")

# Adresten koordinat çekme fonksiyonu
def koordinat_al(satir):
    adres_secenekleri = [
        ['mahalle', 'köy', 'ilçe', 'il'],
        ['köy', 'ilçe', 'il'],
        ['ilçe', 'il'],
        ['il']
    ]

    for alanlar in adres_secenekleri:
        adres_bolumleri = []
        for alan in alanlar:
            if alan in satir and pd.notna(satir[alan]):
                deger = str(satir[alan]).strip()
                if deger:
                    adres_bolumleri.append(deger)
        tam_adres = ', '.join(adres_bolumleri) + ", Türkiye"
        print(f"Adres deneniyor: {tam_adres}")
        try:
            konum = arama_motoru.geocode(tam_adres, timeout=10)
            if konum:
                return pd.Series([konum.latitude, konum.longitude])
        except GeocoderTimedOut:
            print("tekrar deneniyor...")
            time.sleep(2)
            return koordinat_al(satir)
        except Exception as e:
            print(f"Hata: {e}")
            return pd.Series([None, None])

    print("sonuç vermedi.")
    return pd.Series([None, None])


# AŞAMA 1: İlk 30 veri

test_df = veri.head(30).copy()
test_df[['enlem', 'boylam']] = test_df.apply(koordinat_al, axis=1)
test_df.to_excel("ilk_30_sonuclar.xlsx", index=False)
print(" İlk 30 veri işlendi. Sonuç: ilk_30_sonuclar.xlsx")


input("Devam etmek için Enter'a bas...") 


# AŞAMA 2: Tüm veriler

veri['enlem'] = None
veri['boylam'] = None

for i in range(0, len(veri), 50):
    print(f"\n🔄 {i+1}. satırdan itibaren işleniyor...")
    alt_df = veri.iloc[i:i+50]
    sonuclar = alt_df.apply(koordinat_al, axis=1)
    veri.loc[alt_df.index, ['enlem', 'boylam']] = sonuclar.values
    print("⏸ 5 saniye bekleniyor...")
    time.sleep(5)

veri.to_excel("tum_adresler_koordinatli.xlsx", index=False)
print("Tüm veriler başarıyla işlendi. Dosya: tum_adresler_koordinatli.xlsx")
    
