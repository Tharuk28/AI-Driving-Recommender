import streamlit as st
import pandas as pd
import ollama  # Do not override this later

# Set Streamlit page config (must be first!)
st.set_page_config(page_title="AI V2V Safety Recommender", layout="wide")

# Gemma Recommender using Ollama
class GemmaRecommender:
    def __init__(self):
        self.model_name = "gemma2:2b"

    def generate_text(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            return f"⚠️ Error generating recommendation: {str(e)}"

# Load the model once
@st.cache_resource
def load_model():
    return GemmaRecommender()

gemma = load_model()

st.title("🚗 AI-Based Vehicle-to-Vehicle Safety Recommender")

# Auto-read Excel file
EXCEL_PATH = "D:\Tharuk\College Files\Final Project\Final Project Phase 2\AI Model\drive_data_example.xlsx"  # Update with actual path

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
    st.error(f"Excel file not found at: `{EXCEL_PATH}`")
except Exception as e:
    st.error(f"Error reading Excel file: {e}")
