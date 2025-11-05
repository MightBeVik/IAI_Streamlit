import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd


st.title("Web Scraping App")

url = requests.get(f'https://www.scrapethissite.com/pages/forms/').text
soup = BeautifulSoup(url, 'lxml')

players = soup.find_all('tr')

#st.write(players)
players = soup.find_all('tr')[1:]

#st.write([players[0]])
team_name = []
year_number = []
wins_number = []

for player in players:
    name = player.find_all('td')[0].text.strip()
    year = player.find_all('td')[1].text.strip()
    wins = player.find_all('td')[2].text.strip()
    team_name.append(name)
    year_number.append(year)
    wins_number.append(wins)

data = pd.DataFrame({
    'Team Name': team_name,
    'Year': year,
    'Wins': wins
})

#st.dataframe(data)
st.table(data)

