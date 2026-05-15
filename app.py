import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Modeli yükle
model = joblib.load('churn_model.pkl')

st.set_page_config(page_title="Churn Risk Analiz", page_icon="📞")

st.title("📞 Telco Müşteri Kayıp (Churn) Riski Analizi")
st.markdown("""
Bu uygulama, müşteri verilerini analiz ederek **abonelik iptal riskini** hesaplar. 
Şirketin müşteri tutma (retention) stratejileri için geliştirilmiştir.
""")

# Giriş alanları (Modelin beklediği ana değişkenler)
col1, col2 = st.columns(2)

with col1:
    contract = st.selectbox("Sözleşme Tipi", ["Month-to-month", "One year", "Two year"])
    tenure = st.slider("Kaç Aydır Müşteri?", 0, 72, 12)
    monthly_charges = st.number_input("Aylık Ödeme ($)", value=65.0)

with col2:
    online_security = st.selectbox("Online Güvenlik Var mı?", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Teknik Destek Var mı?", ["Yes", "No", "No internet service"])
    total_charges = st.number_input("Toplam Ödeme ($)", value=500.0)

# Tahmin Butonu
if st.button("Risk Skorunu Hesapla"):
    # Basit bir mapping (Encoder'ların değerlerine göre - Gerçek model sütun sırasına dikkat!)
    # Not: Modelin tam sütun listesini doldurmak için örnek değerler ekliyoruz
    input_df = pd.DataFrame(np.zeros((1, 19))) # Model 19 sütun bekliyor
    
    # Tahmin yap
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1] # Risk olasılığı
    
    if prediction == 1:
        st.error(f"### ⚠️ YÜKSEK RİSK! Müşteri kaybı olasılığı: %{prob*100:.1f}")
        st.write("👉 **Öneri:** Bu müşteriye indirimli yıllık paket veya sadakat puanı teklif edilmeli.")
    else:
        st.success(f"### ✅ GÜVENLİ. Müşteri kaybı olasılığı düşük: %{prob*100:.1f}")
        st.write("👉 **Öneri:** Standart hizmet devam ettirilebilir.")