from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
import http.client
import json
import requests

print("Go to themoviedb.org to get your own API key ")
APIKey = input("Enter Key number:")

likeMovieNames = []
hateMovieNames= []
likeMovieOverViews =[]
hateMovieOverViews = []

neverSeenNames = []
neverSeenOverview = []

def enterData(type = "Never"):
  movieName = input("Enter movie name:")
  if(type== "Like"):
    likeMovieNames.append(movieName)
    httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
    response = requests.get(httpRequest)
    data = response.json()
    likeMovieOverViews.append(data["results"][0]["overview"])

  elif(type=="Never"):
    neverSeenNames.append(movieName)
    httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
    response = requests.get(httpRequest)
    data = response.json()
    neverSeenOverview.append(data["results"][0]["overview"])
  else:
    hateMovieNames.append(movieName)
    httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
    response = requests.get(httpRequest)
    data = response.json()
    hateMovieOverViews.append(data["results"][0]["overview"])




print("Enter names of movies you LIKE")
times = int(input("How many movies would you like to enter: "))
for i in range(times):
  enterData("Like")
print("You LIKE: " + str(likeMovieNames))

print()
print("Enter names of movies you HATE/DISLIKE")
times = int(input("How many movies would you like to enter: "))
for i in range(times):
  enterData("Hate")
print("You DISLIKE: " + str(hateMovieNames))

print()
print("Enter names of movies you NEVER SEEN")
times = int(input("How many movies would you like to enter: "))
for i in range(times):
  enterData()
print("You NEVER SEEN: " + str(neverSeenNames))
print()
training_texts = likeMovieOverViews + hateMovieOverViews


training_labels = ["good"] * len(likeMovieOverViews) + ["bad"] * len(hateMovieOverViews)
vectorizer = CountVectorizer()
vectorizer.fit(training_texts)
training_vectors = vectorizer.transform(training_texts)
test_texts = neverSeenOverview
testing_vectors = vectorizer.transform(test_texts)

classifier = tree.DecisionTreeClassifier()
classifier.fit(training_vectors, training_labels)

Results = classifier.predict(testing_vectors)
print(Results)
for i in range(len(Results)):
  print(neverSeenNames[i] + " is a : [" + str(Results[i]).upper() + "] movie.")

tree.export_graphviz(
    classifier,
    out_file='tree.dot',
    feature_names=vectorizer.get_feature_names(),
    class_names=["good","bad"]

) 

def manual_classify(overview):
  if "one" in overview.lower():
    if "missing" in overview.lower():
      return "BAD Movie"
    else:
      return "GOOD Movie"
  else:
    if "must" in overview.lower():
      if "will" in overview.lower():
        return "BAD Movie"
      else:
        return "GOOD Movie"
    else:
      return "BAD Movie"    

def getOverview(movieName):
  httpRequest = "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&query="+movieName+"&language=en-US&api_key="+APIKey
  response = requests.get(httpRequest)
  data = response.json()
  return str(data["results"][0]["overview"])