from flask_server.flaskServer import app
import logging
logging.basicConfig(filename='adb.log', level=logging.INFO)
print("="*25)
print("Launching Flask app")
app.run(host='0.0.0.0', port=5005)