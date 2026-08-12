import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NutriCare Pro | Advanced Diet Recommendation",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Main background & base styling */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f4f7f5 !important;
    color: #1f2937 !important;
}

/* Header style override */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #064e3b !important;
    font-weight: 700 !important;
}

/* Remove default top padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* Hero Section */
.hero-card {
    background: linear-gradient(135deg, #064e3b 0%, #065f46 40%, #0f766e 100%);
    padding: 3.5rem 2.5rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(6, 78, 59, 0.15);
    position: relative;
    overflow: hidden;
}

.hero-card::after {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(209,250,229,0.1) 0%, rgba(209,250,229,0) 70%);
    border-radius: 50%;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 12px;
}

.hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    font-weight: 500;
    margin-bottom: 1rem;
    color: #d1fae5;
}

.hero-tagline {
    font-size: 1rem;
    opacity: 0.8;
    font-weight: 400;
    max-width: 700px;
}

.badge-pill-header {
    background: rgba(209, 250, 229, 0.2);
    border: 1px solid rgba(209, 250, 229, 0.3);
    color: #d1fae5;
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 1.5rem;
}

/* Form Container Styling */
.form-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Tab styling overrides */
button[data-baseweb="tab"] {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #4b5563 !important;
    padding: 12px 20px !important;
    border-radius: 8px 8px 0 0 !important;
}

button[aria-selected="true"] {
    color: #065f46 !important;
    border-bottom-color: #059669 !important;
}

/* Section Subheaders */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #064e3b;
    border-left: 5px solid #10b981;
    padding-left: 12px;
    margin-bottom: 1.2rem;
    margin-top: 1rem;
}

/* Custom styled Alert/Info box for Bangladeshi and Halal default notice */
.highlight-box {
    background-color: #ecfdf5;
    border: 1px dashed #34d399;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

/* Food Card styling */
.food-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}

.food-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(6, 78, 59, 0.08);
    border-color: #34d399;
}

.food-title {
    font-size: 1.25rem;
    font-weight: 750;
    color: #064e3b;
    margin-bottom: 8px;
    line-height: 1.4;
    min-height: 2.8rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.food-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 14px;
}

.food-badge {
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-cuisine {
    background-color: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}

.badge-category {
    background-color: #f5f3ff;
    color: #6d28d9;
    border: 1px solid #e9d5ff;
}

.badge-halal {
    background-color: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
}

.badge-haram {
    background-color: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

/* Nutrition Fact Grid */
.nutrition-fact-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 12px;
    background-color: #f9fafb;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #f3f4f6;
}

.nutrition-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4px;
}

.nutrition-label {
    font-size: 0.7rem;
    color: #6b7280;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 2px;
}

.nutrition-value {
    font-size: 0.85rem;
    font-weight: 700;
    color: #1f2937;
}

/* Beautiful results card */
.diet-result-card {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 2px solid #34d399;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px rgba(52, 211, 153, 0.1);
}

.diet-result-sub {
    font-size: 0.95rem;
    font-weight: 700;
    color: #047857;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.5rem;
}

.diet-result-main {
    font-size: 2.5rem;
    font-weight: 850;
    color: #064e3b;
    margin-bottom: 1rem;
}

.diet-result-desc {
    font-size: 1.1rem;
    color: #374151;
    max-width: 600px;
    margin: 0 auto;
}

/* Confidence Meters */
.confidence-meter-container {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.confidence-bar-bg {
    background-color: #e5e7eb;
    border-radius: 100px;
    height: 8px;
    width: 100%;
    margin-top: 6px;
}

.confidence-bar-fill {
    background: linear-gradient(90deg, #10b981, #059669);
    border-radius: 100px;
    height: 8px;
}

/* Footer Section */
.footer-container {
    text-align: center;
    padding: 3rem 1.5rem;
    background-color: #0f172a;
    color: #94a3b8;
    border-radius: 20px;
    margin-top: 3rem;
}

.footer-logo {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

/* Big custom action button styling */
.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
    color: white !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Form input elements stylings */
div[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #064e3b !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #4b5563 !important;
}

/* Custom styled containers */
.stTabs {
    background-color: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
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
# HERO HEADER SECTION
# ============================================================

st.markdown("""
<div class="hero-card">
    <div class="badge-pill-header">
        <span>🛡️</span> Academic Research Validation Project
    </div>
    <div class="hero-title">🥗 NutriCare Pro</div>
    <div class="hero-subtitle">Advanced Clinical Diet & Nutrition Recommendation System</div>
    <div class="hero-tagline">
        Get tailored, data-driven food and dietary plans based on your unique clinical profile, biometric readings, and preferred cuisine. Utilizing custom Machine Learning classifications with enhanced localized food profile validation.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# USER INPUT FORM (SECTIONED VIA TABS)
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "👤 Personal Profile",
    "🏥 Health & Clinical Profile",
    "🍽️ Food Preferences & Lifestyle"
])

# -----------------------------
# TAB 1: PERSONAL BIOMETRICS
# -----------------------------
with tab1:
    st.markdown('<div class="section-header">👤 Personal Profile Details</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; margin-top: -10px; margin-bottom: 20px;">Provide basic biometrics and demographic values to calibrate recommendation constraints.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(
            "Age (Years)",
            18,
            100,
            25
        )
        weight = st.number_input(
            "Weight (kg)",
            30.0,
            200.0,
            65.0
        )

    with col2:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )
        height = st.number_input(
            "Height (cm)",
            100.0,
            220.0,
            165.0
        )

    with col3:
        activity = st.selectbox(
            "Physical Activity Level",
            [
                "Sedentary",
                "Moderate",
                "Active"
            ]
        )
        bmi = st.number_input(
            "BMI (Body Mass Index)",
            10.0,
            60.0,
            24.0
        )

# -----------------------------
# TAB 2: HEALTH & CLINICAL PROFILE
# -----------------------------
with tab2:
    st.markdown('<div class="section-header">🏥 Clinical & Health Profile</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; margin-top: -10px; margin-bottom: 20px;">Enter chronic medical conditions and quantitative diagnostic test results.</p>', unsafe_allow_html=True)

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
        cholesterol = st.number_input(
            "Cholesterol (mg/dL)",
            100.0,
            400.0,
            200.0
        )

    with col2:
        severity = st.selectbox(
            "Severity Level",
            [
                "Mild",
                "Moderate",
                "Severe"
            ]
        )
        blood_pressure = st.number_input(
            "Blood Pressure (mmHg)",
            80.0,
            250.0,
            120.0
        )

    with col3:
        glucose = st.number_input(
            "Glucose (mg/dL)",
            50.0,
            300.0,
            100.0
        )
        calories = st.number_input(
            "Daily Caloric Intake (kcal)",
            1000.0,
            5000.0,
            2200.0
        )

# -----------------------------
# TAB 3: DIETARY PREFERENCES & LIFESTYLE
# -----------------------------
with tab3:
    st.markdown('<div class="section-header">🍽️ Preferred Cuisine & Nutrition Filters</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; margin-top: -10px; margin-bottom: 20px;">Personalize food sources, allergens, strict diet principles and localization preferences.</p>', unsafe_allow_html=True)

    # Clean custom notice displaying default local preferences
    st.markdown("""
    <div class="highlight-box">
        <div style="font-size: 1.6rem; margin-right: 4px;">🇧🇩</div>
        <div>
            <strong style="color: #064e3b; font-size: 0.95rem;">Localized Nutrition Enabled</strong><br/>
            <span style="font-size: 0.85rem; color: #0f5132; opacity: 0.9;">
                The platform highlights <strong>Bangladeshi Cuisine</strong> as the default preference, integrated with <strong>Halal Food Only</strong> filtering for regional validation.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        restriction = st.selectbox(
            "Dietary Restriction",
            [
                "None",
                "Low_Sodium",
                "Low_Sugar"
            ]
        )
        allergy = st.selectbox(
            "Allergy Risks",
            [
                "None",
                "Gluten",
                "Peanuts"
            ]
        )

    with col2:
        halal_only = st.toggle(
            "🕌 Halal Food Only",
            value=True
        )
        exercise = st.number_input(
            "Weekly Exercise Hours",
            0.0,
            20.0,
            5.0
        )
        adherence = st.number_input(
            "Current Diet Adherence (%)",
            0.0,
            100.0,
            75.0
        )
        imbalance = st.number_input(
            "Nutrient Imbalance Score",
            0.0,
            5.0,
            2.0
        )


# ============================================================
# RECOMMEND BUTTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

recommend_button = st.button(
    "⚡ ANALYZE PROFILE & GENERATE DIET PLAN",
    use_container_width=True
)


# ============================================================
# PREDICTION & RESULTS
# ============================================================

if recommend_button:

    with st.spinner("🧠 Evaluating clinical biometrics & parsing local nutrition catalogs..."):

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
        # MODEL PREDICTION
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
    # DIET PLAN RESULTS SUMMARY CARD
    # ========================================================

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header" style="margin-bottom: 20px;">
    🎯 Personalized Recommendation Report
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="diet-result-card">
            <div class="diet-result-sub">Recommended Therapeutic Diet</div>
            <div class="diet-result-main">🥗 {predicted_diet}</div>
            <div class="diet-result-desc">
                Your biological profile, physical activities, and medical indicators have been successfully synthesized by our classification model. We have customized the following diet strategy for optimized physiological recovery and health maintenance.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # CONFIDENCE & BIOMETRICS METRIC SECTIONS
    # ========================================================

    col_conf, col_pref = st.columns([1, 1])

    with col_conf:
        st.markdown(
            '<div class="section-header" style="font-size: 1.15rem; margin-top: 0;">📊 Model Confidence Breakdown</div>',
            unsafe_allow_html=True
        )

        for i, row in enumerate(probability_df.head(3).itertuples()):
            prob_pct = row.Probability * 100
            st.markdown(f"""
            <div class="confidence-meter-container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #064e3b; font-size: 0.9rem;">{row.Diet}</span>
                    <span style="font-weight: 800; color: #059669; font-size: 0.9rem;">{row.Probability:.1%}</span>
                </div>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill" style="width: {prob_pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_pref:
        st.markdown(
            '<div class="section-header" style="font-size: 1.15rem; margin-top: 0;">📝 User Preference Synthesis</div>',
            unsafe_allow_html=True
        )

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(
                label="Selected Cuisine",
                value=cuisine
            )
            st.metric(
                label="Physical Activity Level",
                value=activity
            )
        with m_col2:
            st.metric(
                label="Halal Validation Filter",
                value="Active 🕌" if halal_only else "Inactive ❌"
            )
            st.metric(
                label="Target User Age",
                value=f"{age} Years"
            )

    # ========================================================
    # RECOMMENDED FOODS SECTIONS
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">🍛 Recommended Food Selections & Macros</div>',
        unsafe_allow_html=True
    )

    if len(recommended_foods) == 0:

        st.warning(
            "⚠️ No suitable foods were found in the database matching your specific criteria. "
            "Consider broadening your preferred cuisine or disabling restriction filters."
        )

    else:
        st.info(
            "💡 The foods displayed below are classified and prioritized specifically for your recommended diet. "
            "Nutritional components are listed per 100 grams."
        )

        # Draw beautiful nutrition-focused cards
        cols = st.columns(3)

        for i, (_, row) in enumerate(
            recommended_foods.iterrows()
        ):

            with cols[i % 3]:

                food_name = row.get("food", "Food").title()
                food_cuisine = row.get("Cuisine", "Other")
                category = row.get("Food_Category", "Other")
                halal_status = row.get("Halal_Status", "Unknown")

                # Parse Nutrition metrics
                calories_val = row.get("Calories (kcal per 100g)", 0.0)
                protein_val = row.get("Protein (g per 100g)", 0.0)
                carbs_val = row.get("Carbohydrates (g per 100g)", 0.0)
                fat_val = row.get("Fat (g per 100g)", 0.0)
                fiber_val = row.get("Dietary Fiber (g per 100g)", 0.0)
                sodium_val = row.get("Sodium (mg per 100g)", 0.0)

                badge_halal_class = "badge-halal" if halal_status.lower() == "halal" else "badge-haram"

                st.markdown(
                    f"""
                    <div class="food-card">
                        <div class="food-title">🍽️ {food_name}</div>
                        <div class="food-badge-row">
                            <span class="food-badge badge-cuisine">🇧🇩 {food_cuisine}</span>
                            <span class="food-badge badge-category">🥗 {category}</span>
                            <span class="food-badge {badge_halal_class}">🕌 {halal_status}</span>
                        </div>
                        <div style="border-top: 1px dashed #e5e7eb; margin: 10px 0;"></div>
                        <div class="nutrition-fact-grid">
                            <div class="nutrition-item">
                                <span class="nutrition-label">⚡ Cal</span>
                                <span class="nutrition-value">{calories_val:.1f}</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">🥩 Prot</span>
                                <span class="nutrition-value">{protein_val:.1f}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">🍞 Carb</span>
                                <span class="nutrition-value">{carbs_val:.1f}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">🥑 Fat</span>
                                <span class="nutrition-value">{fat_val:.1f}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">🌾 Fiber</span>
                                <span class="nutrition-value">{fiber_val:.1f}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrition-label">🧂 Sod</span>
                                <span class="nutrition-value">{sodium_val:.0f}mg</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ====================================================
        # NUTRITION TABLE
        # ====================================================

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header" style="font-size: 1.15rem;">📋 Comprehensive Dietary Reference Table</div>',
            unsafe_allow_html=True
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

        # Present renamed columns for neatness in table
        df_display = recommended_foods[available_columns].copy()
        df_display.columns = [col.replace(" (kcal per 100g)", "").replace(" (g per 100g)", "").replace(" (mg per 100g)", "").title() for col in df_display.columns]

        st.dataframe(
            df_display.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-container">
        <div class="footer-logo">🥗 NutriCare Pro</div>
        <p style="margin-bottom: 1.5rem; opacity: 0.85; font-size: 1.1rem;">Advanced Personalized Clinical Nutrition & Dietetics Portal</p>
        <p style="font-size: 0.9rem; max-width: 650px; margin: 0 auto 1.5rem auto; opacity: 0.7; line-height: 1.6;">
            Leveraging state-of-the-art Machine Learning recommendation algorithms tailored specifically for Bangladeshi and global cuisine profiles with strict Halal validation.
        </p>
        <div style="width: 80px; height: 2px; background-color: #10b981; margin: 1.5rem auto;"></div>
        <p style="font-size: 0.8rem; opacity: 0.5; margin: 0;">
            © 2025 NutriCare Pro. Academic Project Presentation. For clinical evaluation only.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
