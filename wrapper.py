import random
from abc import ABC, abstractmethod
from typing import Any
from xml.etree import ElementTree

import config


class BaseQuestion(ABC):
    @abstractmethod
    def get_data(self) -> dict[str, Any]:
        pass


class SingleCorrectQuestion(BaseQuestion):
    def __init__(self, element: ElementTree.Element):
        self._data = {
            "text": element.find("text").text,
            "options": [x.text for x in element.find("options").findall("option")],
            "answer": element.find("answers").find("answer").text
        }

    def get_data(self) -> dict[str, Any]:
        return self._data


class MultipleCorrectQuestion(BaseQuestion):
    def __init__(self, element: ElementTree.Element):
        self._data = {
            "text": element.find("text").text,
            "options": [x.text for x in element.find("options").findall("option")],
            "answers": [x.text for x in element.find("answers").findall("answer")]
        }

    def get_data(self) -> dict[str, Any]:
        return self._data


class TrueFalseQuestion(BaseQuestion):
    def __init__(self, element: ElementTree.Element):
        self._data = {
            "text": element.find("text").text,
            "answer": element.find("answers").find("answer").text
        }

    def get_data(self) -> dict[str, Any]:
        return self._data


class NoChoiceQuestion(BaseQuestion):
    def __init__(self, element: ElementTree.Element):
        self._data = {
            "text": element.find("text").text,
            "answer": element.find("answers").find("answer").text
        }

    def get_data(self) -> dict[str, Any]:
        return self._data


class Wrapper:
    def __init__(self, xml_str: str, seed: int):
        self._tree = self.str_to_xml(data=xml_str)

        self._question_list = self._tree.findall("question")
        self._index_list = list(range(self.__len__()))
        random.seed(seed)
        random.shuffle(self._index_list)

    def __len__(self) -> int:
        return len(self._question_list)

    def __getitem__(self, item: int) -> BaseQuestion:
        element = self._question_list[self._index_list[item]]
        question_type = element.find("type").text

        if question_type in config.ALLOWED_QUESTION_TYPES:
            if question_type.lower() == "single correct":
                return SingleCorrectQuestion(element=element)
            elif question_type.lower() == "multiple correct":
                return MultipleCorrectQuestion(element=element)
            elif question_type.lower() == "true/false":
                return TrueFalseQuestion(element=element)
            elif question_type.lower() == "no choice":
                return NoChoiceQuestion(element=element)
            else:
                raise NotImplementedError(f"Question Type '{question_type}' has no implementation!")
        else:
            raise TypeError(f"Question Type '{question_type}' is not allowed. "
                            f"Should be one of {config.ALLOWED_QUESTION_TYPES}!")

    @classmethod
    def get_tree(cls) -> ElementTree.ElementTree:
        return cls.str_to_xml(data="<questions></questions>")

    @staticmethod
    def str_to_xml(data: str) -> ElementTree.ElementTree:
        return ElementTree.ElementTree(ElementTree.fromstring(data))

    @staticmethod
    def xml_to_str(data: ElementTree.ElementTree) -> str:
        return ElementTree.tostring(data.getroot(), encoding="unicode", method="xml")
