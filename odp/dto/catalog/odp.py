# generated by datamodel-codegen:
#   filename:  dataset.schema.json
#   timestamp: 2023-07-19T19:28:43+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra


class Attribute(BaseModel):
    class Config:
        extra = Extra.allow

    name: Optional[str] = None
    description: Optional[str] = None
    traits: Optional[List[str]] = None


class Citation(BaseModel):
    class Config:
        extra = Extra.allow

    cite_as: Optional[str] = None
    doi: Optional[str] = None


class ContactInfo(BaseModel):
    class Config:
        extra = Extra.allow

    contact: Optional[str] = None
    organization: Optional[str] = None
