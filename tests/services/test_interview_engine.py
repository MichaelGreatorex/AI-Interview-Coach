from app.models.interview_response import InterviewResponse
from app.schemas.interview_question import InterviewQuestion
from app.services.interview_engine import InterviewEngine


def test_interview_starts_with_a_question() -> None:
    engine = InterviewEngine()

    first_question = engine.get_first_question()

    assert first_question is not None
    assert first_question.id is not None
    assert first_question.text.strip()


def test_engine_exposes_questions() -> None:
    engine = InterviewEngine()

    questions = engine.questions

    assert questions
    assert all(question.id is not None for question in questions)
    assert all(question.text.strip() for question in questions)


def test_response_produces_next_question() -> None:
    engine = InterviewEngine()

    first_question = engine.get_first_question()

    assert first_question is not None

    response = InterviewResponse(
        interview_session_id=1,
        question_id=first_question.id,
        question_text=first_question.text,
        answer="My answer",
    )

    next_question = engine.get_next_question([response])

    assert next_question is not None
    assert next_question.id != first_question.id
    assert next_question.text.strip()


def test_interview_ends_when_no_next_question_exists() -> None:
    engine = InterviewEngine()

    responses = [
        InterviewResponse(
            interview_session_id=1,
            question_id=question.id,
            question_text=question.text,
            answer=f"Answer to question {question.id}",
        )
        for question in engine.questions
    ]

    next_question = engine.get_next_question(responses)

    assert next_question is None
    
def test_get_first_question_returns_none_when_no_questions_exist() -> None:
    engine = InterviewEngine(questions=())

    assert engine.get_first_question() is None
    
def test_get_next_question_returns_none_when_no_questions_exist() -> None:
    engine = InterviewEngine(questions=())

    assert engine.get_next_question([]) is None