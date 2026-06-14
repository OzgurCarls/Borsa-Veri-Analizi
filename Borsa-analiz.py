import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def veri_cek(ticker, period="3mo"):
    return yf.download(ticker, period=period)


def temel_istatistikler(hisse, isim):
    print(f"\n=== {isim} - TEMEL İSTATİSTİKLER ===")
    print(hisse["Close"].describe())
    print(f"En yüksek kapanış: {hisse['Close'].max().round(2)}")
    print(f"En düşük kapanış: {hisse['Close'].min().round(2)}")


def hareketli_ortalama_grafik(hisse, isim):
    hisse["MA5"] = hisse["Close"].rolling(window=5).mean()
    hisse["MA10"] = hisse["Close"].rolling(window=10).mean()

    plt.figure(figsize=(12, 5))
    plt.plot(hisse["Close"], label="Kapanış", color="gray", alpha=0.5)
    plt.plot(hisse["MA5"], label="5 Günlük Ortalama", color="orange")
    plt.plot(hisse["MA10"], label="10 Günlük Ortalama", color="purple")
    plt.title(f"{isim} - Hareketli Ortalamalar")
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat (TL)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def karsilastirma_grafik(hisse1, hisse2, isim1, isim2):
    karsilastirma = pd.DataFrame({
        isim1: hisse1["Close"].squeeze(),
        isim2: hisse2["Close"].squeeze()
    })

    normalize = karsilastirma / karsilastirma.iloc[0] * 100

    plt.figure(figsize=(12, 5))
    plt.plot(normalize[isim1], label=isim1, color="orange")
    plt.plot(normalize[isim2], label=isim2, color="blue")
    plt.title(f"{isim1} vs {isim2} - Normalize Karşılaştırma (Başlangıç=100)")
    plt.xlabel("Tarih")
    plt.ylabel("Endeks (Başlangıç=100)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    korelasyon = karsilastirma[isim1].corr(karsilastirma[isim2])
    print(f"\n{isim1}-{isim2} korelasyonu: {korelasyon:.2f}")


if __name__ == "__main__":
    tuprs = veri_cek("TUPRS.IS")
    thyao = veri_cek("THYAO.IS")

    temel_istatistikler(tuprs, "Tupraş")
    hareketli_ortalama_grafik(tuprs, "Tupraş")
    karsilastirma_grafik(tuprs, thyao, "Tupraş", "THY")