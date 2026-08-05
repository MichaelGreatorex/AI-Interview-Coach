from app.services.models.interview_question import InterviewQuestion


class InterviewGenerationService:
    QUESTIONS = [
        InterviewQuestion(
            id=1,
            text="Tell me about yourself.",
        ),
        InterviewQuestion(
            id=2,
            text="Why are you interested in this role?",
        ),
        InterviewQuestion(
            id=3,
            text="Describe a challenging project.",
        ),
    ]
    
    def get_first_question(self) -> InterviewQuestion:
        return self.QUESTIONS[0]