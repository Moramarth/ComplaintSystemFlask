from flask import Flask

from db import db

app = Flask(__name__)
db.init_app(app)


@app.after_request
def close_request(response):
    db.session.commit()
    return response


if __name__ == '__main__':
    app.run()
