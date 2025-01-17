import streamlit as st
import pandas as pd

# Set the app's configuration
st.set_page_config(page_title="EroVista&reg; Pole Sizer", layout="wide")

# Title and image side by side
col1, col2 = st.columns([0.5, 6])  # Adjust column widths as needed
with col1:
    st.image("erro-vista/static/logo2.png", use_container_width=True) # Replace with your image path and adjust width

with col2:
    st.title("EroVista® Pole Sizer")

# Load the CSV file into a DataFrame
@st.cache_data
def load_table_data():
    csv_path = "erro-vista/data/data2.csv"  # Update with the path to your data folder
    data = pd.read_csv(csv_path)
    return data

# Load data
table_data = load_table_data()

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("erro-vista/static/style.css")

# Initialize session_state to track terms acceptance
if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

# Display the Terms and Conditions if the user has not accepted them
if not st.session_state.accepted_terms:
    terms = """
    ## Terms and Conditions

    The use of the EroVista Pole Sizer application is for sales presentation only and is not
    to be construed as an engineer's evaluation of the project. Always consult with a
    licensed specifier and refer to EroVista's specification page at [erovista.net/specification](https://erovista.net/specification) 
    for technical information, design tables, important design notes and additional
    information.

    By clicking "Accept", you agree to these terms and conditions.

    """

    # Display the terms on the main page
    st.markdown(terms)

    # Ask the user to accept the terms before proceeding
    accept_terms = st.checkbox("I accept the Terms and Conditions")

    if accept_terms:
        st.session_state.accepted_terms = True  # Set the flag to True when accepted
    else:
        st.warning("You must accept the terms and conditions to use this tool.")
        st.stop()  # This stops further execution until terms are accepted

# Sidebar inputs for user selections (will only show if terms are accepted)
mount_type = st.sidebar.selectbox(
    "Installation Type", table_data["mount_type"].unique()
)
filtered_by_mount_type = table_data[table_data["mount_type"] == mount_type].reset_index(drop=True)


# Ensure the unique values are properly matched and ordered
ordered_unique_fixture_values = [
    x for x in ["Single Top Mount Fixture", "Single Side Mount Fixture", "Two or More Side Mount Fixtures"]
    if x in filtered_by_mount_type["fixture_configuration"].unique()
]

# Sidebar for fixture configuration
fixture_config = st.sidebar.selectbox(
    "Fixture Configuration", ordered_unique_fixture_values
)

filtered_by_fixture_config = filtered_by_mount_type[filtered_by_mount_type["fixture_configuration"] == fixture_config].reset_index(drop=True) 


wind_speed = st.sidebar.selectbox(
    "Wind Speed (Vmph)", filtered_by_fixture_config["wind_speed_mph"].unique()
)
filtered_by_wind_speed = filtered_by_fixture_config[filtered_by_fixture_config["wind_speed_mph"] == wind_speed].reset_index(drop=True)

pole_height = st.sidebar.selectbox(
    "Fixture Height (from top of pedestal foundation or soil line)", filtered_by_wind_speed["pole_height_ft"].unique()
)

filtered_by_pole_height = filtered_by_wind_speed[filtered_by_wind_speed['pole_height_ft'] == pole_height].reset_index(drop=True)

epa_value = st.sidebar.number_input(
    "Combined EPA of Fixture(s)", 
    min_value=0.0, 
    value=0.0, 
    step=0.01, 
    format="%.2f"
)

filtered_by_epa = filtered_by_pole_height[(
    filtered_by_pole_height["epa"] >= epa_value) & 
    (filtered_by_pole_height["epa"] > 0)
]

# Button to display results
if st.sidebar.button("Calculate EroVista Pole Size"):
    try:
        filtered_data = table_data[
            (table_data["mount_type"] == mount_type) &
            (table_data["fixture_configuration"] == fixture_config) &
            (table_data["epa"] >= epa_value) &
            (table_data["epa"] > 0) &
            (table_data["pole_height_ft"] == pole_height) &
            (table_data["wind_speed_mph"] == wind_speed)
        ]
        
        if not filtered_data.empty:
            # Get all unique ero_vista_pole_size values for AYC and SYP
            ayc_pole_sizes = filtered_data[filtered_data['wood_type'] == 'AYC']["ero_vista_pole_size"].unique()
            syp_pole_sizes = filtered_data[filtered_data['wood_type'] == 'SYP']["ero_vista_pole_size"].unique()

            # Check if matching AYC and SYP pole sizes exist
            if len(ayc_pole_sizes) > 0:
                cedar_message = f"{', '.join(map(str, ayc_pole_sizes))}"
            else:
                cedar_message = "No Solution"

            if len(syp_pole_sizes) > 0:
                pine_message = f"{', '.join(map(str, syp_pole_sizes))}"
            else:
                pine_message = "No Solution"

            # Display results using your custom styling
            st.markdown(f"""
            <div class="content">
                <h1>Recommended Solutions:</h1>
                <table>
                    <tr>
                        <th>Fixture Configuration</th>
                        <td>{fixture_config}</td>
                    </tr>
                    <tr>
                        <th>Fixture Height (ft)</th>
                        <td>{pole_height}</td>
                    </tr>
                    <tr>
                        <th>Wind Speed (Vmph)</th>
                        <td>{wind_speed}</td>
                    </tr>
                    <tr>
                        <th>Combined EPA of Fixture(s) (ft<sup>2</sup>)</th>
                        <td>{epa_value}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # Display the second table for minimum section sizes
            st.markdown(f"""
            <div class="content">
                <h2>Minimum Section Size(s):</h2>
                <table>
                    <tr style="background-color: lightgray;">
                        <th>Alaskan Yellow Cedar</th>
                        <td class="highlight">{cedar_message}</td>
                    </tr>
                    <tr style="background-color: yellow; color: black; font-weight: bold;">
                        <th>Treated Southern Yellow Pine</th>
                        <td>{pine_message}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No matching data found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Ensure the app renders well on mobile devices
st.markdown("""<meta name="viewport" content="width=device-width, initial-scale=1.0">""", unsafe_allow_html=True)

# Add notes at the bottom with smaller font size (only show after accepting terms)
if st.session_state.accepted_terms:
    st.markdown("""
    <div class="notes" style="font-size: 10px;">
        <h3>Notes:</h3>
        <ol>
            <li>Design based on AASHTO LRFDLTS-1 using wind pressures derived from ASCE 7-10 and ASCE 7-16 using an Importance Factor of 1.0 and Wind Exposure C. EPAs are applicable for IBC 2015, 2018, and 2021.</li>
            <li>Poles are Alaskan Yellow Cedar or Southern Yellow Pine glue-laminated columns, supplied by EroVista and manufactured in accordance with ANSI A190.1. Southern Yellow Pine poles are pressure treated to a retention level required for Use Category UC4B per AWPA UC-1 standard and are suitable for ground contact, contact with freshwater, and exposure to saltwater splash. Design values reduced for wet use conditions.</li>
            <li>Pole height is the distance from grade to the top of the pole.</li>
            <li>Total weight of fixtures is assumed to be less than 50 lb. Maximum fixture offset of 24" assumed for side-mounted fixtures.</li>
            <li>Use of hot-dipped galvanized or stainless steel fasteners recommended. A gasket shall be used to isolate metal fixtures from treated Southern Yellow Pine poles.</li>
            <li>Maximum Fixture EPA shown is for the total of all fixtures and attachment arms.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
