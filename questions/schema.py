from typing import Optional

from ninja import Schema


class QuestionSchema(Schema):
    is_haftom: bool = False
    is_hashtom: bool = False
    is_nohom: bool = False

    is_nobat1: bool = False
    is_nobat2: bool = False

    is_mostamar: bool = False
    is_payani: bool = False

    is_rahat: bool = False
    is_motavasset: bool = False
    is_sakht: bool = False


class BookSchema(Schema):
    is_haftom: bool = False
    is_hashtom: bool = False
    is_nohom: bool = False

    is_amoozeshi: bool = False
    is_emtahani: bool = False
    is_gambegam: bool = False


class SearchSchema(Schema):
    query: Optional[str] = None


class QuestionResponseSchema(Schema):
    title: str
    description: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] = None
    is_solved: bool
    difficulty: Optional[str] = None
    likes_count: int
    tags: Optional[str] = None
    writer: Optional[str] = None


class BookResponseSchema(Schema):
    title: str
    description: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] = None
    publisher: Optional[str] = None
    likes_count: int
    tags: Optional[str] = None
    writer: Optional[str] = None