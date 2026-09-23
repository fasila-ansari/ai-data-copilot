import os
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Streamlit UI Setup
st.set_page_config(
    page_title="Enterprise AI Data Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Enterprise AI Data Copilot")
st.caption("Upload CSV or Excel files to run natural language queries, profile datasets, and generate instant charts.")

# Sidebar - API Key Configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")

if not api_key:
    st.warning("⚠️ Please enter a Groq API key in the sidebar to activate the AI agent.")
    st.stop()

# Initialize LLM with Groq
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=api_key,
    temperature=0
)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# File Upload Section
uploaded_file = st.sidebar.file_uploader("Upload Dataset (.csv, .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # --- SECTION 1: AUTOMATED DATA PROFILING ---
    st.subheader("1. Automated Data Health Check")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", f"{df.shape[0]:,}")
    col2.metric("Total Columns", f"{df.shape[1]}")
    col3.metric("Duplicate Rows", f"{df.duplicated().sum()}")
    col4.metric("Missing Values", f"{df.isnull().sum().sum()}")

    with st.expander("📄 View Raw Dataset & Schema", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

    # --- SECTION 2: NATURAL LANGUAGE INTERACTION ---
    st.markdown("---")
    st.subheader("2. Conversational Analytics Engine")

    # Render previous conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "text" in msg:
                st.write(msg["text"])
            if "dataframe" in msg:
                st.dataframe(msg["dataframe"])
                # Download CSV Button for historical data
                csv_data = msg["dataframe"].to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Data CSV",
                    data=csv_data,
                    file_name="query_result.csv",
                    mime="text/csv",
                    key=f"dl_df_{msg['id']}"
                )
            if "plot" in msg:
                st.image(msg["plot"])
                # Download Chart Button
                st.download_button(
                    label="🖼️ Download Chart PNG",
                    data=msg["plot"],
                    file_name="chart.png",
                    mime="image/png",
                    key=f"dl_chart_{msg['id']}"
                )

    user_query = st.chat_input("Ask a question about your dataset...")

    if user_query:
        # Append User Message to History
        st.session_state.messages.append({"role": "user", "text": user_query})
        st.chat_message("user").write(user_query)
        
        with st.chat_message("assistant"):
            with st.spinner("AI agent analyzing dataset..."):
                try:
                    prompt = f"""
                    You are an expert Data Analyst working with a Pandas DataFrame named `df`.
                    
                    Dataset Columns: {list(df.columns)}
                    Dataset Head:
                    {df.head(3).to_string()}
                    
                    User Query: "{user_query}"
                    
                    Instructions:
                    1. Write Python code using pandas (`df`) to calculate the answer or generate a matplotlib plot.
                    2. Return ONLY executable Python code blocks inside markdown ```python ... ```.
                    3. Format monetary/sales numbers nicely with commas if applicable.
                    4. Assign the final tabular or textual output to a variable named `result` or build a plot with matplotlib.
                    """

                    response = llm.invoke(prompt)
                    raw_content = response.content

                    if "```python" in raw_content:
                        code = raw_content.split("```python")[1].split("```")[0].strip()
                    elif "```" in raw_content:
                        code = raw_content.split("```")[1].split("```")[0].strip()
                    else:
                        code = raw_content.strip()

                    exec_globals = {"df": df, "pd": pd, "plt": plt, "sns": sns}
                    exec_locals = {}
                    
                    exec(code, exec_globals, exec_locals)

                    msg_id = len(st.session_state.messages)
                    assistant_entry = {"role": "assistant", "id": msg_id}

                    # Handle DataFrame/Text Result
                    if "result" in exec_locals or "result" in exec_globals:
                        res = exec_locals.get("result", exec_globals.get("result"))
                        if isinstance(res, pd.DataFrame):
                            st.dataframe(res)
                            csv_bytes = res.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                label="📥 Download Data CSV",
                                data=csv_bytes,
                                file_name="query_result.csv",
                                mime="text/csv",
                                key=f"dl_df_{msg_id}"
                            )
                            assistant_entry["dataframe"] = res
                        else:
                            st.write(res)
                            assistant_entry["text"] = str(res)

                    # Handle Plot Output
                    fig = plt.gcf()
                    if fig.get_axes():
                        buf = io.BytesIO()
                        plt.savefig(buf, format="png", bbox_inches="tight")
                        buf.seek(0)
                        image_bytes = buf.getvalue()
                        
                        st.pyplot(fig)
                        st.download_button(
                            label="🖼️ Download Chart PNG",
                            data=image_bytes,
                            file_name="chart.png",
                            mime="image/png",
                            key=f"dl_chart_{msg_id}"
                        )
                        assistant_entry["plot"] = image_bytes
                        plt.clf()

                    st.session_state.messages.append(assistant_entry)

                except Exception as err:
                    st.error(f"Execution Error: {err}")
else:
    st.info("👈 Please upload a CSV or Excel dataset from the sidebar to begin.")