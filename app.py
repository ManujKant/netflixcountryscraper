from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/countries", methods = ['POST'])
def countries():
    if request.method == "POST":
        item = request.form["media_name"]
        countries = []
        listedItem = [character.lower() for character in item]

        punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''

        for char in punctuations:
            if char in listedItem:
                listedItem.remove(char)

        item = "".join(listedItem)
        item = item.split(" ")
        item = "-".join(item)

        try:
            source = requests.get(f"https://www.flixwatch.co/tvshows/{item}/").text
            soup = BeautifulSoup(source, "lxml")
            countryBox = soup.find("div", class_ = "country-box").p
            for country in countryBox.find_all("a"):
                countries.append(country.text)
        except:
            try:
                source = requests.get(f"https://www.flixwatch.co/movies/{item}/").text
                soup = BeautifulSoup(source, "lxml")
                countryBox = soup.find("div", class_ = "country-box").p
                for country in countryBox.find_all("a"):
                    countries.append(country.text)
            except:
                countries = False

        nordVPN = ["USA", "Canada", "Germany", "UK", "France", "Italy", "Japan", "Australia", "Netherlands", "Spain", "India", "Brazil", "South Korea", "Finland"]
        if countries != False:
            countriesNordVPN = [country for country in nordVPN if country in countries]
        else:
            countriesNordVPN = False

        if countries and countriesNordVPN != False:
            countries = " ".join(countries)
            countriesNordVPN = " ".join(countriesNordVPN)

        if countries and countriesNordVPN != False:
            return render_template("countries.html", countries=countries, countriesNordVPN=countriesNordVPN)
        else:
            return render_template("nonexistent.html")




if __name__ == "__main__":
    app.debug = True
    app.run(port="5037")
