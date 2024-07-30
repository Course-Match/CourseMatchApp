import dotenv ,os
dotenv.load_dotenv()

from flask_app import app

app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"))

