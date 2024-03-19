# Required libraries for the script functionality
import requests  # For making API requests to the PVGIS API
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For plotting monthly production data
import folium  # For creating interactive maps with satellite imagery
import streamlit as st # Core Streamlit library for creating web apps
from streamlit_folium import st_folium

#Title section 
st.title('PV Production Estimator') 
repo_url = 'https://github.com/aswath-space/pv-estimator' 
st.markdown(f'By Aswath Subramanian. You can find the GitHub repo [here]({repo_url}).')

def prompt_for_location_and_panel_details():
    """
    Uses Streamlit widgets to prompt the user for the geographic location by address and panel specifications.
    
    Provides an input field for an address and offers a dropdown for selecting the watt-peak of a single solar panel from predefined options.
    Uses the Nominatim API to convert the address to latitude and longitude coordinates.
    
    Displays:
    - Text input for address.
    - Dropdown for selecting panel watt-peak.
    
    Returns:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - panel_watt_peak (int): The selected watt-peak of a single panel, determining its maximum output under ideal conditions.
    """
    # Streamlit widget for user address input
    address_input = st.text_input("Enter the address of the location:", "")
    
    # Dropdown for selecting panel watt-peak
    panel_watt_peak_options = [395, 415, 430]
    panel_watt_peak = st.selectbox("Select the watt-peak of a single panel (in watts):", options=panel_watt_peak_options)

    # Use Nominatim API to convert address to coordinates
    if address_input:
        try:
            nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={address_input}"
            response = requests.get(nominatim_url)
            if response.status_code == 200:
                response_json = response.json()
                if response_json:
                    lat = float(response_json[0]['lat'])
                    lon = float(response_json[0]['lon'])
                else:
                    st.error("Could not find location. Please enter a more specific address.")
                    return None, None, None
            else:
                st.error(f"Failed to fetch coordinates. HTTP status code: {response.status_code}")
                return None, None, None
        except Exception as e:
            st.error(f"An error occurred while fetching the coordinates: {e}")
            return None, None, None
    else:
        eturn None, None, None


    return lat, lon, panel_watt_peak

def display_location_on_map_with_satellite(lat, lon):
    """
    Displays the specified location on an interactive map using ESRI Satellite imagery within a Streamlit app.

    This function creates a Folium map centered at the given latitude and longitude, adds a marker for the location,
    and overlays it with ESRI's World Imagery tile layer for high-resolution satellite images. It then uses the
    streamlit_folium package to display this interactive map in a Streamlit application.

    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.

    The function directly renders the map in the Streamlit app, thus it does not return a value.
    """
    # Map initialization with ESRI Satellite imagery
    m = folium.Map(location=[lat, lon], zoom_start=18)
    
    esri_imagery = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.Marker([lat, lon], popup='Location').add_to(m)
    folium.LayerControl().add_to(m)  # Adds layer control to toggle between map layers
    
    # Use st_folium to display the Folium map in Streamlit, instead of returning the map object
    st_folium(m, width=725, height=500)

def prompt_for_arrays():
    """
    Uses Streamlit widgets to collect user input for configuring up to four PV arrays.
    
    Provides input fields for the number of panels, pitch (tilt angle), azimuth (orientation),
    and a dropdown for shading level. The shading level input adjusts the annual production based on predefined loss percentages.
    
    Returns:
    - arrays_info (list of dicts): A list containing configuration details for each array, including shading loss.
    """
    shading_levels = ['Low', 'Moderate', 'High', 'Extreme']
    shading_loss_mapping = {'Low': 6, 'Moderate': 12, 'High': 18, 'Extreme': 30}
    
    arrays_info = []

    for i in range(1, 5):  # Assuming up to 4 arrays
        with st.expander(f"Array {i} Configuration", expanded=True if i == 1 else False):
            enabled = st.checkbox(f"Enable Array {i}", value=True if i == 1 else False, key=f"enable_{i}")
            
            if enabled:
                panels = st.number_input("Enter the number of panels:", min_value=1, value=10, key=f"panels_{i}")
                pitch = st.number_input("Enter the pitch (tilt angle) in degrees:", min_value=0, max_value=90, value=35, key=f"pitch_{i}")
                azimuth = st.number_input("Enter the azimuth (orientation) in degrees:", value=0, key=f"azimuth_{i}")
                shading_input = st.selectbox("Select the shading level:", options=shading_levels, index=0, key=f"shading_{i}")
                
                array_info = {
                    'panels': panels,
                    'pitch': pitch,
                    'azimuth': azimuth,
                    'shading_loss': shading_loss_mapping[shading_input]
                }
                arrays_info.append(array_info)
    
    return arrays_info

def get_pv_production_for_multiple_arrays(lat, lon, panels_info, panel_watt_peak):
    """
    Fetches and compares PV estimates for multiple arrays with varying configurations in Streamlit.
    
    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - panels_info (list of dicts): Detailed configurations for each array, including shading impact.
    - panel_watt_peak (float): Watt-peak of a single panel.
    
    Displays in Streamlit:
    - A table comparison of monthly energy production for all arrays and their total.
    - A bar chart of the total monthly PV production.
    - The grand total annual energy production for all arrays is also returned and displayed.
    """
    df_monthly = pd.DataFrame(index=range(1, 13))
    df_monthly.index.name = 'Month'
    total_annual_production = 0

    for i, array_info in enumerate(panels_info, start=1):
        peak_power = array_info['panels'] * panel_watt_peak / 1000  # Convert to kWp
        tilt = array_info['pitch']
        azimuth = array_info['azimuth']
        
        system_loss = 14 + array_info['shading_loss']  # Base loss + shading loss
        api_url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
        params = {
            'lat': lat,
            'lon': lon,
            'peakpower': peak_power,
            'loss': system_loss,
            'mountingplace': 'building',
            'angle': tilt,
            'aspect': azimuth,
            'outputformat': 'json'
        }
        
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            monthly_data = data['outputs']['monthly']['fixed']
            monthly_production = [month['E_m'] for month in monthly_data]
            df_monthly[f'Array {i} (Azimuth {azimuth})'] = monthly_production
            total_annual_production += data['outputs']['totals']['fixed']['E_y']
        else:
            st.error(f'Failed to fetch data for Array {i} (Azimuth {azimuth})')
            return None, 'Failed to fetch data from PVGIS API'
    
    df_monthly['Total'] = df_monthly.sum(axis=1)
    df_monthly.loc['Total per Array'] = df_monthly.drop('Total', axis=1).sum()
    df_monthly_transposed = df_monthly.transpose()
    
    # Displaying the DataFrame in Streamlit
    #st.write("Monthly Production Comparison:", df_monthly_transposed)
    
   # Plotting the total monthly PV production for visual analysis
    fig, ax = plt.subplots()
    df_monthly['Total'].plot(kind='bar', ax=ax)

    # Assuming you have 12 months of data, explicitly setting the x-ticks to match
    ax.set_xticks(range(12))  # Set 12 x-ticks for the 12 months
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

    ax.set_ylabel('Energy Production (kWh)')
    ax.set_xlabel('Month')
    ax.set_title('Total Monthly PV Production')

    st.pyplot(fig)

    
    # Displaying the grand total annual production
    #st.write(f"Grand Total Annual Production: {total_annual_production} kWh")
    
    # Note: Returning the DataFrame and total annual production is optional unless needed for further processing
    return df_monthly_transposed, total_annual_production


# Main execution block
st.header('Input Parameters')
lat, lon, panel_watt_peak = prompt_for_location_and_panel_details()

# Collect panels info right after the panel watt-peak selection
panels_info = prompt_for_arrays()

# Proceed only if we have valid latitude and longitude
if lat is not None and lon is not None:
    st.header('Visualization')
    display_location_on_map_with_satellite(lat, lon)

    st.header('Production Estimates')
    if st.button('Calculate PV Production') and panels_info:
        monthly_production_comparison, grand_total_annual_production = get_pv_production_for_multiple_arrays(lat, lon, panels_info, panel_watt_peak)
        if monthly_production_comparison is not None:
            st.dataframe(monthly_production_comparison)
            st.metric(label="Grand Total Annual Production", value=f"{grand_total_annual_production} kWh")
        else:
            st.error("Failed to calculate PV production.")
else:
    st.error("Please enter a valid address to proceed.")