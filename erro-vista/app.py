import streamlit as st
import pandas as pd

# Set the app's configuration
st.set_page_config(page_title="EroVista EPA Configuration", layout="wide")

# Load the CSV file into a DataFrame
@st.cache_data
def load_table_data():
    csv_path = "erro-vista/data/data.csv"  # Update with the path to your data folder
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

st.title("EroVista EPA Configuration")

# Sidebar inputs for user selections
mount_type = st.sidebar.selectbox(
    "Mount Type", table_data["mount_type"].unique()
)
fixture_config = st.sidebar.selectbox(
    "Fixture Configuration", table_data["fixture_configuration"].unique()
)
pole_size = st.sidebar.selectbox(
    "Pole Size", table_data["ero_vista_pole_size"].unique()
)
pole_height = st.sidebar.selectbox(
    "Pole Height (ft)", table_data["pole_height_ft"].unique()
)
wind_speed = st.sidebar.selectbox(
    "Wind Speed (mph)", table_data["wind_speed_mph"].unique()
)

# Button to display results
if st.sidebar.button("Calculate Max Fixture EPA..."):
    try:
        filtered_data = table_data[
            (table_data["mount_type"] == mount_type) &
            (table_data["fixture_configuration"] == fixture_config) &
            (table_data["ero_vista_pole_size"] == pole_size) &
            (table_data["pole_height_ft"] == pole_height) &
            (table_data["wind_speed_mph"] == wind_speed)
        ]
        if not filtered_data.empty:
            cedar = filtered_data["Alaskan Yellow Cedar Poles"].values[0]
            pine = filtered_data["Southern Yellow Pine Poles"].values[0]

            # Handle cases where one or both values are 0
            cedar_message = f"**Alaskan Yellow Cedar Max Fixture EPA (ft<sup>2</sup>):** {cedar}" if cedar > 0 else "**Alaskan Yellow Cedar Max Fixture EPA:** Selected Configuration is not Possible"
            pine_message = f"**Southern Yellow Pine Max Fixture EPA (ft<sup>2</sup>):** {pine}" if pine > 0 else "**Southern Yellow Pine Max Fixture EPA:** Selected Configuration is not Possible"

            # Display results using your custom styling
            st.markdown(f"""
            <div class="content">
                <h1>Outcome</h1>
                <table>
                    <tr>
                        <th>Fixture Configuration</th>
                        <td>{fixture_config}</td>
                    </tr>
                    <tr>
                        <th>Pole Size</th>
                        <td>{pole_size}</td>
                    </tr>
                    <tr>
                        <th>Pole Height (ft)</th>
                        <td>{pole_height}</td>
                    </tr>
                    <tr>
                        <th>Wind Speed (mph)</th>
                        <td>{wind_speed}</td>
                    </tr>
                    <tr>
                        <th>Alaskan Yellow Cedar Max Fixture EPA (ft<sup>2</sup>)</th>
                        <td class="highlight">{'N/A' if cedar == 0 else cedar}</td>
                    </tr>
                    <tr>
                        <th>Southern Yellow Pine Max Fixture EPA (ft<sup>2</sup>)</th>
                        <td class="highlight">{'N/A' if pine == 0 else pine}</td>
                    </tr>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No matching data found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Ensure the app renders well on mobile devices
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)
# Add notes as footnotes
st.markdown("""
<div class="notes">
    <h2>Notes:</h2>
    <ol>
        <li>Design based on AASHTO LRFDLTS-1 using wind pressures derived from ASCE 7-10 and ASCE 7-16 using an Importance Factor of 1.0 and Wind Exposure C. EPAs are applicable for IBC 2015, 2018, and 2021.</li>
        <li>Poles are Alaskan Yellow Cedar or Southern Yellow Pine glue-laminated columns supplied by EroVista and manufactured in accordance with ANSI A190.1. Southern Yellow Pine poles are pressure treated to a retention level required for Use Category UC4B per AWPA UC-1 standard and are suitable for ground contact, contact with freshwater, and exposure to saltwater splash. Design values reduced for wet use conditions.</li>
        <li>Pole height is the distance from grade to the top of the pole.</li>
        <li>Total weight of fixtures assumed to be less than 50 lb. Maximum fixture offset of 24" assumed for side-mounted fixtures.</li>
        <li>Use of hot-dipped galvanized or stainless steel fasteners recommended. A gasket shall be used to isolate metal fixtures from treated SYP poles.</li>
        <li>Maximum Fixture EPA shown is for the total of all fixtures and attachment arms.</li>
    </ol>

    <h3>Minimum Embedment Below Grade (ft)</h3>
    <table>
        <thead>
            <tr>
                <th>Pole Size</th>
                <th>Gravel Soils</th>
                <th>Sandy Soils</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>5" x 5-1/2"</td>
                <td>3'-6"</td>
                <td>4'-0"</td>
            </tr>
            <tr>
                <td>6-3/4" x 6-3/4"</td>
                <td>4'-6"</td>
                <td>5'-0"</td>
            </tr>
            <tr>
                <td>8-1/4" x 8-1/2"</td>
                <td>5'-6"</td>
                <td>6'-0"</td>
            </tr>
        </tbody>
    </table>

    <ol start="7">
        <li>Recommended embedment depth based on pole being encased in a 24" diameter pier below grade or as designed by a licensed professional engineer.</li>
        <li>Direct embedment depth based on the following soil properties: Gravel Soils (GW, GP): φ = 34°, γ = 130 lb/ft³, c = 0 lb/ft². Sandy Soils (SW, SP, SM, SC, GM, GC): φ = 30°, γ = 120 lb/ft³, c = 0 lb/ft².</li>
    </ol>
</div>
""", unsafe_allow_html=True)
