class CalculatorError(Exception):
    pass


class IncorrectOrgNodeValueError(CalculatorError):
    pass


class ColumnMissingCodeValueError(CalculatorError):
    pass


class ColumnMissingTextValueError(CalculatorError):
    pass


class ColumnMinValueMustBeSmallerThanMaxValueError(CalculatorError):
    pass
