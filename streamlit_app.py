
import streamlit as st
import random
from quiz100 import malware_questions, pentest_questions, forensics_questions, cloud_questions
from quiz100 import network_questions, vmware_questions, iot_questions, appsec_questions
from quiz100 import reverse_engineering_questions, cryptography_questions

# Merge all questions into a single list
all_questions = (
    malware_questions + pentest_questions + forensics_questions + cloud_questions +
    network_questions + vmware_questions + iot_questions + appsec_questions +
    reverse_engineering_questions + cryptography_questions
)

# App title and description
st.title("🔐 Cybersecurity Field Recommendation Quiz")
st.write("Welcome! This quiz will help you discover the cybersecurity field that best matches your interests and programming knowledge.")

# Sidebar inputs
st.sidebar.header("👤 Your Profile")
interests = st.sidebar.multiselect(
    "Select your interests in cybersecurity:",
    sorted(set(q["field"] for q in all_questions))
)
languages = st.sidebar.multiselect(
    "Which programming languages do you know?",
    sorted(set(q["language_required"] for q in all_questions if q["language_required"] != "N/A"))
)

# Filter questions
def filter_questions(questions, interests, languages):
    return [
        q for q in questions
        if q["field"] in interests or q.get("language_required") in languages
    ]

filtered_questions = filter_questions(all_questions, interests, languages)
random.shuffle(filtered_questions)
quiz_questions = filtered_questions[:10]  # limit to 10 questions

# Collect user answers
user_answers = {}
if quiz_questions:
    st.header("📝 Quiz Section")
    for idx, q in enumerate(quiz_questions):
        user_choice = st.radio(
            f"Q{idx+1}: {q['question']}",
            q["options"],
            key=q["id"]
        )
        user_answers[q["id"]] = user_choice

    # Submit and score
    if st.button("Submit Quiz"):
        score = 0
        field_scores = {}

        for q in quiz_questions:
            if user_answers.get(q["id"]) == q["correct_answer"]:
                score += 1
                field_scores[q["field"]] = field_scores.get(q["field"], 0) + 1

        st.success(f"🎯 Your Score: {score}/{len(quiz_questions)}")

        if field_scores:
            st.markdown("### 🧠 Recommended Field(s):")
            max_score = max(field_scores.values())
            top_fields = [f for f, s in field_scores.items() if s == max_score]
            for field in top_fields:
                st.markdown(f"- **{field}**")
        else:
            st.warning("No clear recommendation. Try selecting broader interests or skills.")
else:
    st.info("⬅️ Choose interests and languages from the sidebar to begin the quiz.")
