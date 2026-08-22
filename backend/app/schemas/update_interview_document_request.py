from pydantic import BaseModel


class UpdateInterviewDocumentRequest(BaseModel):
    extracted_text: str