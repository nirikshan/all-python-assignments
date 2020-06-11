from datetime import datetime 
import re

# Email is unique if same action is performed in database Primary Key = Email
class EventPlanning:
    def __init__(self):
        self.data = {
            'userStore':[],
            'eventStore':[],
            'bookings':[]
        }
        self.Block = '\n---------------------------------------------------------------------------------------------------------------'


    def RecursiveInput(self , text , InvalidText , condition):
        inputData   = input(text)
        if(condition(inputData)):
            return(inputData)
        else:
            return self.RecursiveInput(InvalidText , InvalidText , condition)


    def TestEmail(self , email):
        if len(email) > 7:
            mainTest = re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email);
            return bool(mainTest)

    def TestName(self , name):
        return len(name) > 1


    def TestUsertype(self , text ):
        return text.upper() == 'ADULT' or text.upper() == 'child'


    def TestReferCode(self , code):
        if not code.isdigit():
            return False
        else:
            code = int(code)
            if(code > 10000):
                return True
            else:
                return False


    def TestDate(self , date_text):
        try:
            return datetime.strptime(date_text, "%Y/%m/%d")
        except ValueError:
            return False


    def TestSeat(self , seats):
        if not seats.isdigit():
            return False
        else:
            seats = int(seats)
            if(seats >= 1):
                return True
            else:
                return False


    def InputUserInfo(self):
        name     = self.RecursiveInput('\n Enter Your Name :'   , '\n Please Enter Your valid Name :' , self.TestName)
        email    = self.RecursiveInput('\n Enter Your Email :' , '\n Please Enter Your valid Email :' , self.TestEmail)
        refcode  = self.RecursiveInput('\n Please Enter Your Refer Code (e.g. 10000) :' , '\n Please Enter valid Refer Code (e.g. 10000) :' , self.TestReferCode)
        usertype = self.RecursiveInput('\n Please Enter User Type (adult / child) :' , '\n Please Enter Your valid User Type (e.g adult/child) :' , self.TestUsertype)
        info = {
                'name':name,
                'email':email,
                'refcode':refcode,
                'usertype':usertype,
                "id":len(self.data['userStore']) + 1
            }
        if not self.isOldUser(email):
            self.data['userStore'].append(info)
            return(info)
        else:
            print('The Email is already used.')
            return(info)


    def GetMyFormatTime(self ):
        return datetime.now().strftime('%Y/%m/%d')


    def TimeDifferents(self , time1 , time2):
        Format = '%Y/%m/%d'
        differ = datetime.strptime(time1, Format) - datetime.strptime(time2, Format)
        min  , secs = divmod(differ.days * 86400 + differ.seconds, 60)
        hour , minutes = divmod(min, 60)
        return({'Hour': hour , 'Minutes': minutes , 'Second':secs })


    def isOldUser(self , email):
        List = self.data['userStore']
        for item in List:
            if email == item['email']:
                return True
        return False



    def EventOrStaff(self):
        eventAgent = input("\n Your are (1 = Event Organizer / 2 = User): ")
        if eventAgent == '1':
            return [1]
        elif eventAgent == '2':
            return [2]
        else:
            return [3 , '\n Invalid Input , Please Supply Valid Input.']


    def isDublicateEvent(self , name , time , User_info):
        List = self.data['eventStore']
        for item in List:
            if name == item['name'] and time == item['time'] and 'email' in item['user'] and item['user']['email'] == User_info['email']:
                return True
        return False


    def ContinueProcess(self , User_info):
        menu = input("\n Do You want to exit ? ( y = Yes / n = No / save = Save All Report) / Any key = login as new user : ")
        if menu.upper() == 'Y':
            return
        elif menu.upper() == 'N':
            InitProgram(User_info)
        elif menu.upper() == 'SAVE':
            fileName = self.RecursiveInput("\n Please enter file name to save Booking and Event report : " , "\n Please enter valid file name to save Booking and Event report : " , self.TestName)
            self.GenerateReport(fileName)
            self.ContinueProcess(User_info)
        else:
            info = event.InputUserInfo()
            InitProgram(info)
        return


    def PrintAllList(self , List , title): 
        print(self.Block)
        print(title.rjust(int(len(self.Block) / 2)))
        print(self.Block)
        for item in List:
            print(self.Block)
            print("| Event ID: {0} ,| Event Name: {1} ,| Event Time: {2} ,| Available Seats : {3} | Total Seat: {4}".format(item['id'] , item['name'] , item['time'] , int(item['seat']) - int(item['seatState']) , item['seat']))
            print(self.Block)

 
    def PrintMyBookingList(self , List , title):
        print(self.Block)
        print(title.rjust(int(len(self.Block) / 2)))
        print(self.Block)
        for item in List:
            print(self.Block)
            print("| Booking ID: {0} ,| Booked Event Name: {1} ,| Booking Time: {2}".format(int(item['bookingId']) , item['EventName'] , item['BookedTime']))
            print(self.Block)


    def GiveAllEventsInfo(self):
        self.PrintAllList(self.data['eventStore'] , 'All Available Events')


    def RegisterEvent(self , User_info):
        eventName = self.RecursiveInput("\n Please enter the name of the event to register: " , '\n Please Enter valid event Name :' , self.TestName)
        eventseat = self.RecursiveInput("\n Please enter the total number of seats available in this event: " , "\n Please enter the valid total number of seats available in this event which must me greater then 1: " , self.TestSeat)
        eventTime = self.RecursiveInput("\n Please enter the time of this event ('YYYY/MM/DD') : ", "\n Please enter the valid time of this event ('YYYY/MM/DD') : " , self.TestDate)
        NowDate   = self.GetMyFormatTime()
        diff      = self.TimeDifferents(eventTime , NowDate)

        if(diff['Hour'] > 0):
            if (not self.isDublicateEvent(eventName , eventTime , User_info)):
                eventconfirmation = input("\n Event Name: {0} , Event Time: {1} , Please Confirm (y = Yes / n = No): ".format(eventName , eventTime))
                if (eventconfirmation.upper() == 'Y'):
                    self.data['eventStore'].append({
                        'name':eventName,
                        'time':eventTime,
                        'seat':eventseat,
                        'user':User_info,
                        'id':len(self.data['eventStore']) + 1,
                        'seatState':0
                    })
                    print('\n Thank You !! for registering new event.')
                    self.ContinueProcess(User_info)
                else:
                    self.ContinueProcess(User_info)
            else:
                print('\n You have already register this event , Please register new event.\n')
                self.ContinueProcess(User_info)
        else:
            print('Sorry You cannot plan event for past . Event Planning date must be future date.')
            self.ContinueProcess(User_info)
    


    def SelectEvent(self , Input):
        List = self.data['eventStore']
        for item in List:
            if Input == item['name'] or Input == str(item['id']):
                return [1 , item]
        return [0 , item]


    def CheckByBoth(self , anyInput , eventInput):
        List = self.data['eventStore']
        for item in List:
            if eventInput == item['name'] or eventInput == str(item['id']):
                if (anyInput == item['name'] or anyInput == str(item['id'])):
                    return True
        return False


    def CanIBook(self , User_info , EventInput):
        List = self.data['bookings']
        for item in List: 
            if User_info['id'] == item['user']['id'] and self.CheckByBoth(str(EventInput) , item['Event']):
                return False
        return True


    def MyOldBookings(self , info):
        MyEventLists = []
        List = self.data['bookings']
        for item in List:
            if item['user']['email'] == info['email']:
                MyEventLists.append(item)
        return([
            len(MyEventLists) > 0,
            MyEventLists
        ])  

    def CancelMyOldBookings(self , BookingId):
        CancelBookingsData = {
            'BookingIndex':None,
            'EventIndex':None,
            'SeatCount':None,
            'EventTime':None
        }
        List = self.data['bookings']
        for index1 , item in enumerate(List):
            if str(item['bookingId']) == str(BookingId):
                EventId = item['EventData']['id']
                CancelBookingsData['BookingIndex'] = index1
                # del self.data['bookings'][index1]
                # remove This Booking from self.data['bookings'] from loop index found
                for index2 , event in enumerate(self.data['eventStore']):
                    if(str(event['id']) == str(EventId)):
                        count = int(self.data['eventStore'][index2]['seatState'])
                        CancelBookingsData['EventIndex'] = index2
                        CancelBookingsData['SeatCount'] = count
                        CancelBookingsData['EventTime'] = self.data['eventStore'][index2]['time']
                        # self.data['eventStore'][index2]['seatState'] = count - 1
                        # edit seatState of EventId from self.data['eventStore']

        if(CancelBookingsData['BookingIndex'] != None and CancelBookingsData['EventIndex'] != None and CancelBookingsData['SeatCount'] != None and CancelBookingsData['EventTime'] != None):
            EventTime = CancelBookingsData['EventTime']
            NowDate   = self.GetMyFormatTime()
            diff      = self.TimeDifferents(EventTime , NowDate)

            if(diff['Hour'] > 0):
                index1 = CancelBookingsData['BookingIndex']
                index2 = CancelBookingsData['EventIndex']
                count  = CancelBookingsData['SeatCount']
                del self.data['bookings'][index1]
                self.data['eventStore'][index2]['seatState'] = count - 1
                return([True , '\n Booking canceled successfully!!'])
            elif (diff['Hour'] < 0):
                return([False ,'\n Sorry you cannot cancel the past completed event.'])
            else:
                return([False ,'\n Sorry You cannot canceled the event , Booking cancellation is allowed less than 24 hours before an event'])
        else:
            return([False , '\n Invalid Booking Id , Please enter valid booking Id to cancel booking.'])


    def CancelMyOldBookingsActivity(self , Info):
        OldBookingAction = input("\n Do You Want to Cancel your Bookings ? y = Yes , n = No :")
        if OldBookingAction.upper() == 'Y':
            MyBookings = self.MyOldBookings(Info)
            self.PrintMyBookingList(MyBookings[1] , 'Your Bookings')
            CancelBookingAction = input("\n Please Enter Bookings Id to cancel? OR back = to return main Menu :")
            if CancelBookingAction == 'back':
                self.ContinueProcess(Info)
            else:
                var = self.CancelMyOldBookings(CancelBookingAction)
                print(var[1])
                self.ContinueProcess(Info)
        else:
            self.ContinueProcess(Info)


    def MyOldBookingsActivity(self , Info):
        MyBookings = self.MyOldBookings(Info)
        if MyBookings[0]:
            self.PrintMyBookingList(MyBookings[1] , 'Your Bookings')
            self.CancelMyOldBookingsActivity(Info)
            self.ContinueProcess(Info)
        else:
            NoBooking = input("\n You don't have any booking ? press 1 = Create new Booking , Any key = return main Menu: ")
            if (NoBooking == '1'):
                self.GiveAllEventsInfo()
                self.BookEvent(Info)
            else:
                self.ContinueProcess(Info)


    def PersonalActivity(self , Info):
        Activity = input("\n Which task do You want to perform ? 1 = See or Cancel Old Bookings , 2 = Create new Booking , Any key = return main Menu: ")
        if Activity == '1':
            self.MyOldBookingsActivity(Info)
        elif Activity == '2':
            self.GiveAllEventsInfo()
            self.BookEvent(Info)
        else:
            self.ContinueProcess(Info)


    def BookEvent(self , User_info):
        event = input("\n Please enter the name of the event or ID of the event you want to Book: ")
        if self.CanIBook(User_info , event):
            foundEvent = self.SelectEvent(event)
            if foundEvent[0] == 1:
                foundEvent = foundEvent[1]
                if int(foundEvent['seatState']) >= int(foundEvent['seat']):
                    print('\n Sorry you can\'t book seat for this event , The seat for this event has exeeded it\'s seat avaiability ')
                    self.ContinueProcess(User_info)
                else:
                    BookingId = len(self.data['bookings']) + 1
                    foundEvent['seatState'] = int(foundEvent['seatState']) + 1; 
                    bookingconfirmation = input("\n Event Name: {0} , Event Time: {1} , Please Confirm your booking? (y = Yes / n = No) ".format(foundEvent['name'] , foundEvent['time'] , BookingId))
                    if (bookingconfirmation.upper() == 'Y'):
                        self.data['bookings'].append({
                            'bookingId':BookingId,
                            'user':User_info,
                            'BookingCount':foundEvent['seatState'],
                            'Event':event,
                            'EventName':foundEvent['name'],
                            'EventData':foundEvent,
                            'BookedTime':self.GetMyFormatTime()
                        })
                        print('\n You have Successfully booked event Event Name: {0} , Your Booking Id: {1}'.format(foundEvent['name'] , BookingId))
                        self.ContinueProcess(User_info)
                    else:
                        self.ContinueProcess(User_info)
            else:
                print('\n Sorry event not found , Due to invalid input.')
                self.ContinueProcess(User_info)
        else:
            print('\n Sorry , Same User cannot book multiple seats at an event.')
            self.ContinueProcess(User_info)


    def GenerateReport(self , fileName = 'index'):
        Alldata  = self.data
        User    =  Alldata['userStore']
        Event   =  Alldata['eventStore']
        Booking =  Alldata['bookings']
        UserKeys = None
        EventKeys = None
        BookingKeys = None
        if(len(User) > 0):
            UserKeys = User[0].keys()
        if(len(Event) > 0):
            EventKeys = Event[0].keys()
        if(len(Booking) > 0):
            BookingKeys = Booking[0].keys()
        if(UserKeys != None or EventKeys != None or BookingKeys != None):
            with open(fileName+'_event.txt', 'w') as f:    
                if(UserKeys != None):
                    f.writelines(self.Block+'\n')
                    #   Block  # generate header
                    f.writelines('Users'.rjust(int(len(self.Block) / 2)))
                    for item in User:
                        f.writelines(self.Block+'\n')
                        for item2 in UserKeys:
                            f.writelines(' '+(item2+': '+str(item[item2])).rjust( int(len(UserKeys)) )+'  |')
                    f.writelines(self.Block+'\n')
                    f.writelines('\n')

                if(EventKeys != None):
                    validTitles = {
                        'name'      : 'Event Name',
                        'time'      : 'Event Time',
                        'seat'      : 'Totle seats',
                        'user'      : 'Owner Name',
                        'id'        : 'Event Id',
                        'seatState' : 'Booked Seat'
                    }
                    # f.writelines(event.Block+'\n')
                    f.writelines('\n')
                    f.writelines(self.Block+'\n')
                    f.writelines('Events Created'.rjust(int(len(self.Block) / 2)))
                    for item in Event:
                        f.writelines(self.Block+'\n')
                        for item2 in EventKeys:
                            f.writelines(' '+(validTitles[item2]+': '+GetUID_Report(item[item2] , item2)).rjust( int(len(EventKeys)) )+'  |')
                    f.writelines(self.Block+'\n')

                if(BookingKeys != None):
                    validTitles = {
                        'EventData':''
                    }   
                    RemoveEventData = lambda arg : None if 'EventData' == arg else arg
                    f.writelines('\n')
                    f.writelines(self.Block+'\n')
                    f.writelines('Booking Created'.rjust(int(len(self.Block) / 2)))
                    for item in Booking:
                        f.writelines(self.Block+'\n')
                        for item2 in BookingKeys:
                            BookingKey = RemoveEventData(item2)
                            if(BookingKey != None):
                                f.writelines(' '+(BookingKey+': '+GetUID_Report(item[item2] , item2) ).rjust( int(len(BookingKeys)) )+'  |')
                    f.writelines(self.Block+'\n')
            

def GetUID_Report(data , name):
    if(type(data) is dict):
        if('usertype' in data):
            return data['name']+' | Owner Email: '+ data['email']
    if(name == 'EventData'):
        return ' '
    return str(data)


def InitProgram(Info):
    eventagent = event.EventOrStaff()
    if eventagent[0] == 1:
        event.RegisterEvent(Info)
    elif eventagent[0] == 2:
        event.PersonalActivity(Info)
    else:
        print(eventagent[1])
        event.ContinueProcess(Info)

if __name__ == "__main__":
    event = EventPlanning()
    info = event.InputUserInfo()
    InitProgram(info)