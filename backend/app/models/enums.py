from enum import Enum

class DocumentType(str, Enum):
    CV = "cv"
    JOB_DESCRIPTION = "job_description"