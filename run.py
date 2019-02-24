"""
Pet Service Runner

Start the Pet Service and initializes logging
"""

import os
from app import app, routes

# Pull options from environment
HOST = os.getenv('HOST', '0.0.0.0')
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "****************************************"
    print " P E T   S E R V I C E   R U N N I N G"
    print "****************************************"
    routes.initialize_logging()
    app.run(host=HOST, port=int(PORT), debug=DEBUG)
