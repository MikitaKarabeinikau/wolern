from pydantic import BaseModel, Field
from typing import List, Optional

class WebhookPayload(BaseModel):
    data: dict
    object: str
    type: str


class UserCreateRequest(BaseModel):
    clerk_user_id: str
    username: str = None
    email: str

class AddWordRequest(BaseModel):
    word: str
    

class Translation(BaseModel):
    id: int
    word_id: int
    language: Optional[str] = None
    

    translated_word: str = Field(alias='translation')

    class Config:
        from_attributes = True
        populate_by_name = True 


class TranslationResponse(BaseModel):
    translations: List[Translation]


class Synonym(BaseModel):
    id: int
    word_id: int
    synonym: str

    class Config:
        from_attributes = True

class SynonymResponse(BaseModel):
    synonyms: List[Synonym]

class Definition(BaseModel):
    id: int
    word_id: int
    part_of_speech: Optional[str] = None
    definition: str

    class Config:
        from_attributes = True

class DefinitionResponse(BaseModel):
    definitions: List[Definition]

class Example(BaseModel):
    id: int
    word_id: int
    part_of_speech: Optional[str] = None
    example_sentence: str = Field(alias='example_sentence')

    class Config:
        from_attributes = True
        populate_by_name = True

class ExampleResponse(BaseModel):
    examples: List[Example]

class Tag(BaseModel):
    id: int
    word_id: int
    tag: str

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    tags: List[Tag]

class Warning(BaseModel):
    id: int
    word_id: int
    warning_message: str = Field(alias='warning')

    class Config:
        from_attributes = True 
        populate_by_name = True
         
class WarningResponse(BaseModel):
    warnings: List[Warning]