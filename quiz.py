import random

import streamlit as st

from database import Database
from wrapper import BaseQuestion
from wrapper import MultipleCorrectQuestion
from wrapper import NoChoiceQuestion
from wrapper import SingleCorrectQuestion
from wrapper import TrueFalseQuestion
from wrapper import Wrapper


class Quiz:
    def __init__(self):
        st.set_page_config(page_title="Quiz App")

        self._init_session_variables()
        self._define_custom_css()

        self.database = Database()

        self.name = "Quiz"
        self.quiz = None
        if "key" in st.query_params.keys():
            result = self.database.get_quiz_by_key(key=st.query_params["key"])
            if result:
                self.name = result["name"]
                self.quiz = Wrapper(xml_str=result["quiz_xml"], seed=st.session_state.seed)

    @staticmethod
    def _init_session_variables():
        # Initialize session variables if they do not exist
        default_values = {
            "current_index": 0,
            "score": 0,
            "seed": random.randint(0, 2_000_000),
            "selected_options": [],
            "submit_pressed": False,
            "answer_submitted": False
        }
        for key, value in default_values.items():
            st.session_state.setdefault(key, value)

    @staticmethod
    def _define_custom_css():
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            display: block;
            margin: 0 auto;
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def _next_question():
        st.session_state.current_index += 1
        st.session_state.selected_options = []
        st.session_state.answer_submitted = False

    @staticmethod
    def _restart_quiz():
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.selected_options = []
        st.session_state.answer_submitted = False

    @staticmethod
    def _show_result_message(answers: list, selected_options: list):
        counter = 0
        for answer in answers:
            if answer in selected_options:
                counter += 1

        if counter == len(answers):
            st.success(f"Correct answer")
        elif counter == 0:
            st.error(f"Incorrect answer. Should be: {answers if len(answers) > 1 else answers[0]}")
        else:
            st.warning(f"Partially correct answer. Should be: {answers}")

    def _handle_question_display_and_logic(self, question: BaseQuestion) -> tuple[list, float]:
        question_data = question.get_data()

        selected_options = []
        current_score = 0

        # Display the question and answer options
        st.subheader(f"Question {st.session_state.current_index + 1} out of {len(self.quiz)}")
        st.write(f"{question_data['text']}")
        st.markdown("""___""")

        # Answer selection
        if type(question) is SingleCorrectQuestion:
            options = question_data["options"]
            answer = question_data["answer"]

            if st.session_state.answer_submitted:
                user_choice = st.radio(
                    label="radio",
                    options=options,
                    index=options.index(st.session_state.selected_options[0]),
                    label_visibility="collapsed",
                    disabled=True
                )
                self._show_result_message(answers=[answer], selected_options=st.session_state.selected_options)

            else:
                user_choice = st.radio(
                    label="radio",
                    options=options,
                    index=None,
                    label_visibility="collapsed"
                )
                if user_choice:
                    selected_options = [user_choice]
                    current_score = 1 if user_choice == answer else 0

        elif type(question) is MultipleCorrectQuestion:
            options = question_data["options"]
            answers = question_data["answers"]

            if st.session_state.answer_submitted:
                user_choice = [st.checkbox(
                    label=x,
                    value=x in st.session_state.selected_options,
                    disabled=True
                ) for x in options]
                self._show_result_message(answers=answers, selected_options=st.session_state.selected_options)
            else:
                user_choice = [st.checkbox(label=x) for x in options]
                if sum(user_choice) > 0:
                    for i in range(len(options)):
                        is_selected = user_choice[i]
                        if is_selected:
                            selected_options.append(options[i])
                            current_score += 1 if options[i] in answers else 0
                    current_score /= len(answers)

        elif type(question) is TrueFalseQuestion:
            options = ["True", "False"]
            options_lowercase = [x.lower() for x in options]
            answer = question_data["answer"]

            if st.session_state.answer_submitted:
                user_choice = st.radio(
                    label="radio",
                    options=options,
                    index=options_lowercase.index(st.session_state.selected_options[0]),
                    label_visibility="collapsed",
                    disabled=True
                )
                self._show_result_message(
                    answers=[options[options_lowercase.index(answer)]],
                    selected_options=[options[options_lowercase.index(x)] for x in st.session_state.selected_options]
                )

            else:
                user_choice = st.radio(
                    label="radio",
                    options=options,
                    index=None,
                    label_visibility="collapsed"
                )
                if user_choice:
                    selected_options = [user_choice.lower()]
                    current_score = 1 if user_choice.lower() == answer else 0

        elif type(question) is NoChoiceQuestion:
            answer = question_data["answer"]

            if st.session_state.answer_submitted:
                user_choice = st.text_input(
                    label="text_input",
                    value=st.session_state.selected_options[0],
                    max_chars=256,
                    placeholder="Input your answer",
                    label_visibility="collapsed",
                    disabled=True
                )
                self._show_result_message(answers=[answer], selected_options=st.session_state.selected_options)

            else:
                user_choice = st.text_input(
                    label="text_input",
                    max_chars=256,
                    placeholder="Input your answer",
                    label_visibility="collapsed",
                )
                if user_choice:
                    selected_options = [user_choice]
                    current_score = 1 if user_choice.lower() == answer.lower() else 0

        return selected_options, current_score

    def _build_page(self):
        # Title and description and metric
        st.title(self.name)
        total_percentage = round(100 * st.session_state.score / len(self.quiz), 2)

        if st.session_state.current_index >= len(self.quiz):
            # End of quiz
            st.header(f"Quiz completed!", anchor=False)
            st.subheader(f"Your score is:", anchor=False)
            st.title(f"{total_percentage}% / 100%", anchor=False)
            if st.button('Restart', on_click=self._restart_quiz):
                pass

        else:
            # Quiz in progress
            question = self.quiz[st.session_state.current_index]
            st.metric(label="Score", value=f"{total_percentage}% / 100%")

            # Progress bar
            progress_bar_value = (st.session_state.current_index + 1) / len(self.quiz)
            st.progress(progress_bar_value)

            selected_options, current_score = self._handle_question_display_and_logic(question=question)
            st.markdown("""___""")

            # Submission button and response logic
            if st.session_state.answer_submitted:
                st.button('Next', on_click=self._next_question)

            else:
                if st.button('Submit'):
                    # Check if an option has been selected
                    if len(selected_options):
                        st.session_state.answer_submitted = True
                        st.session_state.selected_options = selected_options
                        st.session_state.score += current_score
                        st.rerun()
                    else:
                        # If no option selected, show a message and do not mark as submitted
                        st.warning("Please select an option before submitting.")

    @staticmethod
    def _quiz_dont_exist():
        st.title("This Quiz dont exist!")
        st.subheader(f"Check if your link is valid")

    @staticmethod
    def _build_quiz_pool():
        print(st.session_state.quiz_pool)

    def run(self):
        if self.quiz:
            self._build_page()
        else:
            self._quiz_dont_exist()


page = Quiz()
page.run()
