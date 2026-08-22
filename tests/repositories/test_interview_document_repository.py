from sqlalchemy.orm import Session

from app.models.enums import DocumentType
from app.models.interview_document import InterviewDocument
from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_document_repository import InterviewDocumentRepository
from app.repositories.interview_session_repository import InterviewSessionRepository


def create_session(db_session: Session, public_id: str) -> InterviewSession:
	return InterviewSessionRepository(db_session).create(
		InterviewSession(
			interview_session_id=public_id,
			status=InterviewStatus.CREATED,
		)
	)


def test_get_by_interview_session_id_returns_saved_documents(
	db_session: Session,
) -> None:
	session = create_session(db_session, "session-docs")
	repository = InterviewDocumentRepository(db_session)

	first_document = repository.create(
		InterviewDocument(
			interview_session_id=session.id,
			document_type=DocumentType.CV,
			original_filename="cv.pdf",
			stored_filename="stored-cv.pdf",
			mime_type="application/pdf",
			file_size=10,
			storage_path="/tmp/stored-cv.pdf",
		)
	)
	second_document = repository.create(
		InterviewDocument(
			interview_session_id=session.id,
			document_type=DocumentType.JOB_DESCRIPTION,
			original_filename="job.pdf",
			stored_filename="stored-job.pdf",
			mime_type="application/pdf",
			file_size=20,
			storage_path="/tmp/stored-job.pdf",
		)
	)

	documents = repository.get_by_interview_session_id(session.id)

	assert [document.id for document in documents] == [first_document.id, second_document.id]
	assert [document.document_type for document in documents] == [
		DocumentType.CV,
		DocumentType.JOB_DESCRIPTION,
	]


def test_delete_removes_document(db_session: Session) -> None:
	session = create_session(db_session, "session-delete-doc")
	repository = InterviewDocumentRepository(db_session)
	document = repository.create(
		InterviewDocument(
			interview_session_id=session.id,
			document_type=DocumentType.CV,
			original_filename="cv.pdf",
			stored_filename="stored-cv.pdf",
			mime_type="application/pdf",
			file_size=10,
			storage_path="/tmp/stored-cv.pdf",
		)
	)

	repository.delete(document)
	db_session.commit()

	assert repository.get_by_interview_session_id(session.id) == []


def test_get_by_id_returns_saved_document(db_session: Session) -> None:
	session = create_session(db_session, "session-get-by-id")
	repository = InterviewDocumentRepository(db_session)
	document = repository.create(
		InterviewDocument(
			interview_session_id=session.id,
			document_type=DocumentType.CV,
			original_filename="cv.pdf",
			stored_filename="stored-cv.pdf",
			mime_type="application/pdf",
			file_size=10,
			storage_path="/tmp/stored-cv.pdf",
			extracted_text="Original text",
		)
	)

	result = repository.get_by_id(document.id)

	assert result is not None
	assert result.id == document.id
	assert result.extracted_text == "Original text"


def test_update_persists_changed_extracted_text(db_session: Session) -> None:
	session = create_session(db_session, "session-update-doc")
	repository = InterviewDocumentRepository(db_session)
	document = repository.create(
		InterviewDocument(
			interview_session_id=session.id,
			document_type=DocumentType.CV,
			original_filename="cv.pdf",
			stored_filename="stored-cv.pdf",
			mime_type="application/pdf",
			file_size=10,
			storage_path="/tmp/stored-cv.pdf",
			extracted_text="Original text",
		)
	)

	document.extracted_text = "Updated extracted text"
	repository.update(document)

	db_session.expire_all()
	updated = repository.get_by_id(document.id)

	assert updated is not None
	assert updated.extracted_text == "Updated extracted text"
