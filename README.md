# yapay-zeka-asistani

Streamlit ve Google Gemini API (`gemini-3.6-flash`) kullanılarak geliştirilmiş, özelleştirilmiş sistem istemleri (prompts) ve anlık maliyet takibi sunan minimalist bir sohbet arayüzü.

## Özellikler

- **Model Entegrasyonu:** Gemini 3.6 Flash ile hızlı ve akıcı yanıt akışı (streaming).
- **Uzmanlık Modları:** Kod analizi, dil koçluğu, doküman özeti ve matematik için hazır yönlendirmeler.
- **Multimodal Desteği:** Görsel (PNG, JPG) ve dosya (PDF, TXT) yükleyip analiz ettirme.
- **Token & Maliyet Takibi:** Kullanılan girdi/çıktı token sayıları ve anlık tahmini API maliyeti hesabı.
- **Arayüz:** Koyu tema odaklı, minimalist sohbet arayüzü.

## Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/yredNN/yapay-zeka-asistani.git](https://github.com/yredNN/yapay-zeka-asistani.git)
   cd yapay-zeka-asistani

2. Bağımlılıkları yükleyin:
    pip install -r requirements.txt

3. API Anahtarını Tanımlayın:
    .streamlit/secrets.toml dosyası oluşturup içine API anahtarınızı ekleyin:
    GEMINI_API_KEY = "your_api_key_here"

4. Uygulamayı çalıştırın:
    streamlit run app.py
