import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
import hmac
import re
import html

from nutrition_agent import NutritionAgent
from diet_agent import DietRecommendationAgent
from health_agent import HealthAdvisoryAgent
from food_log_agent import FoodLogAgent

from database import (
    create_tables,
    save_meal,
    get_meal_logs
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NutriAI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

create_tables()

FEEDBACK_DB = "user_feedback.db"


# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "food_result" not in st.session_state:
    st.session_state.food_result = None
# =========================================================
# HEALTH ADVISORY
# =========================================================

elif page == "❤️ Health Advisory":

    st.title("❤️ Health Advisory")

    st.write(
        "Get simple nutrition guidance based on your health needs."
    )

    condition = st.selectbox(
        "What would you like nutrition guidance for?",
        [
            "Healthy",
            "Diabetes",
            "Heart Health",
            "High Blood Pressure",
            "Obesity",
            "PCOS",
            "High Cholesterol",
            "Anemia",
            "General"
        ]
    )

    question = st.text_area(
        "Tell us what you would like to know",
        placeholder="Example: What foods should I include in my diet?"
    )

    if st.button("❤️ Get Health Advice"):

        if not question.strip():

            question = (
                f"Give general nutrition guidance for {condition}"
            )

        try:

            # =================================================
            # FIX:
            # HealthAdvisoryAgent.get_advice()
            # accepts only ONE argument after self.
            # =================================================

            health_query = f"""
Health condition: {condition}

User question:
{question}
"""

            result = health_agent.get_advice(
                health_query
            )

            st.success(
                "Health guidance generated."
            )

            # =================================================
            # DISPLAY RESULT
            # =================================================

            if isinstance(result, dict):

                for key, value in result.items():

                    st.markdown(
                        f"### {key.replace('_', ' ').title()}"
                    )

                    if isinstance(value, list):

                        for item in value:
                            st.write(f"• {item}")

                    else:

                        st.write(value)

            else:

                st.write(result)

            # =================================================
            # MEDICAL DISCLAIMER
            # =================================================

            st.info(
                "⚠️ This information is for general educational "
                "purposes and is not a substitute for professional "
                "medical advice."
            )

        except Exception as e:

            st.error(
                f"Unable to generate health advice: {e}"
            )

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_html_text(value):
    """
    Removes HTML tags such as:
    <li>
    <div>
    <ul>
    <br>
    etc.

    This prevents raw HTML from appearing in the UI.
    """

    if value is None:
        return ""

    if isinstance(value, (list, tuple)):

        cleaned_items = []

        for item in value:
            cleaned_items.append(
                clean_html_text(item)
            )

        return cleaned_items

    if isinstance(value, dict):

        cleaned_dict = {}

        for key, item in value.items():
            cleaned_dict[key] = clean_html_text(item)

        return cleaned_dict

    text = str(value)

    # Replace common HTML line breaks
    text = re.sub(
        r"<\s*br\s*/?\s*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Replace list item tags with bullets
    text = re.sub(
        r"<\s*li\s*>",
        "• ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"<\s*/\s*li\s*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Remove remaining HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # Decode HTML entities
    text = html.unescape(text)

    # Clean excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


def display_result_value(value):
    """
    Displays agent results cleanly without exposing
    raw HTML markup.
    """

    if value is None:
        return

    if isinstance(value, pd.DataFrame):

        st.dataframe(
            value,
            use_container_width=True
        )

        return

    if isinstance(value, dict):

        for key, item in value.items():

            st.markdown(
                f"### {str(key).replace('_', ' ').title()}"
            )

            display_result_value(item)

        return

    if isinstance(value, list):

        for item in value:

            cleaned = clean_html_text(item)

            if cleaned:
                st.markdown(
                    f"- {cleaned}"
                )

        return

    cleaned_value = clean_html_text(value)

    if cleaned_value:

        st.write(cleaned_value)


# =========================================================
# DARK / LIGHT MODE SETTINGS
# =========================================================

st.sidebar.markdown("## ⚙️ Settings")

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)


# =========================================================
# DARK MODE CSS
# =========================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL DARK MODE
        ===================================================== */

        .stApp {
            background-color: #0e1117 !important;
            color: #ffffff !important;
        }

        .main {
            background-color: #0e1117 !important;
        }

        .block-container {
            color: #ffffff !important;
        }


        /* =====================================================
           GLOBAL TEXT
        ===================================================== */

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            color: #ffffff !important;
        }

        .stApp p,
        .stApp li,
        .stApp label {
            color: #ffffff !important;
        }

        [data-testid="stMarkdownContainer"] {
            color: #ffffff !important;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] strong {
            color: #ffffff !important;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] [data-baseweb="radio"] label {
            color: #ffffff !important;
        }


        /* =====================================================
           CARDS
        ===================================================== */

        .dashboard-card,
        .agent-card,
        .info-card {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;

            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }


        /* =====================================================
           CARD HOVER EFFECT
        ===================================================== */

        .dashboard-card:hover,
        .agent-card:hover,
        .info-card:hover {
            transform: translateY(-6px);
            box-shadow:
                0 10px 25px rgba(0, 0, 0, 0.35);
            border-color: #2ea043 !important;
        }


        /* =====================================================
           METRICS
        ===================================================== */

        [data-testid="stMetric"] {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 15px;

            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.30);
            border-color: #2ea043 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #c9d1d9 !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }

        [data-testid="stMetricDelta"] {
            color: #ffffff !important;
        }


        /* =====================================================
           TEXT INPUT
        ===================================================== */

        [data-testid="stTextInput"] {
            color: #ffffff !important;
        }

        [data-testid="stTextInput"] input {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border: 1px solid #484f58 !important;
            border-radius: 8px !important;
            caret-color: #ffffff !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: #2ea043 !important;
            box-shadow:
                0 0 0 1px #2ea043 !important;
        }

        [data-testid="stTextInput"] input::placeholder {
            color: #8b949e !important;
            opacity: 1 !important;
        }


        /* =====================================================
           TEXT AREA
        ===================================================== */

        [data-testid="stTextArea"] textarea {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border: 1px solid #484f58 !important;
            border-radius: 8px !important;
            caret-color: #ffffff !important;
        }

        [data-testid="stTextArea"] textarea:focus {
            border-color: #2ea043 !important;
            box-shadow:
                0 0 0 1px #2ea043 !important;
        }

        [data-testid="stTextArea"] textarea::placeholder {
            color: #8b949e !important;
            opacity: 1 !important;
        }


        /* =====================================================
           NUMBER INPUT
        ===================================================== */

        [data-testid="stNumberInput"] {
            color: #ffffff !important;
        }

        [data-testid="stNumberInput"] input {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border: 1px solid #484f58 !important;
        }

        [data-testid="stNumberInput"] button {
            background-color: #21262d !important;
            color: #ffffff !important;
            border-color: #484f58 !important;
        }

        [data-testid="stNumberInput"] button:hover {
            background-color: #30363d !important;
        }


        /* =====================================================
           SELECT BOX
        ===================================================== */

        [data-testid="stSelectbox"] {
            color: #ffffff !important;
        }

        [data-testid="stSelectbox"] label {
            color: #ffffff !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] {
            background-color: #161b22 !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border-color: #484f58 !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] * {
            color: #ffffff !important;
        }


        /* =====================================================
           SELECTBOX DROPDOWN
        ===================================================== */

        [role="listbox"] {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border: 1px solid #484f58 !important;
        }

        [role="option"] {
            background-color: #161b22 !important;
            color: #ffffff !important;
        }

        [role="option"] * {
            color: #ffffff !important;
        }

        [role="option"]:hover {
            background-color: #30363d !important;
            color: #ffffff !important;
        }

        [role="option"][aria-selected="true"] {
            background-color: #21262d !important;
            color: #ffffff !important;
        }


        /* =====================================================
           RADIO
        ===================================================== */

        [data-testid="stRadio"] label {
            color: #ffffff !important;
        }

        [data-testid="stRadio"] p {
            color: #ffffff !important;
        }


        /* =====================================================
           CHECKBOX
        ===================================================== */

        [data-testid="stCheckbox"] label {
            color: #ffffff !important;
        }


        /* =====================================================
           SLIDER
        ===================================================== */

        [data-testid="stSlider"] label {
            color: #ffffff !important;
        }

        [data-testid="stSlider"] * {
            color: #ffffff !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            background-color: #238636 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                background-color 0.2s ease;
        }

        .stButton > button p {
            color: #ffffff !important;
        }

        .stButton > button:hover {
            background-color: #2ea043 !important;
            color: #ffffff !important;
            transform: translateY(-2px);
            box-shadow:
                0 5px 15px rgba(46, 160, 67, 0.35);
        }


        /* =====================================================
           DOWNLOAD BUTTON
        ===================================================== */

        .stDownloadButton > button {
            background-color: #238636 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .stDownloadButton > button * {
            color: #ffffff !important;
        }

        .stDownloadButton > button:hover {
            background-color: #2ea043 !important;
            color: #ffffff !important;
            transform: translateY(-2px);
            box-shadow:
                0 5px 15px rgba(46, 160, 67, 0.35);
        }


        /* =====================================================
           FILE UPLOADER
        ===================================================== */

        [data-testid="stFileUploader"] {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
        }

        [data-testid="stFileUploader"] section {
            background-color: #161b22 !important;
            border-color: #484f58 !important;
        }

        [data-testid="stFileUploader"] * {
            color: #ffffff !important;
        }

        [data-testid="stFileUploader"] small {
            color: #8b949e !important;
        }


        /* =====================================================
           EXPANDER
        ===================================================== */

        details {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
        }

        details summary {
            color: #ffffff !important;
        }


        /* =====================================================
           ALERTS
        ===================================================== */

        [data-testid="stAlert"] {
            background-color: #161b22 !important;
            color: #ffffff !important;
        }

        [data-testid="stAlert"] * {
            color: #ffffff !important;
        }


        /* =====================================================
           DATAFRAME
        ===================================================== */

        [data-testid="stDataFrame"] {
            background-color: #161b22 !important;
            color: #ffffff !important;
        }


        /* =====================================================
           PLOTLY
        ===================================================== */

        .js-plotly-plot {
            background-color: #161b22 !important;
            border-radius: 10px !important;
        }


        /* =====================================================
           FOOD RESULT FIX
        ===================================================== */

        .food-result-card {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 15px !important;
            padding: 20px !important;
            margin: 12px 0 !important;

            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }

        .food-result-card:hover {
            transform: translateY(-4px);
            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.30);
            border-color: #2ea043 !important;
        }

        .food-result-title {
            color: #ffffff !important;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .food-result-value {
            background-color: #21262d !important;
            color: #ffffff !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            margin-bottom: 10px !important;
        }

        .food-list {
            background-color: #161b22 !important;
            color: #ffffff !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
            padding: 15px 20px !important;
        }

        .food-list li {
            color: #ffffff !important;
            margin: 5px 0 !important;
        }


        /* =====================================================
           TABLE / CODE / PRE
        ===================================================== */

        pre,
        code {
            background-color: #161b22 !important;
            color: #ffffff !important;
        }


        /* =====================================================
           HORIZONTAL RULE
        ===================================================== */

        hr {
            border-color: #30363d !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LIGHT MODE CSS
# =========================================================

else:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #ffffff;
            color: #222222;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #222222;
        }


        /* =====================================================
           CARDS
        ===================================================== */

        .dashboard-card,
        .agent-card,
        .info-card {
            background-color: #f8f9fa;
            border: 1px solid #dddddd;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;

            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }


        /* =====================================================
           CARD HOVER
        ===================================================== */

        .dashboard-card:hover,
        .agent-card:hover,
        .info-card:hover {
            transform: translateY(-6px);
            box-shadow:
                0 10px 25px rgba(0, 0, 0, 0.15);
            border-color: #2ea043;
        }


        /* =====================================================
           METRIC HOVER
        ===================================================== */

        [data-testid="stMetric"] {
            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.12);
            border-color: #2ea043;
        }


        /* =====================================================
           BUTTON HOVER
        ===================================================== */

        .stButton > button {
            border-radius: 8px;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                background-color 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.15);
        }


        /* =====================================================
           DOWNLOAD BUTTON
        ===================================================== */

        .stDownloadButton > button {
            transition: all 0.2s ease;
        }

        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.15);
        }


        /* =====================================================
           FOOD RESULT
        ===================================================== */

        .food-result-card {
            background-color: #f8f9fa;
            border: 1px solid #dddddd;
            border-radius: 15px;
            padding: 20px;
            margin: 12px 0;

            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }

        .food-result-card:hover {
            transform: translateY(-4px);
            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.12);
            border-color: #2ea043;
        }

        .food-result-title {
            color: #222222;
            font-size: 20px;
            font-weight: 700;
        }

        .food-result-value {
            background-color: #ffffff;
            color: #222222;
            border: 1px solid #dddddd;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 10px;
        }

        .food-list {
            background-color: #ffffff;
            color: #222222;
            border: 1px solid #dddddd;
            border-radius: 10px;
            padding: 15px 20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INITIALIZE AGENTS
# =========================================================

@st.cache_resource
def load_agents():

    nutrition_agent = NutritionAgent()
    diet_agent = DietRecommendationAgent()
    health_agent = HealthAdvisoryAgent()
    food_log_agent = FoodLogAgent()

    return (
        nutrition_agent,
        diet_agent,
        health_agent,
        food_log_agent
    )


(
    nutrition_agent,
    diet_agent,
    health_agent,
    food_log_agent
) = load_agents()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown("## 🥗 NutriAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔎 Nutrition Knowledge",
        "🍽️ Diet Recommendation",
        "📝 Food Log",
        "❤️ Health Advisory",
        "🔐 Owner / Admin"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🥗 NutriAI")

    st.subheader(
        "Intelligent Multi-Agent Nutrition Assistant"
    )

    st.markdown(
        """
        <div class="dashboard-card">

        <h3>👋 Welcome to NutriAI</h3>

        <p>
        NutriAI helps you understand food, create personalized
        nutrition plans, track meals and get simple health guidance.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🔎 Nutrition",
            "Search"
        )

    with col2:
        st.metric(
            "🍽️ Diet",
            "Personalized"
        )

    with col3:
        st.metric(
            "📝 Food Log",
            "Track"
        )

    with col4:
        st.metric(
            "❤️ Health",
            "Guidance"
        )

    st.markdown("---")

    st.markdown("### 🤖 Our AI Agents")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="agent-card">

            <h3>🔎 Nutrition Agent</h3>

            <p>
            Search food information and understand
            calories, protein, carbohydrates, fats,
            vitamins and minerals.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="agent-card">

            <h3>🍽️ Diet Recommendation Agent</h3>

            <p>
            Creates a personalized nutrition plan
            based on your body details, activity level
            and goals.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="agent-card">

            <h3>📝 Food Log Agent</h3>

            <p>
            Record your meals and track your
            nutrition history.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="agent-card">

            <h3>❤️ Health Advisory Agent</h3>

            <p>
            Get simple nutrition guidance for
            common health conditions.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# NUTRITION KNOWLEDGE
# =========================================================

elif page == "🔎 Nutrition Knowledge":

    st.title("🔎 Nutrition Knowledge")

    st.write(
        "Search for a food to see its nutrition information."
    )

    query = st.text_input(
        "What food or nutrition information are you looking for?",
        placeholder="Example: chicken, rice, apple..."
    )

    if st.button("🔍 Search"):

        if not query.strip():

            st.warning(
                "Please enter a food name."
            )

        else:

            try:

                result = nutrition_agent.find_food(
                    query
                )

                if result is None:

                    st.warning(
                        "No nutrition information found."
                    )

                else:

                    st.session_state.food_result = result

            except Exception as e:

                st.error(
                    f"Unable to search nutrition data: {e}"
                )

    if st.session_state.food_result is not None:

        result = st.session_state.food_result

        st.markdown("---")

        st.subheader(
            "🥗 Nutrition Information"
        )

        if isinstance(result, pd.DataFrame):

            st.dataframe(
                result,
                use_container_width=True
            )

        elif isinstance(result, dict):

            for key, value in result.items():

                clean_key = (
                    str(key)
                    .replace("_", " ")
                    .title()
                )

                # -------------------------------------------------
                # SPECIAL FOOD LIST
                # -------------------------------------------------

                if isinstance(value, list):

                    st.markdown(
                        f"""
                        <div class="food-result-card">

                        <div class="food-result-title">
                        {clean_key}
                        </div>

                        <div class="food-list">
                        <ul>
                        """,
                        unsafe_allow_html=True
                    )

                    for item in value:

                        clean_item = clean_html_text(
                            item
                        )

                        st.markdown(
                            f"<li>{html.escape(clean_item)}</li>",
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        """
                        </ul>
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # -------------------------------------------------
                # NORMAL VALUE
                # -------------------------------------------------

                else:

                    clean_value = clean_html_text(
                        value
                    )

                    st.markdown(
                        f"""
                        <div class="food-result-card">

                        <div class="food-result-title">
                        {html.escape(clean_key)}
                        </div>

                        <div class="food-result-value">
                        {html.escape(clean_value)}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            clean_result = clean_html_text(
                result
            )

            st.markdown(
                f"""
                <div class="food-result-card">

                <div class="food-result-value">
                {html.escape(clean_result)}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# DIET RECOMMENDATION
# =========================================================

elif page == "🍽️ Diet Recommendation":

    st.title(
        "🍽️ Personalized Diet Recommendation"
    )

    st.write(
        "Tell us a little about yourself and we'll create "
        "a simple nutrition plan for you."
    )

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=20
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=60.0
        )

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=165.0
        )

    with col2:

        activity_options = {

            "🪑 Mostly sitting — little or no exercise":
                "Sedentary",

            "🚶 Lightly active — exercise 1–3 days/week":
                "Light",

            "🏃 Moderately active — exercise 3–5 days/week":
                "Moderate",

            "🏋️ Very active — exercise 6–7 days/week":
                "Active"
        }

        activity_label = st.selectbox(
            "How active are you?",
            list(activity_options.keys())
        )

        activity_level = (
            activity_options[activity_label]
        )

        goal = st.selectbox(
            "What is your main goal?",
            [
                "Weight Loss",
                "Weight Gain",
                "Maintain Weight",
                "Build Muscle"
            ]
        )

        diet_type = st.selectbox(
            "What type of food do you prefer?",
            [
                "Vegetarian",
                "Non-Vegetarian",
                "Vegan"
            ]
        )

        cultural_preference = st.selectbox(
            "What type of cuisine do you prefer?",
            [
                "Indian",
                "South Indian",
                "North Indian",
                "Western",
                "Any"
            ]
        )

    st.markdown("---")

    if st.button(
        "🍽️ Generate My Diet Plan"
    ):

        try:

            result = diet_agent.generate_plan(
                age=age,
                gender=gender,
                weight=weight,
                height=height,
                activity_level=activity_level,
                goal=goal,
                diet_type=diet_type,
                cultural_preference=cultural_preference
            )

            st.success(
                "Your personalized nutrition plan is ready!"
            )

            if isinstance(result, dict):

                # =================================================
                # BMI / BMR / CALORIES
                # =================================================

                if "bmi" in result:

                    st.subheader(
                        "📊 Your Body Information"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.metric(
                            "BMI",
                            result.get(
                                "bmi"
                            )
                        )

                    with c2:

                        st.metric(
                            "BMR",
                            result.get(
                                "bmr",
                                "N/A"
                            )
                        )

                    with c3:

                        st.metric(
                            "Daily Calories",
                            result.get(
                                "daily_calories",
                                result.get(
                                    "calories",
                                    "N/A"
                                )
                            )
                        )


                # =================================================
                # MACROS
                # =================================================

                if "macros" in result:

                    st.subheader(
                        "🥗 Daily Macronutrients"
                    )

                    macros = result["macros"]

                    if isinstance(
                        macros,
                        dict
                    ):

                        c1, c2, c3 = st.columns(3)

                        with c1:

                            st.metric(
                                "Protein",
                                f"{macros.get('protein', 0)} g"
                            )

                        with c2:

                            st.metric(
                                "Carbohydrates",
                                f"{macros.get('carbs', 0)} g"
                            )

                        with c3:

                            st.metric(
                                "Fat",
                                f"{macros.get('fat', 0)} g"
                            )

                    else:

                        display_result_value(
                            macros
                        )


                # =================================================
                # MEAL PLAN
                # =================================================

                if "meal_plan" in result:

                    st.subheader(
                        "🍱 Meal Plan"
                    )

                    meal_plan = result[
                        "meal_plan"
                    ]

                    if isinstance(
                        meal_plan,
                        dict
                    ):

                        for meal, foods in meal_plan.items():

                            st.markdown(
                                f"### 🍴 {meal}"
                            )

                            if isinstance(
                                foods,
                                list
                            ):

                                for food in foods:

                                    clean_food = (
                                        clean_html_text(
                                            food
                                        )
                                    )

                                    st.write(
                                        f"• {clean_food}"
                                    )

                            else:

                                display_result_value(
                                    foods
                                )

                    else:

                        display_result_value(
                            meal_plan
                        )


                # =================================================
                # HEALTH ADVICE
                # =================================================

                if "health_advice" in result:

                    st.subheader(
                        "❤️ Health Advice"
                    )

                    display_result_value(
                        result["health_advice"]
                    )


                # =================================================
                # ALLERGY WARNING
                # =================================================

                if "allergy_warning" in result:

                    st.warning(
                        clean_html_text(
                            result["allergy_warning"]
                        )
                    )


                # =================================================
                # OTHER RESULTS
                # =================================================

                ignored_keys = [
                    "bmi",
                    "bmr",
                    "daily_calories",
                    "calories",
                    "macros",
                    "meal_plan",
                    "health_advice",
                    "allergy_warning"
                ]

                for key, value in result.items():

                    if key in ignored_keys:
                        continue

                    if value is None:
                        continue

                    if value == "":
                        continue

                    st.markdown(
                        f"### {str(key).replace('_', ' ').title()}"
                    )

                    display_result_value(
                        value
                    )

            else:

                display_result_value(
                    result
                )

        except Exception as e:

            st.error(
                f"Unable to generate diet plan: {e}"
            )


# =========================================================
# FOOD LOG
# =========================================================

elif page == "📝 Food Log":

    st.title("📝 Food Log")

    st.write(
        "Record what you eat and keep track of your meals."
    )

    input_type = st.radio(
        "How would you like to add your meal?",
        [
            "⌨️ Text",
            "🖼️ Image",
            "🎤 Voice"
        ],
        horizontal=True
    )

    meal_text = ""


    # =====================================================
    # TEXT
    # =====================================================

    if input_type == "⌨️ Text":

        meal_text = st.text_area(
            "What did you eat?",
            placeholder=(
                "Example: 2 idlis with sambar "
                "and one banana"
            )
        )


    # =====================================================
    # IMAGE
    # =====================================================

    elif input_type == "🖼️ Image":

        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="food_image_uploader"
        )

        if uploaded_image:

            st.image(
                uploaded_image,
                caption="Uploaded Food Image",
                use_container_width=True
            )

            st.success(
                "Image uploaded successfully."
            )

            meal_text = st.text_input(
                "What foods are in the image?",
                placeholder=(
                    "Example: Idli, sambar, banana"
                )
            )


    # =====================================================
    # VOICE
    # =====================================================

    else:

        st.info(
            "Voice input can be connected to a speech-to-text service."
        )

        meal_text = st.text_input(
            "Enter what you said",
            placeholder="Example: I ate two idlis and a banana"
        )


    st.markdown("---")


    # =====================================================
    # ANALYZE MEAL
    # =====================================================

    if st.button(
        "🔍 Analyze Meal"
    ):

        if not meal_text.strip():

            st.warning(
                "Please enter your meal details."
            )

        else:

            try:

                result = (
                    food_log_agent.analyze_meal(
                        meal_text
                    )
                )

                st.success(
                    "Meal analyzed successfully!"
                )

                if isinstance(
                    result,
                    dict
                ):

                    for key, value in result.items():

                        clean_key = (
                            str(key)
                            .replace("_", " ")
                            .title()
                        )

                        st.markdown(
                            f"### {clean_key}"
                        )

                        display_result_value(
                            value
                        )

                else:

                    display_result_value(
                        result
                    )

            except Exception as e:

                st.error(
                    f"Unable to analyze meal: {e}"
                )


    # =====================================================
    # SAVE MEAL
    # =====================================================

    if meal_text.strip():

        st.markdown("---")

        if st.button(
            "💾 Save Meal"
        ):

            try:

                save_meal(
                    meal_text
                )

                st.success(
                    "Meal saved successfully!"
                )

            except Exception as e:

                st.error(
                    f"Unable to save meal: {e}"
                )


    # =====================================================
    # MEAL HISTORY
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📈 Meal History"
    )

    try:

        logs = get_meal_logs()

        if logs:

            df_logs = pd.DataFrame(
                logs
            )

            st.dataframe(
                df_logs,
                use_container_width=True
            )

            numeric_columns = (
                df_logs
                .select_dtypes(
                    include="number"
                )
                .columns
                .tolist()
            )

            if numeric_columns:

                y_column = numeric_columns[0]

                fig = px.line(
                    df_logs,
                    y=y_column,
                    title="Nutrition History"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.info(
                "No meal history available yet."
            )

    except Exception:

        st.info(
            "Meal history is not available yet."
        )


# =========================================================
# HEALTH ADVISORY
# =========================================================

elif page == "❤️ Health Advisory":

    st.title(
        "❤️ Health Advisory"
    )

    st.write(
        "Get simple nutrition guidance based on your health needs."
    )

    condition = st.selectbox(
        "What would you like nutrition guidance for?",
        [
            "Healthy",
            "Diabetes",
            "Heart Health",
            "High Blood Pressure",
            "Obesity",
            "PCOS",
            "High Cholesterol",
            "Anemia",
            "General"
        ]
    )

    question = st.text_area(
        "Tell us what you would like to know",
        placeholder=(
            "Example: What foods should I include in my diet?"
        )
    )

    if st.button(
        "❤️ Get Health Advice"
    ):

        if not question.strip():

            question = (
                f"Give general nutrition guidance for "
                f"{condition}"
            )

        try:

            result = health_agent.get_advice(
                condition,
                question
            )

            st.success(
                "Health guidance generated."
            )

            if isinstance(
                result,
                dict
            ):

                for key, value in result.items():

                    st.markdown(
                        f"### {str(key).replace('_', ' ').title()}"
                    )

                    display_result_value(
                        value
                    )

            else:

                display_result_value(
                    result
                )

            st.info(
                "⚠️ This information is for general educational "
                "purposes and is not a substitute for professional "
                "medical advice."
            )

        except Exception as e:

            st.error(
                f"Unable to generate health advice: {e}"
            )


# =========================================================
# OWNER / ADMIN
# =========================================================

elif page == "🔐 Owner / Admin":

    st.title(
        "🔐 Owner / Admin"
    )

    st.write(
        "This section is available only to the project owner."
    )

    password = st.text_input(
        "Admin Password",
        type="password"
    )

    admin_password = os.getenv(
        "NUTRIAI_ADMIN_PASSWORD",
        "admin123"
    )

    if st.button(
        "🔓 Login"
    ):

        if hmac.compare_digest(
            password,
            admin_password
        ):

            st.success(
                "Admin access granted."
            )

            st.markdown("---")

            st.subheader(
                "📊 User Feedback"
            )

            try:

                conn = sqlite3.connect(
                    FEEDBACK_DB
                )

                feedback_df = pd.read_sql_query(
                    "SELECT * FROM feedback",
                    conn
                )

                conn.close()

                if not feedback_df.empty:

                    st.dataframe(
                        feedback_df,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No feedback available."
                    )

            except Exception:

                st.info(
                    "No feedback table available."
                )


            st.markdown("---")

            st.subheader(
                "📁 Nutrition Dataset"
            )

            try:

                if os.path.exists(
                    "nutrition_data.csv"
                ):

                    nutrition_df = pd.read_csv(
                        "nutrition_data.csv"
                    )

                    st.dataframe(
                        nutrition_df,
                        use_container_width=True
                    )

                    csv_data = (
                        nutrition_df.to_csv(
                            index=False
                        )
                    )

                    st.download_button(
                        "⬇️ Download Nutrition Data",
                        csv_data,
                        "nutrition_data.csv",
                        "text/csv"
                    )

                else:

                    st.warning(
                        "nutrition_data.csv not found."
                    )

            except Exception as e:

                st.error(
                    f"Unable to load dataset: {e}"
                )

        else:

            if password:

                st.error(
                    "Incorrect password."
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:20px;">

    <h4>🥗 NutriAI</h4>

    <p>
    Intelligent Multi-Agent Nutrition Assistant
    </p>

    <p>
    Eat Better • Live Better • Stay Healthy
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
