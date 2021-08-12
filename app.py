from flask import Flask
import requests
from bs4 import BeautifulSoup
import json
app = Flask(__name__)
#cron scheduler
#* * * * * cd Desktop && /usr/bin/python3.5 webscrap.py >> test.out
link = None
link = input("Enter match link  :")
selected = []
i=0
#for x in range(11):
#    if i ==0 :
#        val = input("Enter captains name  :")
#    elif i == 1:
#        val = input("Enter Vice captains name  :")
#    else:
#        val = input("Enter players name  :")
    #selected[i] = " "+val+" "
#    selected.insert(i," "+val+" ")
#    i=i+1

#selected = [' Babar Azam ',' Ben Stokes ',' Zak Crawley ',' Fakhar Zaman ',' Mohammed Rizwan ',' Dawid Malan ',' Shaheen Afridi ',' Saqib Mahmood ',' Shadab Khan ',' Matthew Parkinson ',' Sohaib Maqsood ']
selected_points = [4,4,4,4,4,4,4,4,4,4,4]

@app.route('/', methods = ['GET','POST'])
def index():
    return "Welcome to Dream11 fantasy point API"

@app.route('/get_input',methods =['GET','POST'])
def get():
    i=0
    for x in range(11):
        if i ==0 :
            val = input("Enter captains name  :")
        elif i == 1:
            val = input("Enter Vice captains name  :")
        else:
            val = input("Enter players name  :")
        #selected[i] = " "+val+" "
        selected.insert(i," "+val+" ")
        i=i+1
    return "Selected Playing11 Aquired"

@app.route('/batting_point',methods =['GET','POST'])
def batting():
    #res = requests.get('https://www.cricbuzz.com/live-cricket-scorecard/32027/eng-vs-pak-1st-odi-pakistan-tour-of-england-2021')
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    score = soup.find_all('div', class_  = 'cb-col cb-col-100 cb-scrd-itms')



    #store name in list
    name = []
    i=0
    for x in score:
        fname = score[i]
        if fname.div.text == 'Extras' or fname.div.text == 'Total' or fname.div.text ==' Did not Bat ':
            i=i+1;
            continue
        else:
            name.append(fname.a.text)
        i=i+1


    #find bowled or lbw
    out = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='text-gray'):
            out.append(tag.next)
            i=i+1
        j=j+1



    #store runs in list
    runs = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='cb-col cb-col-8 text-right text-bold'):
            runs.append(tag.text)
            i = i+1
        j = j+1


    # store fours and six in list
    srate = []
    boundary = []
    six =[];
    balls = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='cb-col cb-col-8 text-right'):
            if i==0:
                balls.append(tag.text)
            if i==3:
                srate.append(tag.text)
            if i== 1:
                boundary.append(tag.text)
            if i==2:
                six.append(tag.text)
            i=i+1
        j=j+1


    #strike rate calculation
    additional = []
    i=0
    for x in srate:
        if float(x) > 140 and float(balls[i])>=20:
            additional.append(6)
        elif float(x) >120 and float(x) <=140 and float(balls[i])>=20:
            additional.append(4)
        elif float(x) >= 100 and float(x)<=120 and float(balls[i])>=20:
            additional.append(2)
        elif float(x) >=40  and float(x)<=50 and float(balls[i])>=20:
            additional.append(-2)
        elif float(x)>=30 and float(x)<40 and float(balls[i])>=20:
            additional.append(-4)
        elif float(x)<30 and float(balls[i])>=20:
            additional.append(-6)
        else:
            additional.append(0)






    #total points calculation
    total =[]
    i=0
    l = len(six)
    for x in range(l):
        if int(runs[i]) >= 100:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+additional[i] + 8 )
        elif int(runs[i]) >= 50:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+ additional[i]+ 4 )
        else:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+additional[i])
        if(total[i] == 0):
            total[i] = -3
        i=i+1



    batting_point = dict()
    i=0
    for x in name:
        batting_point[x] = total[i]
        i=i+1

    json_data = json.dumps(batting_point)
    return json_data


@app.route('/bowling_point',methods=['GET','POST'])
def bowling():
    #res = requests.get('https://www.cricbuzz.com/live-cricket-scorecard/32027/eng-vs-pak-1st-odi-pakistan-tour-of-england-2021')
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    score = soup.find_all('div', class_  = 'cb-col cb-col-100 cb-scrd-itms')
    bowl = soup.find_all('div',class_='cb-col cb-col-100 cb-scrd-itms ')

    #bowler name list
    bname = []
    i=0
    for x in bowl:
        fname = bowl[i]
        bname.append(fname.a.text)
        i = i +1

    #find bowled or lbw
    out = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='text-gray'):
            out.append(tag.next)
            i=i+1
        j=j+1

    #maiden list
    maiden = []
    j = 0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-8 text-right'):
            if i == 1:
                maiden.append(tag.text)
            i = i+1
        j = j +1

    #wickets list
    wicket = []
    j=0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-8 text-right text-bold'):
            wicket.append(tag.next)
            i = i+1
        j = j+1

    #economy rate
    erate = []
    j=0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-10 text-right'):
            if i==1:
                erate.append(tag.text)
            i = i+1
        j = j+1


    additional1 = []
    i=0
    for x in erate:
        if float(x) < 2.5:
            additional1.append(6)
        elif float(x)>= 2.5 and float(x)<=3.49:
            additional1.append(4)
        elif float(x)>=3.5 and float(x)<=4.5:
            additional1.append(2)
        elif float(x)>= 8.01 and float(x)<=9:
            additional1.append(-4)
        elif float(x)>9:
            additional1.append(-6)
        else:
            additional1.append(0)

    #bowling points calculation
    bpoint = []
    i=0
    for x in bowl:
        if int(wicket[i]) == 4:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 +4 + additional1[i])
        elif int(wicket[i]) >= 5:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 +8 + additional1[i] )
        else:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 + additional1[i] )
        i = i+1


    #separate bowled and lbw and catch name
    lbw = []
    catch = []
    for x in out:
        s = x
        if s[0] == 'l':
            str = s.split(' ')
            l =len(str)
            if l == 4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == ' ':
            str = s.split(' ')
            l = len(str)
            if l==4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == 'c':
            str = s.split(' ')
            l = len(str)
            if l==6:
                var = " "+str[1]+" "+str[2]+" "
                catch.append(var)
            elif l==4:
                var = " "+str[1]
                catch.append(var)
            elif l==5:
                var = " "+str[1]
                if(str[2]!='b'):
                    var = var+str[2]+" "
                catch.append(var)

    #add lbw/bowled bonus
    for x in lbw:
        i = 0
        for y in bname:
            if(x == y):
                bpoint[i] = bpoint[i] + 8
            i = i+1



    bowling_point = dict()
    i=0
    for x in bname:
        bowling_point[x] = bpoint[i]
        i=i+1

    json_data = json.dumps(bowling_point)
    return json_data

@app.route('/fielding_point',methods=['GET','POST'])
def fielding():
    #res = requests.get('https://www.cricbuzz.com/live-cricket-scorecard/32027/eng-vs-pak-1st-odi-pakistan-tour-of-england-2021')
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    score = soup.find_all('div', class_  = 'cb-col cb-col-100 cb-scrd-itms')

    #find bowled or lbw
    out = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='text-gray'):
            out.append(tag.next)
            i=i+1
        j=j+1

    #separate bowled and lbw and catch name
    lbw = []
    catch = []
    for x in out:
        s = x
        if s[0] == 'l':
            str = s.split(' ')
            l =len(str)
            if l == 4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == ' ':
            str = s.split(' ')
            l = len(str)
            if l==4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == 'c':
            str = s.split(' ')
            l = len(str)
            if l==6:
                var = " "+str[1]+" "+str[2]+" "
                catch.append(var)
            elif l==4:
                var = " "+str[1]
                catch.append(var)
            elif l==5:
                var = " "+str[1]
                if(str[2]!='b'):
                    var = var+str[2]+" "
                catch.append(var)

    #we store name and no of catches by a player
    count = dict()
    l = len(catch)
    for i in range(l):
        if catch[i] in count.keys():
            count[catch[i]]+=1
        else:
            count[catch[i]] = 1


    #fielld point calculation
    fpoint = []
    for x in count:
        if count[x] >= 3:
            fpoint.append(count[x]*8 + 4)
            continue
        fpoint.append(count[x]*8)



    fielding_point = dict()
    i=0
    for x in count:
        fielding_point[x] = fpoint[i]
        i=i+1

    json_data = json.dumps(fielding_point)
    return json_data


@app.route('/fantasy_point',methods=['GET','POST'])
def fantasy():
    #res = requests.get('https://www.cricbuzz.com/live-cricket-scorecard/32027/eng-vs-pak-1st-odi-pakistan-tour-of-england-2021')
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    score = soup.find_all('div', class_  = 'cb-col cb-col-100 cb-scrd-itms')



    #store name in list
    name = []
    i=0
    for x in score:
        fname = score[i]
        if fname.div.text == 'Extras' or fname.div.text == 'Total' or fname.div.text ==' Did not Bat ':
            i=i+1;
            continue
        else:
            name.append(fname.a.text)
        i=i+1


    #find bowled or lbw
    out = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='text-gray'):
            out.append(tag.next)
            i=i+1
        j=j+1



    #store runs in list
    runs = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='cb-col cb-col-8 text-right text-bold'):
            runs.append(tag.text)
            i = i+1
        j = j+1


    # store fours and six in list
    srate = []
    boundary = []
    six =[];
    balls = []
    j=0
    for x in score:
        i=0
        for tag in score[j].find_all(class_='cb-col cb-col-8 text-right'):
            if i==0:
                balls.append(tag.text)
            if i==3:
                srate.append(tag.text)
            if i== 1:
                boundary.append(tag.text)
            if i==2:
                six.append(tag.text)
            i=i+1
        j=j+1


    #strike rate calculation
    additional = []
    i=0
    for x in srate:
        if float(x) > 140 and float(balls[i])>=20:
            additional.append(6)
        elif float(x) >120 and float(x) <=140 and float(balls[i])>=20:
            additional.append(4)
        elif float(x) >= 100 and float(x)<=120 and float(balls[i])>=20:
            additional.append(2)
        elif float(x) >=40  and float(x)<=50 and float(balls[i])>=20:
            additional.append(-2)
        elif float(x)>=30 and float(x)<40 and float(balls[i])>=20:
            additional.append(-4)
        elif float(x)<30 and float(balls[i])>=20:
            additional.append(-6)
        else:
            additional.append(0)






    #total points calculation
    total =[]
    i=0
    l = len(six)
    for x in range(l):
        if int(runs[i]) >= 100:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+additional[i] + 8 )
        elif int(runs[i]) >= 50:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+ additional[i]+ 4 )
        else:
            total.append(int(boundary[i])+(int(six[i])*2) + int(runs[i])+additional[i])
        if(total[i] == 0):
            total[i] = -3
        i=i+1



    bowl = soup.find_all('div',class_='cb-col cb-col-100 cb-scrd-itms ')

    #bowler name list
    bname = []
    i=0
    for x in bowl:
        fname = bowl[i]
        bname.append(fname.a.text)
        i = i +1


    #maiden list
    maiden = []
    j = 0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-8 text-right'):
            if i == 1:
                maiden.append(tag.text)
            i = i+1
        j = j +1

    #wickets list
    wicket = []
    j=0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-8 text-right text-bold'):
            wicket.append(tag.next)
            i = i+1
        j = j+1

    #economy rate
    erate = []
    j=0
    for x in bowl:
        i=0
        for tag in bowl[j].find_all(class_='cb-col cb-col-10 text-right'):
            if i==1:
                erate.append(tag.text)
            i = i+1
        j = j+1


    additional1 = []
    i=0
    for x in erate:
        if float(x) < 2.5:
            additional1.append(6)
        elif float(x)>= 2.5 and float(x)<=3.49:
            additional1.append(4)
        elif float(x)>=3.5 and float(x)<=4.5:
            additional1.append(2)
        elif float(x)>= 8.01 and float(x)<=9:
            additional1.append(-4)
        elif float(x)>9:
            additional1.append(-6)
        else:
            additional1.append(0)

    #bowling points calculation
    bpoint = []
    i=0
    for x in bowl:
        if int(wicket[i]) == 4:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 +4 + additional1[i])
        elif int(wicket[i]) >= 5:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 +8 + additional1[i] )
        else:
            bpoint.append(int(wicket[i])*25 + int(maiden[i])*4 + additional1[i] )
        i = i+1



    #separate bowled and lbw and catch name
    lbw = []
    catch = []
    for x in out:
        s = x
        if s[0] == 'l':
            str = s.split(' ')
            l =len(str)
            if l == 4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == ' ':
            str = s.split(' ')
            l = len(str)
            if l==4:
                var = " "+str[2]+" "+str[3]+" "
                lbw.append(var)
            elif l==3:
                var = str[2]+" "
                lbw.append(var)
        if s[0] == 'c':
            str = s.split(' ')
            l = len(str)
            if l==6:
                var = " "+str[1]+" "+str[2]+" "
                catch.append(var)
            elif l==4:
                var = " "+str[1]
                catch.append(var)
            elif l==5:
                var = " "+str[1]
                if(str[2]!='b'):
                    var = var+str[2]+" "
                catch.append(var)

    #add lbw/bowled bonus
    for x in lbw:
        i = 0
        for y in bname:
            if(x == y):
                bpoint[i] = bpoint[i] + 8
            i = i+1


    #we store name and no of catches by a player
    count = dict()
    l = len(catch)
    for i in range(l):
        if catch[i] in count.keys():
            count[catch[i]]+=1
        else:
            count[catch[i]] = 1


    #fielld point calculation
    fpoint = []
    for x in count:
        if count[x] >= 3:
            fpoint.append(count[x]*8 + 4)
            continue
        fpoint.append(count[x]*8)





    #user selected 11 players and their initial points
    #selected = [' Babar Azam ',' Ben Stokes ',' Zak Crawley ',' Fakhar Zaman ',' Mohammed Rizwan ',' Dawid Malan ',' Shaheen Afridi ',' Saqib Mahmood ',' Shadab Khan ',' Matthew Parkinson ',' Sohaib Maqsood ']
    #selected_points = [4,4,4,4,4,4,4,4,4,4,4]

    # adding batting points to selected_points
    j=0
    for x in selected:
        i=0
        for y in name:
            if (y.find(x) != -1):
                selected_points[j] = selected_points[j]+total[i]
            elif (x.find(y) != -1):
                selected_points[j] = selected_points[j]+total[i]
            else:
                q = y
                str = q.split(' ')
                l = len(str)
                if l == 4:
                    k = str[1]+" "
                    if (x.find(k)!=-1 and (str[2]=='(wk)' or str[2] =='(c)')):
                        selected_points[j] = selected_points[j] + total[i]
            i=i+1
        j=j+1


    #adding bowling poin to selected_points
    j=0
    for x in selected:
        i=0
        for y in bname:
            if (y.find(x) != -1):
                selected_points[j] = selected_points[j] + bpoint[i]
            elif (x.find(y)!=-1):
                selected_points[j] = selected_points[j] + bpoint[i]
            else:
                q=y
                str=q.split(' ')
                l=len(str)
                if l==4:
                    k = str[1]+" "
                    if(x.find(k)!=-1 and (str[2]=='(wk)' or str[2]=='(c)')):
                        selected_points[j] = selected_points[j]+total[i]
            i=i+1
        j=j+1


    #adding fielding points to the selected_points
    j=0
    for x in selected:
        i=0
        for y in count:
            if (y.find(x)!=-1):
                selected_points[j]= selected_points[j]+ fpoint[i]
            elif (x.find(y)!=-1):
                selected_points[j]=selected_points[j]+fpoint[i]
            i=i+1
        j = j+1




    #i=0
    #for x in selected:
    #    print(x,selected_points[i])
    #    i=i+1

    sum =0
    for x in selected_points:
        sum = sum + x


    #print('\n')
    #print("Total Points earned by USER  :",sum)

    #print('\n')

    answer = dict()
    i=0
    for x in selected:
        answer[x] = selected_points[i]
        i=i+1

    answer["Total Points earned by User"]= sum

    json_data3 = json.dumps(answer)
    return json_data3
    #for x in bpoint:
    #    print(x)

if __name__ =="__main__":
    app.run(debug=True)
