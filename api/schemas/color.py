from typing import Annotated

from pydantic import BaseModel, Field


class Color(BaseModel):
    
    red: Annotated[int, Field(ge=0, le=255)]
    green: Annotated[int, Field(ge=0, le=255)]
    blue: Annotated[int, Field(ge=0, le=255)]
    white: Annotated[int | None, Field(ge=0, le=255)]
    twinkle: bool | None

    def to_colat_format(self):
        value = f"{self.red},{self.green},{self.blue}"
        value += f",{self.white}" if self.white else ",0"
        value += f",{self.twinkle}" if self.twinkle else ""
        return value
