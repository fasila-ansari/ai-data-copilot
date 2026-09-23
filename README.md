# 📊 Enterprise AI Data Copilot

An interactive data analysis and conversational analytics web application built with **Streamlit**, **Pandas**, and **LangChain-Groq**. Upload CSV or Excel datasets to profile data, generate summary metrics, and run natural language queries with automated chart visualizations.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Groq-green)

---

## ✨ Features

- **Automated Data Profiling**: Instant dataset breakdown including total rows, column counts, missing values, and duplicate record checks.
- **Conversational Analytics**: Ask questions about your dataset in plain English and receive instant analytical summaries.
- **Dynamic Visualizations**: Automatically generates bar charts, trends, and plots based on query intent.
- **Multi-Format Support**: Native handling for both `.csv` and multi-tab `.xlsx` Excel spreadsheets.
- **Export Capabilities**: Download processed data subsets as CSV files or export generated charts as PNG images.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: Streamlit
- **LLM Orchestration**: LangChain, Groq API (Llama 3 / Mixtral models)
- **Data Manipulation**: Pandas, OpenPyXL
- **Data Visualization**: Matplotlib, Seaborn

---

## 🚀 Live Demo

Check out the live application on Streamlit Cloud:  
👉 **[Enterprise AI Data Copilot](https://ai-data-copilot-7e8qwktkudqbjyzfjphna.streamlit.app)**

---

## 💻 Local Setup & Installation

1. **Clone the repository**:
```bash
git clone https://github.com/fasila-ansari/ai-data-copilot.git
cd ai-data-copilot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```
3. **Configure Environment Variables**:
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key_here"
```
4. **Run the Streamlit application**:
```bash
streamlit run app.py
```
