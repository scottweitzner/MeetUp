# file invoked to startup development server - gets copy of app from package and runs it

from meetup import app
import os

app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=port)
