# Kamera ile El Hareketlerinden Fare Kontrolü

Bu program kameradan elinizi takip eder ve fareyi el hareketleriyle kontrol eder.

## Hareketler

- İşaret parmağı: imleci hareket ettirir
- Başparmak + işaret parmağı: sol tık
- Başparmak + orta parmak: sağ tık
- Başparmak + yüzük parmağı: sürükle/bırak
- `Q`: programdan çıkış

## Çalıştırma

PowerShell içinde bu klasörde şu komutu çalıştırın:

```powershell
.\run.ps1
```

Alternatif olarak `run.bat` dosyasını da çalıştırabilirsiniz.

Eğer PowerShell betik çalıştırmayı engellerse şunu kullanın:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

## Ayarlar

Farklı kamera kullanmak için:

```powershell
.\.venv\Scripts\python.exe .\hand_mouse.py --camera 1
```

İmleç daha yavaş/kararlı olsun isterseniz:

```powershell
.\.venv\Scripts\python.exe .\hand_mouse.py --smoothing 0.18
```

İmleç ekran kenarlarına zor ulaşıyorsa:

```powershell
.\.venv\Scripts\python.exe .\hand_mouse.py --margin 0.08
```

## Güvenlik Notu

PyAutoGUI'de acil durdurma açıktır. Fare imlecini ekranın sol üst köşesine götürürseniz program kendini durdurabilir.
