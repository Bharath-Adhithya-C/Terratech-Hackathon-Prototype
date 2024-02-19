import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
import plotly.express as px

# Function to fetch latitude and longitude based on pin code
def get_coordinates(data, crop_id):
    # Filter data based on the entered crop ID
    filtered_data = data[data['CROP ID'] == crop_id]
    
    # Initialize an empty list to store coordinates
    coordinates = []

    # Iterate over filtered data to get coordinates for each pin code
    for index, row in filtered_data.iterrows():
        pin_code = row['PIN CODE']
        lat, lon = fetch_lat_lon(pin_code)
        coordinates.append((lat, lon))

    return coordinates

# Example function to fetch latitude and longitude based on pin code
def fetch_lat_lon(pin_code):
    # Example function to map pin codes to coordinates
    # Replace this function with your actual pin code to coordinates mapping logic
    if pin_code == 422210:
        return (19.8762, 75.3433)  # Example coordinates for pin code 422210
    elif pin_code == 422105:
        return (19.8708, 75.3438)  # Example coordinates for pin code 422105
    else:
        return (0, 0)  # Default coordinates if pin code not found

def load_data(csv_file):
    data = pd.read_csv(csv_file)
    return data

def main():
    st.title("Crop Analysis Dashboard")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload Crop Data CSV", type=["csv"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        # Display map or data analysis based on user choice
        analysis_choice = st.radio("Select Analysis:", ("Map", "Data Analysis"))

        if analysis_choice == "Map":
            # Get unique crop IDs from the data
            crop_ids = data['CROP ID'].unique()

            # User input for crop ID
            crop_id = st.selectbox("Select Crop ID:", crop_ids)

            # Get coordinates based on the selected crop ID
            coordinates = get_coordinates(data, crop_id)

            # Create map centered on India
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

            # Add markers for each pin code
            for lat, lon in coordinates:
                folium.Marker(location=[lat, lon]).add_to(m)

            # Display the map
            st.write("### Crop Pin Code Map:")
            folium_static(m)

        elif analysis_choice == "Data Analysis":
            st.subheader("Crop Production Data Analysis")

            # Get unique pin codes
            unique_pin_codes = data['PIN CODE'].unique()

            # Filter by Pin Code
            pin_code_selection = st.selectbox('Select Pin Code:', unique_pin_codes)

            # Filter data by selected Pin Code
            filtered_df = data[data['PIN CODE'] == pin_code_selection]

            # Define color sequence
            color_sequence = px.colors.qualitative.Plotly

            # Plot bar chart for Crop Production by Crop ID
            bar_chart = px.bar(filtered_df, 
                               x='CROP ID', 
                               y='CROP PRODUCTION',
                               text='CROP PRODUCTION',
                               color='CROP NAME',
                               template='plotly_white',
                               title='Crop Production by Crop ID',  # Add title
                               labels={'CROP PRODUCTION': 'Crop Production', 'CROP ID': 'Crop ID'},  # Update axis labels
                               width=800,  # Adjust chart width
                               height=500,  # Adjust chart height
                               hover_name='CROP NAME',  # Add hover information
                               hover_data={'CROP ID': False},  # Specify hover data
                               color_discrete_sequence=color_sequence  # Use the same color sequence
                              )

            bar_chart.update_layout(
                xaxis=dict(tickfont=dict(size=12)),  # Update x-axis tick font size
                yaxis=dict(tickfont=dict(size=12)),  # Update y-axis tick font size
                font=dict(size=12, color='black'),  # Change global font size and color
                plot_bgcolor='rgba(0,0,0,0)',  # Make plot background transparent
                paper_bgcolor='rgba(0,0,0,0)',  # Make paper background transparent
                showlegend=True,  # Show legend
                legend=dict(title='Crop Name', font=dict(size=12)),  # Update legend font size
            )

            # Remove gridlines
            bar_chart.update_xaxes(showgrid=False)
            bar_chart.update_yaxes(showgrid=False)

            # Update hover label background color and font size
            bar_chart.update_traces(hoverlabel=dict(bgcolor='white', font_size=12))

            # Adjust bar width
            bar_chart.update_traces(marker=dict(line=dict(width=1, color='gray')))

            # Display the bar chart
            st.plotly_chart(bar_chart, use_container_width=True)

            # Plot pie chart for Crop Production by Crop Name
            pie_chart = px.pie(filtered_df, 
                               names='CROP NAME', 
                               values='CROP PRODUCTION',
                               title='Crop Production Distribution by Crop Name',
                               width=800,  # Adjust chart width
                               height=500,  # Adjust chart height
                               color_discrete_sequence=color_sequence  # Use the same color sequence
                              )

            # Display the pie chart
            st.plotly_chart(pie_chart, use_container_width=True)

if __name__ == "__main__":
    main()
