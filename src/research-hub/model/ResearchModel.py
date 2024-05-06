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
    title: str
    description: str
    created_by: str
    created_by_UID: str
    created: int = int(time.time() * 1000)  # Convert to milliseconds
    dead_line: int = None
    tags: str = ""

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
        tags_list = json.loads(self.tags)
        return [TagModel(**tag) for tag in tags_list]

# def test():
#     dummy_json = '''
#     [{"created_by": "user1", "name": "tag1", "created": 1715018917632}, {"created_by": "user2", "name": "tag2", "created": 1715018917632}]'''
#
#     model = ResearchModel(title="Title", description="Description", created_by="User", created_by_UID="UID",
#                           tags=dummy_json)
#     print(model.formattedTime)
#     print(model.formattedDeadline)
#     print(model.tagsToList)
#
