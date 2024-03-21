from nltk.corpus import wordnet as wn
import random
from bs4 import BeautifulSoup
import requests

from country_list import countries_for_language

def get_food():

    food = wn.synset('food.n.02') # Get the synsets (synonyms) for the noun "food"

    #go down the hierarchy from more general terms to more specific terms 
    #for each synset encountered get lemma names (base forms of words), set() removes duplicates, then put them in a list
    food_words = list(set([w for s in food.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))
    return random.choice(food_words)

def get_animal():

    animals = wn.synset('animal.n.01')
    animal_words = list(set([w for s in animals.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))
    return random.choice(animal_words)

def get_movie():
    url = 'https://www.timeout.com/film/the-100-best-movies-of-the-21st-century-so-far'

    response = requests.get(url) #retrieve the content of the web page located at the URL
    soup = BeautifulSoup(response.text, "html.parser")  #HTML content of the web page 
    title_elements = soup.find_all('h3', class_='_h3_cuogz_1') # Find all elements containing movie titles

    # Extract titles and store them in a list
    movie_titles = []
    for title_element in title_elements:
        title = title_element.text.strip() #getting text

        title_without_num = title.split(".") #removing irrelevent part at the beginning
        title_without_year =title_without_num[-1].split("(") #removing the year

        movie_titles.append(title_without_year[0].strip()) #add clean title to the list

    #2 last elements are not movies so remove them
    movie_titles.pop(100)
    movie_titles.pop(99)

    return random.choice(movie_titles) #return a random movie from a list

def get_country():

    countries_dict = dict(countries_for_language('en')) #get a dictionary of countries in English
    countries = list(countries_dict.values()) #get the values (actual countries), add to a list
    return random.choice(countries)

#######################################
#######################################

word =""
number_mist = 0
word_guessed = False

def main():
    global word_guessed
    global word
    global number_mist
    letters_tried = []

    #start the game/ choose category
    start = input("Ready to play? Choose a category: food | animals | movies | countries\n")
    
    #get a random word based on category
    if start == "food":
        word = get_food()
    elif start == "animals":
        word = get_animal()
    elif start == "movies":
        word = get_movie()
    elif start == "countries":
        word = get_country()
    else:
        print("You need to choose a category :(")
    
    print(word)

    #display the incription of the word
    incription = letters_count(word)
    print(f"Word: {incription}")

    #start guessing
    while number_mist < 16 and not word_guessed:

        print(f"\nFails left: {16-number_mist}") #how many more attempts left
        print(f"\nTried letters: {letters_tried}") # a list of letters a user tried

        letter = input("\nGuess a letter: ")
        letters_tried.append(letter)
       
        index_of_letter = check_letter(letter) #check if letter is present
        drawing_l = drawing(number_mist) #get a drawing based on mistakes
        print(f"\n+---+\n{drawing_l}\n=========\n")

        if index_of_letter != None: #if letter is present, update the incription
            for i in index_of_letter:
                result = correct_inc(i, letter) #function call with index of letter and letter to update incription
            print(f"Word: {result}")
        else:
            print(''.join(list_of_signs)) #if letter is not present, print previous incription

    if number_mist >= 16:
        print(f"\nGame Over. The word was '{word}'.\n")
    elif word_guessed:
        print(f"\nCongrats! You guessed the word, it is '{word}'.\n")
        

#drawing of a 'hangman' based on mistakes
def drawing(num_missed):
    drawing=""
    if num_missed == 1:
        return "_"
    elif num_missed == 2:
        return "__"
    elif num_missed == 3:
        return "___"
    elif num_missed == 4:
        return "|___"
    elif num_missed == 5:
        return "|\n|___"
    elif num_missed == 6:
        return "|\n|\n|___"
    elif num_missed == 7:
        return "|\n|\n|\n|___"
    elif num_missed == 8:
        return "|\n|\n|\n|\n|___"
    elif num_missed == 9:
        return " _\n|\n|\n|\n|\n|___"
    elif num_missed == 10:
        return " _\n| |\n|\n|\n|\n|___"
    elif num_missed == 11:
        return " _\n| |\n| 0\n|\n|\n|___"
    elif num_missed == 12:
        return " _\n| |\n| 0\n| |\n|\n|___"
    elif num_missed == 13:
        return " _\n| |\n| 0\n|\|\n|\n|___"
    elif num_missed == 14:
        return " _\n| |\n| 0\n|\|/\n|\n|___"
    elif num_missed == 15:
        return " _\n| |\n| 0\n|\|/\n| /\n|___"
    elif num_missed == 16:
        return " _\n| |\n| 0\n|\|/\n| /\\ \n|___"
    return drawing


#correct the incription (add to it guessed letters)
def correct_inc(index_of_letter, letter):
    global word_guessed
    #change _ into the letter
    list_of_signs[index_of_letter] = letter
    #check if word is guessed
    if "_ " not in list_of_signs:
        word_guessed = True

    return ''.join(list_of_signs)

#check if letter is in the list and return the index of it if yes
def check_letter(letter):
    global number_mist
    if letter in word.lower():
        #find index of guessed letter
        index_of_letter = [index for index, char in enumerate(word.lower()) if char == letter]
        #print(f"\nBot: Good job!'{letter}' is present\n")
        return index_of_letter
    else:
        number_mist+=1
        #print(f"Sorry, no {letter} here. Try again.\n")

list_of_signs= []
#make an incription of a word (ex. _ _ _ _)
def letters_count(word):
    global list_of_signs 

    for i in word:
        if i == "_":
            sign="   "
            
        elif i==" ":
            sign="   "
            
        else:
            sign="_ "

        list_of_signs.append(sign)

    return ''.join(list_of_signs)

main()
