import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
def get_match_data(date):    
    url = 'https://www.filgoal.com/matches/?date={}'.format(date)
    response  = requests.get(url)
    print("Response Status Code:", response.status_code)  # Check if the request was successful
    print("Response Content:", response.text)  # Print the raw content to debug
    if response.status_code == 200:
        return response.content
    else:
        return none 

today = datetime.now().date()
formateddate = today.strftime('%Y-%m-%d')
data = get_match_data(formateddate)
if data:
    soup = BeautifulSoup(data,"html.parser")
    all_matches = []
    league_blocks = soup.find_all("div",class_ = "mc-block")
    for league_block in league_blocks :
        league_name = league_block.find("h6").find("span").text.strip()
        
        for match_info in league_block.find_all("div",class_="cin_cntnr"):
            #print(match_info.prettify())
            if match_info:
                teams = match_info.find_all("strong")
                scores = match_info.find_all('b')
                status = match_info.find('span', class_='status')
                info = match_info.find_all('span')         
                # Ensure that info has enough elements before accessing them
                all_matches.append({             
                    'league' : league_name,
                    'Team1' : teams[0].text.strip() if len(teams) > 0 else '' ,
                    'Score1' : scores[0].text.strip() if len(scores) > 0 else '' ,
                    'Team2' : teams[1].text.strip() if len(teams) > 0 else '' ,
                    'Score2' : scores[1].text.strip() if len(scores) > 0 else '' ,
                    'Status' : status.text.strip() if status else '',
                    'stadium': info[0].text.strip(),            
                    'channel': info[1].text.strip(),
                    'dateTime': info[2].text.strip()
                })

           

    # Create a DataFrame and save to CSV
df = pd.DataFrame(all_matches)
df.to_csv("csv/"+formateddate+'.csv', index=False, encoding='utf-8-sig')
print("Data saved to all_leagues_matches.csv")