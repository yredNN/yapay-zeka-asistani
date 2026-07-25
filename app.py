import io
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

MODEL_NAME = "gemini-3.6-flash"

st.set_page_config(
    page_title="Yapay Zeka Asistanı",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif !important;
        }

        .stApp {
            background: radial-gradient(circle at 50% -10%, #1c1c22 0%, #0d0d11 100%) !important;
            background-attachment: fixed !important;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        div[data-testid="stHeader"] > div:nth-child(1) > button {
            visibility: visible !important;
            z-index: 99999 !important;
            border-radius: 50% !important;
            width: 34px !important;
            height: 34px !important;
            background-color: rgba(255, 255, 255, 0.06) !important;
            backdrop-filter: blur(12px) !important;
            color: #f5f5f7 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stHeader"] > div:nth-child(1) > button:hover {
            background-color: rgba(255, 255, 255, 0.18) !important;
            border-color: rgba(255, 255, 255, 0.28) !important;
            transform: scale(1.05);
        }

        section[data-testid="stSidebar"] {
            background-color: rgba(20, 20, 23, 0.65) !important;
            backdrop-filter: blur(25px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        @keyframes slideDown {
            0% { opacity: 0; transform: translateY(-30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes typingPulse {
            0%, 100% { opacity: 0.25; transform: scale(0.92); }
            50% { opacity: 1; transform: scale(1.08); }
        }

        div[data-testid="stChatMessage"] div[data-testid="stChatMessageContent"]:not(:has(p))::after,
        div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"]:empty::after {
            content: "• • •";
            display: inline-block;
            font-size: 1.3rem;
            letter-spacing: 4px;
            color: rgba(255, 255, 255, 0.8);
            animation: typingPulse 1.2s infinite ease-in-out;
            padding: 2px 6px;
        }

        .animated-header {
            animation: slideDown 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        [data-testid*="ChatMessageAvatar"],
        [data-testid*="stChatMessageAvatar"],
        [data-testid*="avatar"],
        div[data-testid="stChatMessage"] > div:first-child:not([data-testid="stChatMessageContent"]) {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stChatMessage"] {
            width: fit-content !important;
            max-width: 80% !important;
            min-width: 54px !important;
            padding: 12px 18px !important;
            margin-bottom: 14px !important;
            backdrop-filter: blur(16px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
            animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            transition: all 0.2s ease-in-out !important;
            gap: 0 !important;
        }

        div[data-testid="stChatMessage"]:has(div[aria-label*="user"]),
        div[data-testid="stChatMessage"]:has(span[aria-label*="user"]) {
            margin-left: auto !important;
            margin-right: 0 !important;
            background: linear-gradient(135deg, #007aff 0%, #0051a8 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px 20px 4px 20px !important;
        }

        div[data-testid="stChatMessage"]:has(div[aria-label*="assistant"]),
        div[data-testid="stChatMessage"]:has(span[aria-label*="assistant"]) {
            margin-left: 0 !important;
            margin-right: auto !important;
            background-color: rgba(255, 255, 255, 0.06) !important;
            color: #f5f5f7 !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 20px 20px 20px 4px !important;
        }

        .stChatInput > div {
            border-radius: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            background-color: rgba(255, 255, 255, 0.04) !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25) !important;
        }

        .stChatInput > div:focus-within {
            border-color: rgba(255, 255, 255, 0.35) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2) !important;
        }

        .stButton > button, div[data-testid="stPopover"] > button {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #f5f5f7 !important;
            transition: all 0.2s ease-in-out !important;
            font-weight: 500 !important;
        }
        
        .stButton > button:hover, div[data-testid="stPopover"] > button:hover {
            border-color: rgba(255, 255, 255, 0.3) !important;
            background-color: rgba(255, 255, 255, 0.12) !important;
            transform: scale(1.01);
        }

        .token-card {
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 14px;
            margin-top: 10px;
            backdrop-filter: blur(12px);
        }
    </style>
""", unsafe_allow_html=True)

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0

if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0

if "prompt_to_use" not in st.session_state:
    st.session_state.prompt_to_use = None

with st.sidebar:
    st.header("⚙️ Ayarlar & Dosyalar")
    st.write(f"Model: **{MODEL_NAME}**")
    st.divider()

    with st.popover("➕ Dosya / Görsel Ekle", use_container_width=True):
        uploaded_file = st.file_uploader(
            "Bir dosya seçin", 
            type=["png", "jpg", "jpeg", "pdf", "txt"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            file_type = uploaded_file.type
            if "image" in file_type:
                st.session_state.uploaded_image = Image.open(uploaded_file)
                st.session_state.uploaded_doc = None
                st.image(st.session_state.uploaded_image, caption="Seçilen Görsel", use_container_width=True)
            else:
                st.session_state.uploaded_doc = {
                    "name": uploaded_file.name,
                    "bytes": uploaded_file.getvalue(),
                    "type": file_type
                }
                st.session_state.uploaded_image = None
                st.info(f"📄 **{uploaded_file.name}** yüklendi.")

    if st.session_state.get("uploaded_image") is not None:
        st.success("📷 Görsel gönderilmeye hazır!")
    elif st.session_state.get("uploaded_doc") is not None:
        st.success(f"📄 {st.session_state.uploaded_doc['name']} gönderilmeye hazır!")

    st.divider()

    st.markdown("### 📊 Kullanım & Maliyet")
    total_tokens = st.session_state.total_input_tokens + st.session_state.total_output_tokens
    est_cost = (st.session_state.total_input_tokens * 0.000000075) + (st.session_state.total_output_tokens * 0.00000030)

    st.markdown(f"""
        <div class="token-card">
            <div style="font-size: 0.85rem; color: #a1a1a6;">Girdi / Çıktı Token:</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #f5f5f7;">{st.session_state.total_input_tokens:,} / {st.session_state.total_output_tokens:,}</div>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 8px 0;">
            <div style="font-size: 0.85rem; color: #a1a1a6;">Tahmini Maliyet:</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #30d158;">${est_cost:.6f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("Sohbeti Temizle", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("""
    <div class="animated-header" style="text-align: center; padding: 15px 0 20px 0;">
        <h1 style="font-weight: 600; font-size: 2.2rem; letter-spacing: -0.6px; color: #f5f5f7; margin-bottom: 6px;">
            Yapay Zeka Asistanım
        </h1>
    </div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image") is not None:
            st.image(message["image"], width=300)
        if message.get("doc") is not None:
            st.info(f"📄 Doküman: {message['doc']['name']}")
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("""
        <p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.9rem; margin-bottom: 12px;'>
            Nereden başlamak istersiniz?
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Kod Mimarisini İncele", use_container_width=True):
            st.session_state.prompt_to_use = "Kodumu kıdemli bir yazılım mimarı gözüyle incele: Clean Code, güvenlik, performans (Big-O) ve mimari açıdan analiz et."
            st.rerun()
        if st.button("🇬🇧 İleri Seviye İngilizce Koçu", use_container_width=True):
            st.session_state.prompt_to_use = "Seninle profesyonel İngilizce pratik yapmak istiyorum. Cümlelerimi doğal konuşma kalıplarına (idioms) göre optimize et ve hatalarımı detaylandır."
            st.rerun()
    with col2:
        if st.button("📄 Doküman Analizi & Sentez", use_container_width=True):
            st.session_state.prompt_to_use = "Yüklediğim dokümanı/metni bir kıdemli araştırmacı gibi analiz et: Yönetici Özeti (Executive Summary), Kritik Bulgular ve Eylem Adımları çıkar."
            st.rerun()
        if st.button("📐 Matematik & Derin Mantık", use_container_width=True):
            st.session_state.prompt_to_use = "Karmaşık bir matematik/mantık problemini adım adım pedagojik derinlikle açıkla, teoremleri ve ispat adımlarını göster."
            st.rerun()

prompt_input = st.chat_input("Mesajınızı yazın...")
prompt = prompt_input or st.session_state.prompt_to_use

if prompt:
    st.session_state.prompt_to_use = None

    current_image = st.session_state.get("uploaded_image", None)
    current_doc = st.session_state.get("uploaded_doc", None)

    with st.chat_message("user"):
        if current_image:
            st.image(current_image, width=300)
        if current_doc:
            st.info(f"📄 Doküman: {current_doc['name']}")
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "image": current_image,
        "doc": current_doc
    })

    formatted_history = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        parts = []

        if msg.get("image") is not None:
            img_byte_arr = io.BytesIO()
            msg["image"].save(img_byte_arr, format="PNG")
            parts.append(
                types.Part.from_bytes(data=img_byte_arr.getvalue(), mime_type="image/png")
            )

        if msg.get("doc") is not None:
            parts.append(
                types.Part.from_bytes(
                    data=msg["doc"]["bytes"], 
                    mime_type=msg["doc"]["type"]
                )
            )
            
        parts.append(types.Part.from_text(text=msg["content"]))
        formatted_history.append(types.Content(role=role, parts=parts))

    EXPERT_SYSTEM_INSTRUCTION = """
    Sen yüzeysel ve genelgeçer cevaplar veren sıradan bir yapay zeka değilsin. Girdiğin her rolde alanının en üst düzey yetkili uzmanı (Principal / Master / Lead) gibi davranan, derinlikli, yapıcı ve yüksek kaliteli yanıtlar üreten üst seviye bir Asistansın.

    Kullanıcının girdisine göre aşağıdaki UZMANLIK MODLARINDAN birine OTOMATİK olarak geç ve o yetkinlikle yanıt ver:

    🎯 1. YAZILIM & MİMARİ UZMANI (Principal Software Engineer)
    - Yalnızca çalışan kod vermekle kalma; kodun performansını (Big-O zaman/hafıza karmaşıklığı), güvenliğini, okunabilirliğini ve 'Clean Code' prensiplerine uygunluğunu analiz et.
    - Tasarım desenleri (Design Patterns), kenar durumlar (Edge Cases) ve best-practice'leri belirt.
    - Hata tespitinde hatanın kök nedenini (Root Cause) açıkla ve refactored (iyileştirilmiş) temiz kodu sun.

    🎓 2. DİL & DİLBİLİM UZMANI (Native Master English Coach)
    - Kullanıcının İngilizce seviyesini (CEFR: A1-C2) göz önünde bulundurarak doğal ve profesyonel öneriler sun.
    - Gramer hatalarını düzeltirken hatanın mantığını, neden öyle olduğunu ve ana dili İngilizce olan kişilerin (native speakers) o ifadeyi daha doğal nasıl kullandığını (idioms, phrasal verbs) açıkla.

    📑 3. DERİN DOKÜMAN & VERİ ANALİSTİ (Lead Academic Researcher)
    - Yüklenen PDF/Metin içeriklerini bir kıdemli analist gibi parçala.
    - Yanıtlarını 'Yönetici Özeti (Executive Summary)', 'Kritik Bulgular & Sentez' ve 'Eylem Adımları / Çıkarımlar' şeklinde yapılandırılmış markdown ile sun.

    🧮 4. MATEMATİK & MANTIK PROFESÖRÜ (Mathematics Professor)
    - Soruları doğrudan sonuç verip geçmek yerine; teoremleri, mantıksal adımları ve formülleri adım adım, pedagojik bir derinlikle açıkla.

    💬 5. GENEL SOHBET & DANIŞMAN (Grounded Adaptive Collaborator)
    - Samimi, zeki, empati kuran ve yapıcı bir tonda iletişim kur. Net, etkileyici ve ufuk açıcı yanıtlar ver.

    📌 GENEL UZMANLIK PRENSİPLERİ:
    - Yanıtların sonunda, eğer konuyu bir adım öteye taşıyacaksa **"💡 Uzman Tavsiyesi (Pro-Tip):"** başlığı altında ekstra bir püf noktası veya perspektif ekle.
    """

    with st.chat_message("assistant"):
        try:
            try:
                in_token_res = client.models.count_tokens(
                    model=MODEL_NAME,
                    contents=formatted_history
                )
                st.session_state.total_input_tokens += in_token_res.total_tokens
            except Exception:
                st.session_state.total_input_tokens += len(str(formatted_history)) // 4

            response_stream = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=formatted_history,
                config=types.GenerateContentConfig(
                    system_instruction=EXPERT_SYSTEM_INSTRUCTION
                )
            )
            
            full_response = st.write_stream(
                chunk.text for chunk in response_stream if chunk.text
            )

            if full_response:
                out_tokens = max(1, len(full_response) // 4)
                st.session_state.total_output_tokens += out_tokens

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "image": None,
                    "doc": None
                })

                st.session_state.uploaded_image = None
                st.session_state.uploaded_doc = None
                st.rerun()

        except APIError as e:
            if "403" in str(e) or "PERMISSION_DENIED" in str(e):
                st.error("🚫 **Erişim Engellendi (403):** Lütfen [Google AI Studio](https://aistudio.google.com/) üzerinden geçerli bir API Key aldığınızdan emin olun.")
            elif "404" in str(e) or "NOT_FOUND" in str(e):
                st.error(f"❌ **Model Bulunamadı (404):** Google API tarafında '{MODEL_NAME}' isminde bir model bulunamadı.")
            else:
                st.warning(f"⚠️ **API Hatası:** {e}")
        except Exception as e:
            st.error(f"⚠️ **Beklenmeyen Hata:** {e}")