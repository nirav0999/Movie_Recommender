<h1>Movie_Recommender</h1> 
Website deployed on Heroku Link : https://movie-reccomendation.herokuapp.com/ <br>
NOTE-User-User Based Recommendation System and Matrix decomposition are working fine on website however Item-Item is generating timeout,
can show that locally 

0*)If the page does not load initially(console of the browser shows no movement) please try to reload it atleast once <br>
1)MongoDB Collection has just been added as a json file and the link used in MongoClient has been removed to ensure privacy <br>
2)The program is slower than usual as the data is being pullled from the MongoDB server being computed upon and then asked for again by the program <br>
3)Wait atleast 1 min for the Datatable on each page to load. <br>
4)Comments have been added in the algos.py file however not in app.py <br>
5)scrapeIMDB.py is the python File I used for scraping IMDB USing bs4 and sometimes selenium <br>
6)make_pics.py is a file I used to keep a stash of pictures in my Flask static folder <br>

Approach Followed-
---------------------------------------------------------------------------------------------


Scraping
-----------


Scraped Directly from the IMDB Pages using BeautifulSoup(New) and Selenium. <br>
Scraped movie name ,image ,genres(fixed 12 genres mentioned in scrapeIMDB.py),,date of release,summary of the movie,IMDBRating ,no of voters. <br>
Stored all the data in the MongoDB. <br><br>
Attached Json MongoDB file in the repo as Moviedata.json



Backend
-----------
Each Client must rate 10 movies the reason for this is to decrease the sparsity of the matrix. Optimal performance,Client convenience and 
Accuracy are the reasons for choosing this number. <br>
Implemented the Algos found in "Recommender Systems: The Textbook" for User-User and Item-Item Based. <br>
Implemented Matrix Factorization by finding Algorith in Various Medium blogs. <br>
I have taken an initial 50 dummy users who have all rated any 10 movies randomly from 1-5. <br>

Frontend
--------------------
Made 2 flask Webpages Welcome and result which collect data from the  User End and communicate with app.py using ajax calls.
