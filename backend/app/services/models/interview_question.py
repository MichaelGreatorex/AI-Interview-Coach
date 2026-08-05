from dataclasses import dataclass


@dataclass(frozen=True)
class InterviewQuestion:
    id: int
    text: str