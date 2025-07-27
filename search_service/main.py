from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from duckduckgo_search import DDGS

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

@app.post("/search/", response_model=list[SearchResult])
def search(request: SearchRequest):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(request.query, region='wt-wt', safesearch='moderate', max_results=5):
                results.append(SearchResult(
                    title=r.get("title", ""),
                    link=r.get("href", ""),
                    snippet=r.get("body", "")
                ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
