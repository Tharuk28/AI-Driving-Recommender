import streamlit as st
import pandas as pd
import openpyxl
import requests
import os

st.set_page_config(page_title="AI V2V Safety Recommender", layout="wide")

# ------------------- Config -------------------
OLLAMA_URL = "https://customs-delayed-explorer-fetish.trycloudflare.com"
MODEL_NAME = "gemma2:2b"
EXCEL_PATH = "drive_data_example.xlsx"  # Local path inside repo

# ------------------- Recommender -------------------
class GemmaRecommender:
    def __init__(self):
        self.url = f"{OLLAMA_URL}/api/chat"

    def generate_text(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.url,
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"⚠️ Error generating recommendation: {str(e)}"

@st.cache_resource
def load_model():
    return GemmaRecommender()

gemma = load_model()

st.title("🚗 AI-Based Vehicle-to-Vehicle Safety Recommender")

# ------------------- Auto Load Excel -------------------
try:
    df = pd.read_excel(EXCEL_PATH)
    st.subheader("📊 Preview of Input Data")
    st.dataframe(df)

    if st.button("Generate AI Recommendations"):
        st.subheader("📌 AI Recommendations:")
        with st.spinner("Generating safety actions..."):
            for idx, row in df.iterrows():
                context = (
                    f"Speed = {row['Speed (km/h)']} km/h, "
                    f"{row['Brake Pattern']}, "
                    f"{row['Time of Day']} time, "
                    f"{row['Road Type']} road with {row['Traffic']} traffic."
                )

                prompt = f"Given the driving context: {context}, recommend a safety warning or action for the driver."
                recommendation = gemma.generate_text(prompt)

                with st.expander(f"DATA {idx+1}"):
                    st.markdown(f"**Context:** {context}")
                    st.markdown(f"**AI Recommendation:** {recommendation}")

except FileNotFoundError:
    st.error(f"⚠️ Excel file not found at `{EXCEL_PATH}`")
except Exception as e:
    st.error(f"⚠️ Error processing Excel file: {e}")
