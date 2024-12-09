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
                </table>
                # <p>{cedar_message}</p>
                # <p>{pine_message}</p>
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
