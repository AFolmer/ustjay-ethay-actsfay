import os

import requests
from flask import Flask, request, redirect, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("https://random-simile-generator.herokuapp.com/")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("h1")

    # Inspecting RSG site shows that simile is second h1 element
    return facts[1].getText()


def pig_latinize(fact):
    url = "https://pig-latinizer.herokuapp.com/piglatinize"
    data = {'input_text': fact}
    try:
        response = requests.post(url, data=data, allow_redirects=True)
        response.raise_for_status()

        # Get the redirect url
        pig_latin_url = response.url

        # Get the body of the page I'm redirected to and filter to simile in pig latin
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body')
        pig_latin_response = ''
        for element in body.find_all(text=True):
            if element.parent.name not in ['h1', 'h2', 'h3']:
                pig_latin_response += str(element).strip().replace('"', '')
        return pig_latin_response, pig_latin_url

    except requests.exceptions.RequestException as e:
        return f'Error: {e}'


@app.route('/')
def home():
    fact = get_fact()
    pig_latin_fact, pig_latin_url = pig_latinize(fact)
    return render_template('home.html', fact=fact, pig_latin_fact=pig_latin_fact,
                           pig_latin_url=pig_latin_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
