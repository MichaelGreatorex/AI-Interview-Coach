from app.services.models.interview_question import InterviewQuestion
from app.models.interview_response import InterviewResponse
from app.data.interview_questions import QUESTIONS

class InterviewEngine:
    def __init__(self) -> None:
        self._questions = QUESTIONS

    
    def get_first_question(self) -> InterviewQuestion | None:
        if not self._questions:
            return None
        return self._questions[0]
    
    def get_next_question(self, responses: list[InterviewResponse]) -> InterviewQuestion | None:
        next_index = len(responses)

        if next_index >= len(self._questions):
            return None

        return self._questions[next_index]