RUNS = {}  # maps run_id → { "terms": [...], "vecs": [...] }
def start_run(run_id: str):
    RUNS[run_id] = {"terms": [], "vecs": []}
def append_run(run_id: str, items):
    # validate run_id exists etc
    for item in items:
        RUNS[run_id]["terms"].append(item.term)
        RUNS[run_id]["vecs"].append(item.vec)
def finalize_run(run_id: str):
    # retrieve terms & vecs, convert to numpy, do clustering, return assignments etc
