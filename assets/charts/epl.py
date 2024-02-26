import csv
import requests
from io import BytesIO
import zipfile
import os
import plotly.graph_objects as go

def download_and_unzip(url, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the zip file
    response = requests.get(url)
    zip_file = zipfile.ZipFile(BytesIO(response.content))

    # Extract the contents of the zip file
    zip_file.extractall(output_dir)

    # Get the list of extracted files
    extracted_files = zip_file.namelist()

    # Close the zip file
    zip_file.close()

    # Return the list of extracted files
    return extracted_files

def publication_trend_line_chart(file_path):
    year_counts = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year_str = row['Año publicación']
            if year_str != 'N/A':
                try:
                    year = int(year_str[:4])  # Extract first four characters and convert to integer
                    if year in year_counts:
                        year_counts[year] += 1
                    else:
                        year_counts[year] = 1
                except ValueError:
                    print(f"Ignoring invalid year value: {year_str}")
    
    # Sort the year_counts by year
    sorted_year_counts = dict(sorted(year_counts.items()))

    # Create Plotly line chart
    fig = go.Figure(data=go.Scatter(x=list(sorted_year_counts.keys()), y=list(sorted_year_counts.values()), mode='lines'))
    fig.update_layout(title='Libros publicados por año',
                      xaxis_title='Año',
                      yaxis_title='Cantidad de libros')
    #fig.show()
    fig.write_html("publicacion.html")

def genre_distribution_bar_chart(file_path):
    genre_counts = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            genres = row['Géneros'].split(';')
            for genre in genres:
                genre = genre.strip()
                # Check if the genre contains a comma
                if ',' in genre:
                    # Split the genre string by comma and get the first part
                    main_genre = genre.split(',')[0].strip()
                    # Increment the count for the main genre
                    if main_genre in genre_counts:
                        genre_counts[main_genre] += 1
                    else:
                        genre_counts[main_genre] = 1
                else:
                    # Increment the count for the genre
                    if genre in genre_counts:
                        genre_counts[genre] += 1
                    else:
                        genre_counts[genre] = 1
    
    # Create Plotly bar chart
    fig = go.Figure(data=[go.Bar(x=list(genre_counts.keys()), y=list(genre_counts.values()))])
    fig.update_layout(title='Cantidad de libros por género',
                      xaxis_title='Género',
                      yaxis_title='Cantidad de libros')
    fig.write_html("genero.html")
    #fig.show()

def language_distribution_pie_chart(file_path):
    language_counts = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            language = row['Idioma']
            if language in language_counts:
                language_counts[language] += 1
            else:
                language_counts[language] = 1
    
    # Create Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=list(language_counts.keys()), values=list(language_counts.values()))])
    fig.update_traces(textposition='inside', textinfo='label+percent', insidetextfont=dict(color='#FFFFFF'))
    fig.update_layout(title='Cantidad de libros por idioma')
    fig.write_html("idiomas.html")
    #fig.show()

# Example usage
download_url = 'https://rss.epublibre.org/csv'
output_directory = './downloaded_files'
extracted_files = download_and_unzip(download_url, output_directory)
csv_file_path = os.path.join(output_directory, extracted_files[0])
publication_trend_line_chart(csv_file_path)
genre_distribution_bar_chart(csv_file_path)
language_distribution_pie_chart(csv_file_path)
