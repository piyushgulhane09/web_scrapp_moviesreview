from flask import Flask, render_template, jsonify,request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log",level=logging.INFO,format = '%(asctime)s %(name)s %(levelname)s  %(message)s')


app = Flask(__name__)


@app.route("/",methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review",methods = ['POST'])
@cross_origin()
def review():
    if (request.method == 'POST'):
        try :
            movie_name = request.form['search_input'].replace(" ","+")
            url_raw = "https://icheckmovies.com/movies/" + movie_name
            
            logging.info("Raw url"+url_raw)

            url_opened = uReq(url_raw)

            url_readable = url_opened.read()
            url_opened.close()
            url_html = bs(url_readable,"html.parser")


            container = url_html.findAll('div',{'class':'span-7 last'})
            len(container[0].dl)
            len(container[0].findAll('dd'))
            container_data = container[0].findAll('dd')
            l1 = []
            for i in container_data:
                l1.append(i.text.replace("\n","").replace("\r","").replace(" ",""))

            logging.info("list of reviews {l}".format(l =l1))

            # Comment box
                # Author name
            comment_box = url_html.findAll('div',{'class':'listItemContent'})
            author_list = []

            for i in comment_box[0:3]:
                author_list.append(i.a.text)
            
            logging.info("list of authors{author_l}".format(author_l = author_list))
                

            #Author comments
            comment_box = url_html.findAll('div',{'class':'listItemContent'})
            comment_box[0].span.text.replace("\n","").replace("\r","").replace("\t","")
            comments = []
            for i in comment_box[0:3]:
                comments.append(i.span.text.replace("","").replace("\r","").replace("\t",""))
                
            logging.info("List of comments{comments_l}".format(comments_l = comments))

            return render_template("result.html",movie_name =  movie_name,reviews = l1,author_name = author_list,comments = comments)
            
        except Exception as e:
            logging.info(e)
            return "Something went wrong"


if __name__=="__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
    # app.run(host="0.0.0.0")