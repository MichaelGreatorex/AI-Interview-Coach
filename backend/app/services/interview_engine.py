from app.schemas.interview_question import InterviewQuestion
from app.models.interview_response import InterviewResponse
from app.data.interview_questions import QUESTIONS

class InterviewEngine:
    _interview_engine: "InterviewEngine"

    def __init__(
        self,
        questions: tuple[InterviewQuestion, ...] | None = None,
    ) -> None:
        self._questions = questions if questions is not None else QUESTIONS

    @property
    def questions(self) -> tuple[InterviewQuestion, ...]:
        return tuple(self._questions)
    
    def get_first_question(self) -> InterviewQuestion | None:
        if not self._questions:
            return None
        return self._questions[0]
    
    def get_next_question(self, responses: list[InterviewResponse]) -> InterviewQuestion | None:
        next_index = len(responses)
        if next_index >= len(self._questions):
            return None

        return self._questions[next_index]