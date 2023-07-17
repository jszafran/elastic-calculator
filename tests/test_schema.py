from typing import Any

import pytest

from elastic_calculator.errors import (
    ColumnMinValueMustBeSmallerThanMaxValueError,
    ColumnMissingCodeValueError,
    ColumnMissingTextValueError,
)
from elastic_calculator.schema import Column, ColumnType, Schema


@pytest.fixture
def column_test_data() -> dict[str, Any]:
    return {
        "code": "c1",
        "text": "c1 text",
        "min_value": 1,
        "max_value": 5,
        "nullable": True,
    }


def test_creating_question_with_ok_data(column_test_data):
    question = Column(
        type=ColumnType.QUESTION,
        **column_test_data,
    )

    assert question.type == ColumnType.QUESTION
    assert question.code == column_test_data.get("code")
    assert question.text == column_test_data.get("text")
    assert question.min_value == column_test_data.get("min_value")
    assert question.max_value == column_test_data.get("max_value")
    assert question.nullable is column_test_data.get("nullable")


def test_creating_demographics_with_ok_data(column_test_data):
    question = Column(
        type=ColumnType.DEMOGRAPHICS,
        **column_test_data,
    )

    assert question.type == ColumnType.DEMOGRAPHICS
    assert question.code == column_test_data.get("code")
    assert question.text == column_test_data.get("text")
    assert question.min_value == column_test_data.get("min_value")
    assert question.max_value == column_test_data.get("max_value")
    assert question.nullable is column_test_data.get("nullable")


@pytest.mark.parametrize(
    "params,exception",
    [
        ({"code": ""}, ColumnMissingCodeValueError),
        ({"text": ""}, ColumnMissingTextValueError),
        (
            {"min_value": 2, "max_value": 2},
            ColumnMinValueMustBeSmallerThanMaxValueError,
        ),
        (
            {"min_value": 2, "max_value": 1},
            ColumnMinValueMustBeSmallerThanMaxValueError,
        ),
    ],
)
def test_column_raises_error_when_created_with_bad_data(
    params, exception, column_test_data
):
    with pytest.raises(exception):
        data = column_test_data | params
        Column(
            type=ColumnType.QUESTION,
            **data,
        )


def test_creating_schema():
    q1 = Column(
        type=ColumnType.QUESTION,
        code="q1",
        text="q1 text",
        min_value=1,
        max_value=2,
        nullable=True,
    )
    q2 = Column(
        type=ColumnType.QUESTION,
        code="q1",
        text="q1 text",
        min_value=1,
        max_value=3,
        nullable=True,
    )

    d1 = Column(
        type=ColumnType.DEMOGRAPHICS,
        code="d1",
        text="d1 text",
        min_value=1,
        max_value=2,
        nullable=False,
    )

    schema = Schema(
        org_node_column_name="org_node",
        columns=tuple([q1, q2, d1]),
    )

    assert schema.questions == (q1, q2)
    assert schema.demographics == (d1,)
