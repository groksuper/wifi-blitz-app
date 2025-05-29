import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification, CLIPProcessor, CLIPModel
import torch
from PIL import Image
import requests
from io import BytesIO

# تحميل نموذج التصنيف النصي (دعم الإنجليزية والعربية)
model_name_text = "aubmindlab/bert-base-arabertv2"  # نموذج عربي
tokenizer_text = BertTokenizer.from_pretrained(model_name_text)
model_text = BertForSequenceClassification.from_pretrained(model_name_text, num_labels=2)

# تحميل نموذج تحليل الصور (CLIP)
model_name_image = "openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(model_name_image)
model_image = CLIPModel.from_pretrained(model_name_image)

# إعداد واجهة المستخدم
st.title("WiFi Blitz Pro - Text & Image Analysis")
st.markdown("**تعليمات**: أدخل نصًا (حتى 512 حرفًا) أو ارفع صورة للتحليل والإجابة الذكية.")

# قسم التصنيف النصي
st.subheader("تحليل النصوص")
example_texts = ["This is a great app!", "أحب هذا التطبيق", "I hate this service.", "أكره هذه الخدمة", "The sky is blue today."]
selected_text = st.selectbox("اختر نصًا تجريبيًا:", example_texts)
user_text = st.text_area("أدخل نصًا للتصنيف:", selected_text)

if st.button("صنّف النص"):
    with st.spinner("جارٍ التصنيف..."):
        inputs = tokenizer_text(user_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model_text(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        labels = ["Negative", "Positive"]
        arabic_labels = ["سلبي", "إيجابي"]
        st.markdown(f"**التصنيف**: <span style='color:red'>{arabic_labels[predicted_class]}</span> - <span style='color:green'>{labels[predicted_class]}</span>", unsafe_allow_html=True)

# قسم تحليل الصور
st.subheader("تحليل الصور")
uploaded_image = st.file_uploader("ارفع صورة للتحليل", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    with st.spinner("جارٍ تحليل الصورة..."):
        # تحميل الصورة
        image = Image.open(uploaded_image).convert("RGB")
        inputs = processor(images=image, return_tensors="pt", padding=True)
        
        # توليد الوصف
        outputs = model_image.get_image_features(**inputs)
        # محاكاة إجابة ذكية (يمكن تحسينها بتدريب إضافي)
        description = "الصورة تحتوي على مشهد طبيعي رائع."  # مثال، يمكن تحسينه
        st.image(image, caption="الصورة المرفوعة")
        st.write(f"**الوصف**: {description}")

# قسم الدردشة الأساسية (اختياري)
st.subheader("دردشة ذكية")
user_chat = st.text_input("أدخل رسالتك للدردشة:")
if st.button("أرسل"):
    with st.spinner("جارٍ التفكير..."):
        inputs = tokenizer_text(user_chat, return_tensors="pt")
        # محاكاة رد ذكيت (يمكن تحسينه بنموذج محادثة)
        response = "أنا أفهمك! هل يمكنني مساعدتك في شيء آخر؟"
        st.write(f"**الرد**: {response}")

# تحسينات بصرية
st.markdown("<style>body {background-color: #1a1a1a; color: white;}</style>", unsafe_allow_html=True)
