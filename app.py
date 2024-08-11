import dotenv ,os
dotenv.load_dotenv()

from flask_app import app
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=os.getenv("FLASK_RUN_PORT"))
