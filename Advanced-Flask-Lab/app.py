from flask import Flask, jsonify, request, render_template, url_for
import random
import requests, json

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

# Variables for tasks
image_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/2560px-MIT_logo.svg.png"
user_bio = "Middle East Entrepreneurs of Tomorrow. Enabling the next generation of Israeli and Palestinian leaders."

posts = {
    "data:image/png;base64,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": "2021 cohort's Y3 Accelerator!",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/MIT_logo.png/1200px-MIT_logo.png": "MEeT graduation!",
    "https://pbs.twimg.com/media/FPvsO6xVkAEcrBm?format=jpg&name=900x900": "#Throwback to one of our favorite #MEETsummer events: #BowlingNight!",
    "https://pbs.twimg.com/media/FI_UkcnVIAAUvWN?format=jpg&name=medium": "2020 cohort in their Y1 summer!!"}

rl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #bonus task!
#####


@app.route('/')  # '/' for the default page
def home():
    return render_template('index.html' , image_link=image_link , user_bio= user_bio , posts=posts , rl=rl)


@app.route('/about')  # '/' for the default page
def about():
    return render_template('about.html')


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)
