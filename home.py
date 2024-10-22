from urllib.parse import urljoin

import streamlit as st

import config
from database import Database
from generator import Generator
from reader import Reader


class Home:
    def __init__(self):
        st.set_page_config(page_title="Home")

        self._init_session_variables()
        self._define_custom_css()

        self.database = Database()
        self.generator = Generator()
        self.reader = Reader()

    @staticmethod
    def _init_session_variables():
        # Initialize session variables if they do not exist
        default_values = {
            "show_generator": True,
            "quiz_pool": []
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
    def _display_quiz_link(link: str):
        st.code(link, language="text")
        st.link_button(label="Go To Quiz", url=link)

    @staticmethod
    def _toggle_show_generator_flag():
        st.session_state.show_generator = not st.session_state.show_generator

    def _show_history(self):
        st.title("Quiz History")
        st.button(label="Go Back", on_click=self._toggle_show_generator_flag)

        if len(st.session_state.quiz_pool):
            for name, link in st.session_state.quiz_pool[::-1]:
                with st.container(border=True):
                    st.write(name)
                    self._display_quiz_link(link=link)

    def _build_page(self):
        st.title("Quiz Generator")

        file_label = "Upload File"
        name_label = "Quiz Name"
        question_number_label = "Number of Questions"
        difficulty_label = "Difficulty Level"
        question_types_label = "Choose Type of Questions"
        single_option_number_label = "Number of option for 'Single Correct' Questions"
        multiple_option_number_label = "Number of option for 'Multiple Correct' Questions"

        # the input form
        with st.form("user_inputs"):
            file = st.file_uploader(label=file_label, type=config.ALLOWED_FILE_TYPES)

            name = st.text_input(
                label=name_label,
                value="Quiz",
                max_chars=256
            )
            question_number = st.number_input(
                label=question_number_label,
                min_value=1,
                max_value=100,
                value=10
            )
            difficulty = st.selectbox(
                label=difficulty_label,
                options=config.ALLOWED_DIFFICULTY_LEVELS,
                index=0
            )
            question_types = st.multiselect(
                label=question_types_label,
                options=config.ALLOWED_QUESTION_TYPES,
                default=config.ALLOWED_QUESTION_TYPES[1]
            )
            single_option_number = st.number_input(
                label=single_option_number_label,
                min_value=2,
                max_value=10,
                value=4
            )
            multiple_option_number = st.number_input(
                label=multiple_option_number_label,
                min_value=3,
                max_value=20,
                value=6
            )

            button = st.form_submit_button("Generate")

            if button:
                if not file:
                    st.warning(body=f"Please select file in '{file_label}'!", icon="⚠️")
                elif not name:
                    st.warning(body=f"Please input '{name_label}'!", icon="⚠️")
                elif not question_number:
                    st.warning(body=f"Please select '{question_number_label}'!", icon="⚠️")
                elif not difficulty:
                    st.warning(body=f"Please select '{difficulty_label}'!", icon="⚠️")
                elif not question_types:
                    st.warning(body=f"Please select '{question_types_label}'!", icon="⚠️")
                elif not single_option_number:
                    st.warning(body=f"Please select '{single_option_number_label}'!", icon="⚠️")
                elif not multiple_option_number:
                    st.warning(body=f"Please select '{multiple_option_number_label}'!", icon="⚠️")
                else:
                    with st.spinner("Loading..."):
                        text = self.reader.process_file(file=file)
                        text_chunks = self.reader.get_text_chunks(text=text)

                        quiz_xml = self.generator.generate_questions(
                            text_chunks=text_chunks,
                            question_number=question_number,
                            difficulty=difficulty,
                            question_types=question_types,
                            single_option_number=single_option_number,
                            multiple_option_number=multiple_option_number
                        )

                        key = self.database.add_new_quiz(quiz_xml=quiz_xml, name=name)
                        link = urljoin(st.secrets["BASE_URL"], f"quiz?key={key}")

                        st.session_state.quiz_pool.append(
                            (name, link)
                        )

                        st.markdown("""___""")
                        st.subheader("Link for generated quiz", anchor=False)
                        self._display_quiz_link(link=link)

        if len(st.session_state.quiz_pool):
            st.button(label="Show History", on_click=self._toggle_show_generator_flag)

    def run(self):
        if st.session_state.show_generator:
            self._build_page()
        else:
            self._show_history()


page = Home()
page.run()
