````markdown
# K-Means Clustering Service (Text Embeddings)  

A lightweight Python API service built with FastAPI that accepts text embedding vectors, clusters them using K-Means (with cosine similarity), automatically selects the optimal number of clusters (k) via the silhouette score, enforces minimum cluster size, and returns results in a simple JSON format.  

## 🚀 Why this service  
When you have lots of text embeddings (for example: sentences, product descriptions, support tickets, live commerce items), you want a quick way to group them into meaningful clusters **without** manually labeling everything. This service:  
- Accepts batches of embeddings + terms.  
- Runs clustering behind-the-scenes.  
- Returns each term with a `cluster_id`, plus clustering metadata (`chosen_k`, `silhouette_score`).  
- Can be deployed easily on a VPS or containerized.  

## 🧩 Features  
- REST API with endpoints: `/start`, `/append`, `/finalize`, `/healthz`.  
- Cosine-style K-Means (via vector normalization + Euclidean KMeans).  
- Auto-k determination by sweeping k in a configurable range and picking via silhouette.  
- Minimum cluster size enforcement (merges tiny clusters).  
- Optional maximum cluster size splitting.  
- Configurable via environment variables.  
- Lightweight, in-memory buffer for runs (no external DB required for baseline).  
- Example curl/test commands included.  

## 📦 Tech stack  
- Python 3.10+  
- FastAPI  
- Uvicorn (ASGI server)  
- NumPy  
- scikit-learn  
- Pydantic (schema + settings)  
- (Optional) Docker for container deployment  

## 🛠 Setup & Run  

### 1. Clone & install  
```bash
git clone <your-repo-url>
cd <repo-folder>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Configure

Copy `.env.example` to `.env` and adjust variables as needed:

```
K_MIN=2
K_MAX=10
MIN_SIZE=5
MAX_SIZE=1000  # optional, leave blank to disable
RANDOM_STATE=42
```

### 3. Run locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test with curl

```bash
curl -X POST http://localhost:8000/start \
     -H "Content-Type: application/json" \
     -d '{"run_id":"run1"}'

curl -X POST http://localhost:8000/append \
     -H "Content-Type: application/json" \
     -d '{"run_id":"run1","items":[{"term":"item1","vec":[0.12,0.34, …]},{"term":"item2","vec":[…]}]}'

curl -X POST http://localhost:8000/finalize \
     -H "Content-Type: application/json" \
     -d '{"run_id":"run1"}'

curl http://localhost:8000/healthz
```

## 📋 Endpoints

| Endpoint    | Method | Description                                     |
| ----------- | ------ | ----------------------------------------------- |
| `/start`    | POST   | Create or clear buffer for a `run_id`.          |
| `/append`   | POST   | Append terms + embedding vectors to the buffer. |
| `/finalize` | POST   | Run clustering; return assignments + metadata.  |
| `/healthz`  | GET    | Simple health check; returns status OK.         |

### Example response for `/finalize`:

```json
{
  "ok": true,
  "chosen_k": 7,
  "silhouette": 0.43,
  "assignments": [
    { "term": "item1", "cluster_id": 0 },
    { "term": "item2", "cluster_id": 3 },
    …
  ]
}
```

## ✅ What you’ll deliver

* Source code (`app/`, `models.py`, `clustering.py`, `settings.py`, etc)
* `requirements.txt`
* `.env.example`
* `README.md` (this file)
* (Optional) `Dockerfile` for containerised deployment
* Tested on ~1,500 items × ~1,536-dim vectors in “seconds” scale on a typical dev machine

## ⚠️ Limitations & Next Steps

* Currently uses in-memory storage; for large scale or persistence you may need external DB or caching.
* Vector dimension must be uniform across all items in a run.
* Performance tuned for ~1k–5k items; for much larger loads you may need batch clustering or distributed approaches.
* Optional features like splitting very large clusters exist but may require tuning.

## 🧠 Notes for Client

* Please supply the **embedding vectors** (numeric arrays) along with their corresponding terms; this service does *not* compute embeddings itself.
* Ensure vectors are all same length (e.g., 1536 dims) for correct clustering.
* Use minimal overhead to deploy on your VPS: simply run `uvicorn` or build the Docker image and map port 8000 to your host.
* Monitor clustering results: check that the `cluster_id`s make sense for your data, silhouette score is acceptable, and no cluster is below configured `MIN_SIZE`.
* For future scaling: consider persisting runs, monitoring performance, handling concurrency, and possibly using GPU or distributed clustering.

---

## 📄 License

This code is provided “as is” for your internal use. No warranties are implied. Use at your own risk.

---

*End of README*
