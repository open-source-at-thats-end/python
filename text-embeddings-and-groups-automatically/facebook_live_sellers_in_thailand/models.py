from pydantic import BaseModel
from typing import List
class AppendItem(BaseModel):
    term: str
    vec: List[float]
class AppendRequest(BaseModel):
    run_id: str
    items: List[AppendItem]
class FinalizeRequest(BaseModel):
    run_id: str
class FinalizeItem(BaseModel):
    term: str
    cluster_id: int
class FinalizeResponse(BaseModel):
    ok: bool
    chosen_k: int
    silhouette: float
    assignments: List[FinalizeItem]
