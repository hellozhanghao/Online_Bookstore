# Online_Bookstore
Our web application employed model-view-controller framework using python language with flask package. We used SQLAlchemy to initialize the tables in python at the beginning. Each table will be considered as an object, so that we could build connection between database and python code directly.

Flask will assign a HTML file for a URL to generate UI for different addresses as well as governing the pages which require authentication. User will be rejected if they didn’t sign in if the page requires login information. 

There are buttons and blanks provided in HTML files and users could use those forms to achieve interaction with our web application. POST message will be sent to our main program if certain button is clicked and we will read the input based on unique ID for different button or blank. The corresponding insertion, deletion or update function will be executed based on user’s request such as adding books into shopping cart or writing review for a book.





