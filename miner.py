import requests #to call api and use it
import json  #to process json object
import demjson  #to process json objects
import numpy as numberGenerator
# as per order in image
# first part is logitude that is index 0 for simplicity saying it x
# and next part is latitude that is index 1 for simplicity saying it y
x=0
y=1
CornerPoint1=[30.670223,76.741483]
CornerPoint2=[30.732659,76.843773]
CornerPoint3=[30.791937,76.788161]
CornerPoint4=[30.733599,76.687577]
# to make further process easier
CornerPointsList=[CornerPoint1,CornerPoint2,CornerPoint3,CornerPoint4] 
# all things as per image
# equation of line 1 
delx=[] 
dely=[]
# precalulating all delx and dely for all lines to decrease computations
def calculateDel():
	for i in range(0,4):
		delx.append(CornerPointsList[(i+1)%4][x]-CornerPointsList[i][x])
		dely.append(CornerPointsList[(i+1)%4][y]-CornerPointsList[i][y])
# equation line 1 
def Line1(Point):
	# equation of line in form L=(x2-x1)*(y-y1)-(y2-y1)*(x-x1)
	L=delx[0]*(Point[y]-CornerPoint1[y])-dely[0]*(Point[x]-CornerPoint1[x])
	return(L)
# equation of line 2
def Line2(Point):
	L=delx[1]*(Point[y]-CornerPoint1[y])-dely[1]*(Point[x]-CornerPoint1[x])
	return(L)
	return()
# equation of line 3
def Line3(Point):
	L=delx[2]*(Point[y]-CornerPoint1[y])-dely[2]*(Point[x]-CornerPoint1[x])
	return(L)
	return()
# equation of line 4
def Line4(Point):
	L=delx[3]*(Point[y]-CornerPoint1[y])-dely[3]*(Point[x]-CornerPoint1[x])
	return(L)
	return()
# googelDistaceAndTime function will return a list of string 
# list index 0 will have distance between origin and target 
# list index 1 will have average time at api call between origin and target average
# google maps access token to be placed as a string below
GoogleAPIkey=#getYourApiKeyAndPlaceHere
def GoogleDistanceAndTime(origin,target):
	ApiCaller="https://maps.googleapis.com/maps/api/distancematrix/json?origins="+ str(origin[0]) +","+ str(origin[1]) +"&destinations=" + str(target[0]) +","+ str(target[1]) + "&key="+ GoogleAPIkey
	# contains the api HTTP calling gormat
	ApiResult=requests.get(ApiCaller)
	ApiResultText=ApiResult.text 
	# conveted to bytes file to text for demjson
	resultObject=demjson.decode(ApiResultText)
	# after studying api format of google
	try:
		return([resultObject['rows'][0]['elements'][0]['distance']['value'],resultObject['rows'][0]['elements'][0]['duration']['value']])
	except:
		return([-1,-1])
# for centroid
# Line1<0
# Line2>0
# Line3>0
# Line4<0
# as centroid is always inside the figure here, so hence all set
def chekBlueRegion(Point):
	if(Line1(Point)<=0 and Line2(Point)>=0 and Line3(Point)>=0 and Line4(Point)<=0):
		# point is a valid point
		return(1)
	else:
		# point is in red region
		return(0)
#all driver
def main():  
	calculateDel()
	driverLogitude=numberGenerator.arange(CornerPoint4[y],CornerPoint2[y],0.01)
	driverLatitude=numberGenerator.arange(CornerPoint1[x],CornerPoint3[x],0.01)
	driverLogitude2=driverLogitude
	driverLatitude2=driverLatitude
	errorInfoFile=open("apiconnectionerror.txt","rt")
	numberOfBluesWritten=errorInfoFile.read()
	numberOfBluesWritten=int(numberOfBluesWritten)
	errorInfoFile.close()
	numberOfBlueLoopON=0
	for originLatitude in driverLatitude:
		for orgiginLongitude in driverLogitude:
			if(chekBlueRegion([originLatitude,orgiginLongitude])==1):
				for destinationLatitude in driverLatitude2:
					for destinationLongitude in driverLogitude2:
						try:
							DataFile=open("chandigarh_road_data.csv","at") #opens the csv file we are working with
						except:
							print("some file stream error")
							return(-1)  #returns a status of -1 if file is not opened properly
						connectionStatus=1
						start=[originLatitude,orgiginLongitude]
						terminate=[destinationLatitude,destinationLongitude]
						CheckBlue=chekBlueRegion(terminate)
						if(CheckBlue==1):
								numberOfBlueLoopON=numberOfBlueLoopON+1
						if(numberOfBluesWritten<numberOfBlueLoopON):
							if(CheckBlue==1):
								while(connectionStatus):
									try:
										temp=GoogleDistanceAndTime(start,terminate)
										connectionStatus=0
									except:
										print("\t\t\t\t:::SOME Connection Issue:::\t\t\t:::RETRYING::::")
									if(temp[0]==-1):
										errorInfoFile=open("apiconnectionerror.txt","wt")
										errorInfoFile.write(str(numberOfBlueLoopON-1))
										errorInfoFile.close()
										print("API Daily requests qota achieved")
										DataFile.close()
										return()
								DataFile.write(str(start[0])+","+str(start[1])+","+str(terminate[0])+","+str(terminate[1])+","+str(temp[0])+","+str(temp[1])+"\n")
								print("start::",start,"terminate::",terminate,"::::IN BLUE REGION \n \t\t\t",temp,":::DONE")
							else:
								print("start::",start,"terminate::",terminate,"::::IN RED REGION \n \t\t\t:::DONE")
						else:
							print("Already Written DataSet")	
					DataFile.close()
			else:
				print("\t\t\tORININ IN RED:::",[originLatitude,orgiginLongitude],":::DONE:::")
	print("completed")
main()
