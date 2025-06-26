import streamlit as st
import random

from quiz_data import all_questions

st.set_page_config(page_title="Cybersecurity Quiz App", layout="wide")
st.title("Cybersecurity Quiz App")

# User preferences
user_interests = st.multiselect(
    "Select your fields of interest:",
    options=list(set(q["field"] for q in all_questions)),
    default=["Malware Analysis", "Penetration Testing"]
)

user_languages = st.multiselect(
    "Select languages you are comfortable with:",
    options=sorted(set(q["language_required"] for q in all_questions if q["language_required"] != "N/A")),
    default=["Python", "C/C++"]
)

# Filter questions
def filter_questions(questions, interests, languages):
    return [
        q for q in questions
        if q["field"] in interests or q["language_required"] in languages
    ]

selected_questions = filter_questions(all_questions, user_interests, user_languages)

if not selected_questions:
    st.warning("No questions matched your interests and known languages.")
    st.stop()

# Store user answers
user_answers = {}
st.subheader("Answer the questions below:")

for idx, question in enumerate(selected_questions):
    st.markdown(f"**Q{idx + 1}: {question['question']}**")
    user_answers[question["id"]] = st.radio(
        "Select your answer:",
        options=question["options"],
        key=f"q_{question['id']}"
    )

# Submit button
if st.button("Submit Quiz"):
    def score_quiz(questions, user_answers):
        score = 0
        field_scores = {}
        for q in questions:
            correct = q["correct_answer"]
            user = user_answers.get(q["id"])
            if user == correct:
                score += 1
                field_scores[q["field"]] = field_scores.get(q["field"], 0) + 1
        return score, field_scores

    def recommend_field(field_scores):
        if not field_scores:
            return "No strong recommendation"
        max_score = max(field_scores.values())
        top_fields = [field for field, score in field_scores.items() if score == max_score]
        return ", ".join(top_fields)

    total_score, field_scores = score_quiz(selected_questions, user_answers)
    recommended = recommend_field(field_scores)

    st.success(f"Your Total Score: {total_score} / {len(selected_questions)}")
    st.markdown("### Field-wise Scores:")
    for field, score in field_scores.items():
        st.write(f"- {field}: {score} correct")

    st.markdown(f"### Recommended Field(s): **{recommended}**")
