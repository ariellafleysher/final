"""
Name:   Ariella Fleysher
CS230: Section 4
Data: McDonald's

Description: This program interacts with the user. The user is able to see a map of the McDonald's locations across the United States.
The web app allows the user to choose to see a bar chart of the top 5 cities with the most or least McDonald's compared to the average.
A pie chart is shown describing the percentage makeup by state of McDonald's locations compared to the other states that the user is
able to choose as well. A pivot table is used to describe a particular state's McDonald's store types and calculates the sum.

"""
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import seaborn as sns

new_file = "mcdonalds_clean1.csv"
df = pd.read_csv(new_file, names = ["lon", "lat", "Store Number", "Store Type", "Address", "City", "State", "Zip", "Phone Number", "Playplace", "Drive Through", "Arch Card", "Free Wifi", "Store URL"])
#df = pd.DataFrame(new_file, columns=["lat", "lon", "Store Number", "Store Type", "Address", "City", "State", "Zip", "Phone Number", "Playplace", "Drive Through", "Arch Card", "Free Wifi", "Store URL"])
df = df[1:]

#chart functions
#bar chart highest frequency of locations by city
def barchart_high():
    df1 = pd.read_csv("mcdonalds_clean1.csv")
    df1["index_col"] = df1.index
    states =  df1["state"].value_counts()
    top5_cities_by_state = df1.groupby("city")["state"].count().sort_values(ascending = False)[:5] #gets top 5 cities w highest number of mcdonalds locations
    #print(top5_cities_by_state)
    cities = df1["city"].value_counts()
    cities = cities.mean()
    city_labels = ["HOUSTON", "CHICAGO", "SAN ANTONIO", "LOS ANGELES", "LAS VEGAS"] #got values from printing the top 5 while writing code

    plt.subplots(figsize = (8,4))
    sns.barplot(x = top5_cities_by_state.index, y = top5_cities_by_state, order = top5_cities_by_state.index, palette = "plasma")

    plt.xticks(np.arange(5), city_labels, rotation = 75, size = 8) #relabel x with list above
    plt.hlines(cities, -.5 ,4.5, colors = "red", label = "Average McDonald's per City") # adds line to compare the average, the average looks off b/c there is an average of only 2 McDonald's per city, while the top 5 contain a much greater value
    plt.xlabel("Cities", size = 14)
    plt.ylabel("Frequency", size = 14)
    plt.title("Cities with the Highest Frequency of McDonald's", size = 16, y = 1.08)
    plt.legend()

#bar chart lowest frequency of locations by city
def barchart_low():
    df1 = pd.read_csv("mcdonalds_clean1.csv")
    df1["index_col"] = df1.index
    states =  df1["state"].value_counts()
    bottom5_cities_by_state = df1.groupby("city")["state"].count().sort_values(ascending = True)[:5] #gets top 5 cities w lowest number of mcdonalds locations
    #print(bottom5_cities_by_state)
    cities = df1["city"].value_counts()
    cities = cities.mean()
    city_labels = ["LOLO", "MONTVILLE", "MOON TOWNSHIP", "MOONVILLE", "MOOREFIELD"] #got values from printing the top 5 while writing code

    plt.subplots(figsize = (8,4))
    sns.barplot(x = bottom5_cities_by_state.index, y = bottom5_cities_by_state, order = bottom5_cities_by_state.index, palette = "plasma")

    plt.xticks(np.arange(5), city_labels, rotation = 75, size = 8) #relabel x with list above
    plt.hlines(cities, -.5 ,4.5, colors = "red", label = "Average McDonald's per City") #adds line to compare the average

    plt.xlabel("Cities", size = 14)
    plt.ylabel("Frequency", size = 14)
    plt.title("Cities with the Lowest Frequency of McDonald's", size = 16, y = 1.08)
    plt.legend()

#function to make pie chart
def piechart():
    df1 = pd.read_csv("mcdonalds_clean1.csv")
    #df1["index_col"] = df1.index
    #states =  df1["state"].value_counts()
    state_labels = ["CA", "TX", "FL", "IL", "NY", "OH", "MI", "PA", "NC", "GA",
                    "VA", "IN", "TN", "MO", "MD", "WI", "AZ", "WA", "NJ", "KY",
                    "AL", "LA", "MA", "SC", "MN", "CO", "OK", "AR", "OR", "NV",
                    "IA", "MS", "KS", "CT", "UT", "WV", "NM", "NE", "HI", "ID",
                    "ME", "NH", "MT", "DE", "RI", "DC", "AK", "SD", "VT", "WY",
                    "ND"]
    states_chosen = st.sidebar.multiselect("Select the states that you wish to see in the pie chart. ", state_labels)
    df1 = df1.loc[df1["state"].isin(states_chosen)]
    df1["index_col"] = df1.index
    states =  df1["state"].value_counts()
    plt.figure(figsize = (20,14))
    explode = np.zeros(len(states_chosen))
    colors = ["gray", "blue", "lightskyblue", "lightpink", "lightgreen", "lightblue", "steelblue", "purple", "cyan", "magenta", "wheat", "salmon"]
    labels = states_chosen
    plt.pie(states, labels = labels, startangle = 90, explode = explode, colors = colors, autopct = '%1.1f%%', shadow = True, labeldistance = 1.1, textprops = {'fontweight':'bold', 'fontsize': 18}, wedgeprops = {"linewidth": 3, "edgecolor" : "k"})
    plt.legend(loc=3, fontsize=15)
    plt.title("McDonald's Location Makeup by State", fontweight = "bold", fontsize = 21, pad = 20)
    plt.axis("equal")
    return plt

#function to make simple map
def map():
    MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"

    df2=df.copy()
    df2.drop(columns=["Store Number", "Store Type", "Address", "City","State","Zip","Phone Number","Playplace","Drive Through","Arch Card","Free Wifi","Store URL"])

    df2["lat"] = df2["lat"].astype(float)
    df2["lon"] = df2["lon"].astype(float)


    dfcoord = pd.DataFrame(df2, columns= ["lon", "lat"])
    #st.dataframe(dfcoord)
    st.write("Map of Mcdonald's Locations")
    st.text("This map shows the spread of McDonald's across the United States.\nFeel free to zoom in to any particular state or city you wish to explore more.")
    st.map(dfcoord)
    #view_state = pdk.ViewState(latitude=dfcoord["lat"].mean(), longitude=dfcoord["lon"].mean(), zoom=11, pitch=0)
    #tool_tip = {"html": "Coordinate:</b>({lat},{lon}})</b> ","style": { "backgroundColor": "black", "color": "white"}}
    #layer1 = pdk.Layer('ScatterplotLayer',data=dfcoord, get_position='[lon, lat]', get_radius=100, pickable=True)
    #map1 = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, mapbox_key=MAPKEY, layers=[layer1], tooltip=tool_tip)
    #st.pydeck_chart(map1)
    #above code for map is not working, dots will not show up, tutors don't know what the issue is

#function to make pivot table
def pivot_table(state,data):
    df_state = df[df['State'] == state]
    #sum_stores = df_state.sum()
    sum_types = df_state.pivot_table(index='Store Type', aggfunc='size')
    return sum_types

def main():
    st.title("Ariella Fleysher Final Project")
    map() #simple map
    st.set_option('deprecation.showPyplotGlobalUse', False) #lets user choose
    optionColumns = ["Highest", "Lowest"] #options to choose from
    dataSelection = st.sidebar.selectbox("Would you like to see a bar chart about the highest or lowest frequency of McDonald's in the United States by City? ", list(optionColumns))
    st.write("Bar Chart")
    if dataSelection == "Highest": #if user selects high, high bar chart function will be used, if low then low bar chart function will be used
        st.pyplot(barchart_high())
    elif dataSelection == "Lowest":
        st.pyplot(barchart_low())
    st.write("Pie Chart")
    st.text("Make sure to choose the states that you wish to see represented in the pie chart to\navoid any errors.")
    st.pyplot(piechart())
    state_labels = ["CA", "TX", "FL", "IL", "NY", "OH", "MI", "PA", "NC", "GA",
                    "VA", "IN", "TN", "MO", "MD", "WI", "AZ", "WA", "NJ", "KY",
                    "AL", "LA", "MA", "SC", "MN", "CO", "OK", "AR", "OR", "NV",
                    "IA", "MS", "KS", "CT", "UT", "WV", "NM", "NE", "HI", "ID",
                    "ME", "NH", "MT", "DE", "RI", "DC", "AK", "SD", "VT", "WY",
                    "ND"]
    state_chosen = st.sidebar.selectbox("Choose a state you would like to see a pivot table for the number of store types in that specific state. ", state_labels)
    st.write("Pivot Table")
    st.text("Below is a pivot table. The pivot table shows the make up of different store types\nof the specific state you chose has.")
    st.write(pivot_table(state_chosen, df))

main()

#matplotlib warning message when I try to run the code in pycharm, streamlit web app works completely fine though
