from flask import Flask, jsonify, request, render_template, url_for
import random
import requests, json

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

# Variables for tasks
image_link = "data:image/jpeg;base64,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"

user_bio = "Middle East Entrepreneurs of Tomorrow. Enabling the next generation of Israeli and Palestinian leaders."

posts = {
    "https://imageio.forbes.com/blogs-images/samarmarwan/files/2018/03/MEET-Students-1200x800.jpg": "Group projects <3",
    "https://uploads-ssl.webflow.com/5dd64bd3a930f96c82bd137a/63024ce64d943673cb004a4c_2022.07.17%20-%20Summer%20Day%201.png": "MEET summer!",
    "https://uploads-ssl.webflow.com/5dd64bd3a930f9d04abd1363/5de6d502d6d70c0ad49a060c_6.jpg": "#MEET_DU",
    "https://global-uploads.webflow.com/5fe28feebcae602620061802/5fe5401840671a36cd1d47d5_5de6d5024dd1a74670173aed_1-p-1080.jpeg": "Our lovely TAs!"}


#####


@app.route('/')  # '/' for the default page
def home():
    return render_template('index.html', user_bio= user_bio, image_link=image_link, posts = posts)


@app.route('/about')  # '/' for the default page
def about():
    return render_template('about.html')


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)
