from datetime import datetime

globalCollection = {
    'RegisteredFlights':[],
    'RegisteredUser':[],
    'alluserBooking':[],
}


class ReportGenerator:
     
    def __init__(self , asktext):
        wall = GenerateWall(100 , '^')
        print(wall+'\n Text file name will be generated where report of all the users , booking and flight will be generated \n'+wall)
        self.name = self.CheckFilename(asktext)
        self.MainGenerater()
    
    def CheckFilename(self , msg):
        input_data = input(msg)
        return input_data if(len(input_data) > 0) else self.CheckFilename('file name must contain some character , Please enter file name again:: ')
    
    def MainGenerater(self):
        FlightData  = globalCollection['RegisteredFlights']
        UserData    = globalCollection['RegisteredUser']
        BookingData = globalCollection['alluserBooking']
        wall = GenerateWall(100 , '^')
        with open(self.name+'.txt', 'w') as file:
            if(0 < len(FlightData)):
                self.GenerateFlightData(FlightData , file , wall)
            if(0 < len(UserData)):
                self.GenerateUserData(UserData , file , wall)
            if(0 < len(BookingData)):
                self.GenerateBookingData(BookingData , file , wall)

    def GenerateFlightData(self , FlightData , file , wall):
        file.writelines('\n\n')
        file.writelines('( Flight Data )\n'.rjust(int(len(wall) / 2)))
        for Flight in FlightData:
            file.writelines('\n' +wall * 4)
            file.writelines('\n' + str(Flight))
            file.writelines('\n' +wall * 4)
        file.writelines('\n\n')

    def GenerateUserData(self , UserData , file , wall):
        file.writelines('\n\n')
        file.writelines('( User Data )\n'.rjust(int(len(wall) / 2)))
        for User in UserData:
            file.writelines('\n' +wall * 4)
            file.writelines('\n' + str(User))
            file.writelines('\n' +wall * 4)
        file.writelines('\n\n')

    def GenerateBookingData(self , BookingData , file , wall):
        file.writelines('\n\n')
        file.writelines('( All Booking Data )\n'.rjust(int(len(wall) / 2)))
        for Booking in BookingData:
            file.writelines('\n' +wall * 4)
            file.writelines('\n' + str(Booking))
            file.writelines('\n' +wall * 4)
        file.writelines('\n\n')


# SIMPLE FUNCTIONS

def CheckName(text):
    name = input(text)
    return name if(len(name) > 2) else CheckName('Name must have more then 2 character , Please enter your name again:: ')            

def CheckAddress(text):
    name = input(text)
    return name if(len(name) > 2) else CheckAddress('Address must contain more then 2 character , Please enter your address again:: ')

def CheckthreeDigitCode(text):
    threedigitcode = input(text)
    return (threedigitcode if (int(threedigitcode) > 3) else CheckthreeDigitCode('The three digit code must contain more then 3 digit , Please enter three digit code again :: ')
    if threedigitcode.isdigit() else CheckthreeDigitCode('The three digit code should be numeric value , Please enter three digit code again:: '))
   
def CheckisMuslim(question):
    ismuslim = input(question)
    return (CheckisMuslim('Please enter Y if you are muslim and N if you are not muslim::') if ismuslim.isdigit() else
    ismuslim if ('Y' == ismuslim.upper() or 'N' == ismuslim.upper()) else CheckisMuslim('Please enter Y if you are muslim and N if you are not muslim:: '))

def Checkflightname(question):
    question = input(question)
    return question if(len(question) > 2) else Checkflightname('Flight name must contain more then 2 character , Please enter your flight name again:: ')

def CheckNumberOfSeat(question):
    seat = input(question)
    return ((seat if (int(seat) > 1) else CheckNumberOfSeat('Number of seat must be greater then 1 , Please enter number of seat on your flight again :: ') ) 
    if seat.isdigit() else CheckNumberOfSeat('Number of seat should be numeric value , Please enter three digit code again:: '))
    
def CheckTimeDiffers(t1 , t2):
    distance = datetime.strptime(t1, '%d-%m-%Y') - datetime.strptime(t2, '%d-%m-%Y')
    min  , secs = divmod(distance.days * 86400 + distance.seconds, 60)
    hour , minutes = divmod(min, 60)
    return({'h': hour})

def Checkdate(datemsg):
    date = input(datemsg)
    try:
        datetime.strptime(date, '%d-%m-%Y')
        return date
    except ValueError:
        return Checkdate('Date must be in this format [i.e (yyyy-mm-dd)] , Please enter date again:: ')
    
def CheckFrom(msg):
    source = input(msg)
    return source if(len(source) > 2) else CheckFrom('Source name must have more then 2 character , Please enter flight source name again:: ')
    
def CheckTo(msg):
    source = input(msg)
    return source if(len(source) > 2) else CheckTo('Destination name must have more then 2 character , Please enter flight destination name again :: ')

def checkolduser(alluserinfo):
    for user in globalCollection['RegisteredUser']:
        if(user['UserCode'] == alluserinfo['UserCode']):        
            return ['Welcome back , we found you are old user you can see your old bookings' , user , 1]
    return ['You have successfully logined , Now you can book flights and register new flights.' , alluserinfo , 0]

def checkoldflight(allflightinfo):
    for flight in globalCollection['RegisteredFlights']:
        if(int(flight['AddedBy']['UserId']) == int(allflightinfo['AddedBy']['UserId']) and 
           flight['FlightName'] == allflightinfo['FlightName'] and 
           flight['From'] == allflightinfo['From'] and 
           flight['To'] == allflightinfo['To'] and 
           int(flight['Seats']) == int(allflightinfo['Seats'])):        
            return ['\n You have already registered this flight. \n' , flight , 1]
    return ['\n You have successfully register your flight info , Now other people book your flights. \n' , allflightinfo , 0]

def checkoldBooking(alluserinfo , selectedFlight):
    for booking in globalCollection['alluserBooking']:
        if(booking['FlightInfo']['FlightId'] == selectedFlight['FlightId'] and booking['UserInfo']['UserId'] == alluserinfo['UserId']):
            return ['You have already booked this flight , You cannot book flight seats more then 1.' , booking , 0]
    return ['You can book this flight.' , selectedFlight , 1]

def getAllUserInformation():
    alluserinfo     = {
        'UserId'     : len(globalCollection['RegisteredUser']) + 1,
        'UserName'   : CheckName('Please enter your full name:: '),
        'UserAdderss': CheckAddress('Please enter your address:: '),
        'UserCode'   : CheckthreeDigitCode('Please enter your three digit code number:: '),
        'IsMuslim'   : CheckisMuslim('Are You muslim press Y for yes and N for No:: ')
    }
    info = checkolduser(alluserinfo)
    print(info[0])
    if(not info[2]):
        globalCollection['RegisteredUser'].append(alluserinfo)
    return(info[1])

def getFlightInfo(userinformation):
    allflightinfo = {
        'FlightId'    : len(globalCollection['RegisteredFlights']) + 1,
        'FlightName'  : Checkflightname('Please enter flight name to register:: '),
        'From'        : CheckFrom('Please enter Flight source place name (From):: '),
        'To'          : CheckTo('Please enter Flight destination place name (To):: '),
        'Seats'       : CheckNumberOfSeat('Please enter total seat on flight:: '),
        'FlightTime'  : Checkdate('Please enter flight date in format of DD-MM-YYYY ::'),
        'AddedBy'     : userinformation,
        'BookedSeats' : 0
    }
    info = checkoldflight(allflightinfo)
    print(info[0])
    if(not info[2]):
        globalCollection['RegisteredFlights'].append(allflightinfo)
    return(info[1])

def GenerateWall(count , item):
    walls = []
    for aa in range(0 , count):
        walls.append(item)
    return(''.join(walls))

def flightTable(flightdata , text):
    wall = GenerateWall(100 , '^')
    print(wall+'\n'+text)
    for item in flightdata:
        print(wall)
        print(('Flight ID::{0} \nFlight Name::{1} \nFrom:: {2} \nTo:: {3} \nTotal Seat on flight :: {4} , \nBooked Seats:: {5} , \nRemaining seat:: {6}'.format(item['FlightId'] , item['FlightName'] , item['From'] , item['To'] , item['Seats'] , item['BookedSeats'] , (int(item['Seats']) - int(item['BookedSeats']) ) ) ) )
        print(wall)
    print('\n')

def BookingTable(bookingsdata , text):
    wall = GenerateWall(100 , '^')
    print(wall+'\n'+text)
    for item in bookingsdata:
        print(wall * 2)
        print(('Booking ID:{0} \nFlight ID::{1} \nFlight Name::{2} \nFrom:: {3} \nTo:: {4} \nTotal Seat on flight :: {5} \nBooked Time:: {6} '.format( item['BookingID'] , item['FlightInfo']['FlightId'] , item['FlightInfo']['FlightName'] , item['FlightInfo']['From'] , item['FlightInfo']['To'] , item['FlightInfo']['Seats'] , item['BookingTime'])))
        print(wall * 2)
    print('\n')

def TestFlightId(suppliedId):
    for i , flight in enumerate(globalCollection['RegisteredFlights']):
        if flight['FlightId'] == suppliedId:
            return([True , flight , i])
    return([False])

def BookingValidation(flight):
    if(int(flight['BookedSeats']) >= int(flight['Seats'])):
        return([False , 'Sorry !! there are no More Seat Available on this flight.'])
    else:
        if(CheckTimeDiffers(flight['FlightTime'] , datetime.now().strftime('%d-%m-%Y') )['h'] > 0):
            return([True , 'You can Book this flights.'])
        else:
            return([False , 'Flight Date has already passed.'])


def getActualBookingIndex(idd):
    # print('\n' , idd , '--------', '------------' , globalCollection['alluserBooking'] , '\n')
    for  index , item in enumerate(globalCollection['alluserBooking']):
        # print('\n' ,item['BookingID'] , int(idd) , '+++++1+++++' ,'\n')
        if int(item['BookingID']) == int(idd):
            return index 
    return None

def getActualFlightIndex(idd2):
    # print('\n', idd2 , '+++++++++++','+++++++++++' , globalCollection['RegisteredFlights'] , '\n')
    for  index , item in enumerate(globalCollection['RegisteredFlights']):
        # print('\n' ,item['FlightId'] , int(idd2) , '+++++2+++++' ,'\n')
        if(int(item['FlightId']) == int(idd2)):
            return index
    return None

def CancelBookings(result , userinformation): 
    askToRemove  = input('Enter [<Booking Id> to Cancel Booking] and [<Any Key> to Discard and return main menu]:: ')
    if(askToRemove.isdigit()):
        for item in result:#looking at only my booking rather then all booking
            if(int(item['BookingID']) == int(askToRemove)):
                ActualBookingIndex = getActualBookingIndex(item['BookingID']);
                ActualFlightIndex  = getActualFlightIndex(item['FlightInfo']['FlightId'])
                # print(ActualBookingIndex , 'ActualBookingIndex')
                # print(ActualFlightIndex , 'ActualFlightIndex')
                if(ActualBookingIndex != None and ActualFlightIndex != None):
                    globalCollection['RegisteredFlights'][ActualFlightIndex]['BookedSeats'] -= 1
                    del globalCollection['alluserBooking'][ActualBookingIndex]
                    print('Your Booking Was Successfully canceled..')
                else:
                    print('Data not found')
    else:
        FirstRun(userinformation)   

def BookingFunction(userinformation , msg='Please Enter Flight ID to book that flight:: '):
    flightTable(globalCollection['RegisteredFlights'] , '***All Registered Flights***')
    askflightid = input(msg)
    if(askflightid.isdigit()):
        askflightid = int(askflightid)
        TestData  = TestFlightId(askflightid)
        if(TestData[0]):
            SelectedFlightIndex = int(TestData[2])
            SelectedFlight = TestData[1]
            TestValidation = BookingValidation(SelectedFlight);
            if(TestValidation[0]):
                askconformation = input('Press [Y to Confirm this booking] and [<Any Key> to Discard and return main menu]:: ')
                if(askconformation.upper() == 'Y'):
                    BookingInfo = {
                        'BookingID'    : len(globalCollection['alluserBooking']) + 1,
                        'UserInfo'     : userinformation,
                        'FlightInfo'   : SelectedFlight,
                        'BookingTime' : datetime.now().strftime('%d-%m-%Y')
                    }
                    response = checkoldBooking(userinformation , SelectedFlight)
                    if(response[2]):
                        globalCollection['RegisteredFlights'][SelectedFlightIndex]['BookedSeats'] += 1
                        globalCollection['alluserBooking'].append(BookingInfo)
                        print('\n Congratulations , Your Flight was Booked successfully. \n')
                    else:
                        print(response[0])
            else:
                print(TestValidation[1])
        else:
            print('Sorry !! Flight corresponding to your supplied flight id is not found.')
    FirstRun(userinformation)


def FirstRun(userinformation): 
    ask = input('\n Press [1 to Book Flights ] [2 to See Old Bookings] [3 to Add your Flight Information] [4 to Login as New User] [5 to create booking and flight report]:: ')
    if(ask.isdigit()):
        ask = int(ask)
        if(ask == 1):
            BookingFunction(userinformation)
        elif(ask == 2):
            result = [item for item in globalCollection['alluserBooking'] if 'UserInfo' in item and item['UserInfo']['UserId'] == userinformation['UserId']]
            BookingTable(result , '*** Flights You Have Booked ***')
            CancelBookings(result , userinformation)
            FirstRun(userinformation)
        elif(ask == 3):
            getFlightInfo(userinformation)
            FirstRun(userinformation)
        elif(ask == 4):
            newUserInfo = getAllUserInformation()
            FirstRun(newUserInfo)
        elif(ask == 5):
            ReportGenerator('Please Define file name For Report File ::')
            FirstRun(newUserInfo)
        else:
            FirstRun(userinformation)
    else:
        FirstRun(userinformation)


if "__main__" == __name__:
    FirstRun(getAllUserInformation())
   