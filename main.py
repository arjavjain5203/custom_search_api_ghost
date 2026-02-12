from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from automation import SearchAutomation

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    html_content: str

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    automation = SearchAutomation()
    try:
        await automation.launch_browser()
        html_content = await automation.perform_search(request.query)
        return SearchResponse(html_content=html_content)
    except Exception as e:
        print(f"Internal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await automation.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
