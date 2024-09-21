<!--- Icon image with a summary of the app  -->

# <img src="assets git/icon.png" width="24" alt="App Icon"> TicTic-TacTac-ToeToe with KivyMD

This app is a cross-platform Tic-Tac-Toe game, which was originally developed in Tkinter but now has been converted to Kivy for Android support.

* The game is scalable and therefore can be used on multiple devices.
* The game supports 2 to 6 players.
* You can play against a ghost player.
* The grid is scalable up to 10 by 10 grid, which can be also non-symmetric.
* The number of symbols in sequence for a win can be also adjusted (or turned off).


<br/>



<!--- Installation Instructions -->

## Installation Instructions

Go to my [releases in this repo](https://github.com/AminShapso/Application04_TicTic-TacTac-ToeToe/releases) and download the latest .apk from there.  
OR  
Download from the direct link from [here](https://github.com/AminShapso/Application04_TicTic-TacTac-ToeToe/releases/latest/download/TicTacToe-1.0-arm64-v8a_armeabi-v7a-debug.apk)
  
You may need to enable installation from unknown sources.  
See this tutorial for more help:  
[https://www.androidauthority.com/how-to-install-apks-31494/](https://www.androidauthority.com/how-to-install-apks-31494/)

<br/>

## Installation Instructions (Hebrew) הוראות הורדה
לכו ל [אתר הזה](https://github.com/AminShapso/Application04_TicTic-TacTac-ToeToe/releases) ותלחצו על הקובץ .apk  
או (הדרך הפשוט יותר)  
לכו ל[קישור](https://github.com/AminShapso/Application04_TicTic-TacTac-ToeToe/releases/latest/download/TicTacToe-1.0-arm64-v8a_armeabi-v7a-debug.apk) הזה שאוטומטית יתחיל את ההורדה  

יכול להיות שתצטרכו להדליק "יישומים לא מוכרים" בהגדרות.
#### הסבר על התהליך הזה: 
תיכנסו להגדרות המכשיר > אבטחה > וסמנו את Unknown sources (יישומים לא מוכרים) בדפדפן שלכם, אשרו את התיבה שנפתחת ואז תפתחו את הקובץ.

<br/>



<!--- Game Instructions - Main menu  -->

## Game Instructions

<img src="Screenshots/Tutorial/02 Main Menu with annotations.jpg" width="360" align="left" alt="Main Menu with annotations">

<br/>

1. Number of Players:  
   Choose the number of players ranging from 2 to 6, "Ghost" player included.

2. Ghost:  
   Play against my algorithm.

3. Grid:    
   Choose your grid size ranging from 3 to 10.  
   It can be asymmetrical (like 3 by 10).

4. Symbol Sequence:  
   Choose the number of symbols in a series for the winner to be chosen, ranging from 2 to 10.  
   Each axis (column, row, and diagonal) can be controlled separately.  
   It can be also turned off.

5. Start Game:  
   Click here to start the game.

<br/><br/>



<!--- Game Instructions - Game screen  -->

<img src="Screenshots/Tutorial/03 Game Screen.jpg" width="360" align="left" alt="Game Screen">

<br/><br>

1. Back to Menu:  
   Exit the game and go back to the main menu (game status and scores are not saved).

2. Reset Game:  
   Reset the current board without resetting the scores.

3. Reset Results:    
   Reset the scores without resetting the current board.

4. View Scores:  
   See the current scores.  
   Scores are reset when you exit back to the main menu.

<br/><br/><br/><br><br/><br><br>



<!--- Game Instructions - Game example  -->

An example of a game of 3 players, with a grid of 6x4, with only the diagonal sequence enabled:

<img src="Screenshots/Tutorial/04 Game Example - Settings.jpg" width="360" align="left" alt="Game Screen">
<img src="Screenshots/Tutorial/05 Game Example - In game.jpg" width="360" align="left" alt="Game Screen">



<br/><br/><br/><br/><br/><br><br/><br/><br/><br/><br/><br><br/><br/><br/><br/><br/><br><br/><br/><br>



<!--- Demo + Requirements + To do list -->


## Demo

<img src="assets git/demo.gif" width="360" alt="App Demo">


<br/>

## Requirements

* certifi==2024.6.2
* charset-normalizer==3.3.2
* Cython==3.0.10
* docutils==0.21.2
* idna==3.7
* Kivy==2.3.0
* kivy-deps.angle==0.4.0
* kivy-deps.glew==0.3.1
* kivy-deps.sdl2==0.7.0
* Kivy-Garden==0.1.5
* Pygments==2.18.0
* pyjnius==1.6.1
* pypiwin32==223
* pywin32==306
* requests==2.32.3
* urllib3==2.2.2


<br/>

## For future development

* Add animations.
* Option to save scores.


<br/>

## Usage

APK File: "\bin\" OR "Releases" tab in GitHub
