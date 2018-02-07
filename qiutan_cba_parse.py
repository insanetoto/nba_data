'''
 球探网数据解析
'''
from bs4 import BeautifulSoup
import re
import requests

output = open('cba_score.csv', 'a')
header='时间,主队,客队,主队得分,客队得分,上半场主队得分,上半场客队得分,让分,总分盘\n'
# output.write(header)

html = requests.get('http://nba.win007.com/jsData/matchResult/17-18/l5_1_2018_1.js').content
html_doc = str(html,'utf-8')
line_list=[]
team_dic={}
record_dic={}
for line in html_doc.split(';'):
    line_list.append(line)
#联赛名称
league_name = line_list[0][line_list[0].find('['):].strip('[').strip(']').split(',')[1].strip('\'')
#队伍名称
line_team = line_list[1][line_list[1].find('[')+1:-1]
team_name_list = re.findall("(\[.*?\])",line_team)
for team_name in team_name_list:
    team=[]
    for i in  team_name.strip('[').strip(']').split(','):
        team.append(i)
    team_dic[team[0]]=team[1]
line_score = line_list[4][line_list[4].find('[')+1:-1]
score_list = re.findall("(\[.*?\])",line_score)
for score_record in score_list:
    score=[]
    for i  in score_record.strip('[').strip(']').split(','):
        score.append(i)
    time = score[2].strip('\'')
    team1=team_dic[score[3]].strip('\'')
    team2=team_dic[score[4]].strip('\'')
    score1=score[5]
    score2=score[6]
    half_score1=score[7]
    half_score2=score[8]
    socre_spread=score[10]
    pro_total_score=score[11]

    wirte_line=time+','+team1+','+team2+','+score1+','+score2+','+half_score1+','+half_score2+','+socre_spread+','+pro_total_score+'\n'
    output.write(wirte_line)
output.close()