"# Movie_Recommender" 
Website deployed on Heroku Link : https://movie-reccomendation.herokuapp.com/
NOTE-User-User Based Recommendation System and Matrix decomposition are working fine on website however Item-Item is generating timeout,
can show that locally 
0)I have taken an initial 50 dummy users who have all rated any 10 movies randomly from 1-5.
0*)If the page does not load initially(console of the browser shows no movement) please try to reload it atleast once
1)MongoDB Collection has just been added as a json file and the link used in MongoClient has been removed to ensure privacy
2)The program is slower than usual as the data is being pullled from the MongoDB server being computed upon and then asked for again by the program
3)Wait atleast 1 min for the Datatable on each page to load.
4)Comments have been added in the algos.py file however not in app.py
5)scrapeIMDB.py is the python File I used for scraping IMDB USing bs4 and sometimes selenium
6)make_pics.py is a file I used to keep a stash of pictures in my Flask static folder
