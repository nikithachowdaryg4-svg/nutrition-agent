import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
import hmac
from nutrition_agent import NutritionAgent

from diet_agent import DietRecommendationAgent
from health_agent import HealthAdvisoryAgent
from food_log_agent import FoodLogAgent

from database import (
    create_tables,
    save_meal,
    get_meal_logs
)


# ==================================================
# DATABASE
# ==================================================

create_tables()


# ==================================================
# USER FEEDBACK DATABASE
# ==================================================

FEEDBACK_DB = "database/user_feedback.db"


def create_feedback_table():
    """Create the user feedback table if it does not exist."""
    connection = sqlite3.connect(FEEDBACK_DB)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal TEXT,
            rating INTEGER NOT NULL,
            feedback TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def save_user_feedback(meal, rating, feedback):
    """Save user feedback to SQLite."""
    connection = sqlite3.connect(FEEDBACK_DB)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_feedback (meal, rating, feedback)
        VALUES (?, ?, ?)
        """,
        (meal, rating, feedback)
    )

    connection.commit()
    connection.close()


def get_user_feedback():
    """Return all submitted user feedback."""
    connection = sqlite3.connect(FEEDBACK_DB)

    rows = connection.execute(
        """
        SELECT id, meal, rating, feedback, submitted_at
        FROM user_feedback
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()
    return rows


create_feedback_table()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NutriAI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# SESSION STATE
# ==================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "food_result" not in st.session_state:
    st.session_state.food_result = None


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🥗 NutriAI")

st.sidebar.markdown(
    """
    **Intelligent Multi-Agent Nutrition Agent**

    Personalized nutrition powered by AI,
    RAG and multi-agent architecture.
    """
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔎 Nutrition Knowledge",
        "🍱 Diet Recommendation",
        "📝 Food Log",
        "❤️ Health Advisory",
        "🔐 Owner / Admin"
    ]
)

st.sidebar.divider()

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "NutriAI • AI-powered nutrition assistant"
)


# ==================================================
# CUSTOM CSS
# ==================================================

if st.session_state.dark_mode:

    st.markdown(
        """
        <style>

        /* =========================================
           DARK MODE
           ========================================= */

        .stApp {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }

        .main {
            padding-top: 1rem;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        .stApp p,
        .stApp label {
            color: #f8fafc !important;
        }


        /* SIDEBAR */

        [data-testid="stSidebar"] {
            background-color: #111827 !important;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }


        /* DASHBOARD CARDS */

        .dashboard-card {
            background-color: #1e293b;
            color: #f8fafc;
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #334155;
            text-align: center;
            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border 0.3s ease;
            cursor: pointer;
            margin-bottom: 15px;
        }

        .dashboard-card:hover {
            transform: scale(1.04) translateY(-8px);
            box-shadow:
                0 18px 40px rgba(0, 166, 126, 0.35);
            border: 2px solid #00A67E;
        }

        .dashboard-card h2 {
            color: #00A67E !important;
            margin-bottom: 5px;
        }

        .dashboard-card h4 {
            color: #f8fafc !important;
        }

        .dashboard-card p {
            color: #cbd5e1 !important;
        }


        /* AGENT CARDS */

        .agent-card {
            background-color: #1e293b;
            color: #f8fafc;
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #334155;
            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border 0.3s ease;
            cursor: pointer;
            margin-bottom: 15px;
        }

        .agent-card:hover {
            transform: scale(1.03) translateY(-7px);
            box-shadow:
                0 15px 35px rgba(0, 166, 126, 0.30);
            border: 2px solid #00A67E;
        }

        .agent-card h3 {
            color: #f8fafc !important;
            margin-bottom: 8px;
        }

        .agent-card p {
            color: #cbd5e1 !important;
        }


        /* METRICS */

        [data-testid="stMetric"] {
            background-color: #1e293b !important;
            padding: 15px;
            border-radius: 15px;
            border: 1px solid #334155;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }


        /* INPUTS */

        input,
        textarea {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-color: #475569 !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #94a3b8 !important;
        }


        /* SELECT BOX */

        [data-baseweb="select"] > div {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-color: #475569 !important;
        }


        /* BUTTONS */

        .stButton > button {
            background-color: #00A67E !important;
            color: white !important;
            border: none !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.25s ease;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow:
                0px 8px 20px rgba(0, 166, 126, 0.35);
        }


        /* DIVIDER */

        hr {
            border-color: #334155 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <style>

        /* =========================================
           LIGHT MODE
           ========================================= */

        .main {
            padding-top: 1rem;
        }


        /* DASHBOARD CARDS */

        .dashboard-card {
            background: white;
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            text-align: center;
            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border 0.3s ease;
            cursor: pointer;
            margin-bottom: 15px;
        }

        .dashboard-card:hover {
            transform: scale(1.04) translateY(-8px);
            box-shadow:
                0 18px 40px rgba(0, 166, 126, 0.28);
            border: 2px solid #00A67E;
        }

        .dashboard-card h2 {
            color: #00A67E;
            margin-bottom: 5px;
        }

        .dashboard-card p {
            color: #666666;
            margin-top: 0px;
        }


        /* AGENT CARDS */

        .agent-card {
            background: white;
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            transition:
                transform 0.3s ease,
                box-shadow 0.3s ease,
                border 0.3s ease;
            cursor: pointer;
            margin-bottom: 15px;
        }

        .agent-card:hover {
            transform: scale(1.03) translateY(-7px);
            box-shadow:
                0 15px 35px rgba(0, 166, 126, 0.25);
            border: 2px solid #00A67E;
        }

        .agent-card h3 {
            margin-bottom: 8px;
        }

        .agent-card p {
            color: #666666;
        }


        /* BUTTONS */

        .stButton > button {
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.25s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0px 6px 15px rgba(0, 0, 0, 0.15);
        }


        /* METRICS */

        [data-testid="stMetric"] {
            background: white;
            padding: 15px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
        }


        /* INPUTS */

        textarea {
            color: #111827 !important;
            background-color: #ffffff !important;
        }

        input {
            color: #111827 !important;
        }

        textarea::placeholder,
        input::placeholder {
            color: #6b7280 !important;
            opacity: 1 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# INITIALIZE AGENTS
# ==================================================

nutrition_agent = NutritionAgent()
diet_agent = DietRecommendationAgent()
health_agent = HealthAdvisoryAgent()
food_log_agent = FoodLogAgent()


# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    st.title("🥗 NutriAI")

    st.subheader(
        "Intelligent Multi-Agent Nutrition Agent"
    )

    st.markdown(
        """
        NutriAI combines **AI Agents + RAG + Nutrition Analytics**
        to provide personalized and intelligent nutrition guidance.
        """
    )

    st.divider()


    # ----------------------------------------------
    # DASHBOARD CARDS
    # ----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            """
            <div class="dashboard-card">
                <h2>🤖 4</h2>
                <h4>AI Agents</h4>
                <p>Multi-Agent System</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="dashboard-card">
                <h2>🔎 Active</h2>
                <h4>RAG System</h4>
                <p>Nutrition Knowledge</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="dashboard-card">
                <h2>🍎 40+</h2>
                <h4>Food Records</h4>
                <p>Nutrition Dataset</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            """
            <div class="dashboard-card">
                <h2>🗄️ SQLite</h2>
                <h4>Database</h4>
                <p>Meal Tracking</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ----------------------------------------------
    # MULTI AGENT SYSTEM
    # ----------------------------------------------

    st.markdown("## 🤖 Multi-Agent System")

    agent1, agent2 = st.columns(2)

    with agent1:

        st.markdown(
            """
            <div class="agent-card">
                <h3>🔎 Nutrition Knowledge Agent</h3>
                <p>
                    Retrieves nutrition information from the
                    knowledge base using RAG.
                </p>
                <b>Status: 🟢 Active</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="agent-card">
                <h3>❤️ Health Advisory Agent</h3>
                <p>
                    Provides preventive nutrition guidance for
                    different health conditions.
                </p>
                <b>Status: 🟢 Active</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with agent2:

        st.markdown(
            """
            <div class="agent-card">
                <h3>🍱 Diet Recommendation Agent</h3>
                <p>
                    Creates personalized diet recommendations
                    based on user profile and fitness goals.
                </p>
                <b>Status: 🟢 Active</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="agent-card">
                <h3>📝 Food Log & Feedback Agent</h3>
                <p>
                    Analyzes logged meals and calculates
                    nutritional intake.
                </p>
                <b>Status: 🟢 Active</b>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ----------------------------------------------
    # NUTRITION OVERVIEW
    # ----------------------------------------------

    st.markdown("## 📊 Nutrition Overview")

    macro_data = pd.DataFrame(
        {
            "Nutrient": [
                "Protein",
                "Carbohydrates",
                "Fat"
            ],
            "Percentage": [
                25,
                45,
                30
            ]
        }
    )

    fig = px.pie(
        macro_data,
        names="Nutrient",
        values="Percentage",
        title="Recommended Macro Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "💡 NutriAI provides educational nutrition guidance "
        "and should not replace professional medical advice."
    )


# ==================================================
# NUTRITION KNOWLEDGE
# ==================================================

elif page == "🔎 Nutrition Knowledge":

    st.title("🔎 Nutrition Knowledge Agent")

    st.write(
        "Search the nutrition knowledge base using natural language."
    )

    query = st.text_input(
        "Enter a food or nutrition query",
        placeholder="Example: chicken, rice, high protein foods, vitamin C foods"
    )

    top_k = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("🔍 Search Nutrition Data"):

        if query.strip() == "":

            st.warning(
                "Please enter a search query."
            )

        else:

            results = nutrition_agent.find_food(
                query
            )

            if len(results) == 0:

                st.error(
                    "No nutrition information found."
                )

            else:

                st.success(
                    f"Found {len(results)} nutrition records."
                )


                # --------------------------------------
                # BASIC NUTRITION
                # --------------------------------------

                display_columns = [
                    "Food",
                    "Category",
                    "Serving",
                    "Calories",
                    "Protein",
                    "Carbohydrates",
                    "Fat",
                    "Fiber",
                    "Sugar"
                ]


                # --------------------------------------
                # VITAMINS
                # --------------------------------------

                vitamin_columns = [
                    "Vitamin A",
                    "Vitamin B1",
                    "Vitamin B2",
                    "Vitamin B3",
                    "Vitamin B6",
                    "Vitamin B12",
                    "Vitamin C",
                    "Vitamin D",
                    "Vitamin E",
                    "Vitamin K"
                ]


                available_columns = [
                    column
                    for column in display_columns
                    if column in results.columns
                ]

                available_vitamins = [
                    column
                    for column in vitamin_columns
                    if column in results.columns
                ]

                available_columns.extend(
                    available_vitamins
                )


                # --------------------------------------
                # RESULTS
                # --------------------------------------

                st.dataframe(
                    results[available_columns],
                    use_container_width=True,
                    hide_index=True
                )


                # --------------------------------------
                # VITAMIN INFORMATION
                # --------------------------------------

                if available_vitamins:

                    st.markdown(
                        "## 💊 Vitamin Information"
                    )

                    st.info(
                        "Vitamin information retrieved from "
                        "the nutrition knowledge base."
                    )

                    vitamin_data = results[
                        ["Food"] + available_vitamins
                    ]

                    st.dataframe(
                        vitamin_data,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.warning(
                        "No vitamin columns were found in "
                        "your current nutrition dataset."
                    )


# ==================================================
# DIET RECOMMENDATION
# ==================================================

elif page == "🍱 Diet Recommendation":

    st.title("🍱 Diet Recommendation Agent")

    st.write(
        "Generate a personalized educational diet recommendation."
    )

    st.divider()


    # ----------------------------------------------
    # USER PROFILE
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            placeholder="Enter your name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=20
        )

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male"
            ]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=200.0,
            value=60.0
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=220.0,
            value=165.0
        )


    with col2:

        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Light",
                "Moderate",
                "Active"
            ]
        )

        goal = st.selectbox(
            "Fitness Goal",
            [
                "Weight Loss",
                "Weight Maintenance",
                "Weight Gain"
            ]
        )

        diet_type = st.selectbox(
            "Diet Type",
            [
                "Vegetarian",
                "Non-Vegetarian"
            ]
        )


        # ------------------------------------------
        # CULTURAL PREFERENCE
        # ------------------------------------------

        cultural_preference = st.selectbox(
            "Cultural Food Preference",
            [
                "Any",
                "Indian",
                "Mediterranean",
                "Asian",
                "Western"
            ]
        )


        health_condition = st.text_input(
            "Health Condition",
            placeholder="Example: diabetes, heart health, healthy"
        )

        allergies = st.text_input(
            "Food Allergies",
            placeholder="Example: peanuts, milk"
        )


    st.divider()


    # ----------------------------------------------
    # GENERATE PLAN
    # ----------------------------------------------

    if st.button(
        "✨ Generate Personalized Plan"
    ):

        plan = diet_agent.generate_plan(
            age,
            gender,
            weight,
            height,
            activity_level,
            goal,
            diet_type,
            cultural_preference
        )

        st.success(
            "Personalized nutrition recommendation generated!"
        )


        # ------------------------------------------
        # HEALTH METRICS
        # ------------------------------------------

        st.markdown(
            "## 📊 Your Health Metrics"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "BMI",
                plan["BMI"]
            )

        with c2:

            st.metric(
                "BMI Category",
                plan["BMI Category"]
            )

        with c3:

            st.metric(
                "BMR",
                f'{plan["BMR"]} kcal'
            )

        with c4:

            st.metric(
                "Daily Calories",
                f'{plan["Daily Calories"]} kcal'
            )


        # ------------------------------------------
        # MACROS
        # ------------------------------------------

        st.markdown(
            "## 🥗 Recommended Macros"
        )

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "Protein",
                f'{plan["Protein"]} g'
            )

        with m2:

            st.metric(
                "Carbohydrates",
                f'{plan["Carbohydrates"]} g'
            )

        with m3:

            st.metric(
                "Fat",
                f'{plan["Fat"]} g'
            )


        # ------------------------------------------
        # CULTURAL PREFERENCE
        # ------------------------------------------

        st.markdown(
            "## 🌍 Selected Food Culture"
        )

        st.info(
            f"Food Preference: {plan['Cultural Preference']}"
        )


        # ------------------------------------------
        # MEAL PLAN
        # ------------------------------------------

        st.markdown(
            "## 🍽️ Sample Daily Meal Plan"
        )

        for meal, food in plan["Meals"].items():

            st.markdown(
                f"""
                <div class="agent-card">
                    <h3>{meal}</h3>
                    <p>{food}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ------------------------------------------
        # HEALTH CONDITION
        # ------------------------------------------

        if health_condition.strip() != "":

            st.markdown(
                "## ❤️ Health Advisory"
            )

            advice = health_agent.get_advice(
                health_condition
            )

            st.info(
                advice["Condition"]
            )

            for item in advice["Advice"]:

                st.write(
                    "• " + item
                )


        # ------------------------------------------
        # ALLERGY WARNING
        # ------------------------------------------

        if allergies.strip() != "":

            st.warning(
                f"⚠️ Food allergies provided: {allergies}. "
                "Always verify ingredients before consuming food."
            )

        st.caption(
            "These calculations are educational estimates and "
            "not medical prescriptions."
        )


# ==================================================
# FOOD LOG
# ==================================================

elif page == "📝 Food Log":

    st.title("📝 Food Log & Feedback Agent")

    st.write(
        "Log your meals using text, image, or voice input "
        "and get nutritional analysis."
    )

    st.divider()


    # ==================================================
    # INPUT METHOD
    # ==================================================

    input_method = st.radio(
        "Choose how you want to log your meal:",
        [
            "⌨️ Text",
            "📷 Image",
            "🎤 Voice"
        ],
        horizontal=True
    )


    # ==================================================
    # TEXT INPUT
    # ==================================================

    if input_method == "⌨️ Text":

        meal_text = st.text_area(
            "Enter your meal",
            placeholder="Example: chicken, rice, spinach",
            height=120
        )

        if st.button("🔍 Analyze Meal"):

            if meal_text.strip() == "":

                st.warning(
                    "Please enter at least one food."
                )

            else:

                result = food_log_agent.analyze_meal(
                    meal_text
                )

                st.session_state.food_result = result


    # ==================================================
    # IMAGE INPUT
    # ==================================================

    elif input_method == "📷 Image":

        st.info(
            "Upload a food image for meal logging."
        )

        uploaded_image = st.file_uploader(
            "Upload food image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if uploaded_image is not None:

            st.image(
                uploaded_image,
                caption="Uploaded Meal Image",
                use_container_width=True
            )

            st.warning(
                "Automatic food recognition from images "
                "requires a vision model. For now, enter "
                "the food names shown in the image."
            )

            image_food_text = st.text_input(
                "Food names from image",
                placeholder="Example: rice, chicken, vegetables"
            )

            if st.button("🔍 Analyze Image Meal"):

                if image_food_text.strip() == "":

                    st.warning(
                        "Please enter the food names visible "
                        "in the image."
                    )

                else:

                    result = food_log_agent.analyze_meal(
                        image_food_text
                    )

                    st.session_state.food_result = result


    # ==================================================
    # VOICE INPUT
    # ==================================================

    elif input_method == "🎤 Voice":

        st.info(
            "Upload a voice recording describing "
            "the foods you ate."
        )

        audio_file = st.file_uploader(
            "Upload voice recording",
            type=[
                "wav",
                "mp3",
                "m4a",
                "ogg"
            ]
        )

        st.caption(
            "Example: say 'chicken, rice and spinach'."
        )

        voice_text = st.text_input(
            "Voice transcription",
            placeholder="Enter the transcribed food names here"
        )

        if st.button("🎤 Analyze Voice Meal"):

            if voice_text.strip() == "":

                st.warning(
                    "Please provide the transcribed food names."
                )

            else:

                result = food_log_agent.analyze_voice_text(
                    voice_text
                )

                st.session_state.food_result = result


    # ==================================================
    # DISPLAY FOOD RESULT
    # ==================================================

    if st.session_state.food_result is not None:

        result = st.session_state.food_result

        st.divider()


        # ----------------------------------------------
        # FOODS DETECTED
        # ----------------------------------------------

        st.markdown(
            "## 🍽️ Foods Detected"
        )

        if result["Foods"]:

            for food in result["Foods"]:

                st.write(
                    "• " + str(food)
                )

        else:

            st.warning(
                "No matching foods were found."
            )

        # Show foods that were entered but could not be matched
        # instead of silently replacing them with unrelated foods.
        if result.get("Unrecognized Foods"):

            st.warning(
                "⚠️ Could not confidently identify these foods:"
            )

            for food in result["Unrecognized Foods"]:

                st.write(
                    "• " + str(food)
                )

            st.caption(
                "Try using a more specific food name or a food "
                "that exists in the nutrition database."
            )


        # ----------------------------------------------
        # NUTRITION ANALYSIS
        # ----------------------------------------------

        st.markdown(
            "## 📊 Nutritional Analysis"
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            st.metric(
                "Calories",
                f'{result["Calories"]} kcal'
            )

        with c2:

            st.metric(
                "Protein",
                f'{result["Protein"]} g'
            )

        with c3:

            st.metric(
                "Carbs",
                f'{result["Carbohydrates"]} g'
            )

        with c4:

            st.metric(
                "Fat",
                f'{result["Fat"]} g'
            )

        with c5:

            st.metric(
                "Fiber",
                f'{result["Fiber"]} g'
            )


        # ----------------------------------------------
        # USER FEEDBACK
        # ----------------------------------------------

        st.divider()

        st.markdown("## ⭐ User Feedback")

        st.write(
            "Your feedback helps improve the NutriAI nutrition experience."
        )

        feedback_meal = ", ".join(result["Foods"])

        rating = st.slider(
            "How helpful was this nutrition analysis?",
            min_value=1,
            max_value=5,
            value=5,
            step=1,
            format="%d / 5"
        )

        rating_labels = {
            1: "😞 Very Poor",
            2: "🙁 Poor",
            3: "😐 Average",
            4: "🙂 Good",
            5: "🤩 Excellent"
        }

        st.write(f"**Your rating:** {rating_labels[rating]}")

        feedback_text = st.text_area(
            "What did you think? (Optional)",
            placeholder="Tell us what you liked or what we can improve...",
            height=120,
            key="meal_feedback_text"
        )

        if st.button("📤 Submit Feedback", type="primary"):

            save_user_feedback(
                feedback_meal,
                rating,
                feedback_text.strip()
            )

            st.success(
                "✅ Thank you! Your feedback has been submitted successfully."
            )

            st.session_state.feedback_submitted = True

        if st.session_state.get("feedback_submitted", False):
            st.caption(
                "Your feedback has been recorded. Thank you for helping us improve NutriAI!"
            )


        # ----------------------------------------------
        # SAVE MEAL
        # ----------------------------------------------

        if result["Foods"]:

            if st.button(
                "💾 Save Meal to Database"
            ):

                save_meal(
                    ", ".join(result["Foods"]),
                    result["Calories"],
                    result["Protein"],
                    result["Carbohydrates"],
                    result["Fat"],
                    result["Fiber"]
                )

                st.success(
                    "Meal saved successfully to SQLite database!"
                )


    st.divider()


    # ==================================================
    # MEAL HISTORY
    # ==================================================

    st.markdown(
        "## 📚 Meal History"
    )

    logs = get_meal_logs()

    if logs:

        log_data = pd.DataFrame(
            logs,
            columns=[
                "ID",
                "Food",
                "Calories",
                "Protein",
                "Carbohydrates",
                "Fat",
                "Fiber",
                "Logged At"
            ]
        )

        st.dataframe(
            log_data,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------
        # HISTORY CHART
        # ----------------------------------------------

        st.markdown(
            "## 📈 Meal Calorie History"
        )

        chart_data = log_data.copy()

        chart_data["Meal"] = (
            chart_data["Food"]
            .astype(str)
            .str[:30]
        )

        fig = px.bar(
            chart_data,
            x="Meal",
            y="Calories",
            title="Calories per Logged Meal"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No meals have been logged yet."
        )




# ==================================================
# HEALTH ADVISORY
# ==================================================

elif page == "❤️ Health Advisory":

    st.title("❤️ Health Advisory Agent")

    st.write(
        "Get general nutrition guidance based on a health condition."
    )

    st.divider()


    # ----------------------------------------------
    # HEALTH CONDITIONS
    # ----------------------------------------------

    condition = st.selectbox(
        "Select health condition",
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


    # ----------------------------------------------
    # GET ADVICE
    # ----------------------------------------------

    if st.button(
        "❤️ Get Health Advice"
    ):

        advice = health_agent.get_advice(
            condition
        )

        st.success(
            advice["Condition"]
        )

        for item in advice["Advice"]:

            st.markdown(
                f"""
                <div class="agent-card">
                    <p>✅ {item}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.warning(
            "⚠️ This is general educational nutrition guidance. "
            "For medical conditions, consult a qualified healthcare professional."
        )

# ==================================================
# OWNER / ADMIN DASHBOARD
# ==================================================

elif page == "🔐 Owner / Admin":

    st.title("🔐 Owner / Admin Dashboard")
    st.write("Private dashboard for viewing NutriAI user feedback.")

    ADMIN_PASSWORD = os.getenv("NUTRIAI_ADMIN_PASSWORD", "admin123")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:

        st.markdown("### Owner Login")

        admin_password = st.text_input(
            "Enter owner password",
            type="password",
            placeholder="Owner password"
        )

        if st.button("🔓 Login", type="primary"):
            if hmac.compare_digest(admin_password, ADMIN_PASSWORD):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Incorrect owner password.")

        st.info("Only the owner/admin should use this section.")

    else:

        top1, top2 = st.columns([6, 1])

        with top1:
            st.success("✅ Owner authenticated")

        with top2:
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.divider()

        feedback_rows = get_user_feedback()

        if feedback_rows:

            feedback_data = pd.DataFrame(
                feedback_rows,
                columns=[
                    "ID",
                    "Meal",
                    "Rating",
                    "Feedback",
                    "Submitted At"
                ]
            )

            avg_rating = feedback_data["Rating"].mean()
            total_feedback = len(feedback_data)
            five_star = int((feedback_data["Rating"] == 5).sum())

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "⭐ Average Rating",
                    f"{avg_rating:.1f} / 5"
                )

            with c2:
                st.metric(
                    "📊 Total Feedback",
                    total_feedback
                )

            with c3:
                st.metric(
                    "🤩 5-Star Responses",
                    five_star
                )

            st.divider()

            st.markdown("## 💬 All User Feedback")

            selected_rating = st.selectbox(
                "Filter by rating",
                ["All", 1, 2, 3, 4, 5]
            )

            filtered_data = feedback_data.copy()

            if selected_rating != "All":
                filtered_data = filtered_data[
                    filtered_data["Rating"] == selected_rating
                ]

            st.dataframe(
                filtered_data,
                use_container_width=True,
                hide_index=True
            )

            csv_data = filtered_data.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Download Feedback CSV",
                data=csv_data,
                file_name="nutriai_user_feedback.csv",
                mime="text/csv"
            )

            st.divider()

            st.markdown("## 📈 Rating Distribution")

            rating_counts = (
                feedback_data["Rating"]
                .value_counts()
                .reindex([1, 2, 3, 4, 5], fill_value=0)
                .reset_index()
            )

            rating_counts.columns = ["Rating", "Responses"]

            fig = px.bar(
                rating_counts,
                x="Rating",
                y="Responses",
                title="User Feedback Ratings"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No user feedback has been submitted yet.")

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "🥗 NutriAI — Intelligent Multi-Agent Nutrition Agent | "
    "RAG + AI Agents + SQLite + Analytics"
)
