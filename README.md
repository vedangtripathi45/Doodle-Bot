# <ins>Doodle Bot</ins>

A bot that takes an image of a certain path as input and moves along that path drawing it with a sketch pen. 
The python script uses OpenCV library to process the image, detects the turn points, start point and end point. 
The points are sorted using DFS to get the order in which the bot should move to draw all the lines and 
returns a string containing letters that represent the movement direction. The output string is taken as an 
input by the Arduino that coordinates the movements of the bot. Encoders are used with motors for straight 
aligned movement and accurate rotation at required angles. 
