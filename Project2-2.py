from datetime import datetime


class FlightBooking:

    def __init__(self):
        self.Seperator = '\n***********************************************************************************************************************************'
        self.userCollection   = []
        self.flightCollection = []
        self.allbooking       = []
        self.limit            = 0 

    def inputName(self , text):
        name = input(text)
        if(len(name) > 2):
            return name
        else:
            return self.inputName('The name you have entered is invalid , Please enter valid name :')
            

    def inputAddress(self , text):
        name = input(text)
        if(len(name) > 2):
            return name
        else:
            return self.inputAddress('The address you have entered is invalid , Please enter valid address :')


    def inputthreeDigitCode(self , text):
        threedigitcode = input(text)
        if threedigitcode.isdigit():
            if(len(threedigitcode) >=  3):
                return threedigitcode
            else:
                return self.inputthreeDigitCode('The three digit code must contain more then 3 digit , Please enter valid three digit code :')
        else:
            return self.inputthreeDigitCode('The three digit code must be numerical , Please enter valid three digit code :')


    def inputisMuslim(self , question):
        ismuslim = input(question)
        if not ismuslim.isdigit():
            ismuslim = ismuslim.lower()
            if 'y' == ismuslim or 'n' == ismuslim:
                return ismuslim
            else:
                return self.inputisMuslim('Please enter yes for y and n for no , Are you from muslim community? :')
        else:
            return self.inputisMuslim('Please enter yes for y and n for no , Are you from muslim community? :')


    def inputflightname(self , question):
        question = input(question)
        if(len(question) > 2):
            return question
        else:
            return self.inputflightname('The flight name you have entered is invalid , Please enter valid flight name :')


    def inputNumberOfSeat(self , question):
        seat = input(question)
        if not seat.isdigit():
            return self.inputNumberOfSeat('Number of seat must be numeric data , Please enter valid number of seat in flight :')
        else:
            seats = int(seat)
            if(seats > 1):
                return seat
            else:
                return self.inputNumberOfSeat('Number of seat must be greater then 1 , Please enter valid number of seat in flight :')


    def flightdate(self , datemsg):
        date = input(datemsg)
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            return self.flightdate('The date you have enterer is invalid , Please enter valid date in (yyyy-mm-dd) format :')
    

    def inputSource(self , msg):
        source = input(msg)
        if(len(source) > 1):
            return source
        else:
            return self.inputSource('The source place name you have entered is invalid , Please enter valid source place name :')
    

    def inputDestination(self , msg):
        source = input(msg)
        if(len(source) > 1):
            return source
        else:
            return self.inputDestination('The destination place name you have entered is invalid , Please enter valid destination place name :')

    def inputFilename(self , msg):
        input_data = input(msg)
        if(len(input_data) > 0):
            return(input_data)
        else:
            return self.inputFilename('Please enter the valid file name :')


    def getUserInfo(self):
        data  = {
            'Name':self.inputName('Please Enter Name :'),
            'Address':self.inputAddress('please enter address :'),
            'ThreedigitCode':self.inputthreeDigitCode("Please enter three code three digit code :"),
            'Muslim':self.inputisMuslim('Are you from muslim community :'),
            "id":len(self.userCollection) + 1
        }
        if self.isOldUser(data['ThreedigitCode']):
            print('\n The user who have already used this program was found \n')
            return(data)
        else:
            self.userCollection.append(data)
            return(data)


    def TimeDifferents(self , t1 , t2):
        distance = datetime.strptime(t1, '%Y-%m-%d') - datetime.strptime(t2, '%Y-%m-%d')
        min  , secs = divmod(distance.days * 86400 + distance.seconds, 60)
        hour , minutes = divmod(min, 60)
        return({'h': hour})


    def isOldUser(self , ThreedigitCode):
        List = self.userCollection
        for item in List:
            if ThreedigitCode == item['ThreedigitCode']:
                return(1)
        return(0)


    def checkIsAlreadyRegistered(self , FlightName , Flightseat , FlightTime  , FlightSource , FlightDestination):
        for item in self.flightCollection:
            if item['Seat'] == Flightseat and item['FlightSource']  == FlightSource and item['FlightDestination'] == FlightDestination and item['Name'] == FlightName and item['Time'] == FlightTime:
                return(1)
        return(0)


    def DontExitRepeat(self , info , printText='\n'):
        print(printText)
        menu = input("\n Press ? ( Y to [Exit] / N to [Continue] / SAVE to [Generate Overall report] ) / press Any key to [Login As Another User]: ")
        if menu.lower() == 'y':
            return
        elif menu.lower() == 'n':
            Start(info)
        elif menu.lower() == 'save':
            self.GenerateReport(self.inputFilename("\n Please enter the file name of report file you want to generate: : "))
            self.DontExitRepeat(info)
        else:
            Start(self.getUserInfo())  


    def ShowAllAvailableFlights(self , List , title): 
        print(self.Seperator + title.rjust(int(len(self.Seperator) / 2)) + self.Seperator)
        for item in List:
            print(self.Seperator+"\n Flight ID :{0} ".format(item['Id']) +" Flight Source (From): {0} ---> Flight Destination (To): {1}  \n Flight Name: {2} \n Flight Time: {3} ".format(item['FlightSource'] , item['FlightDestination'] , item['Name'] , item['Time'] ) + " | Available Seats : {0} | Total Seat: {1}".format((int(item['Seat']) - int(item['FlightSeatState'])) , item['Seat']) + self.Seperator)


    def ShowOldBookingAction(self , List , title):
        print(self.Seperator + title.rjust(int(len(self.Seperator) / 2)) + self.Seperator)
        for item in List:
            print(self.Seperator + "\n Flight id you have booked :{0} , your flight Booking id: {1} ".format(item['FlightData']['Id'] , item['bookingId']) + " Flight Source (From):{0} ---> Flight Destination (To): {1}  \n Flight Name: {2} \n Flight Time: {3}".format(item['FlightData']['FlightSource'] , item['FlightData']['FlightDestination'] , item['FlightData']['Name'] , item['FlightData']['Time'] ) + "\nBooked Time: {0}".format(item['BookedTime']) + self.Seperator)


    def AddFlights(self , userData):
        Name          =  self.inputflightname('Please enter the name of flight you wanto to register:')
        Source        =  self.inputSource(' Please enter the source place name (From) :')
        Destination   =  self.inputDestination('Please enter the destination place name (To):')
        Time          =  self.flightdate('Please enter date of flight (yyyy-mm-dd) format :')
        Seat          =  self.inputNumberOfSeat("Please enter number of seat in flight: ")

        if(self.TimeDifferents(Time , datetime.now().strftime('%Y-%m-%d'))['h'] > 0):
            if (self.checkIsAlreadyRegistered(Name , Seat , Time  , Source , Destination)):
                self.DontExitRepeat(userData , '\n This flight is already registered by yourself .. please register new flight.\n')
            else:
                print(self.Seperator)
                print("\n Flight Source (From): {0} ---> Flight Destination (To): {1}  \n Flight Name: {2} \n Flight Time: {3} ".format(Source , Destination , Name , Time))
                print(self.Seperator)
                if (input("\n Please Confirm to Register Flight ? (y = Yes / n = No): ").lower() == 'n'):
                    self.DontExitRepeat(userData)
                else:
                    self.flightCollection.append({
                        'FlightSource':Source,
                        'FlightDestination':Destination,
                        'Name':Name,
                        'Id':len(self.flightCollection) + 1,
                        'Time':Time,
                        'Seat':Seat,
                        'User':userData,
                        'FlightSeatState':0
                    })
                    self.DontExitRepeat(userData , '\n You have successfully added flight detail, Now users can book your flight.')
        else:
            self.DontExitRepeat(userData,'Booked Flight date must be future date not a past date. Please book on a future date')
    

    def FlightMatch(self , inputdata):
        for ind , Flight in enumerate(self.flightCollection):
            if inputdata == str(Flight['Id']):
                return([Flight , 1 , ind])
        return([{} , 0 , 0])


    def RecentBookings(self , info):
        events = []
        for item in self.allbooking:
            if info['ThreedigitCode'] == item['user']['ThreedigitCode']:
                events.append(item)
        state = (len(events) > 0) == True 
        return([
            state,
            events
        ]) 


    def bookOrNot(self , User_info , EventInput):
        for item in self.allbooking: 
            if item['user']['id'] == User_info['id'] and EventInput == item['Flight']:
                return(0)
        return(1)


    def BookingManager(self , User_info):
        Flight = input("\n Please enter the ID of the flight you want to Book: ")
        if self.bookOrNot(User_info , Flight):
            foundFlight = self.FlightMatch(Flight)
            if foundFlight[1] == 1:
                index = foundFlight[2]
                foundFlight = foundFlight[0]
                if int(foundFlight['FlightSeatState']) >= int(foundFlight['Seat']):
                    self.DontExitRepeat(User_info , '\n Sorry we were unable to book seat for you , Seats are not available on this flight.')
                else:
                    Generatedid = 1 + len(self.allbooking) 
                    bookingconfirmationPrompt = input("\n Press Y to confirm your booking and N to discard your booking ? (Y = Yes / N = No) ")
                    if (bookingconfirmationPrompt.lower() == 'n'):
                       self.DontExitRepeat(User_info)
                    else:
                        self.flightCollection[index]['FlightSeatState'] = int(foundFlight['FlightSeatState']) + 1;
                        self.allbooking.append({
                            'user':User_info,
                            'BookingCount':self.flightCollection[index]['FlightSeatState'],
                            'Flight':Flight,
                            'FlightData':foundFlight,
                            'BookedTime':datetime.now().strftime('%Y-%m-%d'),
                            'bookingId':Generatedid
                        })
                        self.DontExitRepeat(User_info , '\n Congratulations!! Your flight was successfully booked ,  Flight Name you have booked : {0} , your Flight Booking Id : {1}'.format(foundFlight['Name'] , Generatedid)) 
            else:
                self.DontExitRepeat(User_info , '\n Sorry Flight you are trying to find is not found in our storage, please supply valid flight id.')
        else:
            self.DontExitRepeat(User_info , '\n Sorry , you cannot book multiple seats of same Flight by using three digit code of same users.')


    def CancelOldBookingsAction(self , BookingId):
        a = None
        b = None
        c = None
        d = None
        List = self.allbooking
        for index1 , item in enumerate(List):
            if str(item['bookingId']) == str(BookingId):
                a = index1
                for index2 , event in enumerate(self.flightCollection):
                    if(str(event['Id']) == str(item['FlightData']['Id'])):
                        c = int(self.flightCollection[index2]['FlightSeatState'])
                        b = index2
                        d = self.flightCollection[index2]['Time']

        if(a != None and b != None and c != None and d != None):
            diff      = self.TimeDifferents(d , datetime.now().strftime('%Y-%m-%d'))
            if(diff['h'] > 0):
                del List[a]
                self.flightCollection[b]['FlightSeatState'] = c - 1
                return([True , '\n Your Booking was canceled successfully.'])
            elif (diff['h'] < 0):
                return([False ,'\n Sorry , You cannot cancel old bookings.'])
            else:
                return([False ,'\n Sorry , Booking cancellation is allowed if you have more than 2 hours before the flight time'])
        else:
            return([False , '\n Your flight Id didn\'t match any flight id , Please enter valid flight id.'])

    
    def HandelPersonalActions(self , Info):
        myprompt = input("\n Which task do You want to perform ? Press 1 to [Create new Flight Booking] , Press 2 to [See or Cancel Old Flight Bookings] , Any key to [Return main Menu] :")
        if myprompt == '1':
            self.ShowAllAvailableFlights(self.flightCollection , '--[ All Available Flights ]--')
            self.BookingManager(Info)
        elif myprompt == '2':
            MeroBookings = self.RecentBookings(Info)
            if MeroBookings[0]:
                self.ShowOldBookingAction(MeroBookings[1] , '--| Your Flight Bookings |--')
                removemybookingaction = input("\n Please Enter flight Bookings Id to cancel? OR back = to return main Menu :")
                if removemybookingaction == 'back':
                    self.DontExitRepeat(Info)
                else:
                    print(self.CancelOldBookingsAction(removemybookingaction)[1])
                    self.DontExitRepeat(Info)
            else:
                if (input("\n You don't have any flights booking ? press 1 to [ Create new flight Booking ] , Any key = [Return main Menu] :") == '1'):
                    self.ShowAllAvailableFlights(self.flightCollection , '--[ All Available Flights ]--')
                    self.BookingManager(Info)
                else:
                    self.DontExitRepeat(Info)
        else:
            self.DontExitRepeat(Info)


    def GenerateReport(self , fileName = 'index'):
        changeDataView = lambda data , name : data['Name']+' | Three Digit Code of Owner: '+ data['ThreedigitCode'] if type(data) is dict and 'Name' in data and 'ThreedigitCode' in data else ('' if name == 'FlightData' else str(data))
        UserALLData    =  self.userCollection
        AllFlight      =  self.flightCollection
        AllBooking     =  self.allbooking

        with open(fileName+'.report.flight.txt', 'w') as file:
            if(len(UserALLData) > 0):
                file.writelines(self.Seperator+'\n')
                file.writelines('--[ All Registered Users ]--'.rjust(int(len(self.Seperator) / 2)))
                for User in UserALLData:
                    file.writelines(self.Seperator+'\n')
                    for userkey in User.keys():
                        file.writelines(' '+(userkey+': '+str(User[userkey]))+'  |')
                    file.writelines(self.Seperator+'\n')

            file.writelines('\n\n')
            if(len(AllFlight) > 0):
                file.writelines(self.Seperator+'\n')
                file.writelines('--[ All Registered Flights ]--'.rjust(int(len(self.Seperator) / 2)))
                for Flight in AllFlight:
                    file.writelines(self.Seperator+'\n')
                    for Flightkey in Flight.keys():
                        file.writelines(' '+(Flightkey+': '+changeDataView(Flight[Flightkey] , Flightkey))+'  |')
                    file.writelines(self.Seperator+'\n')

            file.writelines('\n\n')
            if(len(AllBooking) > 0):
                file.writelines(self.Seperator+'\n')
                file.writelines('--[ All Registered Flights ] --'.rjust(int(len(self.Seperator) / 2)))
                for Booking in AllBooking:
                    file.writelines(self.Seperator+'\n')
                    for Bookingkey in Booking.keys():
                        file.writelines(' '+(changeDataView(Bookingkey , Bookingkey)+': '+changeDataView(Booking[Bookingkey] , Bookingkey))+'  |')
                    file.writelines(self.Seperator+'\n')

def Start(Info):
    eventAgent = input("\n Select Who are you ? (Press 1 if you are Passenger /Press 2 if you are Airways Staff): ")
    if eventAgent == '2':
        Flight.AddFlights(Info)
    elif eventAgent == '1':
        Flight.HandelPersonalActions(Info)
    else:
        print('\n Invalid Input , Please select valid input (1 if you are Passenger / 2 if you are Airways Staff).')
        Flight.DontExitRepeat(Info)


if __name__ == "__main__":
    Flight = FlightBooking()
    Start(Flight.getUserInfo())