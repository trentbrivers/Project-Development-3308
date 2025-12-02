# !Jeopardy 
## Team Members: Ebrahim Azarisooreh, RJ Barrett, Darvin Conttreras, Rachel Mertz, Trent Rivers, Megan Yeung
### Project Tracker Link: https://not-applicable.atlassian.net/jira/core/projects/NJ/board?filter=&groupBy=status
### Link to Demo Video:
### GitHub Repo: https://github.com/trentbrivers/Project-Development-3308
### Public Hosting: https://not-jeopardy.onrender.com/
### Final Status Report:
#### Completed: 
Contained in this repository is a simple web-hosted version of Jeopardy. The front-end was created using the React JavaScript library and pulls from a variety of CSS files to give the Jeopardy Game a retro type styling. 
The backend of the game is written in Python and connects to a simple database created using SQLite. Communication between the frontend and backend is conducted primarily through Flask Routing Paths using JSON data. 
This was selected as a common data exchange method as JSON is supported by a wide variety of programming languages and was relatively straightforward to implement. 

The game can either be accessed via the public hosting link above or running the build scripts locally in order, build_db.ps1, build.ps1, start.ps1. The build_db script creates the database and runs an HTML extraction 
script pulling Jeopardy Question Data from the HTML file in the /db/data directory into the database. The build.ps1 scripts installs frontend dependencies and package requirements, builds the frontend nodes and activates 
the virtual environment. The start.ps1 script starts both the backend and frontend portions of the codebase for execution. When accessing the public hosting site, all of the above is processed by the hosting site. 

Upon launching the game, the user is prompted for a username and upon entering the username is commited to the Database for score tracking, highscore tracking, and game completion.

![Welcome_Screen.png](/img%2FWelcome_Screen.png)


Upon clicking start game the primarily driving function initialize game is called from db/core.py. 
![Start_Game_Screen.png](/img%2FStart_Game_Screen.png)
This function queries the DataBase and constructs local arrays of questions, answers, and point values, which are passed 
through the React Routing to the frontend as JSON arrays where they are visualizing displayed on the game board. The category and single or double jeopardy tags are encoded in the array index positions. 

![Game_Board.png](/img%2FGame_Board.png)

Upon selecting a question the frontend portion of the code pulls the appropriate question from the local arrays
and populates it for the player. 
![Question Screen.png](/img%2FQuestion%20Screen.png)


Upon the player entering an answer the answer is routed back to the backend portion of the code via the submit answer React route. The answer is scored and updated scores commited to the database
and a correct/incorrect flag is returned to the frontend along with updated scores. The correct answer is displayed along with updated score to the user. 

![Answer_Correct_Screen.png](/img%2FAnswer_Correct_Screen.png)


This process continues throughout the first stage of the game (single jeopardy). Upon completing the last question of single jeoaprdy, double jeopardy is loaded from initial local arrays. The above gameplay loop continues
until the completion of double jeopardy. 

Upon the completion of double jeopardy the player is taken to the final score screen and is shown their final score with an option to return to the main menu, which returns them to the 
start game/leaderboard screen. 

![Final_Score_Screen.png](/img%2FFinal_Score_Screen.png)

#### In the Middle of Implementing:
In progress currently is the implementation of Final Jeopardy. There were several roadblocks encountered that led us to selecting the current iteration as an appropriate stopping point, 
namely the needing user input for selecting a bet amount for final jeopardy as well as adjusting the current routes/JSON array to account for the final jeopardy question and indicate that the round
was final jeopardy. Given the scope of these changes and the time left in the semester we decided to avoid introducing potential bugs and favored shipped a functional product. Additionally, we were planning to adjust the database
to account for multiple games worth of jeopardy questions. As constructed right now the database holds one jeopardy game HTML worth of question data, we would need to adjust the database to support handling multiple games of data and adjust the initialize game function
to select a games worth of data from the database rather than pulling all of the questions in the database. Given the scope of those changes we assessed the chance of introducing bugs as high and this was also put on hold in favor of project delivery. 

#### Planned Future Work: 
There were a variety of features originally planned that were not incorporated into the final version of our game. As discussed above, both Final Jeopardy and support for more than one game's worth of data were planned future work. An iteration of the database after that was
a database that would shuffle all of the questions from multiple games grouping them by category essentially creating "new" jeopardy games that were a mix of questions from multiple different historic games of Jeopardy. Leaderboard functionality was another planned future upgrade. 
Currently, the database does track highscores between multiple different players but in our testing we were constantly wiping and recreating the database when conducting troubleshooting that implementing the leaderboard fell to a lower priority compared to some of the other functionality
implemented. Multiple player support was also planned as a stretch goal/feature but given the current state of the game that is several sprint iterations into the future. 

#### Known Bugs/Issues:
There are a couple no known bugs with the base implementation of the game. The leaderboard button is a stub/placeholder planned for future work and does not take the user to leaderboard. Also after completing the game and being taken to the home screen, selecting start game takes the user back to
the blank board of the just completed game. This release is a minimum viable product and only takes the player through a single game recording their name and highscore in the database. 
