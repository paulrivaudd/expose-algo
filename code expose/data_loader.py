"""Lecture du dataset Adult (UCI Census)."""

from __future__ import annotations

import csv
from dataclasses import dataclass


@dataclass
class Person:
    id: int
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str
    income: str

    def __repr__(self) -> str:
        return (f"Person(id={self.id}, age={self.age}, "
                f"occupation={self.occupation!r}, income={self.income!r})")


def _to_int(value: str) -> int:
    value = value.strip()
    if value in ("", "?"):
        return 0
    return int(value)


def load_csv(path: str) -> list[Person]:
    people: list[Person] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            people.append(Person(
                id=i,
                age=_to_int(row["age"]),
                workclass=row["workclass"].strip(),
                fnlwgt=_to_int(row["fnlwgt"]),
                education=row["education"].strip(),
                education_num=_to_int(row["education_num"]),
                marital_status=row["marital_status"].strip(),
                occupation=row["occupation"].strip(),
                relationship=row["relationship"].strip(),
                race=row["race"].strip(),
                sex=row["sex"].strip(),
                capital_gain=_to_int(row["capital_gain"]),
                capital_loss=_to_int(row["capital_loss"]),
                hours_per_week=_to_int(row["hours_per_week"]),
                native_country=row["native_country"].strip(),
                income=row["class"].strip(),
            ))
    return people
