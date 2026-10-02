import pandas as pd

# Fictional Aurora Hotels properties across EMEA
hotels = [
    ["AH001", "Aurora London Central", "London", "United Kingdom", "Europe"],
    ["AH002", "Aurora Manchester", "Manchester", "United Kingdom", "Europe"],
    ["AH003", "Aurora Edinburgh", "Edinburgh", "United Kingdom", "Europe"],
    ["AH004", "Aurora Paris", "Paris", "France", "Europe"],
    ["AH005", "Aurora Berlin", "Berlin", "Germany", "Europe"],
    ["AH006", "Aurora Amsterdam", "Amsterdam", "Netherlands", "Europe"],
    ["AH007", "Aurora Madrid", "Madrid", "Spain", "Europe"],
    ["AH008", "Aurora Rome", "Rome", "Italy", "Europe"],
    ["AH009", "Aurora Dubai Marina", "Dubai", "United Arab Emirates", "Middle East"],
    ["AH010", "Aurora Abu Dhabi", "Abu Dhabi", "United Arab Emirates", "Middle East"],
    ["AH011", "Aurora Doha", "Doha", "Qatar", "Middle East"],
    ["AH012", "Aurora Riyadh", "Riyadh", "Saudi Arabia", "Middle East"],
    ["AH013", "Aurora Cairo", "Cairo", "Egypt", "Africa"],
    ["AH014", "Aurora Cape Town", "Cape Town", "South Africa", "Africa"],
    ["AH015", "Aurora Nairobi", "Nairobi", "Kenya", "Africa"]
]

# Convert the list into a DataFrame
hotels = pd.DataFrame(
    hotels,
    columns=["HotelID", "HotelName", "City", "Country", "Region"]
)

# Save the hotel master data
hotels.to_csv("data/processed/hotels.csv", index=False)

print(hotels)
print(f"\nCreated {len(hotels)} Aurora properties.")