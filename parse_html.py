'''
    解析nba数据
'''
from bs4 import BeautifulSoup
import re

output = open('nba_score.csv', 'w+')
header='星期 ,日期,队伍1,让分,预期胜率,得分,队伍2,让分2,预期胜率,得分2\n'
output.write(header)

soup = BeautifulSoup(open('1.html'),"lxml")
sections=soup.find_all('section',{'day complete week-ahead shown','day complete shown'})
for section in sections:
    time = section.h3.get_text()
    for table in section.find_all('table'):   
        team1=''
        team2=''
        number_spread1='0'
        number_spread2='0'
        number_chance1=0.00
        number_chance2=0.00
        score1=0
        score2=0
        team_mark=0
        number_spread_mark=0
        number_chance_mark=0
        score_mark=0
        for tr in table.find_all('tr'):
            if(tr.find(name='td',attrs={'class' :re.compile('^td text team')})):
                team=tr.find(name='td',attrs={'class' :re.compile('^td text team')}).get_text()
                if(team_mark==0):
                    team1=team
                    team_mark=1
                else:
                    team2=team
                    team_mark=0
            else:
                pass
            if tr.find('td','td number spread'):
                if(number_spread_mark==0):
                    number_spread1=tr.find('td','td number spread').get_text()
                    number_spread_mark=1
                else:
                    number_spread2=tr.find('td','td number spread').get_text()
                    number_spread_mark=0
            else:
                pass
            if tr.find('td','td number chance'):
                if  number_chance_mark==0:
                    number_chance1=float(tr.find('td','td number chance').get_text().strip('%'))/100;
                    number_chance_mark=1
                else:
                    number_chance2=float(tr.find('td','td number chance').get_text().strip('%'))/100;
                    number_chance_mark=0
            else:
                pass
            if(tr.find(name='td',attrs={'class' :re.compile('^td number score')})):
                if(score_mark==0):
                    score1=tr.find(name='td',attrs={'class' :re.compile('^td number score')}).get_text()
                    score_mark=1
                else:
                    score2=tr.find(name='td',attrs={'class' :re.compile('^td number score')}).get_text()
                    score_mark=0
            else:
                pass
        if(number_chance1>0.5):
            team1,team2 = team2,team1
            number_spread1,number_spread2=number_spread2,number_spread1
            number_chance1,number_chance2=number_chance2,number_chance1
            score1,score2=score2,score1
        line = time+','+team1+','+str(number_spread1)+','+str(number_chance1)+','+str(score1)+','+team2+','+str(number_spread2)+','+str(number_chance2)+','+str(score2)+',\n'

        output.write(line)
output.close()
