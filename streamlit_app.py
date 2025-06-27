
import streamlit as st
import random
from quiz100 import malware_questions, pentest_questions, forensics_questions, cloud_questions
from quiz100 import network_questions, vmware_questions, iot_questions, appsec_questions
from quiz100 import reverse_engineering_questions, cryptography_questions

st.set_page_config(page_title="Cybersecurity Quiz", layout="wide")
st.title("🔐 Cybersecurity Quiz App")

# Combine all questions
all_questions = malware_questions + pentest_questions + forensics_questions + \
                cloud_questions + network_questions + vmware_questions + \
                iot_questions + appsec_questions + reverse_engineering_questions + \
                cryptography_questions

st.sidebar.header("🧠 Your Interests")
fields = sorted(set(q['field'] for q in all_questions))
languages = sorted(set(q['language_required'] for q in all_questions if q['language_required'] != "N/A"))

selected_fields = st.sidebar.multiselect("Select Cyber Fields:", fields)
selected_languages = st.sidebar.multiselect("Select Programming Languages:", languages)

# Filter questions based on user input
def filter_questions(questions, interests, languages):
    return [q for q in questions if q['field'] in interests or q['language_required'] in languages]

filtered_questions = filter_questions(all_questions, selected_fields, selected_languages)

if not filtered_questions:
    st.warning("No questions matched your selection. Please choose different fields or languages.")
    st.stop()

st.markdown("### ✅ Answer the questions below:")
user_answers = {}

for idx, question in enumerate(filtered_questions):
    st.markdown(f"**Q{idx+1}: {question['question']}**")
    user_choice = st.radio("", question['options'], key=question['id'])
    user_answers[question['id']] = user_choice

# Scoring function
def score_quiz(questions, user_answers):
    score = 0
    field_scores = {}
    for q in questions:
        correct = q['correct_answer']
        user = user_answers.get(q['id'])
        if user == correct:
            score += 1
            field_scores[q['field']] = field_scores.get(q['field'], 0) + 1
    return score, field_scores

def recommend_field(field_scores):
    if not field_scores:
        return "No strong recommendation"
    max_score = max(field_scores.values())
    top_fields = [field for field, score in field_scores.items() if score == max_score]
    return ", ".join(top_fields)

if st.button("🎯 Submit Quiz"):
    total_score, field_scores = score_quiz(filtered_questions, user_answers)
    st.success(f"Your Total Score: {total_score} / {len(filtered_questions)}")

    st.markdown("### 📊 Field-wise Scores:")
    for field, score in field_scores.items():
        st.write(f"- **{field}**: {score} correct")

    recommended = recommend_field(field_scores)
    st.markdown(f"### 🔍 Recommended Field: **{recommended}**")
