import dataclasses
import pathlib
from typing import Protocol

import pandas as pd


class InputReader(Protocol):
    def read(self) -> pd.DataFrame:
        ...


@dataclasses.dataclass(frozen=True)
class FeatherReader:
    path: str | pathlib.Path

    def read(self) -> pd.DataFrame:
        return pd.read_feather(self.path)


@dataclasses.dataclass
class FromMemoryReader:
    df: pd.DataFrame

    def read(self) -> pd.DataFrame:
        return self.df
