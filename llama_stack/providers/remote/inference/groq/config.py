
from llama_models.schema_utils import json_schema_type
from pydantic import BaseModel

@json_schema_type
class GroqConfig(BaseModel):
    pass
