from bs4 import BeautifulSoup
import requests
import json

def getNYTPuzzles():
    nyt_link = "https://www.nytimes.com/puzzles/sudoku/hard"

    try:
        nyt_request = requests.get(nyt_link)
        if(nyt_request.ok):
            soup = BeautifulSoup(nyt_request.content, "html.parser")

            key = soup.findAll("script", {"type": "text/javascript"})

            gameData = ""
            for i in key:
                if "window.gameData = " in i.text:
                    gameData = i.text.replace("window.gameData = ", "")

            gameData = json.loads(gameData)

            hard = ("".join([str(i) for i in gameData["hard"]["puzzle_data"]["puzzle"]]))
            medium = ("".join([str(i) for i in gameData["medium"]["puzzle_data"]["puzzle"]]))
            easy = ("".join([str(i) for i in gameData["easy"]["puzzle_data"]["puzzle"]]))

            return (hard, medium, easy)
        else:
            return ()
    except requests.exceptions.RequestException as e:
        return ()