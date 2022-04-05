from distutils.log import debug
from imp import reload
import uvicorn
from src.configs import app
import uvicorn
from src.routes import *

if __name__ == '__main__':
    uvicorn.run(
        "server:app",
        host="0.0.0.0", 
        port=8080,
        debug = True
    )
