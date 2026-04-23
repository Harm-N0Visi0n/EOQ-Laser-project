from typing import Annotated

from pydantic import BaseModel, Field


class Volume(BaseModel):
    level: Annotated[int, Field(strict=True, ge=0, le=30)]
