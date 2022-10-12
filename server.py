from flask import Flask, render_template, request, redirect
import tweepy
import mysql.connector
from flask_mysqldb import MySQL

 
app = Flask(__name__)

# config for the database 
app.config['MYSQL_HOST'] = '......'
app.config['MYSQL_USER'] = '......'
app.config['MYSQL_PASSWORD'] = '......'
app.config['MYSQL_DB'] = 'flask'
mysql = MySQL(app)


@app.route('/') # go to the home page
def home_page():
    return render_template('index.html')


@app.route('/<string:page>') # go to the other pages
def get_page(page=None):
    return render_template(page)

@app.route('/submit_form', methods=['POST']) # submit the message form and save it to the database
def submit():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_data(data) # save to the database
        return redirect('thankyou.html')
    else:
        return 'something went wrong'

@app.route('/result_twitter', methods=['POST']) 
def search():
    if request.method == 'POST':
        data = request.form.to_dict()
        results = search_twitter(data, 50)
        return render_template('results.html', len = len(results[0]), results=results[0])
    else:
        return 'something went wrong'   

@app.route('/get_from_database', methods=['POST']) # a showcase how to get data and connect the tables
def get_data():
    if request.method == 'POST':
        app.config['MYSQL_DB'] = 'messages'

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT u.name AS receiver, u2.name AS sender_name, m.subject, m.body FROM users u INNER JOIN messages m ON u.id = m.user_id_to INNER JOIN users u2 ON m.user_id_from = u2.id")
        results = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return render_template('results.html', len = len(results), results=results)
    else:
        return 'something went wrong'               
    

def write_data(data): # save the message form to the database
    email = data['email']
    subject = data['subject']
    message = data['message']
    # save the message into the database
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO message(email, subject, message) VALUES (%s,%s,%s)''', (email, subject, message))
    mysql.connection.commit()
    cursor.close()

def search_twitter(data, max_results): # serach the keyword on twitter
    # connect to twitter API
    client = tweepy.Client(bearer_token='......', consumer_key='......', consumer_secret='......',access_token='......', access_token_secret='......')
    
    # search
    keyword = data['word']
    tweets = client.search_recent_tweets(query=keyword, max_results=max_results)
    return tweets 