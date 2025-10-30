Pasting Moodle submission instructions for convenience

You will create a list of descriptions for the pages that will be implemented for your project.
You must add a file PAGE_TESTING.md to your repository and provide the following for each page (at least 5 independent pages):

    Page Title
    Page Description (include a mockup or hand drawn image of the page)
    Parameters needed for the page
    Data needed to render the page

    Link destinations for the page

    List of tests for verifying the rendering of the page

Submit a link to your document in your repository. (one submission per team)

## 1) Title Screen

![Title screenshot](img/title_screen_screenshot.png)

### Page description 
This is the screen the player will see upon launching the game. It has the game's name and a start button.

### Parameters needed
- onStart

### Data needed to render
Image of game logo

### Link destinations:
onStart (to navigate to category screen)

### List of tests:
- title image renders correctly
- "Start Game" appears
- clicking start button changes the screen


## 2) Category Screen

![Category screenshot](img/category_board.png)

### Page description 
This is the screen the player will see after clicking the start button on the Title Screen. A grid will be displayed in which there are 6 columns for categories, and 5 rows for each clue. The dollar amounts each clue is worth increases from top to bottom. Each cell is clickable.

### Parameters needed
- onSelectQuestion
- tiles
- setTiles

### Data needed to render
Array of tiles, each tile's index

### Link destinations:
onSelectQuestion (navigate to Question Screen)

### List of tests:
- six categories in top row
- 30 tiles appear (6x5 grid)
- clicking a tile sets it to `null`?
- clicking a tile changes the screen to the Question Screen

## 3) Question Screen

![Question screen](img/question_screenshot.png)

### Page description 
This screen appears after the player selects a clue from the Category Screen. There is a text-box for them to enter their question, and there is a clickable submit button next to it.

### Parameters needed
onBack

### Data needed to render
- Local state `answer`
- Clue text

### Link destinations:
onBack

### List of tests
- text renders
- input box appears and allows typing
- clicking "Submit" button logs answer and returns player to Category screen

## 4) Player's Score?

### Page description 
This page shows the player their score once the game is finished.

### Parameters needed
score

### Data needed to render
Player's score

### Link destinations
- "next" button to navigate to Game Over screen

### List of tests


## 5) Game Over screen?

### Page description 
This page shows the player that the game is finished

### Parameters needed

### Data needed to render
Text for "Game Over" and/or "Thanks for playing!"

### Link destinations

### List of tests