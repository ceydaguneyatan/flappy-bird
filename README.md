# 🕹️ El Hareketi ile Oynanan Flappy Bird

Bu proje, klasik Flappy Bird oyununa modern bir dokunuş getiriyor: Oyuncular kuşu el hareketleri ile kontrol ediyor! Bilgisayar kamerası yardımıyla el pozisyonunu algılayarak oyundaki kuşun dikey konumunu ayarlayabilir, böylece gelen boralardan kaçabilirsiniz.

## 📌 Özellikler

- ✋ **El Hareketi ile Kontrol:** MediaPipe kütüphanesi kullanılarak webcam üzerinden elin işaret parmağı algılanır ve kuşun Y eksenindeki konumu bu veriye göre belirlenir.
- ❤️ **3 Can Sistemi:** Oyuncunun 3 canı vardır. Her çarpışmada bir can kaybedilir, canlar bittiğinde oyun biter.
- 💥 **Geçici Çarpışmazlık ve Kontrol Kilidi:** Çarpışmadan sonra kısa bir süre çarpışma algılanmaz (30 frame), ayrıca kuş kontrolü bir süre kilitlenir (20 frame).
- 🔁 **Oyun Yeniden Başlatma:** SPACE tuşu ile oyun her an yeniden başlatılabilir.
- 🖼️ **Görseller ve Arka Planlar:** Özelleştirilmiş arka plan, zemin, kuş, boru ve kalp görselleri.
- 🎮 **Başlangıç ve Bitiş Ekranları:** Başlangıçta “Press SPACE to Start”, oyun sonunda ise skor gösterimi ve yeniden başlatma ekranı bulunur.
- 🔊 **Pygame ile Ses ve Grafik Desteği (opsiyonel):** Gerekirse ses efektleri ve ek animasyonlar da entegre edilebilir.

## 🛠️ Kullanılan Teknolojiler

- **Python 3**
- **OpenCV** – Webcam görüntüsünü almak için
- **MediaPipe** – El takibi için
- **Pygame** – Oyun motoru, grafik ve olay yönetimi için

## 🎮 Oynanış

1. Oyunu başlattığınızda başlangıç ekranı gelir.
2. SPACE tuşuna basarak oyuna girilir.
3. Elinizi kameraya göstererek işaret parmağınızı yukarı-aşağı hareket ettirerek kuşu kontrol edebilirsiniz.
4. Engellerden kaçınarak skorunuzu artırın!
5. Çarpışınca can kaybedersiniz; canlar bittiğinde "Game Over" ekranı gösterilir.
6. SPACE tuşu ile oyunu yeniden başlatabilirsiniz.

## 🚀 Başlatmak için

### Gereksinimler

- Python 3
- `mediapipe`
- `opencv-python`
- `pygame`

### Kurulum

```bash
pip install mediapipe opencv-python pygame
