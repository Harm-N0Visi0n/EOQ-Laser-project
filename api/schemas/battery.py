from typing import Annotated

from pydantic import BaseModel, Field


class Battery(BaseModel):
    level: Annotated[float, Field(strict=True, ge=0, le=5)]
