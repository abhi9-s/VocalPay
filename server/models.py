from pydantic import BaseModel

class LanguageRequest(BaseModel):
    language: str


class TranslateTextRequest(BaseModel):
    text: dict


class TranslateSpeechRequest(BaseModel):
    speak: dict