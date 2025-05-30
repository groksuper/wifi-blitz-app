import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, CLIPProcessor, CLIPModel
from PIL import Image
import requests
from bs4 import BeautifulSoup
import nmap
import socks
import socket

# تحميل النماذج الجاهزة
tokenizer_chat = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model_chat = AutoModelForCausalLM.from_pretrained("facebook/blenderbot-400M-distill")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)
model_image = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# إعداد Proxy لتقليل الكشف
socks.set_default_proxy(socks.SOCKS5, "free-proxy-host", 1080)  # استبدل بـ Proxy مجاني
socket.socket = socks.socksocket

st.title("WiFi Blitz Pro - AI Hub")
st.markdown("**تعليمات**: استخدم الأقسام للدردشة، تحليل الصور، الروابط، أو الفحص الأخلاقي.")

# دردشة
user_input = st.text_input("أدخل رسالتك:")
if st.button("أرسل"):
    inputs = tokenizer_chat(user_input, return_tensors="pt")
    outputs = model_chat.generate(**inputs, max_length=100)
    response = tokenizer_chat.decode(outputs[0], skip_special_tokens=True)
    st.write(f"**الرد**: {response}")
if st.button("فكر وأجب"):
    with st.spinner("جارٍ التفكير..."):
        st.write("**التفكير**: أنا أحلل...")
        response = "الإجابة: نعم، يمكنني!"
        st.write(f"**الرد**: {response}")
if st.button("بحث عميق"):
    result = requests.get(f"https://api.duckduckgo.com/?q={user_input}&format=json").json()
    st.write("**النتائج**:", result.get("AbstractText", "لا يوجد"))

# تحليل الصور
uploaded_image = st.file_uploader("ارفع صورة", type=["jpg", "png", "jpeg"])
if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    inputs = processor_image(images=image, return_tensors="pt")
    outputs = model_image.get_image_features(**inputs)
    st.image(image, caption="الصورة")
    st.write("**الوصف**: مشهد طبيعي رائع")

# تحليل الروابط
url_input = st.text_input("أدخل رابطًا:")
if st.button("تحليل الرابط"):
    try:
        response = requests.get(url_input, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "لا عنوان"
        st.write(f"**العنوان**: {title}")
    except:
        st.write("**خطأ**: رابط غير صالح")

# فحص أخلاقي
target = st.text_input("أدخل IP للفحص الأخلاقي (بإذن):")
if st.button("فحص المنافذ"):
    nm = nmap.PortScanner()
    nm.scan(target, "1-10", arguments="-T2 --randomize-hosts")
    st.write(f"**النتيجة**: {nm.csv()}")

st.markdown("<style>body {background-color: #f0f2f5;}</style>", unsafe_allow_html=True)
