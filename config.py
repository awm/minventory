import os
import multiprocessing

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'minventory.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = multiprocessing.cpu_count() * 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = """U'zWT|8i=@+q<ji>E#[zfG6;=XNEnf}KIef;kft+k^o0$+zV*COIm~FCEZwJV;%S"""

# Secret key for signing cookies
SECRET_KEY = """N3t1]ujq)RgHqvf'Je9MhW7}^M^RR*([X}1G`VUBc2S}_#vfC_N/LZe'z)?!rnUe"""
