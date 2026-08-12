
import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NutriCare | Diet Recommendation",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #f7faf8;
}

/* Remove default top padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f5132 0%, #198754 55%, #43aa73 100%);
    padding: 42px 45px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(25, 135, 84, 0.18);
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    margin-bottom: 0;
    opacity: 0.92;
}

/* Section title */
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #164b35;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* Info cards */
.info-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e2ebe5;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    margin-bottom: 15px;
}

/* Recommendation card */
.recommendation {
    background: linear-gradient(135deg, #e8f7ee, #f6fff9);
    border: 1px solid #b9dfc8;
    border-radius: 24px;
    padding: 30px;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 25px;
}

.recommendation-label {
    color: #4d6b5b;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.recommendation-title {
    color: #0f5132;
    font-size: 36px;
    font-weight: 850;
    margin-top: 8px;
}

/* Food cards */
.food-card {
    background: white;
    border: 1px solid #e2ebe5;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}

.food-name {
    color: #164b35;
    font-size: 19px;
    font-weight: 750;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    margin-right: 5px;
    margin-top: 8px;
    border-radius: 20px;
    background: #eaf7ef;
    color: #176b43;
    font-size: 12px;
    font-weight: 650;
}

/* Footer */
.footer {
    text-align: center;
    color: #718078;
    font-size: 13px;
    padding-top: 25px;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    font-size: 17px;
    font-weight: 750;
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e2ebe5;
}

/* Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #dce8e0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("diet_recommendation_model.pkl")


# ============================================================
# LOAD FOOD DATA
# ============================================================

@st.cache_data
def load_food_data():
    return pd.read_csv("food_nutrition_updated.csv")


model = load_model()
food = load_food_data()


# ============================================================
# FOOD RECOMMENDATION
# ============================================================

def recommend_foods(
    diet_type,
    food_data,
    cuisine="All",
    halal_only=True,
    top_n=10
):

    df = food_data.copy()

    # -----------------------------
    # Halal filter
    # -----------------------------

    if halal_only and "Halal_Status" in df.columns:

        df = df[
            df["Halal_Status"]
            .astype(str)
            .str.lower()
            .eq("halal")
        ]

    # -----------------------------
    # Cuisine filter
    # -----------------------------

    if cuisine != "All" and "Cuisine" in df.columns:

        cuisine_df = df[
            df["Cuisine"]
            .astype(str)
            .str.lower()
            .eq(cuisine.lower())
        ]

        if len(cuisine_df) > 0:
            df = cuisine_df

    # -----------------------------
    # Required nutrition columns
    # -----------------------------

    required_columns = [
        "Protein (g per 100g)",
        "Dietary Fiber (g per 100g)",
        "Carbohydrates (g per 100g)",
        "Sugars (g per 100g)",
        "Sodium (mg per 100g)",
        "Calories (kcal per 100g)"
    ]

    for col in required_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df = df.dropna(
        subset=[
            col for col in required_columns
            if col in df.columns
        ]
    )

    if len(df) == 0:
        return pd.DataFrame()

    # -----------------------------
    # Scores
    # -----------------------------

    df["protein_score"] = (
        df["Protein (g per 100g)"] /
        max(df["Protein (g per 100g)"].max(), 1)
    )

    df["fiber_score"] = (
        df["Dietary Fiber (g per 100g)"] /
        max(df["Dietary Fiber (g per 100g)"].max(), 1)
    )

    df["carb_score"] = (
        1 -
        df["Carbohydrates (g per 100g)"] /
        max(df["Carbohydrates (g per 100g)"].max(), 1)
    )

    df["sugar_score"] = (
        1 -
        df["Sugars (g per 100g)"] /
        max(df["Sugars (g per 100g)"].max(), 1)
    )

    df["sodium_score"] = (
        1 -
        df["Sodium (mg per 100g)"] /
        max(df["Sodium (mg per 100g)"].max(), 1)
    )

    df["calorie_score"] = (
        1 -
        df["Calories (kcal per 100g)"] /
        max(df["Calories (kcal per 100g)"].max(), 1)
    )

    # -----------------------------
    # Diet scoring
    # -----------------------------

    if diet_type == "Low_Carb":

        df["score"] = (
            0.40 * df["carb_score"] +
            0.25 * df["sugar_score"] +
            0.20 * df["protein_score"] +
            0.15 * df["fiber_score"]
        )

    elif diet_type == "Low_Sodium":

        df["score"] = (
            0.50 * df["sodium_score"] +
            0.20 * df["calorie_score"] +
            0.15 * df["protein_score"] +
            0.15 * df["fiber_score"]
        )

    else:

        df["score"] = (
            0.30 * df["protein_score"] +
            0.25 * df["fiber_score"] +
            0.20 * df["calorie_score"] +
            0.15 * df["carb_score"] +
            0.10 * df["sodium_score"]
        )

    return df.sort_values(
        "score",
        ascending=False
    ).head(top_n)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<h1>🥗 NutriCare</h1>

<p>
Personalized Diet Recommendation System
</p>

<p>
Smart nutrition recommendations based on your
health profile, lifestyle and food preferences.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PERSONAL INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">👤 Personal Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    age = st.number_input(
        "Age",
        18,
        100,
        25
    )

with col2:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col3:

    weight = st.number_input(
        "Weight (kg)",
        30.0,
        200.0,
        65.0
    )


col1, col2, col3 = st.columns(3)

with col1:

    height = st.number_input(
        "Height (cm)",
        100.0,
        220.0,
        165.0
    )

with col2:

    bmi = st.number_input(
        "BMI",
        10.0,
        60.0,
        24.0
    )

with col3:

    activity = st.selectbox(
        "Physical Activity",
        [
            "Sedentary",
            "Moderate",
            "Active"
        ]
    )


# ============================================================
# HEALTH PROFILE
# ============================================================

st.markdown(
    '<div class="section-title">🏥 Health Profile</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    disease = st.selectbox(
        "Disease Type",
        [
            "Diabetes",
            "Hypertension",
            "Obesity",
            "None"
        ]
    )

with col2:

    severity = st.selectbox(
        "Severity",
        [
            "Mild",
            "Moderate",
            "Severe"
        ]
    )

with col3:

    glucose = st.number_input(
        "Glucose (mg/dL)",
        50.0,
        300.0,
        100.0
    )


col1, col2, col3 = st.columns(3)

with col1:

    cholesterol = st.number_input(
        "Cholesterol (mg/dL)",
        100.0,
        400.0,
        200.0
    )

with col2:

    blood_pressure = st.number_input(
        "Blood Pressure (mmHg)",
        80.0,
        250.0,
        120.0
    )

with col3:

    calories = st.number_input(
        "Daily Caloric Intake",
        1000.0,
        5000.0,
        2200.0
    )


# ============================================================
# FOOD PREFERENCES
# ============================================================

st.markdown(
    '<div class="section-title">🍽️ Food Preferences</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    restriction = st.selectbox(
        "Dietary Restriction",
        [
            "None",
            "Low_Sodium",
            "Low_Sugar"
        ]
    )

with col2:

    allergy = st.selectbox(
        "Allergy",
        [
            "None",
            "Gluten",
            "Peanuts"
        ]
    )


col1, col2 = st.columns(2)

with col1:

    cuisine = st.selectbox(
        "🇧🇩 Preferred Cuisine",
        [
            "Bangladeshi",
            "Indian",
            "Chinese",
            "Italian",
            "Mexican",
            "All"
        ],
        index=0
    )

with col2:

    halal_only = st.toggle(
        "🕌 Halal Food Only",
        value=True
    )


# ============================================================
# LIFESTYLE
# ============================================================

st.markdown(
    '<div class="section-title">🏃 Lifestyle & Diet Adherence</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    exercise = st.number_input(
        "Weekly Exercise Hours",
        0.0,
        20.0,
        5.0
    )

with col2:

    adherence = st.number_input(
        "Diet Adherence",
        0.0,
        100.0,
        75.0
    )

with col3:

    imbalance = st.number_input(
        "Nutrient Imbalance Score",
        0.0,
        5.0,
        2.0
    )


# ============================================================
# RECOMMEND BUTTON
# ============================================================

st.markdown("")

st.markdown(
    "### ✨ Ready to get your personalized plan?"
)

recommend_button = st.button(
    "🔍  GET MY PERSONALIZED DIET PLAN",
    use_container_width=True
)


# ============================================================
# PREDICTION
# ============================================================

if recommend_button:

    user_data = {

        "Age": age,

        "Gender": gender,

        "Weight_kg": weight,

        "Height_cm": height,

        "BMI": bmi,

        "Disease_Type": disease,

        "Severity": severity,

        "Physical_Activity_Level": activity,

        "Daily_Caloric_Intake": calories,

        "Cholesterol_mg/dL": cholesterol,

        "Blood_Pressure_mmHg": blood_pressure,

        "Glucose_mg/dL": glucose,

        "Dietary_Restrictions": restriction,

        "Allergies": allergy,

        "Preferred_Cuisine": cuisine,

        "Weekly_Exercise_Hours": exercise,

        "Adherence_to_Diet_Plan": adherence,

        "Dietary_Nutrient_Imbalance_Score": imbalance
    }

    user_df = pd.DataFrame([user_data])

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    predicted_diet = model.predict(
        user_df
    )[0]

    probabilities = model.predict_proba(
        user_df
    )[0]

    classes = model.classes_

    probability_df = pd.DataFrame({

        "Diet": classes,

        "Probability": probabilities

    }).sort_values(
        "Probability",
        ascending=False
    )

    confidence = probability_df.iloc[0]["Probability"]

    # --------------------------------------------------------
    # FOOD RECOMMENDATIONS
    # --------------------------------------------------------

    recommended_foods = recommend_foods(

        predicted_diet,

        food,

        cuisine,

        halal_only,

        9
    )

    # ========================================================
    # RESULT
    # ========================================================

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
    🎯 Your Personalized Result
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="recommendation">

        <div class="recommendation-label">
        Recommended Diet Plan
        </div>

        <div class="recommendation-title">
        {predicted_diet}
        </div>

        <p>
        Your profile has been analyzed using the
        machine learning model.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Prediction Confidence</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    for i, row in enumerate(
        probability_df.head(3).itertuples()
    ):

        if i < 3:

            with [col1, col2, col3][i]:

                st.metric(
                    row.Diet,
                    f"{row.Probability:.1%}"
                )


    # ========================================================
    # USER PREFERENCE SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-title">📝 Your Selected Preferences</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Cuisine",
            cuisine
        )

    with col2:
        st.metric(
            "Halal",
            "Yes" if halal_only else "No"
        )

    with col3:
        st.metric(
            "Activity",
            activity
        )

    with col4:
        st.metric(
            "Age",
            age
        )


    # ========================================================
    # FOOD RECOMMENDATIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">🍛 Recommended Foods</div>',
        unsafe_allow_html=True
    )

    if len(recommended_foods) == 0:

        st.warning(
            "No suitable food was found for the selected "
            "preferences."
        )

    else:

        cols = st.columns(3)

        for i, (_, row) in enumerate(
            recommended_foods.iterrows()
        ):

            with cols[i % 3]:

                food_name = row.get(
                    "food",
                    "Food"
                )

                food_cuisine = row.get(
                    "Cuisine",
                    "Other"
                )

                category = row.get(
                    "Food_Category",
                    "Other"
                )

                halal_status = row.get(
                    "Halal_Status",
                    "Unknown"
                )

                st.markdown(
                    f"""
                    <div class="food-card">

                    <div class="food-name">
                    🍽️ {food_name}
                    </div>

                    <span class="badge">
                    🇧🇩 {food_cuisine}
                    </span>

                    <span class="badge">
                    🥗 {category}
                    </span>

                    <span class="badge">
                    🕌 {halal_status}
                    </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ====================================================
        # NUTRITION TABLE
        # ====================================================

        st.markdown(
            "### 📋 Nutrition Information"
        )

        display_columns = [

            "food",

            "Cuisine",

            "Food_Category",

            "Halal_Status",

            "Calories (kcal per 100g)",

            "Protein (g per 100g)",

            "Fat (g per 100g)",

            "Carbohydrates (g per 100g)",

            "Dietary Fiber (g per 100g)",

            "Sodium (mg per 100g)"

        ]

        available_columns = [

            col

            for col in display_columns

            if col in recommended_foods.columns

        ]

        st.dataframe(

            recommended_foods[
                available_columns
            ].reset_index(drop=True),

            use_container_width=True,

            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">

    🥗 <b>NutriCare</b> —
    Personalized Diet Recommendation System

    <br><br>

    Built with Machine Learning & Streamlit

    <br>

    For educational purposes only.
    This system does not replace professional medical advice.

    </div>
    """,
    unsafe_allow_html=True
)
