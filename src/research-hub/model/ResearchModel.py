import datetime
import json
import time
from dataclasses import dataclass
from typing import List


@dataclass
class TagModel:
    name: str
    created_by: str = ""
    created: int = int(time.time() * 1000)


@dataclass
class ResearchModel:
    key: str
    title: str
    description: str
    created_by: str
    created_by_UID: str
    created: int = int(time.time() * 1000)  # Convert to milliseconds
    dead_line: int = None
    tags: str = ""
    questions: str = ""

    @property
    def formattedTime(self) -> str:
        return datetime.datetime.fromtimestamp(self.created / 1000).strftime('%d %b %Y')

    @property
    def formattedDeadline(self) -> str:
        if self.dead_line is None:
            return "No Deadline"
        else:
            return datetime.datetime.fromtimestamp(self.dead_line / 1000).strftime('%d %b %Y')

    @property
    def tagsToList(self) -> List[TagModel]:
        if not self.tags or self.tags == 'None':
            return []
        try:
            data = json.loads(self.tags.replace('\'', '\"'))
            if isinstance(data, dict):
                return [TagModel(**tag_data) for tag_data in data.values()]
            elif isinstance(data, list):
                return [TagModel(**tag_data) for tag_data in data]
        except json.JSONDecodeError:
            print(f"Unable to parse tags: {self.tags}")
            return []


@dataclass
class QuestionModel:
    question: str
    answer: str


@dataclass
class ApplicationModel:
    studentEmail: str
    studentName: str
    studentPhoneNumber: str
    filledDate: int
    answers: str

    @property
    def convert_answer_json_to_question_model(self):
        if not self.answers or self.answers == 'None':
            return []
        try:
            data = json.loads(self.answers)
            if isinstance(data, dict):
                return [QuestionModel(**tag_data) for tag_data in data.values()]
            elif isinstance(data, list):
                return [QuestionModel(**tag_data) for tag_data in data]
        except json.JSONDecodeError:
            print(f"Unable to parse answers: {self.answers}")
            return []
