import math
import random

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

    def generate_questions(self, text_chunks: list[str], question_number: int, difficulty: str,
                           question_types: list[str], single_option_number: int, multiple_option_number: int) -> str:
        chunk_number = len(text_chunks)
        average_chunk_size = sum([len(x) for x in text_chunks]) / chunk_number

        random_indexes = list(range(chunk_number))
        random.shuffle(random_indexes)

        result_xml = Wrapper.get_tree()
        result_xml_root = result_xml.getroot()

        # Text chunks are fed to LLM in random order
        for i in random_indexes:
            current_chunk = text_chunks[i]

            question_per_chunk = self.get_question_per_chunk(
                question_number=question_number,
                chunk_number=chunk_number,
                average_chunk_size=average_chunk_size,
                current_chunk_size=len(current_chunk)
            )

            current_questions = self._chain.question_generation(
                document=current_chunk,
                question_number=question_per_chunk,
                difficulty=difficulty,
                question_types=question_types,
                single_option_number=single_option_number,
                multiple_option_number=multiple_option_number
            )

            current_questions = Wrapper.str_to_xml(data=current_questions)
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
