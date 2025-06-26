
import streamlit as st
import random
from quiz100 import malware_questions, pentest_questions, forensics_questions, cloud_questions
from quiz100 import network_questions, vmware_questions, iot_questions, appsec_questions
from quiz100 import reverse_engineering_questions, cryptography_questions

# Combine all question sets
all_questions = (
    malware_questions + pentest_questions + forensics_questions + cloud_questions +
    network_questions + vmware_questions + iot_questions + appsec_questions +
    reverse_engineering_questions + cryptography_questions
)

# App title
st.set_page_config(page_title="Cybersecurity Field Quiz", page_icon="🔐")
st.title("🔐 Cybersecurity Field Recommendation Quiz")
st.write("Welcome! This quiz helps you discover your ideal cybersecurity field based on your interests and coding knowledge.")

# Sidebar
st.sidebar.header("👤 Your Profile")
interests = st.sidebar.multiselect(
    "Select your cybersecurity interests:",
    sorted(set(q["field"] for q in all_questions))
)
languages = st.sidebar.multiselect(
    "Which programming languages do you know?",
    sorted(set(q["language_required"] for q in all_questions if q["language_required"] != "N/A"))
)

# Filter logic
def filter_questions(questions, interests, languages):
    return [
        q for q in questions
        if q["field"] in interests or q.get("language_required") in languages
    ]

filtered_questions = filter_questions(all_questions, interests, languages)
random.shuffle(filtered_questions)
quiz_questions = filtered_questions[:10]

user_answers = {}
if quiz_questions:
    st.header("📝 Quiz")
    for idx, q in enumerate(quiz_questions):
        answer = st.radio(
            f"Q{idx + 1}: {q['question']}",
            q["options"],
            key=q["id"]
        )
        user_answers[q["id"]] = answer

    if st.button("Submit Quiz"):
        score = 0
        field_scores = {}

        for q in quiz_questions:
            if user_answers.get(q["id"]) == q["correct_answer"]:
                score += 1
                field_scores[q["field"]] = field_scores.get(q["field"], 0) + 1

        st.success(f"✅ Your Score: {score}/{len(quiz_questions)}")

        if field_scores:
            max_score = max(field_scores.values())
            recommended_fields = [f for f, s in field_scores.items() if s == max_score]

            st.markdown("### 🧠 Recommended Field(s):")
            for field in recommended_fields:
                st.markdown(f"- **{field}**")
        else:
            st.warning("No strong recommendation. Try choosing more interests or languages.")
else:
    st.info("⬅️ Please select interests and languages in the sidebar to start the quiz.")
