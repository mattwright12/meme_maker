#Read Me

There are two files in this section

#meme_formatter
This file contains the function to format the meme

It takes the following arguements:
    topString- the text to go at the top of the image
    bottomString- the text to go at the bottom of the image
    filename- the filepath of the image you would like to use
    name- what you would like to call your output file
    
It saves a .png file in the set directory

#image_finder

Downloads the first image result on google for the inputted search phrase

It takes the following arguements:
  title- the search phrase you would like to use
  
It is important to note that the function adds ' original' to the arguement to try and get the plain base image

It will save the image on in the directory, and return the file path of it
