# Open Trivia API Game

## Overview

Let's create an Open Trivia API game.
The first step is to create a backend API that dynamically represents trivia questions and the neccessary components that come with it. There are a few configuration options that can be implemented to change the type of questions. We have to find a way to find a way to dynamically change the config of the questions given the API URL.

For example, the URL:

`https://opentdb.com/api.php?amount=10`

Returns an HTTP representation of a JSON file that we can use to start the game.
The problem is that it is not dynamic, as it always contain 10 questions of any field, category, difficulty and type (encoding will be excluded, as it is semi-irrelevant to this project)

Other URL options can be something like...

`https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple`

Which we can modify manually to give us different questions as a form of a JSON result.

So, let's get started.

###Log 1:

To start, I will create three main modules:

1. `auxiliary.py` This module will contain all the guardian-checking functions, logistical functions, API request functions, input functions, and possibly custom classes if needed later on.
2. `url_request.py` This module will utilize functions from auxiliary.py to build the URL based on the player's input.
3. `main.py` This module will initialize the game window using the Pygame library. It will import the default function, get_trivia, from url_request.py.

Starting off with auxiliary.py, I began by importing the `requests` library.

I moved on to creating the "guardian code" functions that will return mostly boolean values, to later be used and compared to raise errors.
The `check_category` function was interesting. I had to check the input category alone using the API. Is this neccessary?
In my opinion, it is. I wanted to make sure that whatever information is updated from Open Trivia's side is also updated to my program. And although it makes things a bit slower and more complex than they might've been otherwise, at least I get to reinforce my knowledge and practice.

Moving on to the `url_request.py` module was straight forward as I just needed to import every function and piece them together. After some debugging, I am confident in saying that this part of the game is now done. Now I need to move on to figuring out the pygame library in the main module. Which might take some time.

The main file remains empty as of now.

###Log 2:

Following this next update:

I began by introducing a new terminal logging system for `url_request.py` and  `main.py`. These messages will serve as a way to introduce possible vulnerabilities and to faciliate error management. It also looks pretty nice and cool.

I continued to work with the Pygame library in the main module. It has taken me a while to figure out the various components that this library has. Thankfully, I was able to look at documentation provided by pygame.org (https://www.pygame.org/news), which was helpful to an extent. I was able to set the foundations to the game, added error excpetion catching, logging and introduced the main background image for the main game menu. This image as well as future images will be stored in the newly created assests folder.

Finally, I added the next a new file, `button.py` —also located within the assets folder— that will set the global font for the game, will create the button classes and functions intanciating these classes to be called in the main python file as a default function. This will now be my focus as it remains empty.

###Log 3:

There were lots of changes introduced. This section is what took the most time by far.

I started by creating the implementations for the essential class, Button that will be one our primary asset throuhgout the game. I added various possible configurations for the button instances, which included types of font, color, and hovering mouse event coloring options. 

###### Button Class

    def __init__(self, x:int, y:int, width:int, height:int, text:str, font:pygame.font.Font, fontColor:tuple, color:tuple, hover:tuple) -> None:
        self.x = x
        self.y = y

        self.box = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = color
        self.hover = hover
        self.font = font
        self.fontColor = fontColor

        self.clicked = False
        self.visible = True


This class contains three methods; `draw`, `undraw` and `isclicked`. For the sake of documentations I will explain what each of these do and how they are usefull.

The `undraw` method simply changes the attribute of the button's visibility into False, making the button unable to render. This method is meant to display clarity within my own code given the method's name.

The `draw` method checks if the attribute of the instanciated class is meant to be visible or not. If it isn't  it simply returns nothing, ending the functionality of the method. It will get the positioning of the cursor. If the cursor hovers over the button box, it will change color from its default. If the button is meant to be visible, it will then render the button box and its text.

The `isclicked` method is pretty self explanatory. When the mouse event indicates a click within the button's boundry (given by `pygame.MOUSEBUTTONDOWN`) then it will change the state of the clicked attribute. This is to ensure that there can only be one click when mouse button is down, considering this implementation will be inside a while loop. I ran into issues where while the button is down it will trigger the event lots of times until button is up.

I initialized some modules whtin the `assets` folder, which conatins:
- `button.py` that has the Button class.
- The font .ttf file for the font I wanted to use.
- `components.py` that further contains:
	- The button instanced in variables to be imported into the main file.
		- `main_start_btn `, `main_quit_btn `, `quit_confirm_yes `, `quit_confirm_no `
	- Variables: Default configurations, Windows, Font, the object holder, the screen.
	- Functions that use global variables (Not the best practice, but will use for sake of simplicity). These functions will condense and simplify the main code sector.

I then implemented all of these assets, insatnces, functions and methos to build the main menu. With and option of game termination. Before ending the game, the user will be promted to decide whether they are sure to quit or not. Modifying the visibility of the buttons accordingly from the start.

I also keep track of the buttons and possible assets contained in the screen, for future window changing purposes. I don't know if this may become an issue, to having to easrase the assets manually when chaing into another window. Just in case I will implement it for now.

The following step is to beggin the game. I need to connect the API request to dynamically  change the questions according to the player's wished configuration. Which will be taking place in the `CONFIG_MENU` window right before the `GAME_MENU` window.



