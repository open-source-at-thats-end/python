from fastapi import FastAPI, HTTPException
from .models import AppendRequest, FinalizeRequest, FinalizeResponse
from .clustering import start_run, append_run, finalize_run

app = FastAPI()

@app.post("/start")
def start(run_id: str):
    start_run(run_id)
    return {"ok": True}

@app.post("/append")
def append(req: AppendRequest):
    try:
        count = append_run(req.run_id, req.items)
        return {"ok": True, "count": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/finalize", response_model=FinalizeResponse)
def finalize(req: FinalizeRequest):
    try:
        chosen_k, silhouette, assignments = finalize_run(req.run_id)
        return FinalizeResponse(ok=True, chosen_k=chosen_k, silhouette=silhouette, assignments=assignments)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
