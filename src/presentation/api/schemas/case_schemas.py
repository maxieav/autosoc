from pydantic import BaseModel


class AssignCaseRequest(BaseModel):
    assigned_to: str
