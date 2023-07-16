import dataclasses
from functools import total_ordering

from elastic_calculator.errors import IncorrectOrgNodeValueError


@dataclasses.dataclass
@total_ordering
class OrgNode:
    levels: tuple[int, ...]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.node})"

    def __len__(self) -> int:
        return len(self.levels)

    def __eq__(self, other: "OrgNode") -> bool:
        return self.levels == other.levels

    def __lt__(self, other: "OrgNode") -> bool:
        if self == other:
            return False

        non_zero_diffs = [
            v1 - v2 for v1, v2 in zip(self.levels, other.levels) if v1 - v2 != 0
        ]

        if not non_zero_diffs:
            return True if len(self) < len(other) else False

        return True if non_zero_diffs[0] < 0 else False

    @property
    def node(self) -> str:
        return f"N{'.'.join(str(i) for i in self.levels)}"

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
