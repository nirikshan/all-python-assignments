from datetime import datetime
import re

# Three Digit Passenger code is unique if same action is performed in database Primary Key = <Three Digit Passenger code>
class BookingAirways:
    def __init__(self):
        self.data = {
            'UserSlack':[],
            'FlightSlack':[],
            'bookings':[]
        }
        self.Block = '\n---------------------------------------------------------------------------------------------------------------'

    def RecursiveInput(self , text , InvalidText , condition):
        inputData   = input(text)
        if(condition(inputData)):
            return(inputData)
        else:
            return self.RecursiveInput(InvalidText , InvalidText , condition)


    def TestName(self , name):
        return len(name) > 1


    def TestYesOrNo(self , text ):
        return text.upper() == 'Y' or text.upper() == 'N'


    def TestPassengerCode(self , code):
        if not code.isdigit():
            return False
        else:
            code = int(code)
            if(code > 100):
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
        name    = self.RecursiveInput('\n Enter Your Name :'   , '\n Please Enter Your valid Name :' , self.TestName)
        address = self.RecursiveInput('\n Enter Your Address :' , '\n Please Enter Your valid Address :' , self.TestName)
        code    = self.RecursiveInput('\n Please Enter Your 3 digit passenger Code (e.g. 100) :' , '\n Please Enter valid 3 digit passenger Code (e.g. 100) :' , self.TestPassengerCode)
        muslim  = self.RecursiveInput('\n Are you from muslim community ( y / n ) :' , '\n  Are you from muslim community ( y / n ) :' , self.TestYesOrNo)
        info = {
                'Name':name,
                'Address':address,
                'ThreedigitCode':code,
                'Muslim':muslim,
                "id":len(self.data['UserSlack']) + 1
            }
        if not self.isOldUser(code):
            self.data['UserSlack'].append(info)
            return(info)
        else:
            print('Old User Detected ThreedigitCode already used.')
            return(info)


    def GetMyFormatTime(self ):
        return datetime.now().strftime('%Y/%m/%d')


    def TimeDifferents(self , time1 , time2):
        Format = '%Y/%m/%d'
        differ = datetime.strptime(time1, Format) - datetime.strptime(time2, Format)
        min  , secs = divmod(differ.days * 86400 + differ.seconds, 60)
        hour , minutes = divmod(min, 60)
        return({'Hour': hour , 'Minutes': minutes , 'Second':secs })


    def isOldUser(self , ThreedigitCode):
        List = self.data['UserSlack']
        for item in List:
            if ThreedigitCode == item['ThreedigitCode']:
                return True
        return False

    def AirwaysOrStaff(self):
        eventAgent = input("\n Your are (1 = Airways Staff / 2 = Passenger): ")
        if eventAgent == '1':
            return [1]
        elif eventAgent == '2':
            return [2]
        else:
            return [3 , '\n Invalid Input , Please Supply Valid Input.']
    

    def isDublicateFlight(self , FlightName , Flightseat , FlightTime  , FlightSource , FlightDestination):
        List = self.data['FlightSlack']
        for item in List:
            if FlightName == item['Name'] and FlightTime == item['Time'] and Flightseat == item['Seat'] and  FlightSource == item['FlightSource'] and FlightDestination == item['FlightDestination']:
                return True
        return False


    def ContinueProcess(self , User_info):
        menu = input("\n Do You want to exit ? ( y = Yes / n = No / save = Save All Report) / Any key = login as new user : ")
        if menu.upper() == 'Y':
            return
        elif menu.upper() == 'N':
            InitProgram(User_info)
        elif menu.upper() == 'SAVE':
            fileName = self.RecursiveInput("\n Please enter file name to save Flight Booking and Flight registration report : " , "\n Please enter valid file name to save Flight Booking and Flight registration report : " , self.TestName)
            self.GenerateReport(fileName)
            self.ContinueProcess(User_info)
        else:
            info = self.InputUserInfo()
            InitProgram(info)
        return  


    def PrintAllList(self , List , title): 
        print(self.Block)
        print(title.rjust(int(len(self.Block) / 2)))
        print(self.Block)
        for item in List:
            print(self.Block)
            print("| Flight ID: {0} ,| Flight Name: {1} ,| Flight Time: {2} ,| Flight Source (From): {3} ,| Flight Destination (To): {4}".format(item['Id'] , item['Name'] , item['Time'] , item['FlightSource'] , item['FlightDestination']))
            print("| Available Seats : {0} | Total Seat: {1}".format((int(item['Seat']) - int(item['FlightSeatState'])) , item['Seat']))
            print(self.Block)


    def PrintMyBookingList(self , List , title):
        print(self.Block)
        print(title.rjust(int(len(self.Block) / 2)))
        print(self.Block)
        for item in List:
            print(self.Block)
            print("|Booking Id:{0} | Flight ID: {1} ,| Flight Name: {2} ,| Flight Time: {3} ,|Booked Time: {4} |  Flight Source (From): {5} ,| Flight Destination (To): {6}".format(item['bookingId'] , item['FlightData']['Id'] , item['FlightData']['Name'] , item['FlightData']['Time'] , item['BookedTime'] ,item['FlightData']['FlightSource'] ,item['FlightData']['FlightDestination']))
            print(self.Block)


    def GiveAllFlightInfo(self):
        self.PrintAllList(self.data['FlightSlack'] , 'All Available Flights')


    def RegisterFlights(self , User_info):
        FlightName          =  self.RecursiveInput("\n Please enter the name of the Flight to register: " , '\n Please Enter valid Flight Name :' , self.TestName)
        FlightSeat          =  self.RecursiveInput("\n Please enter the total number of seats available in this Flight: " , "\n Please enter the total number of seats available in this Flight which must me greater then 1: " , self.TestSeat)
        FlightTime          =  self.RecursiveInput("\n Please enter the time of this Flight ('YYYY/MM/DD') : ", "\n Please enter the valid time of this Flight ('YYYY/MM/DD') : " , self.TestDate)
        FlightSource        =  self.RecursiveInput("\n Please enter the source place name (From) : ", "\n Please enter the source place name (From)  : " , self.TestName)
        FlightDestination   =  self.RecursiveInput("\n Please enter the destination place name (To): ", "\n Please enter the valid destination place name (To): " , self.TestName)

        NowDate   = self.GetMyFormatTime()
        diff      = self.TimeDifferents(FlightTime , NowDate)

        if(diff['Hour'] > 0):
            if (not self.isDublicateFlight(FlightName , FlightSeat , FlightTime  , FlightSource , FlightDestination)):
                print(self.Block)
                print("\n Flight Name: {0} , Flight Time: {1}  , FlightSource (From) : {2} , FlightDestination (To):{3}".format(FlightName , FlightTime , FlightSource , FlightDestination))
                print(self.Block)
                eventconfirmation = input("\n Please Confirm to Register Flight ? (y = Yes / n = No): ")
                if (eventconfirmation.upper() == 'Y'):
                    self.data['FlightSlack'].append({
                        'Name':FlightName,
                        'Time':FlightTime,
                        'Seat':FlightSeat,
                        'User':User_info,
                        'FlightSource':FlightSource,
                        'FlightDestination':FlightDestination,
                        'Id':len(self.data['FlightSlack']) + 1,
                        'FlightSeatState':0
                    })
                    print('\n Thank You !! for registering new flight.')
                    self.ContinueProcess(User_info)
                else:
                    pass
                    self.ContinueProcess(User_info)
            else:
                print('\n You have already register this flight , Please register new flight.\n')
                self.ContinueProcess(User_info)
        else:
            print('Sorry You cannot plan flight for past . flight Planning date must be future date.')
            self.ContinueProcess(User_info)
    


    def SelectFlight(self , Input):
        List = self.data['FlightSlack']
        for item in List:
            if Input == item['Name'] or Input == str(item['Id']):
                return [1 , item]
        return [0]


    def CheckByBoth(self , anyInput , eventInput):
        List = self.data['FlightSlack']
        for item in List:
            if eventInput == item['Name'] or eventInput == str(item['Id']):
                if (anyInput == item['Name'] or anyInput == str(item['Id'])):
                    return True
        return False


    def MyOldBookings(self , info):
        MyEventLists = []
        List = self.data['bookings']
        for item in List:
            if item['user']['ThreedigitCode'] == info['ThreedigitCode']:
                MyEventLists.append(item)
        return([
            len(MyEventLists) > 0,
            MyEventLists
        ]) 


    def CanIBook(self , User_info , EventInput):
        List = self.data['bookings']
        for item in List: 
            if self.CheckByBoth(str(EventInput) , item['Flight']):
                return False
        return True 


    def BookFlight(self , User_info):
        Flight = input("\n Please enter the name of the flight or ID of the flight you want to Book: ")
        if self.CanIBook(User_info , Flight):
            foundFlight = self.SelectFlight(Flight)
            if foundFlight[0] == 1:
                foundFlight = foundFlight[1]
                if int(foundFlight['FlightSeatState']) >= int(foundFlight['Seat']):
                    print('\n Sorry you can\'t book seat for this flight , The seat for this flight has exeeded it\'s seat avaiability ')
                    self.ContinueProcess(User_info)
                else:
                    BookingId = len(self.data['bookings']) + 1
                    print(self.Block)
                    print("| Flight ID: {0} ,| Flight Name: {1} ,| Flight Time: {2} ,| Flight Source (From): {3} ,| Flight Destination (To): {4}".format(foundFlight['Id'] , foundFlight['Name'] , foundFlight['Time'] , foundFlight['FlightSource'] , foundFlight['FlightDestination']))
                    print("| Available Seats : {0} | Total Seat: {1}".format((int(foundFlight['Seat']) - int(foundFlight['FlightSeatState'])) , foundFlight['Seat']))
                    print(self.Block)
                    bookingconfirmation = input("\n Please Confirm your booking? (y = Yes / n = No) ")
                    if (bookingconfirmation.upper() == 'Y'):
                        foundFlight['FlightSeatState'] = int(foundFlight['FlightSeatState']) + 1; 
                        self.data['bookings'].append({
                            'bookingId':BookingId,
                            'user':User_info,
                            'BookingCount':foundFlight['FlightSeatState'],
                            'Flight':Flight,
                            'Flight':foundFlight['Name'],
                            'FlightData':foundFlight,
                            'BookedTime':self.GetMyFormatTime()
                        })
                        print('\n You have Successfully booked Flight ,  Flight Name: {0} , Your Flight Booking Id: {1}'.format(foundFlight['Name'] , BookingId))
                        self.ContinueProcess(User_info)
                    else:
                        self.ContinueProcess(User_info)
            else:
                print('\n Sorry Flight not found , Due to invalid input.')
                self.ContinueProcess(User_info)
        else:
            print('\n Sorry , Same User cannot book multiple seats of Flight..')
            self.ContinueProcess(User_info)


    def CancelMyOldBookings(self , BookingId):
        CancelBookingsData = {
            'BookingIndex':None,
            'FlightIndex':None,
            'SeatCount':None,
            'FlightTime':None
        }
        List = self.data['bookings']
        for index1 , item in enumerate(List):
            if str(item['bookingId']) == str(BookingId):
                EventId = item['FlightData']['Id']
                CancelBookingsData['BookingIndex'] = index1
                # del self.data['bookings'][index1]
                # remove This Booking from self.data['bookings'] from loop index found
                for index2 , event in enumerate(self.data['FlightSlack']):
                    if(str(event['Id']) == str(EventId)):
                        count = int(self.data['FlightSlack'][index2]['FlightSeatState'])
                        CancelBookingsData['FlightIndex'] = index2
                        CancelBookingsData['SeatCount'] = count
                        CancelBookingsData['FlightTime'] = self.data['FlightSlack'][index2]['Time']
                        # self.data['eventStore'][index2]['seatState'] = count - 1
                        # edit seatState of EventId from self.data['eventStore']
        if(CancelBookingsData['BookingIndex'] != None and CancelBookingsData['FlightIndex'] != None and CancelBookingsData['SeatCount'] != None and CancelBookingsData['FlightTime'] != None):
            FlightTime = CancelBookingsData['FlightTime']
            NowDate   = self.GetMyFormatTime()
            diff      = self.TimeDifferents(FlightTime , NowDate)
            if(diff['Hour'] > 0):
                index1 = CancelBookingsData['BookingIndex']
                index2 = CancelBookingsData['FlightIndex']
                count  = CancelBookingsData['SeatCount']
                del self.data['bookings'][index1]
                self.data['FlightSlack'][index2]['FlightSeatState'] = count - 1
                return([True , '\n Booking canceled successfully!!'])
            elif (diff['Hour'] < 0):
                return([False ,'\n Sorry you cannot cancel the past completed flight.'])
            else:
                return([False ,'\n Sorry You cannot canceled the flight , Booking cancellation is allowed if you have more than 2 hours before the flight.'])
        else:
            return([False , '\n Invalid Flight Booking Id , Please enter valid flid booking Id to cancel flight booking.'])


    def CancelMyOldBookingsActivity(self , Info):
        OldBookingAction = input("\n Do You Want to Cancel your Bookings ? y = Yes , n = No :")
        if OldBookingAction.upper() == 'Y':
            MyBookings = self.MyOldBookings(Info)
            self.PrintMyBookingList(MyBookings[1] , 'Your Bookings')
            CancelBookingAction = input("\n Please Enter flight Bookings Id to cancel? OR back = to return main Menu :")
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
            self.PrintMyBookingList(MyBookings[1] , 'Your Flight Bookings')
            self.CancelMyOldBookingsActivity(Info)
            self.ContinueProcess(Info)
        else:
            NoBooking = input("\n You don't have any flights booking ? press 1 = Create new flight Booking , Any key = return main Menu: ")
            if (NoBooking == '1'):
                self.GiveAllFlightInfo()
                self.BookFlight(Info)
            else:
                self.ContinueProcess(Info)


    def PersonalActivity(self , Info):
        Activity = input("\n Which task do You want to perform ? 1 = See or Cancel Old Flight Bookings , 2 = Create new Flight Booking , Any key = return main Menu: ")
        if Activity == '1':
            self.MyOldBookingsActivity(Info)
        elif Activity == '2':
            self.GiveAllFlightInfo()
            self.BookFlight(Info)
        else:
            self.ContinueProcess(Info)


    def GenerateReport(self , fileName = 'index'):
        Alldata  = self.data
        User    =  Alldata['UserSlack']
        Flight   =  Alldata['FlightSlack']
        Booking =  Alldata['bookings']
        UserKeys = None
        FlightKey = None
        BookingKeys = None

        if(len(User) > 0):
            UserKeys = User[0].keys()
        if(len(Flight) > 0):
            FlightKey = Flight[0].keys()
        if(len(Booking) > 0):
            BookingKeys = Booking[0].keys()

        if(UserKeys != None or FlightKey != None or BookingKeys != None):
            with open(fileName+'_Flight.txt', 'w') as f:    
                if(UserKeys != None):
                    f.writelines(self.Block+self.Block+'\n')
                    # generate header
                    f.writelines('Users'.rjust(int(len(self.Block) / 2)))
                    for item in User:
                        f.writelines(self.Block+self.Block+'\n')
                        for item2 in UserKeys:
                            f.writelines(' '+(item2+': '+str(item[item2])).rjust( int(len(UserKeys)) )+'  |')
                    f.writelines(self.Block+self.Block+'\n')
                    f.writelines('\n')

                if(FlightKey != None):
                    # f.writelines(Flight.Block+'\n')
                    f.writelines('\n')
                    f.writelines(self.Block+self.Block+'\n')
                    f.writelines('Flights Created'.rjust(int(len(self.Block) / 2)))
                    for item in Flight:
                        f.writelines(self.Block+self.Block+'\n')
                        for item2 in FlightKey:
                            f.writelines(' '+(item2+': '+GetUID_Report(item[item2] , item2)).rjust( int(len(FlightKey)) )+'  |')
                    f.writelines(self.Block+'\n')
                    f.writelines('\n')

                if(BookingKeys != None):
                    RemoveFlightData = lambda arg , arg2 : ' Flight Destination (TO): '+arg2['FlightData']['FlightDestination']+'| Flight Source (From):'+arg2['FlightData']['FlightSource']+' | Flight Date:'+arg2['FlightData']['Time'] if 'FlightData' == arg else arg
                    f.writelines('\n')
                    f.writelines(self.Block+self.Block+'\n')
                    f.writelines('Flight Booking Created'.rjust(int(len(self.Block) / 2)))
                    for item in Booking:
                        f.writelines(self.Block+self.Block+'\n')
                        for item2 in BookingKeys:
                            BookingKey = RemoveFlightData(item2 , item)
                            if(BookingKey != None):
                                f.writelines(' '+(BookingKey+': '+GetUID_Report(item[item2] , item2) ).rjust( int(len(BookingKeys)) )+'  |')
                    f.writelines(self.Block+'\n')
                    f.writelines('\n')
            

def GetUID_Report(data , name):
    if(type(data) is dict):
        if('Name' in data and 'ThreedigitCode' in data):
            return data['Name']+' | Owner Three Digit Code: '+ data['ThreedigitCode']
    if(name == 'FlightData'):
        return ''
    return str(data)


def InitProgram(Info):
    AirwaysTagent = Airways.AirwaysOrStaff()
    if AirwaysTagent[0] == 1:
        Airways.RegisterFlights(Info)
    elif AirwaysTagent[0] == 2:   
        Airways.PersonalActivity(Info)
    else:
        print(AirwaysTagent[1])
        Airways.ContinueProcess(Info)

if __name__ == "__main__":
    Airways = BookingAirways()
    info = Airways.InputUserInfo()
    InitProgram(info)