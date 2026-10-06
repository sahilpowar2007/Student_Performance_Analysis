import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Make the src folder importable so we can reuse the prediction function
sys.path.append("src")

from predict import predict_performance
from auth import init_db, create_user, authenticate_user

# 1. Page settings
st.set_page_config(page_title="Student Performance Analysis System",
                   page_icon="🎓", layout="wide")
# Initialize authentication database
init_db()
# ---------------- Authentication ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None
def show_auth_page():

    # ---------------- Premium Login Page CSS ----------------
    st.markdown(
        """
        <style>

        /* Main page background */
        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(59,130,246,0.12), transparent 28%),
                radial-gradient(circle at 90% 20%, rgba(99,102,241,0.12), transparent 28%),
                linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #f8faff 100%);
        }

        /* Remove excessive top space */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }

        /* Hero section */
        .login-hero {
            max-width: 900px;
            margin: 15px auto 28px auto;
            padding: 42px 35px;
            text-align: center;
            border-radius: 24px;
            background:
                linear-gradient(135deg, #0f2a5f 0%, #174ea6 52%, #2563eb 100%);
            box-shadow:
                0 18px 45px rgba(30, 64, 175, 0.22),
                inset 0 1px 0 rgba(255,255,255,0.18);
            position: relative;
            overflow: hidden;
        }

        .login-hero::before {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: rgba(255,255,255,0.08);
            top: -110px;
            right: -70px;
        }

        .login-hero::after {
            content: "";
            position: absolute;
            width: 170px;
            height: 170px;
            border-radius: 50%;
            background: rgba(255,255,255,0.06);
            bottom: -100px;
            left: -50px;
        }

        .hero-icon {
            font-size: 42px;
            margin-bottom: 8px;
        }

        .hero-title {
            color: white;
            font-size: 42px;
            font-weight: 800;
            line-height: 1.15;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: #e8f1ff;
            font-size: 17px;
            line-height: 1.6;
            max-width: 720px;
            margin: 14px auto 0 auto;
        }

        .hero-tag {
            display: inline-block;
            margin-top: 18px;
            padding: 7px 16px;
            border-radius: 30px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
        }

        /* Login area */
        .login-wrapper {
            max-width: 560px;
            margin: 0 auto;
        }

        /* Form labels */
        label {
            font-weight: 600 !important;
        }

        /* Input boxes */
        div[data-baseweb="input"] {
            border-radius: 12px !important;
        }

        div[data-baseweb="input"] input {
            font-size: 15px !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important;
        }

        /* Buttons */
        .stFormSubmitButton > button {
            width: 100%;
            min-height: 48px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            border: none;
            background: linear-gradient(90deg, #174ea6, #2563eb);
            color: white;
            transition: all 0.2s ease;
            box-shadow: 0 8px 18px rgba(37,99,235,0.20);
        }

        .stFormSubmitButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(37,99,235,0.28);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            justify-content: center;
            margin-bottom: 20px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 28px;
            border-radius: 12px;
            font-weight: 700;
            background: #e9f0ff;
        }

        .stTabs [aria-selected="true"] {
            background: #2563eb !important;
            color: white !important;
        }

        /* Welcome headings */
        h3 {
            color: #173b73;
            font-weight: 750;
        }

        /* Success / error messages */
        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1rem;
            }

            .login-hero {
                padding: 30px 18px;
                border-radius: 20px;
                margin-top: 5px;
            }

            .hero-title {
                font-size: 29px;
            }

            .hero-subtitle {
                font-size: 14px;
            }

            .hero-icon {
                font-size: 34px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 9px 14px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )
   # ---------------- Hero Header ----------------
st.html(
        """
        <div class="login-hero">
            <div class="hero-icon">🎓</div>
            <div class="hero-title">
                Student Performance Analysis System
            </div>
            <div class="hero-subtitle">
                Analyse student performance, generate predictions
                and identify academic attention indicators.
            </div>
            <div class="hero-tag">
                📊 Data Analytics &nbsp; • &nbsp; 🤖 AI Prediction &nbsp; • &nbsp; 🎯 Student Insights
            </div>
        </div>
        """
        )
    # ---------------- Login Area ----------------
left, center, right = st.columns([1, 2, 1])
with center:

        login_tab, signup_tab = st.tabs(
            ["🔐 Sign In", "📝 Sign Up"]
        )

        # ---------------- Sign In ----------------
        with login_tab:

            st.subheader("Welcome Back")
            st.caption("Sign in to access your student performance dashboard.")

            with st.form("login_form"):

                email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "🔐 Sign In",
                    use_container_width=True
                )

            if login_button:

                if not email or not password:

                    st.error("Please enter email and password.")

                else:

                    user = authenticate_user(
                        email,
                        password
                    )

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user = user

                        st.success("Login successful!")

                        st.rerun()

                    else:

                        st.error("Invalid email or password.")

        # ---------------- Sign Up ----------------
        with signup_tab:

            st.subheader("Create Account")
            st.caption("Create your account to start analysing student performance.")

            with st.form("signup_form"):

                full_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

                email = st.text_input(
                    "Email",
                    key="signup_email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="signup_password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                signup_button = st.form_submit_button(
                    "📝 Create Account",
                    use_container_width=True
                )

            if signup_button:

                if not full_name or not email or not password:

                    st.error("Please fill all required fields.")

                elif password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    success, message = create_user(
                        full_name,
                        email,
                        password
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Account created successfully. "
                            "Now open the Sign In tab and login."
                        )

                    else:

                        st.error(message)

# Show Login / Sign Up page before dashboard
if not st.session_state.logged_in:
    show_auth_page()
    st.stop()
ORDER = ["Low", "Average", "High"]
LEVEL_COLORS = {"Low": "#e74c3c", "Average": "#f39c12", "High": "#27ae60"}
INDICATOR_TEXT = {
    "low_recent_grade": "Low recent grade (G2 below 10)",
    "grade_drop": "Grade drop of 2 or more marks from G1 to G2",
    "past_failures": "One or more past failures",
    "high_absences": "High absences (top 25% of students)",
}
INDICATORS = list(INDICATOR_TEXT.keys())

# 2. Custom CSS for a clean, professional look
st.markdown(
    """
    <style>
    .banner {background: linear-gradient(90deg, #1e3a5f, #2c7be5);
             padding: 1.4rem 1.8rem; border-radius: 12px; margin-bottom: 1rem;}
    .banner h1 {color: white; margin: 0; font-size: 2rem;}
    .banner p {color: #dbe8ff; margin: 0.3rem 0 0 0;}
    [data-testid="stMetric"] {background: #ffffff; border: 1px solid #e3e8ef;
             border-left: 5px solid #2c7be5; padding: 0.8rem 1rem;
             border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);}
    [data-testid="stMetricLabel"] p {color: #4b5563;}
    [data-testid="stMetricValue"] {color: #1e3a5f;}
    .stTabs [data-baseweb="tab"] {background: #e3ecf7; border-radius: 8px 8px 0 0;
             padding: 0.5rem 1rem;}
    .stTabs [aria-selected="true"] {background: #2c7be5;}
    .stTabs [aria-selected="true"] p {color: white;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="banner">
        <h1>🎓 Student Performance Analysis System</h1>
        <p>Data analysis, performance prediction and academic attention indicators
        | Dataset: UCI Student Performance (student-mat.csv)</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# 3. Load all data once (cache makes the app faster)
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/student-mat-featured.csv")
    df.insert(0, "student_id", df.index + 1)
    att = pd.read_csv("reports/attention_indicators.csv")
    df = df.merge(att[["student_id"] + INDICATORS + ["indicator_count", "review_suggested"]],
                  on="student_id")
    reg = pd.read_csv("reports/regression_comparison.csv")
    clf = pd.read_csv("reports/classification_comparison.csv")
    imp = pd.read_csv("reports/feature_importance.csv")
    return df, reg, clf, imp


df, reg, clf, imp = load_data()
absence_limit = df["absences"].quantile(0.75)


# 4. Helper functions
def show(fig):
    st.pyplot(fig)
    plt.close(fig)


def bar_chart(series, title, xlabel, ylabel, colors="#2c7be5", fmt="%d"):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(series.index.astype(str), series.values, color=colors)
    ax.bar_label(bars, fmt=fmt)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def active_indicators(g1, g2, failures, absences):
    found = []
    if g2 < 10:
        found.append(INDICATOR_TEXT["low_recent_grade"])
    if g1 - g2 >= 2:
        found.append(INDICATOR_TEXT["grade_drop"])
    if failures >= 1:
        found.append(INDICATOR_TEXT["past_failures"])
    if absences > absence_limit:
        found.append(INDICATOR_TEXT["high_absences"])
    return found


def show_level(level):
    text = f"Predicted performance level: {level}"
    if level == "Low":
        st.error(text)
    elif level == "Average":
        st.warning(text)
    else:
        st.success(text)


def show_probabilities(probs):
    for name in ORDER:
        st.write(f"{name}: {round(probs[name] * 100, 1)}%")
        st.progress(float(probs[name]))


# 5. Sidebar filters
st.sidebar.title("🔧 Filters")
schools = sorted(df["school"].unique())
school_f = st.sidebar.multiselect("School", schools, default=schools)
sex_f = st.sidebar.multiselect("Sex", ["F", "M"], default=["F", "M"])
level_f = st.sidebar.multiselect("Performance level", ORDER, default=ORDER)
age_range = st.sidebar.slider("Age range", int(df["age"].min()), int(df["age"].max()),
                              (int(df["age"].min()), int(df["age"].max())))

fdf = df[
    df["school"].isin(school_f)
    & df["sex"].isin(sex_f)
    & df["performance_level"].isin(level_f)
    & df["age"].between(age_range[0], age_range[1])
]

st.sidebar.markdown("---")
st.sidebar.write(f"**Students selected:** {len(fdf)} of {len(df)}")
st.sidebar.caption("Filters apply to the Overview and Attention Indicators tabs.")

if fdf.empty:
    st.warning("No students match the selected filters. Please change the filters.")
    st.stop()

# 6. Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Overview", "🔎 Student Explorer", "🤖 Model Performance",
     "⚠️ Attention Indicators", "🎯 Predict", "📁 Upload Data"]
)

# ---------------- Tab 1: Overview ----------------
with tab1:
    passed = int((fdf["G3"] >= 10).sum())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Students", len(fdf))
    k2.metric("Average Final Grade (G3)", round(fdf["G3"].mean(), 2))
    k3.metric("Students with G3 of 10 or more", f"{passed} ({round(passed / len(fdf) * 100)}%)")
    k4.metric("Review Suggested", int(fdf["review_suggested"].sum()))

    st.subheader("Performance and grades")
    a, b = st.columns(2)
    counts = fdf["performance_level"].value_counts().reindex(ORDER).fillna(0)
    with a:
        show(bar_chart(counts, "Performance Level Distribution", "Performance Level",
                       "Number of Students", colors=[LEVEL_COLORS[x] for x in ORDER]))
    with b:
        grades = fdf[["G1", "G2", "G3"]].mean()
        show(bar_chart(grades, "Average Grade Progress (G1 to G3)", "Period",
                       "Average Grade", fmt="%.1f"))

    st.subheader("What is linked with the final grade?")
    c, d = st.columns(2)
    with c:
        show(bar_chart(fdf.groupby("studytime")["G3"].mean(), "Average G3 by Study Time",
                       "Study Time (1 = lowest, 4 = highest)", "Average G3",
                       colors="#16a085", fmt="%.1f"))
    with d:
        show(bar_chart(fdf.groupby("failures")["G3"].mean(), "Average G3 by Past Failures",
                       "Past Failures", "Average G3", colors="#8e44ad", fmt="%.1f"))

    e, f = st.columns(2)
    with e:
        show(bar_chart(fdf.groupby("school")["G3"].mean(), "Average G3 by School",
                       "School", "Average G3", colors="#34495e", fmt="%.1f"))
    with f:
        show(bar_chart(fdf.groupby("sex")["G3"].mean(), "Average G3 by Sex",
                       "Sex", "Average G3", colors="#d35400", fmt="%.1f"))

# ---------------- Tab 2: Student Explorer ----------------
with tab2:
    st.subheader("Student Profile")
    student_id = st.number_input("Enter Student ID (1 to 395)", min_value=1,
                                 max_value=len(df), value=1, step=1)
    row = df[df["student_id"] == student_id].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Performance Level", row["performance_level"])
    m2.metric("G1", int(row["G1"]))
    m3.metric("G2", int(row["G2"]))
    m4.metric("G3 (Final)", int(row["G3"]))

    n1, n2, n3, n4 = st.columns(4)
    n1.metric("Study Time", int(row["studytime"]))
    n2.metric("Past Failures", int(row["failures"]))
    n3.metric("Absences", int(row["absences"]))
    n4.metric("Attention Indicators", int(row["indicator_count"]))

    left, right = st.columns(2)
    with left:
        st.markdown("**Academic attention indicators**")
        found = active_indicators(row["G1"], row["G2"], row["failures"], row["absences"])
        if found:
            for text in found:
                st.write("• " + text)
        else:
            st.success("No indicators for this student.")
        st.caption("These are analytical indicators only, not final judgements.")
    with right:
        st.markdown("**Model prediction (using G1, G2 and other inputs, not G3)**")
        level, probs = predict_performance(
            row["school"], row["sex"], int(row["age"]), int(row["studytime"]),
            int(row["failures"]), int(row["absences"]), int(row["G1"]), int(row["G2"]))
        show_level(level)
        show_probabilities(probs)

    st.subheader("Top 10 students by final grade")
    top_cols = ["student_id", "school", "sex", "age", "G1", "G2", "G3", "studytime", "absences"]
    st.dataframe(fdf.nlargest(10, "G3")[top_cols], hide_index=True)

    st.subheader("Students with the most attention indicators")
    most = fdf.sort_values(["indicator_count", "G3"], ascending=[False, True]).head(10)
    st.dataframe(most[["student_id", "G1", "G2", "failures", "absences",
                       "indicator_count", "performance_level"]], hide_index=True)

# ---------------- Tab 3: Model Performance ----------------
with tab3:
    best_model = clf.loc[clf["Accuracy"].idxmax(), "Model"]
    st.info(f"Best classification model: **{best_model}** "
            f"(accuracy {clf['Accuracy'].max()}). It is used for predictions.")

    r1, r2 = st.columns(2)
    r1.subheader("Regression (predict G3)")
    r1.dataframe(reg, hide_index=True)
    r2.subheader("Classification (Low / Average / High)")
    r2.dataframe(clf, hide_index=True)

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Feature importance")
        imp_sorted = imp.sort_values("Importance")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.barh(imp_sorted["Feature"], imp_sorted["Importance"], color="#2c7be5")
        ax.set_xlabel("Importance Score")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        show(fig)
    with g2:
        st.subheader("Confusion matrix (Random Forest)")
        st.image("visualizations/confusion_matrix_rf.png")

    st.caption("G1 and G2 are earlier grades, so they are the strongest inputs. "
               "G3 is never used as an input to avoid target leakage.")

# ---------------- Tab 4: Attention Indicators ----------------
with tab4:
    st.write("These are analytical indicators only, not final judgements about students.")
    with st.expander("How are the indicators defined?"):
        for text in INDICATOR_TEXT.values():
            st.write("• " + text)
        st.write("• Review suggested = 2 or more indicators present")

    x1, x2 = st.columns(2)
    with x1:
        ind_counts = fdf[INDICATORS].sum()
        show(bar_chart(ind_counts, "Students per Indicator", "Indicator", "Number of Students"))
    with x2:
        ct = pd.crosstab(fdf["performance_level"], fdf["review_suggested"])
        ct = ct.reindex(index=ORDER, columns=[0, 1], fill_value=0)
        ct.columns = ["Not flagged", "Review suggested"]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ct.plot(kind="bar", ax=ax, color=["#95a5a6", "#e67e22"])
        ax.set_title("Review Suggested by Performance Level", fontweight="bold")
        ax.set_xlabel("Performance Level")
        ax.set_ylabel("Number of Students")
        ax.tick_params(axis="x", rotation=0)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        show(fig)

    show_flagged = st.checkbox("Show only students with review suggested")
    table = fdf[fdf["review_suggested"] == 1] if show_flagged else fdf
    table = table.sort_values("indicator_count", ascending=False)
    att_cols = ["student_id", "school", "sex", "age", "G1", "G2", "failures", "absences",
                "indicator_count", "review_suggested", "performance_level"]
    st.dataframe(table[att_cols], hide_index=True)
    st.download_button("⬇️ Download this table as CSV",
                       table[att_cols].to_csv(index=False).encode("utf-8"),
                       file_name="attention_indicators_filtered.csv", mime="text/csv")

# ---------------- Tab 5: Predict ----------------
with tab5:
    st.subheader("Predict Student Performance")
    st.write("Enter a student's details to predict the performance level.")

    with st.form("predict_form"):
        p1, p2, p3, p4 = st.columns(4)
        school = p1.selectbox("School", ["GP", "MS"])
        sex = p2.selectbox("Sex", ["F", "M"])
        age = p3.number_input("Age", min_value=15, max_value=22, value=17)
        studytime = p4.selectbox("Study time (1 = lowest, 4 = highest)", [1, 2, 3, 4], index=1)

        p5, p6, p7, p8 = st.columns(4)
        failures = p5.number_input("Past failures", min_value=0, max_value=4, value=0)
        absences = p6.number_input("Absences", min_value=0, max_value=100, value=4)
        G1 = p7.number_input("G1 (first period grade, 0-20)", min_value=0, max_value=20, value=10)
        G2 = p8.number_input("G2 (second period grade, 0-20)", min_value=0, max_value=20, value=10)

        submitted = st.form_submit_button("Predict")

    if submitted:
        level, probs = predict_performance(school, sex, age, studytime, failures,
                                           absences, G1, G2)
        res1, res2 = st.columns(2)
        with res1:
            show_level(level)
            show_probabilities(probs)
        with res2:
            st.markdown("**Academic attention indicators for this input**")
            found = active_indicators(G1, G2, failures, absences)
            if found:
                for text in found:
                    st.write("• " + text)
            else:
                st.success("No indicators.")
        st.caption("This is a model prediction for learning purposes, "
                   "not a final judgement about a student.")

# ---------------- Tab 6: Upload Data ----------------
with tab6:
    st.subheader("Upload Student Data")
    st.write("Upload a CSV or Excel file with your own students to get "
             "predictions and attention indicators.")

    REQUIRED = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]

    # 1. Template file the user can download and fill in
    template = pd.DataFrame([
        {"student_name": "Student A", "school": "GP", "sex": "F", "age": 17,
         "studytime": 2, "failures": 0, "absences": 4, "G1": 10, "G2": 11},
        {"student_name": "Student B", "school": "MS", "sex": "M", "age": 16,
         "studytime": 3, "failures": 1, "absences": 12, "G1": 14, "G2": 9},
    ])
    st.download_button("⬇️ Download template CSV",
                       template.to_csv(index=False).encode("utf-8"),
                       file_name="student_template.csv", mime="text/csv")
    st.caption("Required columns: school (GP/MS), sex (F/M), age, studytime (1-4), "
               "failures, absences, G1 (0-20), G2 (0-20). "
               "Extra columns like student_name are kept.")

    # 2. File upload
    uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded is not None:
        up = None
        try:
            if uploaded.name.lower().endswith(".csv"):
                up = pd.read_csv(uploaded)
            else:
                up = pd.read_excel(uploaded)
        except Exception as error:
            st.error(f"Could not read the file: {error}")

        if up is not None:
            up.columns = [str(c).strip() for c in up.columns]
            missing = [c for c in REQUIRED if c not in up.columns]

            if missing:
                st.error("Missing columns: " + ", ".join(missing))
            else:
                # 3. Clean and check the data
                up["school"] = up["school"].astype(str).str.strip().str.upper()
                up["sex"] = up["sex"].astype(str).str.strip().str.upper()
                number_cols = ["age", "studytime", "failures", "absences", "G1", "G2"]
                for c in number_cols:
                    up[c] = pd.to_numeric(up[c], errors="coerce")

                problems = []
                if up[number_cols].isnull().any().any():
                    problems.append("Some number cells are empty or not valid numbers.")
                if not up["school"].isin(["GP", "MS"]).all():
                    problems.append("school must be GP or MS.")
                if not up["sex"].isin(["F", "M"]).all():
                    problems.append("sex must be F or M.")
                if not up["G1"].between(0, 20).all() or not up["G2"].between(0, 20).all():
                    problems.append("G1 and G2 must be between 0 and 20.")
                if not up["studytime"].between(1, 4).all():
                    problems.append("studytime must be between 1 and 4.")
                if (up["failures"] < 0).any() or (up["absences"] < 0).any():
                    problems.append("failures and absences cannot be negative.")

                if problems:
                    for p in problems:
                        st.error(p)
                else:
                    # 4. Predict for every student
                    levels, confidence = [], []
                    for _, r in up.iterrows():
                        level, probs = predict_performance(
                            r["school"], r["sex"], int(r["age"]), int(r["studytime"]),
                            int(r["failures"]), int(r["absences"]),
                            int(r["G1"]), int(r["G2"]))
                        levels.append(level)
                        confidence.append(round(max(probs.values()) * 100, 1))
                    up["predicted_level"] = levels
                    up["confidence_%"] = confidence

                    # 5. Attention indicators (same rules as before)
                    up["low_recent_grade"] = (up["G2"] < 10).astype(int)
                    up["grade_drop"] = ((up["G1"] - up["G2"]) >= 2).astype(int)
                    up["past_failures"] = (up["failures"] >= 1).astype(int)
                    up["high_absences"] = (up["absences"] > absence_limit).astype(int)
                    up["indicator_count"] = up[INDICATORS].sum(axis=1)
                    up["review_suggested"] = (up["indicator_count"] >= 2).astype(int)

                    # 6. Summary
                    st.success(f"File checked successfully: {len(up)} students.")
                    u1, u2, u3, u4 = st.columns(4)
                    u1.metric("Students", len(up))
                    u2.metric("Predicted Low", int((up["predicted_level"] == "Low").sum()))
                    u3.metric("Predicted High", int((up["predicted_level"] == "High").sum()))
                    u4.metric("Review Suggested", int(up["review_suggested"].sum()))

                    chart_counts = up["predicted_level"].value_counts().reindex(ORDER).fillna(0)
                    show(bar_chart(chart_counts, "Predicted Performance Levels",
                                   "Performance Level", "Number of Students",
                                   colors=[LEVEL_COLORS[x] for x in ORDER]))

                    # 7. Coloured result table
                    def color_level(value):
                        colors = {"Low": "#f8d7da", "Average": "#fff3cd", "High": "#d4edda"}
                        return f"background-color: {colors.get(value, '')}"

                    st.dataframe(up.style.map(color_level, subset=["predicted_level"]),
                                 hide_index=True)

                    st.download_button("⬇️ Download results as CSV",
                                       up.to_csv(index=False).encode("utf-8"),
                                       file_name="uploaded_students_results.csv",
                                       mime="text/csv")
                    st.caption("Predictions come from the saved model. The model is not "
                               "retrained on your file. These are analytical indicators, "
                               "not final judgements about students.")

# 7. Footer
st.markdown("---")
st.caption("Note: The UCI dataset does not contain attendance percentage, assignment marks "
           "or practical marks. Absences, study time, failures and grades are used instead.")