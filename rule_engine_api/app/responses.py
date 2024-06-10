from pydantic import BaseModel


class StandardResponse(BaseModel):
    """
    Standardized response model.
    """

    status: str
    status_code: int
    message: str
