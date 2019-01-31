#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 18:33:12 2019

@author: MatthewWright
"""


from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
import pandas as pd
import markovify as mk
from google_images_download import google_images_download




def make_meme(topString, bottomString, filename, name):

	img = Image.open(filename)
	imageSize = img.size

	# find biggest font size that works
	fontSize = int(imageSize[1]/5)
	font = ImageFont.truetype("Impact.ttf", fontSize)
	topTextSize = font.getsize(topString)
	bottomTextSize = font.getsize(bottomString)
	while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
		fontSize = fontSize - 1
		font = ImageFont.truetype("Impact.ttf", fontSize)
		topTextSize = font.getsize(topString)
		bottomTextSize = font.getsize(bottomString)

	# find top centered position for top text
	topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
	topTextPositionY = 0
	topTextPosition = (topTextPositionX, topTextPositionY)

	# find bottom centered position for bottom text
	bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
	bottomTextPositionY = imageSize[1] - bottomTextSize[1]
	bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

	draw = ImageDraw.Draw(img)

	# draw outlines
	# there may be a better way
	outlineRange = int(fontSize/15)
	for x in range(-outlineRange, outlineRange+1):
		for y in range(-outlineRange, outlineRange+1):
			draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
			draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

	draw.text(topTextPosition, topString, (255,255,255), font=font)
	draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

	img.save("{}.png".format(name))







def get_image(title):
    response = google_images_download.googleimagesdownload()
    search = title + ' original'
    arguments = {"keywords":"{}".format(search),"limit":1,"print_urls":True}
    paths = response.download(arguments)
    image_path = paths[search]
    return image_path
    
    
    
    
    
    


dataset = pd.read_csv('memegenerator.csv')

all_text = dataset.iloc[:, 6].tolist()

text = open("Text.txt", encoding="utf8").read().split('\n')

text_generator = mk.NewlineText(text)



corpus = []
bad_ones = []
for i, review in enumerate(all_text):
    try:
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = ' '.join(review)
        corpus.append(review)
    except:
        corpus.append('Hello')
        bad_ones.append(i)
        pass

# Creating the Bag of Words model
cv = CountVectorizer(max_features = 10000)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 2].tolist()

categories = {}
count = 0
for j in y:
    if j not in categories.values():
        categories[j] = count
        count += 1
        
reverse_categories = {}
for i in categories.keys():
    reverse_categories[categories[i]] = i
    
for i in range(len(y)):
    y[i] = categories[y[i]]
        
        
# Fitting Naive Bayes to the Training set
classifier = GaussianNB()
classifier.fit(X, y)

def do(name):
    k = [text_generator.make_sentence()]
    s = k
    s = cv.transform(s).toarray()
    s = classifier.predict(s)[0]
    s = reverse_categories[s]
    
    image_path = get_image(s)[0]
    length = len(k[0].split())
    topString = ' '.join(k[0].split()[:length//2])
    bottomString = ' '.join(k[0].split()[length//2:])
    return topString, bottomString, image_path, name
    

x, y, z, d= do(input('What would you like to call the file: '))
make_meme(x, y, z, d)

