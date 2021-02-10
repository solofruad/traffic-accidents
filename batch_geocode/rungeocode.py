import socket
from batch_geocode.app import app

if __name__ == "__main__":
    #print( f"*** Now running application on http://{HOST}.cluster.ihme.washington.edu:{PORT} ***" )
    app.run(host="0.0.0.0")
    