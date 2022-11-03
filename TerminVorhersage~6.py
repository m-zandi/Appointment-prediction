import requests
import json
import sys
import datetime
import convertdate
from convertdate import persian
from datetime import timedelta
import calendar
#file excel
# import openpyxl
# import xlrd
#import telegram.parsemode
#test update working
# from datetime import datetime


def main():
    update_id = 1000
    #optimistic numbers
    oDurationSecondEmailPess = 173
    oDurationInverPess = 13
    oDurationVisumPess = 30

    #realistic numbers 
    durationSecondEmailPess = 545
    durationInverPess = 55
    durationVisumPess = 60
                        
    #pessimistic numbers
    pDurationSecondEmailPess = 569
    pDurationInverPess = 79
    pDurationVisumPess = 90

    runMember = []
    demand = []
    usernames = []
    numberUpdate=0
    startApp = datetime.datetime.now()

    while True:
        try:
            # numberUpdate=+1
            updates = get_updates(offset=update_id)
            numberUpdate=numberUpdate+1

            print("numberUpdate = ",numberUpdate)
            now = datetime.datetime.now()
            duration = now - startApp
            print("duration = ",duration)
            updates = updates["result"]
            
            if updates:
                        for item in updates:
                            update_id = item["update_id"]
                            from_ = item["message"]["from"]["id"]
                            try:
                               uName = item["message"]["from"]["username"]
                            except:
                               uName = "first name = "+item["message"]["from"]["first_name"]
                        #        send_message("Members = {}\nDemands = {}\nUsernames = {}\nCurrent User = {}\nMembers ids = {}".format(quantityMember,quantityDemand,usernames,uName,runMember),130405462)

                            
                            
                                  
                                    

                            try:
                                date_entry = item["message"]["text"]
                                
                                    # <b> </b>
                                try:
                                        # counting demand and member
                                        demand.append(from_)
                                        quantityDemand = len(demand)
                                        print("Demands quantity = ",quantityDemand)
                                        # conunting usernames
                                        #print("uName = ",uName)
                                        if uName not in usernames:
                                                usernames.append(uName) 
                                                print("added members usernames = ",usernames)
                                        print("members usernames = ",usernames)


                                        if from_ not in runMember:
                                                runMember.append(from_)
                                                quantityMember = len(runMember)
                                                print("added run Member count = ",quantityMember)
                                                print("added run Members ids = ",runMember)
                                            
                                        print("run Member count = ",quantityMember)
                                        print("run Members ids = ",runMember)
                                        if date_entry =="cherabahk":   
                                                send_message("Members = {}\nDemands = {}".format(quantityMember,quantityDemand),from_)
                                                break
                                        send_message("duration = {}\nnumber Update = {}\nMembers = {}\nDemands = {}\nUsernames = {}\nCurrent User = {}\nMembers ids = {}".format(duration,numberUpdate,quantityMember,quantityDemand,usernames,uName,runMember),130405462)
                                except:
                                        print("conuning and demand problem")
                                if date_entry == "/start":
                                    #print("date_entry input ={}".format(date_entry))
                                    send_message('با درود و سلام مجدد خدمت شما دوست عزیز🌸🌺 \n خواهشمندم تاریخ ایمیل اول دریافت شده خود را توسط سفارت آلمان به میلادی مانند ساختار گفته شده وارد کنید \n   DD-MM-YYYY \n نمونه :\n 28-12-2018 ', from_)
                                    break

                                cha = list(date_entry)
                                #print("cha = ", cha)
                                funcLength(cha,from_)
                            except:
                                send_message(" خواهشمندم به میلادی تاریخ ایمیل اول را درست وارد کنید!\n(از ارسال spam خودداری کنید!⛔️)\n \n  Ex: DD-MM-YYYY \n نمونه :\n 28-12-2018 ", from_)
                                #send_message("خواهشمندم تاریخ ایمیل اول را درست وارد کنید!\n \n  Ex: DD-MM-YYYY", from_)
                                break 
                            try:
                                #print(cha)
                                xDay,xMonth,xYear= map(int, date_entry.split("-"))
                                
                            except:
                                date_entry = None
                                from_ = item["message"]["from"]["id"]
                                send_message("خواهشمندم از - بین سال , ماه , روز استفاده کنید! Ex:DD-MM-YYYY",from_)
                                # send_message("خواهشمندم تاریخ ایمیل اول را درست وارد کنید!\n first\n  Ex: DD-MM-YYYY", from_)

                            try:
                                        yearInt(xYear,from_)
                                        #yearDashMont(cha[4],from_)
                                        monthInt(xMonth,from_)
                                        #monthDashDay(cha[7],from_)
                                        dayInt(xDay,from_)
                                        
                                        day, month, year = map(int, date_entry.split("-"))
                                        firstEmail = datetime.date(year,month,day)
                                        # print("firstEmail =",firstEmail)
                                        cO= calculateOptimistic(firstEmail,oDurationSecondEmailPess,oDurationInverPess,oDurationVisumPess,from_) 
                                        #print("cO =",cO)
                                        cR= calculate(firstEmail,durationSecondEmailPess,durationInverPess,durationVisumPess,from_)
                                        #print("cR =",cR)
                                        cP= calculatePessimistic(firstEmail,pDurationSecondEmailPess,pDurationInverPess,pDurationVisumPess,from_)
                                        # print("cP = ",cP)
                                        calculateSum(firstEmail,cO,cR,cP,todayTimeDate(),from_)
                            except:
                                        print("got a some issue")
                                        #send_message("خواهشمندم تاریخ ایمیل اول را درست وارد کنید!\n \n  Ex: DD-MM-YYYY", from_)
                           
        except:
            print("resualt error")


# def send_message( msg,parse_mode, chat_id):
def send_message( msg, chat_id):
        #m…m token
        
        # token = "156154229:AAEProZDOrv2JXgMQBYq4E6AV8JJ8F26Lb0"
        #dana termin vorhersage
        token = "765228612:AAGDhNQOXDq3QmJu2d3gv3yVM8fQwjb4jDo"
        
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(token,chat_id, msg)
        # print("url = {}".format(url))
        if msg is not None:
            requests.get(url)

        



def get_updates(offset=None):
        #m...m token
        # token = "156154229:AAEProZDOrv2JXgMQBYq4E6AV8JJ8F26Lb0"
        #dana termin vorhersage
        token = "765228612:AAGDhNQOXDq3QmJu2d3gv3yVM8fQwjb4jDo"
        
        url = "https://api.telegram.org/bot{}/getUpdates?timeout=2&".format(token)
        if offset:
                url = url + "&offset={}".format(offset + 1)
                # print("numberUpdate = ",numberUpdate)
                now = datetime.datetime.now()
                print("now = ",now)
                # duration = now - startApp
                # print("duration = ",duration)
                
                # print("url = {}".format(url))
        try:
            r = requests.get(url)
            return json.loads(r.content)
        except:
            print("we've company on internat connection")

#Cristian functions
def seprateDate(argument):
        argumentStr = str(argument)
        year, month, day = map(int, argumentStr.split("-"))
        monthName = monthNumToAlpha(month)
        x = str("{}-{}-{}".format(day,monthName,year))
        
        return x

#Cristian functions today
def seprateDateToday(argument):
        argumentStr = str(argument)
        year, month, day = map(int, argumentStr.split("-"))
        monthName = monthNumToAlpha(month)
        x = str("{}-{}-{}".format(day,monthName,year))
        return x

def monthNumToAlpha(argument): 
        switcher = { 
            1: "January", 
            2: "February", 
            3: "March", 
            4: "April", 
            5: "May", 
            6: "June", 
            7: "July", 
            8: "Agust", 
            9: "September", 
            10: "October", 
            11: "November", 
            12: "December", 
            } 
        return switcher.get(argument, "nothing") 

#  shamsi fuctions
def seprateDateSh(argument):
        argumentStr1 = str(argument)
        print(f"argumentStr1 = {argumentStr1}")
        argumentStr = argumentStr1.replace("(","")
        argumentStr = argumentStr.replace(")","")
        print(f"argumentStr = {argumentStr}")
        year, month, day = map(int, argumentStr.split(","))
        monthName = monthNumToShamAlpha(month)
        return "{}-{}-{}".format(day,monthName,year)

def monthNumToShamAlpha(argument): 
        switcher = { 
            1: "فروردین", 
            2: "اردیبهشت", 
            3: "خرداد", 
            4: "تیر", 
            5: "مرداد", 
            6: "شهریور", 
            7: "مهر", 
            8: "آبان", 
            9: "آذر", 
            10: "دی", 
            11: "بهمن", 
            12: "اسفند", 
            } 
        return switcher.get(argument, "nothing") 


#optimistic prediction
def calculateOptimistic(f,dSec,dInter,dVis,from_):
      secondEmailPess = f + timedelta(days=dSec)
    #   print("secondEmailPess : ",secondEmailPess)
      interviewPess = secondEmailPess + timedelta(days=dInter)
    #   print("interviewPess : ",interviewPess)
      visumPess = interviewPess + timedelta(days=dVis)
    #   print("visumPess : ",visumPess)
      shCalOp = convertToshamsi(secondEmailPess,interviewPess,visumPess)
      
      op=" ️🗓پیش بینی زمان ها به صورت🗓\n                  😌((خوشبینانه))\n\n ایمیل دوم :   {}\n            {} \n\n مصاحبه   :    {}\n            {}\n\n ویزا          :    {}\n            {}".format(shCalOp[0],seprateDate(secondEmailPess),shCalOp[1],seprateDate(interviewPess),shCalOp[2],seprateDate(visumPess))
      #print("op = ",op)
      return op
      

#realistic prediction
def calculate(f,dSec,dInter,dVis,from_):
      secondEmailPess = f + timedelta(days=dSec)
      interviewPess = secondEmailPess + timedelta(days=dInter)
      visumPess = interviewPess + timedelta(days=dVis)
      shCalReal = convertToshamsi(secondEmailPess,interviewPess,visumPess)
      rp = "     🗓پیش بینی زمان ها به صورت🗓\n                  😐((واقع بینانه))\n\n ایمیل دوم :   {}\n            {} \n\n مصاحبه   :   {}\n            {}\n\n ویزا          :    {}\n            {}".format(shCalReal[0],seprateDate(secondEmailPess),shCalReal[1],seprateDate(interviewPess),shCalReal[2],seprateDate(visumPess))
      
      return rp
      
 #pessimistic prediction
def calculatePessimistic(f,dSec,dInter,dVis,from_):
      secondEmailPess = f + timedelta(days=dSec)
      interviewPess = secondEmailPess + timedelta(days=dInter)
      visumPess = interviewPess + timedelta(days=dVis)
      shCalPess = convertToshamsi(secondEmailPess,interviewPess,visumPess)
      cp="     🗓پیش بینی زمان ها به صورت🗓\n                  ☹️((بدبینانه))\n\n ایمیل دوم :   {}\n            {} \n\n مصاحبه   :    {}\n            {}\n\n ویزا          :    {}\n            {} \n\n 📈📉🗒▫️▫️▫️▫️▫️▫️▫️▫️".format(shCalPess[0],seprateDate(secondEmailPess),shCalPess[1],seprateDate(interviewPess),shCalPess[2],seprateDate(visumPess))
      return cp


#convert date to shamsi
def dateConvertToShamsi(fe):
        dateInput =str(fe)
        a,b,c=map(int, dateInput.split("-"))
        # print("a = {},b = {},c = {}".format(a,b,c))
        shDate=convertdate.persian.from_gregorian(a,b,c)
        return shDate





 #convert to shamsi
def convertToshamsi(secEm,interPass,visPess):
        secEm =str(secEm)
        a,b,c=map(int, secEm.split("-"))
        # print("a = {},b = {},c = {}".format(a,b,c))
        shSecondEmail=convertdate.persian.from_gregorian(a,b,c)
        # print("shSecondEmail = ",shSecondEmail)
        interPass= str(interPass)
        d,e,f= map(int, interPass.split("-"))
        shInterviewPess=convertdate.persian.from_gregorian(d,e,f)
        # print("shInterviewPess = ",shInterviewPess)
        visPess=str(visPess)
        g,h,i= map(int, visPess.split("-"))
        shaVisumPess=convertdate.persian.from_gregorian(g,h,i)
        # print("shaVisumPess = ",shaVisumPess)
        h= [seprateDateSh(shSecondEmail),seprateDateSh(shInterviewPess),seprateDateSh(shaVisumPess)]
        return h
       

 
        
 #realistic optimistic pessimistic prediction 
def calculateSum(fe,cO,cR,cP,todayTimeDate,from_):
      feAl = seprateDate(fe)
      shFiEm = dateConvertToShamsi(fe)
      shFiEmAlpha = seprateDateSh(shFiEm)
      lineA = "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️"
      lineB = "⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️⚪️"
      send_message("👩‍🎓👨‍🎓\n📧ایمیل اول : {} \n                       {}\n {} \n {} \n {} \n {} \n {} \n{} \n {} \n @TerminVorhersage_bot \n @DeutschOhal ".format(shFiEmAlpha,feAl,lineA,cO,lineB,cR,lineB,cP,todayTimeDate),from_)


def funcLength(x,from_):
            z = len(x)
            # print("x value funcLenght = {}".format(z))
            if int(x[0]+x[6]+x[7]) == False :
                  
                  return 2/0
            elif 7<z < 11:
                  return True
            else:
                send_message('خواهشمندم به میلادی تاریخ ایمیل اول خود را مانند ساختار گفته شده وارد کنید! \n   DD-MM-YYYY \n نمونه :\n 2018-12-28   ', from_)



# def yearDashMont(x,from_):
#       if x == "-":
#           return True
#       else :
#             send_message("خواهشمندم از - بین سال و ماه استفاده کنید! Ex:YYYY-MM",from_)
#             return False

def monthDashDay(x,from_):
      if x == "-":
          #print("here year dash mount x = {}".format(x))
          return True
      else :
            send_message("خواهشمندم از - بین ماه و روز استفاده کنید! Ex:DD-MM ",from_)
            return False

# def yearDuration(x,from_):
#          if 2016 >x or x> 2022:
#               return False
#              send_message("خواهشمندم سال ایمیل را درست وارد کنید!",from_)

       
            
   
             

def yearInt(y,from_):
          if 2016 >y or y> 2022:
                send_message("خواهشمندم سال ایمیل را درست وارد کنید!",from_)
                return False


    



def monthDuration(x,from_):
      if x<1 or x>12:
            send_message("خواهشمندم ماه ایمیل را درست وارد کنید!",from_)



def dayDuration(x,from_):
      if x<1 or x>31:
            send_message("خواهشمندم روز ایمیل را درست وارد کنید!",from_)



def dayInt(x,from_):
      try:
         x=int(x)
         dayDuration(x,from_)
         return True 
      except:
        send_message("خواهشمندم روز ایمیل را درست وارد کنید! Ex: 23",from_)



def monthInt(x,from_):
      try:
         x=int(x)
         monthDuration(x,from_)
         return True
      except:
         send_message("خواهشمندم ماه را مانند نمونه گفته شده وارد کنید! Ex: 09",from_)


# def memberIn(i,_from):
#     arrayMemIn=[_from]
#     i = 1

def todayTimeDate():
            # today time and date
            nowDateTime = datetime.datetime.now()
            todayYear = nowDateTime.year
            todayMonth = nowDateTime.month
            todayDay = nowDateTime.day
            
            
            todayHour = nowDateTime.hour
            todayMinute = nowDateTime.minute
            todaySecond = nowDateTime.second
            nowDate = str("{}-{}-{}".format(todayYear,todayMonth,todayDay))
            nowTime = str("{}:{}:{}".format(todayHour,todayMinute,todaySecond))
            born = datetime.datetime.strptime(nowDate, '%Y-%m-%d').weekday() 
            weekDay = (calendar.day_name[born]) 
            # print(weekDay)
            # print(weeksDayFunc(weekDay))
            nowDateAlpha = seprateDate(nowDate)
            nowDateConvertedShamsi = dateConvertToShamsi(nowDate)
            nowDateAlphaSh = seprateDateSh(nowDateConvertedShamsi)
            todayOutput = "🗓🕰امروز : {}\n {}                          {}\n{}".format(weeksDayFunc(weekDay),nowTime,nowDateAlpha,nowDateAlphaSh)
            return todayOutput

def weeksDayFunc(weekDay):
        switcher = {
            "Saturday": "شنبه", 
            "Sunday": "یکشنبه",
            "Monday": "دوشنبه", 
            "Tuesday": "سه شنبه", 
            "Wednesday": "چهارشنبه", 
            "Thursday": "پنج شنبه", 
            "Friday": "جمعه"
            } 
        return switcher.get(weekDay, "nothing") 

if __name__ == '__main__':
  main()


#success




