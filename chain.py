import streamlit as st
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import config


class Chain:
    def __init__(self):
        self.llm = ChatAnthropic(
            api_key=st.secrets["ANTHROPIC_API_KEY"],
            model=config.ANTHROPIC_MODEL_NAME
        )

        question_generation_template = ChatPromptTemplate([
            ("user", config.QUESTION_GENERATION_PROMPT)
        ])

        math_solver_template = ChatPromptTemplate([
            ("user", config.MATH_SOLVER_EXAMPLE),
            ("user", config.MATH_SOLVER_PROMPT)
        ])

        self._question_generation_chain = (question_generation_template | self.llm | StrOutputParser())
        self._math_solver_chain = (math_solver_template | self.llm | StrOutputParser())

    def question_generation(self, document: str, question_number_per_type: dict[str, int], difficulty: str,
                            question_types: list[str], single_option_number: int, multiple_option_number: int) -> str:
        return self._question_generation_chain.invoke({
            "document": document,
            "allowed_question_types": config.ALLOWED_QUESTION_TYPES,
            "allowed_difficulty_levels": config.ALLOWED_DIFFICULTY_LEVELS,
            "difficulty": difficulty,
            "question_types": question_types,
            "single_option_number": single_option_number,
            "multiple_option_number": multiple_option_number,
            "question_number_per_type": question_number_per_type
        })

    def math_solver(self, math_problem: str) -> str:
        return self._math_solver_chain.invoke({
            "math_problem": math_problem
        })
