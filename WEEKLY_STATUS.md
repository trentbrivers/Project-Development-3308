# Team: 'Not Applicable' </br> Members: Ebrahim Azarisooreh, RJ Barrett, Darvin Conttreras, Rachel Mertz, Trent Rivers, Megan Yeung

#### TEAM NOTE: for screenshots in markdown, please store and reference them from the ./img directory (if uploaded directly to this file you'll have to use png or jpeg) 

# Weekly Status Updates

### Week of October 5, 2025

#### Jira Snapshot: 

<img width="1150" height="619" alt="image" src="https://github.com/user-attachments/assets/4b2e0265-2755-40af-9231-6324e075c263" />



#### 10/5 RJ's updates:

Built out a high level flow diagram depicting the flow of function calls between the frontend-backend and backend-database. We plan to use this as a baseline for identifying portions of the MVP.
PLan for this coming week is to built out functions for the MVP of displaying a single question block on the frontend and getting the data flow for one block/question/answer correct before scaling
up to multiple questions. Plan is to utilize a dummy question/answer for testing for now while the database is built out and connect later. 

<img width="1150" height="619" alt="image" src="https://github.com/user-attachments/assets/6037e9a1-24ed-48e4-aaa9-1088be44425b"/>

#### 10/5 Ebrahim's updates:
Added initial infrastructure using a flask service backend to communicate game state between the backend/DB and the frontend, in order to facilitate progress through the game as well as
informed rendering for the frontend for clear separation of logic and duties. The template is currently stored in src/backend/core.py

<img width="824" height="756" alt="image" src="https://github.com/user-attachments/assets/758ec574-9307-4034-9231-654b772622a5" />


#### Front-end

![figma_screenshot.png](figma_screenshot.png)

Darvin's Figma might not work out due to free trial limitations; 
however, the mock-up from Figma might still be useful to refer to for 
design ideas. 

![mvp_FLOW.jpeg](mvp_FLOW.jpeg)

Trent drew a high-level sketch of the game's flow. He also added a 
front-end directory and started a corresponding Git branch.
Front-end team had decided to use React to build our game's front-end.

![category_board.png](category_board.png)

Our game has a title screen with the !Jeopardy name and a 'Start Game'
button. Experimenting with adding a background and modifying fonts of
this page. Clicking the start button transitions to the category board 
with dollar amounts on a functioning grid of buttons. 
