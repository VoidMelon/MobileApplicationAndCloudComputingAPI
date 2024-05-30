from flask import Flask, request, make_response, render_template
from flask_restful import Api
from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)

# dialect+driver://username:password@host:port/database

# conn = sqlite3.connect('mobile.db')
# print(conn)

@app.route('/')
def index():
    print("Hello World!")
    return "Hello World!"


# @app.route("/")
# def index():
#     resp = make_response(render_template(...))
#     resp.set_cookie("username", 'mark')
#     return resp
#     #username = request.cookies.get("username")


#@app.route('/')
#def hello_world():  # put application's code here
#    return 'Hello World!'


# Initialize Firestore DB
#cred = credentials.Cert

# @app.route("/<name>")
# def hello(name):
#     return f"Hello, {escape(name)}!"
#
#
# @app.route("/user/<username>")
# def show_user_profile(username):
#     return f"Hello, {escape(username)}!"
#
#
# @app.route("/post/<int:post_id")
# def show_post(post_id):
#     return f"Post {post_id}!"




if __name__ == '__main__':
    app.run()
#    app.run(host='0.0.0.0', port=5002, debug=True)
