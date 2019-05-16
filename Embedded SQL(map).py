import pandas as pd
from pandas import DataFrame
import sqlite3
import matplotlib.pyplot as plt
import os
import folium
import numpy as np

db = input("Enter the name of the database you'd like to use > ")
connection=sqlite3.connect(db)

task1_count = 0
task2_count = 0
task3_count = 0
task4_count = 0

#prompt user input
def main():
    print("1: Q1\n2: Q2\n3: Q3\n4: Q4\nE: Exit")
    while True:
        selection = input("Enter your choice:")
        if selection == "1":
            task1()
        elif selection == "2":
            task2()    
        elif selection == "3":
            task3()    
        elif selection == "4":
            task4()
        elif selection == "E":
            print("Ending program")
            break
        else:
            print("Please enter a valid selection")

# task 1: Given a range of years and crime type, show (in a bar plot) 
# the month-wise total count of the given crime type.
def task1():
    crimes = ["Assault", "Break and Enter", "Homicide", "Robbery", "Sexual Assaults", 
    "Theft From Vehicle", "Theft Of Vehicle", "Theft Over $5000"]
    global task1_count

    # get inputs from user
    while True:
        try: 
            start = input("Enter start year (YYYY):")
            end = input("Enter end year (YYYY):")
            if int(start) >= 2009 and int(start) <=2018 and int(end) >= 2009 and int(end) <= 2018:
                break
            else:
                print("Please enter valid years between 2009 and 2018")
        except ValueError:
            print("Please enter valid years between 2009 and 2018")
            continue
    while True: 
        crime = input("Enter crime type:")
        if crime in crimes:
            break
        else: 
            print("Please enter a valid crime from the following list (case sensitive): ")
            for c in crimes:
                print(" - ",c)

    #how many years we need to iterate
    r=int(end)-int(start)+1
    year=[]

    # adding year into an array
    for i in range(r):
        year.append(str(int(start)+i))
    Crime_Type = str(crime)
    q="select Crime_Type,Month, count(*) as count from crime_incidents where Year in"+str(tuple(year)) + "and Crime_Type=? group by month ORDER BY Month ASC;"
    df = pd.read_sql_query(q,connection,params={Crime_Type})
    plot = df.plot.bar(x="Month")

    #save the plot in png
    task1_count += 1
    title = "Q1-"+str(task1_count)+".png"
    plt.savefig(title)
    plt.plot()
    plt.show()
    #save the plot
    
# task 2: Given an integer N, show (in a map) the N-most populous 
# and N-least populous neighbourhoods with their population count.
def task2():
    global task2_count
    df1 = pd.read_sql_query("select * from population LEFT JOIN coordinates on population.Neighbourhood_Name=coordinates.Neighbourhood_Name ;", connection)
    df1['sum'] = df1['CANADIAN_CITIZEN']+df1['NON_CANADIAN_CITIZEN']+df1['NO_RESPONSE']
    #dispose the neighbour with 0 population 
    df1 = df1[(df1[['sum']] != 0).all(axis=1)]
    while True:
        try: 
            #take user input
            neighbourhoods = int(input("Enter number of neighbourhoods:"))
            if int(neighbourhoods) >= 0 and int(neighbourhoods) <=385:
                break
            else:
                print("Please enter a valid number of neighbourhoods (0-385)")
        except ValueError:
            print("Please enter a valid number of neighbourhoods (0-385)")
            continue

    col=df1.shape[1]
    row=df1.shape[0]

    # Check to make sure the user inputted number of neighbourhood does not exceed the number returned by the sql query
    neighbourhoods = min(row, int(neighbourhoods))

    #sort values from the most to least
    most=df1.sort_values(by='sum', ascending=False)
    most=most.iloc[0:neighbourhoods,:]
    #sort values from the least to most
    least=df1.sort_values(by='sum', ascending=True)
    least=least.iloc[0:neighbourhoods,:]
    #draw the map
    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    for i in range(neighbourhoods):
        NEIGHBOURHOOD_NAME=most.iloc[i,2]
        LATITUDE=(most.iloc[i,7])
        LONGITUDE=(most.iloc[i,8])
        POPULATION=(most.iloc[i,9])
        s1=(str(POPULATION))
        # Add top N neighbourhoods to map with circles
        folium.Circle(
        location=[LATITUDE, LONGITUDE], # location
        popup= NEIGHBOURHOOD_NAME+' <br> Population:'+s1, # popup text
        radius= POPULATION//20, # size of radius in meter
        color= "crimson", # color of the radius
        fill= True, # whether to fill the map
        fill_color="crimson" ).add_to(m)

    for i in range(neighbourhoods):
        NEIGHBOURHOOD_NAME=least.iloc[i,2]
        LATITUDE=(least.iloc[i,7])
        LONGITUDE=(least.iloc[i,8])
        POPULATION=(least.iloc[i,9])
        s2=(str(POPULATION))
        # Add top N neighbourhoods to map with circles
        folium.Circle(
        location=[LATITUDE, LONGITUDE], # location
        popup= NEIGHBOURHOOD_NAME+' <br> Population:'+ s2, # popup text
        radius= POPULATION//20, # size of radius in meter
        color= "crimson", # color of the radius
        fill= True, # whether to fill the map
        fill_color="crimson" 
        ).add_to(m)

    # count task and save
    task2_count += 1
    title = "Q2-"+str(task2_count)+".html"
    m.save(title)


# task 3: Given a range of years, a crime type and an integer N, show (in a map)
# the Top-N neighbourhoods and their crime count where the given crime type occurred
# most within the given range
def task3():
    global task3_count
    crimes = ["Assault", "Break and Enter", "Homicide", "Robbery", "Sexual Assaults", 
    "Theft From Vehicle", "Theft Of Vehicle", "Theft Over $5000"]
    
    # get inputs from user
    while True:
        try: 
            start = input("Enter start year (YYYY):")
            end = input("Enter end year (YYYY):")
            if int(start) >= 2009 and int(start) <=2018 and int(end) >= 2009 and int(end) <= 2018:
                break
            else:
                print("Please enter valid years between 2009 and 2018")
        except ValueError:
            print("Please enter valid years between 2009 and 2018")
            continue
    while True: 
        crime = input("Enter crime type:")
        if crime in crimes:
            break
        else: 
            print("Please enter a valid crime from the following list (case sensitive): ")
            for c in crimes:
                print(" - ",c)
    while True:
        try: 
            neighbourhoods = int(input("Enter number of neighbourhoods:"))
            if int(neighbourhoods) >= 0 and int(neighbourhoods) <=385:
                break
            else:
                print("Please enter a valid number of neighbourhoods (0-385)")
        except ValueError:
            print("Please enter a valid number of neighbourhoods (0-385)")
            continue

    # Run query
    query = "select crime_incidents.Neighbourhood_Name, sum(Incidents_Count) as Incidents_Sum, Latitude, Longitude \
        from crime_incidents LEFT JOIN coordinates on crime_incidents.Neighbourhood_Name=coordinates.Neighbourhood_Name \
        where Year >="+str(start)+" and Year <="+str(end)+" and Crime_Type = '"+str(crime)+"' and Latitude IS NOT NULL \
        group by crime_incidents.Neighbourhood_Name, Crime_Type"
    df = pd.read_sql_query(query, connection).sort_values(by='Incidents_Sum', ascending=False)
    
    # Create Map
    m = folium.Map(location=[53.540735,-113.496110], zoom_start=11)

    # Check to make sure the user inputted number of neighbourhood does not exceed the number returned by the sql query
    n_count = df.shape[0]
    neighbourhoods = min(n_count, int(neighbourhoods))

    # Add top N neighbourhoods to map with circles
    for i in range(int(neighbourhoods)):
        NEIGHBOURHOOD_NAME = df.iloc[i,0]
        CRIMES = df.iloc[i,1]
        LAT = df.iloc[i,2]
        LON = df.iloc[i,3]
        # print(NEIGHBOURHOOD_NAME, CRIMES, LAT, LON)
        folium.Circle(
            location = [LAT, LON], # location
            popup = NEIGHBOURHOOD_NAME+'<br>'+str(CRIMES), # popup text 
            radius= int(CRIMES)*3, # size of radius in meteres
            color = "crimson", #color of the radius
            fill = True, # whether to fill the map
            fill_color= "crimson" # color to fill with
            ).add_to(m)

    # count task and save
    task3_count += 1
    title = "Q3-"+str(task3_count)+".html"
    m.save(title)


# task 4:Given a range of years and an integer N, show (in a map) the Top-N 
# neighbourhoods with the highest crimes to population ratio within the provided 
# range. Also, show the most frequent crime type in each of these neighbourhoods.
def task4():
    global task4_count

    # get inputs from user
    while True:
        try: 
            start = input("Enter start year (YYYY):")
            end = input("Enter end year (YYYY):")
            if int(start) >= 2009 and int(start) <=2018 and int(end) >= 2009 and int(end) <= 2018:
                break
            else:
                print("Please enter valid years between 2009 and 2018")
        except ValueError:
            print("Please enter valid years between 2009 and 2018")
            continue
    while True:
        try: 
            neighbourhoods = int(input("Enter number of neighbourhoods:"))
            if int(neighbourhoods) >= 0 and int(neighbourhoods) <=385:
                break
            else:
                print("Please enter a valid number of neighbourhoods (0-385)")
        except ValueError:
            print("Please enter a valid number of neighbourhoods (0-385)")
            continue

    # Run query
    query = "select a.Neighbourhood_Name, Crime_Type, sum(Incidents_Count) as Incidents_Sum, Latitude, Longitude, Ratio\
            from crime_incidents as a, coordinates as b, (select c.Neighbourhood_Name as Top_Neighbourhood, (sum(Incidents_Count)+0.0)/(CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE) as Ratio\
                    from crime_incidents as c, population as d, coordinates as e\
                    where c.Neighbourhood_Name = d.Neighbourhood_Name\
                    and c.Neighbourhood_Name = e.Neighbourhood_Name\
                    and Year>="+str(start)+" and Year<="+str(end)+"\
                    and (CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE)>0\
                    and Latitude > 0.1\
                    group by c.Neighbourhood_Name\
                    order by Ratio desc limit "+str(neighbourhoods)+") as f\
            where a.Neighbourhood_Name = b.Neighbourhood_Name\
            and f.Top_Neighbourhood = b.Neighbourhood_Name\
            and Year>="+str(start)+" and Year<="+str(end)+"\
            group by a.Neighbourhood_Name, Crime_Type"
    df = pd.read_sql_query(query, connection)
    df = df.loc[df.reset_index().groupby(['Neighbourhood_Name'])['Incidents_Sum'].idxmax()]

    # Create Map
    m = folium.Map(location=[53.540735,-113.496110], zoom_start=11)

    # Check to make sure the user inputted number of neighbourhood does not exceed the number returned by the sql query
    n_count = df.shape[0]
    neighbourhoods = min(n_count, int(neighbourhoods))

    # Add top N neighbourhoods to map with circles
    for i in range(int(neighbourhoods)):
        NEIGHBOURHOOD_NAME = df.iloc[i,0]
        CRIME = df.iloc[i,1]
        LAT = df.iloc[i,3]
        LON = df.iloc[i,4]
        RATIO = df.iloc[i,5]
        # print(NEIGHBOURHOOD_NAME, CRIMES, LAT, LON)
        folium.Circle(
            location = [LAT, LON], # location
            popup = NEIGHBOURHOOD_NAME+'<br>'+str(CRIME)+'<br>'+str(RATIO), # popup text 
            radius= int(RATIO)*300, # size of radius in meteres
            color = "crimson", #color of the radius
            fill = True, # whether to fill the map
            fill_color= "crimson" # color to fill with
            ).add_to(m)

    # count task and save
    task4_count += 1
    title = "Q4-"+str(task4_count)+".html"
    m.save(title)

# run the program
main()