import dataclasses
from functools import total_ordering

from elastic_calculator.errors import IncorrectOrgNodeValueError


@dataclasses.dataclass
@total_ordering
class OrgNode:
    """
    Object representing single node (or unit) in an organization structure.
    Depending on the structure of company, you could think of it as a business unit
    (Marketing, Finance) or some kind of person (manager).
    """

    levels: tuple[int, ...]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.node})"

    def __len__(self) -> int:
        return len(self.levels)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrgNode):
            return NotImplemented
        return self.levels == other.levels

    def __lt__(self, other: "OrgNode") -> bool:
        if self == other:
            return False

        non_zero_diffs = [
            v1 - v2 for v1, v2 in zip(self.levels, other.levels) if v1 - v2 != 0
        ]

        if not non_zero_diffs:
            return len(self) < len(other)

        return non_zero_diffs[0] < 0

    @property
    def node(self) -> str:
        return f"N{'.'.join(f'0{i}' if i < 10 else str(i) for i in self.levels)}"

    @classmethod
    def from_str(cls, v: str) -> "OrgNode":
        """
        Constructs OrgNode object from string. Expects a format of
        N<int>.<int>. ... where number of <int> is equal to depth of
        organizational tree.
        """
        if not v:
            raise IncorrectOrgNodeValueError(
                "Cannot construct org node from empty string."
            )

        v = "".join(v[:-1]) if v[-1] == "." else v
        try:
            levels = tuple([int(x) for x in v[1:].split(".")])
        except ValueError:
            raise IncorrectOrgNodeValueError(
                f"Cannot construct org node from value {v}."
            )
        return cls(levels=levels)

    def to_str(self) -> str:
        pass
