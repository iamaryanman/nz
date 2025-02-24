from fastapi import FastAPI, Query
from mega import Mega
import logging

app = FastAPI()

# Initialize MEGA instance
mega = Mega()

@app.get("/fetch")
async def fetch_mega_link(link: str = Query(..., title="MEGA File Link", description="Public MEGA file link")):
    """
    Fetches MEGA file details and returns JSON with file info.
    """
    try:
        m = mega.login()  # No login needed for public links
        file_info = m.get_public_url_info(link)

        if not file_info:
            return {"error": "Invalid MEGA link or file not accessible."}

        file_name = file_info.get('name', 'Unknown File')
        file_size = file_info.get('size', 0)
        direct_link = link  # MEGA does not provide actual direct URLs

        # Placeholder thumbnail (since MEGA doesn't provide thumbnails)
        thumbnail_url = "https://upload.wikimedia.org/wikipedia/commons/7/79/Mega_logo.png"

        return {
            "direct_link": direct_link,
            "file_name": file_name,
            "link": link,
            "sizebytes": file_size,
            "thumb": thumbnail_url
        }

    except Exception as e:
        logging.error(f"Error fetching MEGA link: {e}")
        return {"error": str(e)}

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
