import sys
from pathlib import Path

# Add the p3.2_series_api directory to the path
sys.path.insert(0, str(Path(__file__).parent / "p3.2_series_api"))

# Now import the app from main
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
