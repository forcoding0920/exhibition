from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.umxignu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.pirates_lv1

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/exhibit', methods=["POST"])
def post_exhibit():
    url_receive = request.form["url_give"]


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser') 

    title = soup.select_one('#container > div.wide-inner > section > h3').text
    period = soup.select_one('#container > div.detial-cont-element.active > div > dl:nth-child(1) > dd').text.strip() #앞에 공백 없애기
    tags = soup.select_one('#container > section.tag-element.poi > p').text.replace('\n'," ") #'/n'줄바꿈을 ' '띄어쓰기로 바꾸기

    image = soup.select('.item')[1]['style'].replace("background-image:url('", '').replace("');", '')
    image = 'https://korean.visitseoul.net'+image

    doc ={
        'url':url_receive,
        'title':title,
        'period':period,
        'tags':tags,
        'image':image
    }

    db.exhibition.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})

if __name__ == "__main__":
	app.run(debug=True, port=8080)