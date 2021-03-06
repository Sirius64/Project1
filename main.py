import json
import altair as alt
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pprint
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

# nltk.download("punkt")
# nltk.download("stopwords")

# extract the api key fromthe json file
api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

# general formatting for the web page using streamlit
st.title("COP 4813 - Web Application Programming")

st.title("Project 1")
st.header("Part A - The Stories API")
st.subheader("This app uses the Top Stories API to display the most common words used in the top current articles "
             "based on a specified topic selected by the user. The data is displayed as a line chart and as a "
             "wordcloud image.")
st.subheader("")
st.header("**I - Topic Selection**")

# input for the first portion, the users name and the desired topic
name = st.text_input("Please enter your name")

interest = st.selectbox("Select a topic of your interest", options=('', 'arts', 'automobiles', 'books', 'business', 'fashion', 'food',
                                                         'health', 'home', 'insider', 'magazine', 'movies', 'nyregion',
                                                         'orbituaries', 'opinion', 'politics', 'realestate', 'science',
                                                         'sports', 'sundayreview', 'technology', 'theater', 't-magazine'
                                                         , 'travel', 'upshot', 'us', 'world') )

stopwords = stopwords.words("english")

# ensures the checkboxes only appear if the topic is selected to avoid a bad url error
if interest != "":
    # complete the url using the chosen topic
    topStoriesURL = "https://api.nytimes.com/svc/topstories/v2/" + interest + ".json?api-key=" + api_key

    # request the result of the url
    response = requests.get(topStoriesURL).json()

    # store the result in a json file and read the file contents
    main_functions.save_to_file(response, "JSON_Files/topStories.json")
    topStoriesOutput = main_functions.read_from_file("JSON_Files/topStories.json")

    # the following block of code cleans up the list variable so only desirable words are left
    toProcess = ""
    for i in topStoriesOutput["results"]:
        toProcess = toProcess + i["abstract"]

    words = word_tokenize(toProcess)

    fdist = FreqDist(words)

    words_no_punc = []
    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    fdist2 = FreqDist(words_no_punc)

    clean_words = []
    for w in words_no_punc:
        if w not in stopwords:
            clean_words.append(w)

    fdist3 = FreqDist(clean_words)

    cleanWordsFinal = ""
    for x in range(0, len(clean_words)):
        cleanWordsFinal = cleanWordsFinal + " " + clean_words[x]
    # end block of cleaning code

    st.write('Hi ' + name + ', you selected the ' + interest + ' topic.')

    # generates the line chart for the ten most common words and their appearances for the selected topic
    st.header("\n**II - Frequency Distribution**")
    checked = st.checkbox("Click here to generate frequency distribution")
    if checked:
        toSeparate = fdist3.most_common(10)
        wordAlone = []
        count = []
        for x, y in toSeparate:
            wordAlone.append(x)
            count.append(y)
        imgOne, axOne = plt.subplots()
        axOne.plot(wordAlone, count, linewidth=2.0)
        axOne.set_xlabel("Words")
        axOne.set_ylabel("Count")
        axOne.tick_params(axis='x', which='major', labelsize="x-small")
        imgOne.savefig("images/img1.png")
        st.pyplot(imgOne)

        # chart_data = pd.DataFrame({'words': wordAlone, 'count': count})
        # alt.Chart(chart_data).mark_line().encode(x=wordAlone,y=count)
        # chart_data.rename(columns='words')
        # st.line_chart(chart_data)

    st.subheader("")

    # generates a wordcloud for the selected topic using the cleaned words list
    st.header("\n**III - Wordcloud**")
    checkedTwo = st.checkbox("Click here to generate wordcloud")
    if checkedTwo:
        wordcloud = WordCloud().generate(cleanWordsFinal)
        imgTwo, axTwo = plt.subplots()
        axTwo.imshow(wordcloud)
        axTwo.axis("off")
        plt.show()
        imgTwo.savefig("images/img2.png")
        st.pyplot(imgTwo)
    st.subheader("")

st.header("Part B - Most Popular Articles")
st.subheader("Select if you want to see the most shared, emailed or viewed articles.")

# provides the options for the user
chosenSet = st.selectbox("Select your preferred set of articles", options=('', 'shared', 'emailed', 'viewed') )

chosenTime = st.selectbox("Select the period of time (last days)", options=('', '1', '7', '30') )

# ensures the user selects at least two options to prevent a bad url
if chosenSet != '':
    if chosenTime != '':
        # construct the url with the choices
        MostPopularURL = "https://api.nytimes.com/svc/mostpopular/v2/" + chosenSet + "/" + chosenTime + ".json?api-key=" + api_key

        # retrieve a response and save it to a json file
        responseTwo = requests.get(MostPopularURL).json()

        main_functions.save_to_file(responseTwo, "JSON_Files/mostPopular.json")
        mostPopularOutput = main_functions.read_from_file("JSON_Files/mostPopular.json")

        # clean the words list by removing undesired words
        toMakeWordcloudTwo = ""
        for i in mostPopularOutput["results"]:
            toMakeWordcloudTwo = toMakeWordcloudTwo + i["abstract"]

        wordsPopular = word_tokenize(toMakeWordcloudTwo)
        wordsPopular_no_punc = []
        for w in wordsPopular:
            if w.isalpha():
                wordsPopular_no_punc.append(w.lower())

        clean_wordsPopular = []
        for w in wordsPopular_no_punc:
            if w not in stopwords:
                clean_wordsPopular.append(w)

        cleanWordsFinalTwo = ""
        for x in range(0, len(clean_wordsPopular)):
            cleanWordsFinalTwo = cleanWordsFinalTwo + " " + clean_wordsPopular[x]

        # generate a word cloud with the clean word list
        wordcloudTwo = WordCloud().generate(cleanWordsFinalTwo)
        imgThree, axThree = plt.subplots()
        axThree.imshow(wordcloudTwo)
        axThree.axis("off")
        plt.show()
        imgThree.savefig("images/img3.png")
        st.pyplot(imgThree)
