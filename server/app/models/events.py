from pydantic import BaseModel


class EventRequest(BaseModel):

    type: str

    message: str