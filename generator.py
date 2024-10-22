import re
import math
import random
from xml.etree import ElementTree

import config
from chain import Chain
from wrapper import Wrapper


class Generator:
    def __init__(self):
        self._chain = Chain()

    @staticmethod
    def get_question_per_chunk(question_number: int, chunk_number: int,
                               current_chunk_size: int, average_chunk_size: float) -> int:
        if question_number < chunk_number:
            return 1
        else:
            coefficient = current_chunk_size / average_chunk_size
            return math.ceil(coefficient * question_number / chunk_number)

    def get_math_problem_answer_clean(self, math_problem: str) -> str:
        answer_tags = ("<answer>", "</answer>")
        model_answer = self._chain.math_solver(math_problem=math_problem)

        answer = "empty"
        answer_start = model_answer.find(answer_tags[0]) + len(answer_tags[0])
        answer_stop = model_answer.find(answer_tags[1])
        if answer_start > -1 and answer_stop > -1:
            possible_answer = model_answer[answer_start:answer_stop]
            possible_answer = re.search(pattern=Wrapper.get_float_regexp(), string=possible_answer)
            if possible_answer:
                answer = possible_answer.group()
        return answer

    def add_answer_to_math_problems(self, questions: ElementTree.ElementTree) -> ElementTree.ElementTree:
        for element in questions.findall("question"):
            element_type = element.find("type").text
            if element_type.lower() == "math problem":
                answers = ElementTree.SubElement(element, "answers")
                answer = ElementTree.SubElement(answers, "answer")
                answer.text = self.get_math_problem_answer_clean(math_problem=element.find("text").text)
        return questions

    def generate_questions(self, text_chunks: list[str], question_number: int, difficulty: str,
                           question_types: list[str], single_option_number: int, multiple_option_number: int) -> str:
        chunk_number = len(text_chunks)
        average_chunk_size = sum([len(x) for x in text_chunks]) / chunk_number

        random_indexes = list(range(chunk_number))
        random.shuffle(random_indexes)

        result_xml = Wrapper.get_tree()
        result_xml_root = result_xml.getroot()

        current_question_type_dist = config.DIFFICULTY_QUESTION_TYPE_DISTRIBUTION[difficulty]
        current_question_type_dist = dict(
            (key, val) for key, val in current_question_type_dist.items() if key in question_types
        )
        current_question_type_dist = dict(
            (key, val / sum(current_question_type_dist.values())) for key, val in current_question_type_dist.items()
        )

        # Text chunks are fed to LLM in random order
        for i in random_indexes:
            current_chunk = text_chunks[i]

            question_per_chunk = self.get_question_per_chunk(
                question_number=question_number,
                chunk_number=chunk_number,
                average_chunk_size=average_chunk_size,
                current_chunk_size=len(current_chunk)
            )

            question_number_per_type_per_chunk = dict(
                (key, math.ceil(val * question_per_chunk)) for key, val in current_question_type_dist.items()
            )

            current_questions = self._chain.question_generation(
                document=current_chunk,
                question_number_per_type=question_number_per_type_per_chunk,
                difficulty=difficulty,
                question_types=question_types,
                single_option_number=single_option_number,
                multiple_option_number=multiple_option_number
            )

            current_questions = Wrapper.str_to_xml(data=current_questions)
            current_questions = self.add_answer_to_math_problems(questions=current_questions)
            current_len = len(current_questions.findall("question"))

            # Trying to stop generation early
            result_len = len(result_xml.findall("question"))
            if result_len + current_len > question_number:
                result_xml_root.extend(current_questions.findall("question")[:question_number - result_len])
                break

            result_xml_root.extend(current_questions.getroot())

        # Failsafe: Ensure the requested number of questions is met
        result_len = len(result_xml.findall("question"))
        if result_len < question_number:
            duplicates = random.sample(population=result_xml_root.findall("question"), k=question_number - result_len)
            result_xml_root.extend(duplicates)

        return Wrapper.xml_to_str(data=result_xml)
