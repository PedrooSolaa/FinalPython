import sys
import os
from pathlib import Path

# Add the p3.2_series_api directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "p3.2_series_api"))

# Change working directory to p3.2_series_api
os.chdir(Path(__file__).parent / "p3.2_series_api")

# Now import the app from main
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
