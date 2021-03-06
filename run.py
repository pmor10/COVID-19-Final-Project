from CovidTracker.app       import app
from CovidTracker.config    import (DEBUG, PORT)
from CovidTracker.connect   import connect_to_db

if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=PORT, debug=DEBUG)