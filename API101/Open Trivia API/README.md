Open Trivia API Game

Overview

Let's create an Open Trivia API game.
The first step is to create a backend API that dynamically represents trivia questions and the neccessary components that come with it. 
There are a few configuration options that can be implemented to change the type of questions.
We have to find a way to find a way to dynamically change the config of the questions give the API URL.

For example, the URL:

https://opentdb.com/api.php?amount=10

Returns an HTTP representation of a JSON file that we can use to start the game.
The problem is that it is not dynamic, as it always contain 10 questions of any field, category, difficulty and type (encoding will be excluded, as it is semi-irrelevant)

Other URL options can be something like...

https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple

Which we can modify manually to give us different questions as a form of a JSON result.

So, let's get started.

Log 1:

To start, I will create three main modeules:

1. auxiliary.py: This module will contain all the guardian-checking functions, logistical functions, API request functions, input functions, and possibly custom classes if needed later.
2. url_request.py: This module will utilize functions from auxiliary.py to build the URL based on the player's input.
3. main.py: This module will initialize the game window using the Pygame library. It will import the default function, get_trivia, from url_request.py.

Starting off with auxiliary.py, I began by importing the `requests` library.

I moved on to creating the "guardian code" functions that will return mostly boolean values, to later be used and compared to raise errors.
The `check_category` function was interesting. I had to check the input category alone using the API?
I wanted to make sure that whatever information is updated from Open Trivia's side is also updated to my program. And although it makes things a bit slower and more complex than they might've been otherwise, at least I get to reinforce my knowledge and practice.

Moving on to the url_request.py module was straight forward as I just needed to import every function and piece them together. After some debugging, I am confident in saying that this part of the game is now done. Now I need to move on to figuring out the pygame library in the main module. Which might take some time.

Log 2

