import streamlit as st
import pandas as pd

# Set the app's configuration
st.set_page_config(page_title="EroVista® Pole Sizer", layout="wide")

# Custom CSS to hide Streamlit branding
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}  /* Hides the hamburger menu */
        footer {visibility: hidden;}    /* Hides the footer */
        footer:after {
            content: ''; 
            display: block; 
            position: relative; 
            color: transparent;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Title and image side by side
col1, col2 = st.columns([0.5, 6])  # Adjust column widths as needed
with col1:
    st.image("erro-vista/static/logo2.png", use_container_width=True)  # Replace with your image path

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
    for technical information, design tables, important design notes, and additional
    information.

    By clicking "Accept", you agree to these terms and conditions.
    """
    # Display the terms on the main page
    st.markdown(terms)
    accept_terms = st.checkbox("I accept the Terms and Conditions")

    if accept_terms:
        st.session_state.accepted_terms = True
    else:
        st.warning("You must accept the terms and conditions to use this tool.")
        st.stop()  # Stop further execution until terms are accepted

# Main page inputs for user selections
mount_type = st.selectbox(
    "Installation Type:", table_data["mount_type"].unique()
)
filtered_by_mount_type = table_data[table_data["mount_type"] == mount_type].reset_index(drop=True)

ordered_unique_fixture_values = [
    x for x in ["Single Top Mount Fixture", "Single Side Mount Fixture", "Two or More Side Mount Fixtures"]
    if x in filtered_by_mount_type["fixture_configuration"].unique()
]

fixture_config = st.selectbox(
    "Fixture Configuration:", ordered_unique_fixture_values
)
filtered_by_fixture_config = filtered_by_mount_type[filtered_by_mount_type["fixture_configuration"] == fixture_config].reset_index(drop=True)

wind_speed = st.selectbox(
    "Wind Speed (Vmph):", filtered_by_fixture_config["wind_speed_mph"].unique()
)
filtered_by_wind_speed = filtered_by_fixture_config[filtered_by_fixture_config["wind_speed_mph"] == wind_speed].reset_index(drop=True)

pole_height = st.selectbox(
    "Fixture Height (ft):", filtered_by_wind_speed["pole_height_ft"].unique()
)
filtered_by_pole_height = filtered_by_wind_speed[filtered_by_wind_speed["pole_height_ft"] == pole_height].reset_index(drop=True)

epa_value = st.number_input(
    "Combined EPA of Fixture(s):",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f"
)

filtered_by_epa = filtered_by_pole_height[
    (filtered_by_pole_height["epa"] >= epa_value) &
    (filtered_by_pole_height["epa"] > 0)
]

# Button to display results
if st.button("Calculate EroVista Pole Size"):
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
            ayc_pole_sizes = filtered_data[filtered_data['wood_type'] == 'AYC']["ero_vista_pole_size"].unique()
            syp_pole_sizes = filtered_data[filtered_data['wood_type'] == 'SYP']["ero_vista_pole_size"].unique()

            cedar_message = f"{', '.join(map(str, ayc_pole_sizes))}" if len(ayc_pole_sizes) > 0 else "No Solution"
            pine_message = f"{', '.join(map(str, syp_pole_sizes))}" if len(syp_pole_sizes) > 0 else "No Solution"

            # Display the first table
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

            # Display the second table
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

# Add notes at the bottom
st.markdown("""
<div class="notes" style="font-size: 10px;">
    <h3>Notes:</h3>
    <ol>
            <li>For poles directly embedded into the soil, consult with a licensed civil engineer and refer to EroVista's Specification Sheet for minimum embedment depth recommendations and important design information. Pole height + embedment depth = overall length of pole.</li>
            <li>Pole height + embedment depth = overall length of pole.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
