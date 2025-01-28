import requests
from bs4 import BeautifulSoup

url = "https://hardstyle.com/en/music/update?artist=&year=&genre=&label=Savage%20Squad%20Recordings"

response = requests.get(url)

# Ensure the page was fetched successfully
if response.status_code != 200:
    print(f"Failed to retrieve page, status code: {response.status_code}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the track blocks (including nested divs)
    track_blocks = soup.find_all('div', class_='track')

    # Initialize the set to store unique track data
    tracks_data = []
    seen_tracks = set()  # Set to track already seen tracks

    for track in track_blocks:
        track_data = {}

        # Extract Track Title and Link
        title_tag = track.find('a', class_='linkTitle trackTitle')
        if title_tag:
            track_data['track_title'] = title_tag.text.strip()
            track_data['track_link'] = title_tag['href']
        else:
            track_data['track_title'] = "No title"
            track_data['track_link'] = "No link"

        # Use a tuple of track_title and track_link to identify duplicates
        track_id = (track_data['track_title'], track_data['track_link'])

        if track_id not in seen_tracks:
            seen_tracks.add(track_id)

            # Extract Artist Names
            artists_tags = track.find_all('a', class_='highlight')
            track_data['artists'] = [artist.text.strip() for artist in artists_tags] if artists_tags else ["No artists"]

            # Extract Image URL
            image_tag = track.find('img')
            track_data['image_url'] = image_tag['src'] if image_tag else "No image"
            
            # Append the track data to the list
            tracks_data.append(track_data)

    # Generate the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Track Releases</title>
            <style>
                @font-face {
                    font-family: 'BodyFont';
                    src: url('fonts/BodyFont.otf') format('opentype');
                }

                @font-face {
                    font-family: 'TitleFont';
                    src: url('fonts/TitleFont.ttf') format('truetype');
                }

                /* Basic reset */
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }

                body {
                    background-color: rgb(16 16 17);
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }

                .container {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);  /* 4 columns in a row */
                    gap: 20px;
                    width: 100%;
                    padding: 10px;
                    margin: 0;
                    max-width: 100%;
                }

                .card {
                    background-color: rgb(16, 16, 17);
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    padding: 20px;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: flex-start;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    margin-bottom: 2em;
                    text-decoration: none;
                    height: 100%;
                    min-height: 400px;
                    position: relative;  /* Adding position relative to ensure transform works */
                }

                /* Hover effect for the card */
                .card:hover {
                    transform: scale(1.1);  /* Making the scale more noticeable */
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                }

                .card img {
                    height: 200px;
                    width: 200px;
                    object-fit: cover;
                    border-radius: 8px;
                }

                .card h3 {
                    color: white;
                    font-size: 1.8rem;
                    margin-top: 0.9em;
                    font-family: 'TitleFont', sans-serif;
                    text-transform: lowercase;
                    flex-grow: 0;
                    flex-shrink: 0;
                    text-align: center;
                }

                .card h3::first-letter {
                    text-transform: uppercase;
                }

                /* Paragraph styling (artists) */
                .card p {
                    color: #666;
                    font-size: 0.8rem;
                    margin-top: 0.7em;
                    font-family: 'BodyFont', sans-serif;
                    text-transform: uppercase;
                    flex-grow: 1;
                    text-align: center;
                }

                /* Responsiveness: stack cards on smaller screens */
                @media (max-width: 1024px) {
                    .container {
                        grid-template-columns: repeat(2, 1fr);  /* 2 columns on medium screens */
                    }
                }

                @media (max-width: 768px) {
                    .container {
                        grid-template-columns: 1fr;  /* 1 column on small screens */
                    }
                }
            </style>
        </head>
    <body>

        <div class="container">
    """

    # Add track data to the card layout
    for track in tracks_data:
        html_content += f"""
        <a href="https://hardstyle.com{track['track_link']}" class="card">
            <img src="https://hardstyle.com{track['image_url']}" alt="{track['track_title']}">
            <h3>{track['track_title']}</h3>
            <p>{', '.join(track['artists'])}</p>
        </a>
        """

    # Close the container and HTML tags
    html_content += """
        </div>

    </body>
    </html>
    """

    # Write the HTML content to a file
    with open("releases.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("HTML file has been generated: releases.html")
