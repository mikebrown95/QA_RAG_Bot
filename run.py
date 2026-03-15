import subprocess
import time

print("Starting FastAPI backend...")
subprocess.Popen(["uvicorn", "app.main:app", "--reload"])

time.sleep(2)

print("Starting Streamlit frontend...")
subprocess.call(["streamlit", "run", "streamlit_app.py"])
