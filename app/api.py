# This file contains most of logis and features
import platform
from app import app

## devlopment tools: /dev/

# this is the first API endpoint, for test only, it will return a sample obj
@app.route("/dev/env")
def dev_env():
    return {
        "backend":"Flask",
        "os": platform.platform()
    }