import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


# URL of the Worldometer COVID-19 data
url = "https://www.worldometers.info/coronavirus/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the COVID-19 data
table = soup.find("table", id="main_table_countries_today")

# Find all the rows in the table
rows = table.find_all("tr")

# Initialize empty lists to store the data
data = []
columns = []

# Extract the column headers from the first row
header_row = rows[0]
header_cells = header_row.find_all("th")
for cell in header_cells:
    columns.append(cell.get_text())

# Extract the data from the remaining rows
for row in rows[1:]:
    cells = row.find_all("td")
    row_data = []
    for cell in cells:
        row_data.append(cell.get_text().strip())
    data.append(row_data)

# Create a Pandas DataFrame from the extracted data
df = pd.DataFrame(data, columns=columns)
# Perform data analysis
# Convert numeric columns to the appropriate data types
df["TotalCases"] = pd.to_numeric(df["TotalCases"].str.replace(",", ""), errors="coerce")
df["TotalDeaths"] = pd.to_numeric(df["TotalDeaths"].str.replace(",", ""), errors="coerce")
df["TotalRecovered"] = pd.to_numeric(df["TotalRecovered"].str.replace(",", ""), errors="coerce")
df["ActiveCases"] = pd.to_numeric(df["ActiveCases"].str.replace(",", ""), errors="coerce")

# Sort the DataFrame by the TotalCases column in descending order
df.sort_values("TotalCases", ascending=False, inplace=True)

# Select the top 10 countries with the highest total cases
top_10_countries = df.head(10)

# Create a bar chart to visualize the top 10 countries with the highest total cases
plt.figure(figsize=(10, 6))
plt.bar(top_10_countries["Country,Other"], top_10_countries["TotalCases"])
plt.xticks(rotation=45)
plt.xlabel("Country")
plt.ylabel("Total Cases")
plt.title("Top 10 Countries with Highest Total COVID-19 Cases")
plt.tight_layout()
plt.show()

