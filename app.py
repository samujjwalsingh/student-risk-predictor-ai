import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- GEMINI API CONFIGURATION ---
try:
    # Use Streamlit's secrets management for the API key [1]
    api_key = st.secrets
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🚨 Gemini API key not found. Please add it to your Streamlit secrets.", icon="🔑")
    st.stop()


# --- THE APP INTERFACE ---

st.title("🎓 Student Dropout Prediction")
st.markdown("Enter a student's key indicators to get an AI-powered prediction of their dropout risk.")

# --- INPUT FORM IN THE SIDEBAR ---
with st.sidebar:
    st.header("📝 Student Data Input")
    
    # Create a form for a cleaner UI that batches inputs
    with st.form("student_data_form"):
        # Input fields for student data
        attendance = st.slider("Attendance Percentage (%)", 0, 100, 85, help="The student's overall attendance rate.")
        avg_score = st.slider("Average Assessment Score (%)", 0, 100, 70, help="The student's average score across recent tests and assignments.")
        failed_subjects = st.number_input("Number of Failed Subjects (Last Term)", min_value=0, max_value=10, value=0, help="How many subjects the student failed in the previous term.")
        fee_status = st.selectbox("Fee Payment Status", ["Paid", "Overdue", "On Extension"], help="The status of the student's tuition fee payments.")
        
        # The submit button for the form
        submitted = st.form_submit_button("🔮 Predict Dropout Risk")

# --- PREDICTION LOGIC AND DISPLAY ---
if submitted:
    # Construct a detailed prompt for the Gemini API
    prompt = f"""
    As an expert educational analyst, predict the dropout risk for a student with the following profile. 
    Provide a clear risk level (Low, Medium, or High) and a concise, bulleted justification for your prediction based on the provided data.

    **Student Data:**
    - **Overall Attendance:** {attendance}%
    - **Average Assessment Score:** {avg_score}%
    - **Failed Subjects Last Term:** {failed_subjects}
    - **Fee Payment Status:** '{fee_status}'

    **Analysis:**
    """

    # Show a spinner while the prediction is being generated
    with st.spinner("🧠 The AI is analyzing the data..."):
        try:
            response = model.generate_content(prompt)
            
            # Display the prediction result
            st.subheader("📊 Prediction Result")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
else:
    # Initial instruction message
    st.info("Please fill in the student's data in the sidebar and click 'Predict Dropout Risk' to see the analysis.")
