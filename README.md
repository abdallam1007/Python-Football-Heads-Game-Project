Name: Abdalla Hassan Mohamed

andrewID: abdallam

15-112 Final Project Description:
My project is based on the famous game “head soccer”. I will add many features that are not offered in the original game.

Game Description: this game is basically two players playing against each other. Each one of them is trying to score in the other player’s goal.
Every player is contained from a head and one leg. The player who scores more goals before the timer hits 90 is the winner. 

Movement: 
  If only one player:
  -	“right arrow” >> move forward
  -	“left arrow” >> move backward
  -	“up arrow” >> jump
  -	“down arrow” >> move the leg to shoot the ball 

  If there is more than one player:
  -	Letter “D” >> move forward
  -	Letter “A” >> move backward
  -	Letter “W” >> jump
  -	Letter “S” >> move the leg to shoot the ball

Features and user interface: when the user open the game the first window will have two choices one of them is a one player against one player mode,
the second choice is one player against computer.It will also have an option to show the instructions of the game.
 
 -	The first choice (Two players):
  The second window will ask player1 and player2 for their names. Then, the third window is the game window which contains the two players, two goals, score board and a timer.
  After counting on the screen from 3 to 1, the ball is dropped in the middle and the game starts.
  Each of the players will try to score goals against the other player. When the timer hits 90 the game stops and whoever scored more goals wins the game. The screen shows the name of the winner.
  After the game stops the players are asked if they want to exit the game or go back to the main window. If the player replies with exit, the game exits and the window is closed.
  If the player decides to go back to the main window, the game will restart and show the first window again.

-	The second choice (player Vs Computer):

	The second window will ask the player for a name. Then, the third window is the game window which contains the player and the computer, two goals, score board and a timer.
	After counting on the screen from 3 to 1, the ball is dropped in the middle and the game starts.
	The player will try to score goals in the computers goal. At the same time the computer will try to defend his goal and not allow the ball to get in by detecting the place of the ball and try to be in the ball’s way.
	When the timer hits 90 the game stops and the screen will show a message saying “You are the Winner” if the player won. Otherwise a message saying “you lost!! ” will be showed.
	After the game stops the player is asked if he/her wants to exit the game or go back to the main window. If the player replies with exit, the game exits and the window is closed. If the player decides to go back to the main window, the game will restart and show the first window again.

Physics: I will implement physics in my project. To make the movement of the ball more realistic, there will be colliding effects between the player and the ball and between the ball and the borders of the game window.

Libraries I will use: (Note: I might add or remove from these libraries depending on what the project needs)
-	PyGame
-	Physics

First check point (Due Sunday November 24):
-	I will be done with the two players mode 
-	I will be done with the interface for the player Vs computer mode

Second check point (Due Monday December 2):
-	I will be done with the player Vs computer mode 
-	The game will be ready to play 

Things that I could add depending on time: 
	-	I could another mode where two players play against each other, but they choose a maximum number of goals to reach before the game starts (I will give this option in this game), the first player to score this number of goals win the game.
	-	I could also add other features in the game that make the ball move faster or make the opponent’s goal bigger for some seconds.

Thank you for your time (:
