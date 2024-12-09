import streamlit as st
import pandas as pd

# Load the CSV file into a DataFrame
@st.cache
def load_table_data():
    csv_path = "erro-vista/data/data.csv"  # Update with the path to your data folder
    # print("Current working directory:", os.getcwd())
    # print("Checking if file exists:", os.path.exists(csv_path))
    # print(csv_path)
    data = pd.read_csv(csv_path)
    return data

# Load data
table_data = load_table_data()

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("static/style.css")

st.title("EroVista EPA Configuration")

# Dropdowns based on unique values in the CSV
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

            # Display results using your custom styling
            st.markdown("""
            <div class="content">
                <h1>Outcome</h1>
                <table>
                    <tr>
                        <th>Fixture Configuration</th>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <th>Pole Size</th>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <th>Pole Height (ft)</th>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <th>Wind Speed (mph)</th>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <th>Alaskan Yellow Cedar</th>
                        <td class="highlight">{}</td>
                    </tr>
                    <tr>
                        <th>Southern Yellow Pine</th>
                        <td class="highlight">{}</td>
                    </tr>
                </table>
            </div>
            """.format(
                fixture_config, pole_size, pole_height, wind_speed, cedar, pine
            ), unsafe_allow_html=True)
        else:
            st.error("No matching data found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
