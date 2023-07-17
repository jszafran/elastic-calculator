import dataclasses
import pathlib
from enum import Enum

import yaml

from elastic_calculator.errors import (
    ColumnMinValueMustBeSmallerThanMaxValueError,
    ColumnMissingCodeValueError,
    ColumnMissingTextValueError,
)


class ColumnType(Enum):
    QUESTION = 0
    DEMOGRAPHICS = 1


@dataclasses.dataclass
class Column:
    """
    Representation of survey's question or demographics.
    """

    type: ColumnType
    code: str
    text: str
    min_value: int
    max_value: int
    nullable: bool = True

    def __post_init__(self) -> None:
        if not self.code:
            raise ColumnMissingCodeValueError()

        if not self.text:
            raise ColumnMissingTextValueError()

        if self.min_value >= self.max_value:
            raise ColumnMinValueMustBeSmallerThanMaxValueError()


@dataclasses.dataclass(frozen=True)
class Schema:
    org_node_column_name: str
    columns: tuple[Column]

    def _columns_of_type(self, of_type: ColumnType) -> tuple[Column]:
        return tuple([c for c in self.columns if c.type == of_type])

    @property
    def questions(self) -> tuple[Column]:
        return self._columns_of_type(ColumnType.QUESTION)

    @property
    def demographics(self) -> tuple[Column]:
        return self._columns_of_type(ColumnType.DEMOGRAPHICS)

    @classmethod
    def from_yaml(cls, path: str | pathlib.Path) -> "Schema":
        with open(path) as f:
            schema = yaml.safe_load(f)

        org_node_column = schema.get("org_node_column")
        questions = schema.get("questions")
        demographics = schema.get("demographics")

        parsed_questions = [
            Column(type=ColumnType.QUESTION, **question) for question in questions
        ]

        parsed_demographics = [
            Column(type=ColumnType.DEMOGRAPHICS, **demographic)
            for demographic in demographics
        ]

        return cls(
            org_node_column_name=org_node_column,
            columns=tuple(parsed_questions + parsed_demographics),
        )
