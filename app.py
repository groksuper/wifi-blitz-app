import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# تحميل النموذج من Hugging Face
model_name = "sir-evil/my-first-model"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# إعداد واجهة المستخدم
st.title("WiFi Blitz Pro - Text Classification")
st.markdown("**تعليمات**: أدخل نصًا باللغة الإنجليزية (حتى 512 حرفًا) وسيتم تصنيفه كـ Positive أو Negative.")

# أمثلة نصوص جاهزة
example_texts = ["This is a great app!", "I hate this service.", "The sky is blue today."]
selected_example = st.selectbox("اختر نصًا تجريبيًا:", example_texts)

# إدخال نص من المستخدم
text = st.text_area("أدخل النص لتصنيفه (يمكنك استخدام النص التجريبي):", selected_example)

if st.button("صنّف النص"):
    with st.spinner("جارٍ التصنيف..."):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        labels = ["Negative", "Positive"]
        st.write(f"**التصنيف**: <span style='color:green'>{labels[predicted_class]}</span>", unsafe_allow_html=True)
