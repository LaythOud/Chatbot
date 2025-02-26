import logging
import sys
import os
from index import application

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(__file__))

 
if __name__ == "__main__":
    application.run(debug=True)