"""
Class: CS230
Name: Daniela
Final Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit as st
from geopy.geocoders import Nominatim


# Load Starbucks location data
def background_color_change(color="#3b3b3b"):
    page_bg_img = f"""
    <style>

    [data-testid="stAppViewContainer"] {{
    background: {color};
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


def read_df():
    data = pd.read_csv("/Users/danielaluzzi/Downloads/starbucks_10000_sample.csv")
    return data


data = read_df()


# Function to calculate distance between two points
# found out how to do this online
def calculate_distance(point1, point2=(
40.7128, 74.0060)):  # [PY1] A function with two or more parameters, one of which has a default value
    lat1, lon1 = point1
    lat2, lon2 = point2
    radius = 6371  # Earth radius in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) * np.sin(dlat / 2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(
        dlon / 2) * np.sin(dlon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = radius * c
    return distance


def find_cooridnates(location, write=True):  # [PY2] A function that returns more than one value & [PY3] A function that
    # returns a value and is called in at least two different places in your program
    loc = Nominatim(user_agent="Geopy Library")
    getlocation = loc.geocode(location)
    if write:
        st.write(f"location= {getlocation.address}")

    return getlocation.latitude, getlocation.longitude


def get_user_address():
    address = st.text_input("Enter your current address:")
    st.subheader("OR Select Below:")
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.selectbox("Country", data[
            "CountryCode"].unique())  # [ST3] At least three Streamlit different widgets (drop down / selectbox)
    with col2:
        state = st.selectbox("State", data[data["CountryCode"] == country]["CountrySubdivisionCode"].unique())
    with col3:
        city = st.selectbox("City", data[(data["CountryCode"] == country) & (data["CountrySubdivisionCode"] == state)][
            "City"].unique())

    if address and address != "":
        return address
    elif st.button("Find Starbucks Locations", use_container_width=True):
        return str(city + "," + state + "," + country)
    return str(city + "," + state + "," + country)


def first_page():
    address = get_user_address()

    user_coords = find_cooridnates(address)
    st.write("latitude= ", find_cooridnates(address, write=False)[0], "| ", " longitude= ",
             find_cooridnates(address, write=False)[1])
    radius = st.slider("Select radius (km):", min_value=1, max_value=50,
                       value=5)  # [ST2] At least three Streamlit different widgets (sliders)

    # Calculate distances and find nearby Starbucks stores
    data['Distance'] = data.apply(lambda row: calculate_distance((row['Latitude'], row['Longitude']), user_coords),
                                  axis=1)  # [DA1] Cleaning or manipulating data, lambda function (if covered in class) &[DA9] performing calculations on Data Frame columns
    nearby_stores = data[
        data['Distance'] <= radius]  # [DA4] Filtering data by one condition # [PY4] A list comprehension

    # sort the stores by distance
    nearby_stores = nearby_stores.sort_values(
        by='Distance')  # [DA2] Sorting data in ascending or descending order, by one or more columns,
    # show us all nearby Starbucks stores on map
    st.subheader("Nearby Starbucks Stores")

    label = "Map Theme (Light | Dark)"
    dark_mode = st.toggle(label, False)  # [ST1] At least three Streamlit different widgets (toggle)
    st.subheader("Zoom in the map to see the Starbucks spots flagged in Red")

    if dark_mode:
        map_style = 'mapbox://styles/mapbox/dark-v10'
    else:
        map_style = 'mapbox://styles/mapbox/light-v9'

    st.pydeck_chart(pdk.Deck(
        # [VIZ1] OR [VIZ4] (i think there was a typo in the assignment tags) At least one detailed map (st.map will only get you partial credit) - for full credit, include dots, icons, text that appears when hovering over a marker, or other flap features

        map_style=map_style,
        initial_view_state=pdk.ViewState(
            latitude=user_coords[0],
            longitude=user_coords[1],
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=nearby_stores,
                get_position='[Longitude, Latitude]',
                get_radius=200,
                get_fill_color=[255, 0, 0],
                pickable=True,
            ),
        ],
    ))

    # Display distances to nearby Starbucks stores
    st.subheader(
        f"Distances to Nearby Starbucks Stores ({len(nearby_stores)} stores in selected radius)")  # [DA7] Add/drop
    # /select/create new/group columns, frequency count, other features

    for index, row in nearby_stores.iterrows():  # [DA8] Iterating through rows of a DataFrame with iterrows
        st.write(f'''{row['Name']}: {str(f"{row['Distance']:.2f}")} km''')


def main():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<header style = "color: #007146 ; font-size: 75px; font-weight: 900;">Starbucks</header>',
                    unsafe_allow_html=True)  # [ST4] Page design features (sidebar, fonts, colors, images, navigation)
        st.title("Location Finder")
    with col2:
        st.image("/Users/danielaluzzi/Downloads/Starbucks-Logo.png")  # [ST4] Page design features (images)

    col1, col2, col3 = st.columns(3)
    with col1:
        color = st.color_picker("choose background color")
    with col2:
        pass
    with col3:
        pass

    background_color_change(color)
    first_page()


if __name__ == "__main__":
    main()

