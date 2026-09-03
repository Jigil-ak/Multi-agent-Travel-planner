import os
import re
import certifi
import airportsdata
import pycountry
from dotenv import load_dotenv

load_dotenv()

#to avoid the path issues
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


