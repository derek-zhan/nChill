import os.path
import requests


from flask import Flask, Response, request, render_template, redirect, url_for


app = Flask(__name__)
app.config.from_object(__name__)


import requests
import json

genres = {"Romance": 6, "Comedy": 4, "Fantasy":4, "Drama": 3, "Action": 3,"Sci-Fi":3, "Horror":0, "Thriller": 1, "Animation":2,"Family":1,"Adventure":4}
MPAA = {"NC-17":20, "R":15,"PG-13":10,"PG":5,"G":1,"N/A":1,"TV-14":10,"NOT RATED":20}

class Movie:
    def  __init__(self, title, genre, MPAAR, IMDBR, RTR ):
        self.title = title
        self.genre = genre
        self.MPAAR = MPAAR
        self.IMDBR = float(IMDBR)
        if (RTR == "N/A"):
            self.RTR = RTR;
        else:
           self.RTR = float(RTR)
        
def calScore( movie ):
    generalTotal = 0;
    listOfGenre =  movie.genre.split(", ")
    
    if ("Horror" in listOfGenre):
        genreAvg = 0;
#        print("it's a horror movie")
    elif ("Romance" in listOfGenre):
        genreAvg = 6;
    else:
        length = len(listOfGenre)
        for x in listOfGenre:
            if (x not in genres):
                length = length -1
            else:
                generalTotal = generalTotal + genres[x]
        genreAvg = generalTotal/length
    if (movie.RTR == "N/A"):
        score = (genreAvg*(MPAA[movie.MPAAR]-1))*0.7 + 0.3* (100/movie.IMDBR)
    else:
        score = (genreAvg*(MPAA[movie.MPAAR]-1))*0.7 + 0.3* (0.5 *(100/movie.IMDBR + 100/movie.RTR))
    movie.score = score *2
    return;

def printMovie(movie):
    print(movie.title,movie.score)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    #return render_template(content) 
    return Response(content, mimetype="text/html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


@app.route('/some-url') 
def get_data():
    inpt = request.args.get('userSelectedThis')
    inpt.replace(" ","+")
    json_data = requests.get('http://www.omdbapi.com/?t='+inpt+'&y=&plot=short&r=json&tomatoes=true').json()
    movieA = Movie(json_data["Title"],json_data["Genre"],json_data["Rated"],json_data["imdbRating"],json_data["tomatoRating"])
    calScore(movieA)
    percent = movieA.score
    printMovie(movieA)
    if(percent > 85):
      return redirect(url_for('totallygettinglaid'))
    elif (percent > 70):
        return redirect(url_for('likely'))
    elif (percent > 50):
        return redirect(url_for('looksPromising'))
    elif (percent > 40):
        return redirect(url_for('stillDoubtful'))
    else:
        return redirect(url_for('probsNot'))


@app.route('/winner', methods=['GET'])
def totallygettinglaid():  # pragma: no cover
    content = get_file('p1.html')
    return Response(content, mimetype="text/html")


@app.route('/probably', methods=['GET'])
def likely():  # pragma: no cover
    content = get_file('p2.html')
    return Response(content, mimetype="text/html")


@app.route('/maybe', methods=['GET'])
def looksPromising():  # pragma: no cover
    content = get_file('p3.html')
    return Response(content, mimetype="text/html")


@app.route('/negative', methods=['GET'])
def stillDoubtful():  # pragma: no cover
    content = get_file('p4.html')
    return Response(content, mimetype="text/html")



@app.route('/urnotgettingany', methods=['GET'])
def probsNot():  # pragma: no cover
    content = get_file('p5.html')
    return Response(content, mimetype="text/html")



if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)