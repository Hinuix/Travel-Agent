import csv

# Define a mapping from index to attribute names for the data fields
index_to_attribute = {
    0: 'PackageNumber',
    1: 'Recreation',
    2: 'Price',
    3: 'NumberOfPersons',
    4: 'Region',
    5: 'Transportation',
    6: 'Duration',
    7: 'Season',
    8: 'Accommodation',
    9: 'Hotel',
}

# List of attributes to get from the customer
attributes_to_input = ['Recreation', 'NumberOfPersons', 'Region', 'Transportation', 'Duration', 'Season', 'Accommodation']

# A dictionary of attributes and their possible values
attribute_values = {
    'Recreation': ['Bathing', 'Active', 'Education', 'City', 'Recreation', 'Wandering', 'Language', 'Skiing'],
    'NumberOfPersons': ['2', '3', '1', '4', '6', '5', '10', '8', '7', '12', '9'],
    'Region': ['Egypt', 'Cairo', 'Belgium', 'Bulgaria', 'Bornholm', 'Fano', 'Lolland', 'Allgaeu', 'Alps', 'Bavaria', 'ErzGebirge', 'Harz', 'NorthSea', 'BalticSea', 'BlackForest', 'Thuringia', 'Atlantic', 'CotedAzur', 'Corsica', 'Normandy', 'Brittany', 'Attica', 'Chalkidiki', 'Corfu', 'Crete', 'Rhodes', 'England', 'Ireland', 'Scotland', 'Wales', 'Holland', 'AdriaticSea', 'LakeGarda', 'Riviera', 'Tyrol', 'Malta', 'Carinthia', 'SalzbergerLand', 'Styria', 'Algarve', 'Madeira', 'Sweden', 'CostaBlanca', 'CostaBrava', 'Fuerteventura', 'GranCanaria', 'Ibiza', 'Mallorca', 'Teneriffe', 'GiantMountains', 'TurkishAegeanSea', 'TurkishRiviera', 'Tunisia', 'Balaton', 'Denmark', 'Poland', 'Slowakei', 'Czechia', 'France', 'LowerAustria', 'Salzkammergut', 'Dolomites', 'Cyprus', 'Morocco', 'Lanzarote'],
    'Transportation': ['Plane', 'Car', 'Train', 'Coach'],
    'Duration': ['14', '21', '7', '3', '4', '8', '10', '6', '9'],
    'Season': ['1', '2', '3', '4'],  # 1 - Spring, 2 - Summer, 3 - Fall, 4 - Winter
    'Accommodation': ['1', '2', '3', '4', '5', '6'],
}

# Empty list to store the data
data_list = []

# Define a dictionary to map months to seasons
month_to_season = {
    'January': '4',     # Winter
    'February': '4',    # Winter
    'March': '1',       # Spring
    'April': '1',       # Spring
    'May': '1',         # Spring
    'June': '2',        # Summer
    'July': '2',        # Summer
    'August': '2',      # Summer
    'September': '3',   # Fall
    'October': '3',     # Fall
    'November': '3',    # Fall
    'December': '4',    # Winter
}
         
# Opening the 'data.txt' file
with open("data.txt", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        data_dict = {index_to_attribute[i]: value.strip("[]").replace("'", "").strip() for i, value in enumerate(row)}
        
        # Map the month to the season
        season_name = data_dict.get("Season")
        if season_name in month_to_season:
            data_dict["Season"] = month_to_season[season_name]

        data_list.append(data_dict)


# Dictionary to store customer input
customer_input = {}

# Prompt the user to enter their preferences for each attribute
# Remove this section if you want to get customer input from the command line
""" for attribute in attributes_to_input: 
     print(f"Available values for {attribute}: {', '.join(attribute_values[attribute])}")
     customer_input[attribute] = input(f"Enter your preferred {attribute}: ")
 """
def calculate_similarity_points(customer_input, data_record):
    similarity_points = {
        'Recreation': 0,
        'NumberOfPersons': 0,
        'Region': 0,
        'Transportation': 0,
        'Duration': 0,
        'Season': 0,
        'Accommodation': 0
    }

    for attribute in attributes_to_input:
        if attribute in ['NumberOfPersons', 'Duration']:
            try:
                a = int(customer_input.get(attribute, '0'))
                b = int(data_record.get(attribute, '0'))

                # Calculate the span of the entire attribute's values
                min_value = min(int(x) for x in attribute_values[attribute])
                max_value = max(int(x) for x in attribute_values[attribute])
                span = max_value - min_value

                # Calculate the similarity for numeric attributes
                similarity = 1 - (abs(a - b) / span)
                similarity_points[attribute] = similarity
            except (ValueError, TypeError):
                similarity_points[attribute] = 0
        elif attribute == 'Season':
            seasons = ['2', '3', '4', '1']
            a_value = customer_input.get(attribute, '').lower()
            b_value = data_record.get(attribute, '').lower()

            if a_value in seasons and b_value in seasons:
                a_idx = seasons.index(a_value)
                b_idx = seasons.index(b_value)
                distance = abs(a_idx - b_idx)

                if distance == 0:
                    similarity = 1  
                elif distance <= 2:
                    similarity = 1 - (distance * 0.25)  
                else:
                    similarity = 0  
            else:
                #print(a_value, b_value)
                similarity = -1  

            similarity_points[attribute] = similarity
        else:
            if attribute in customer_input and attribute in data_record:
                a = customer_input[attribute].lower()
                b = data_record[attribute].lower()
                similarity = 0  # Initialize similarity to 0

                if a == b:
                    similarity = 1
                else:
                    # Specific similarity calculations for each attribute
                    if attribute == 'Recreation':
                        # Extend Recreation similarity calculations using a nested dictionary
                        recreation_similarity = {
                            'bathing': {
                                'active': 0.95,
                                'education': 0.85,
                                'city': 0.80,
                                'recreation': 0.75,
                                'wandering': 0.70,
                                'language': 0.60,
                                'skiing': 0.90,
                            },
                            'active': {
                                'education': 0.88,
                                'city': 0.82,
                                'recreation': 0.77,
                                'wandering': 0.72,
                                'language': 0.62,
                                'skiing': 0.91,
                            },
                            'education': {
                                'city': 0.89,
                                'recreation': 0.84,
                                'wandering': 0.79,
                                'language': 0.69,
                                'skiing': 0.88,
                            },
                            'city': {
                                'recreation': 0.76,
                                'wandering': 0.71,
                                'language': 0.61,
                                'skiing': 0.86,
                            },
                            'recreation': {
                                'wandering': 0.74,
                                'language': 0.64,
                                'skiing': 0.87,
                            },
                            'wandering': {
                                'language': 0.65,
                                'skiing': 0.83,
                            },
                            'language': {
                                'skiing': 0.81,
                            },
                        }
                        # Check if there's a predefined similarity score for the given pair of 'Recreation' values
                        if b in recreation_similarity.get(a, {}):
                            similarity = recreation_similarity[a].get(b, 0)
                        else:
                            similarity = 0  # Default similarity score if no predefined score found
                    elif attribute == 'Region':
                        # Extend Region similarity calculations using a nested dictionary
                        region_similarity = {
                        'Egypt': {
                            'Cairo': 0.9,
                            'Bulgaria': 0.7,
                            'Bornholm': 0.8,
                            'Fano': 0.85,
                            'Lolland': 0.8,
                            'Allgaeu': 0.75,
                            'Alps': 0.7,
                            'Bavaria': 0.8,
                            'ErzGebirge': 0.75,
                            'Harz': 0.7,
                            'NorthSea': 0.75,
                            'BalticSea': 0.75,
                            'BlackForest': 0.8,
                            'Thuringia': 0.75,
                            'Atlantic': 0.7,
                            'CotedAzur': 0.8,
                            'Corsica': 0.85,
                            'Normandy': 0.8,
                            'Brittany': 0.8,
                            'Attica': 0.9,
                            'Chalkidiki': 0.85,
                            'Corfu': 0.8,
                            'Crete': 0.85,
                            'Rhodes': 0.85,
                            'England': 0.8,
                            'Ireland': 0.8,
                            'Scotland': 0.8,
                            'Wales': 0.8,
                            'Holland': 0.75,
                            'AdriaticSea': 0.85,
                            'LakeGarda': 0.8,
                            'Riviera': 0.85,
                            'Tyrol': 0.8,
                            'Malta': 0.9,
                            'Carinthia': 0.85,
                            'SalzbergerLand': 0.8,
                            'Styria': 0.75,
                            'Algarve': 0.9,
                            'Madeira': 0.85,
                            'Sweden': 0.8,
                            'CostaBlanca': 0.85,
                            'CostaBrava': 0.85,
                            'Fuerteventura': 0.8,
                            'GranCanaria': 0.8,
                            'Ibiza': 0.85,
                            'Mallorca': 0.85,
                            'Teneriffe': 0.85,
                            'GiantMountains': 0.7,
                            'TurkishAegeanSea': 0.85,
                            'TurkishRiviera': 0.85,
                            'Tunisia': 0.85,
                            'Balaton': 0.8,
                            'Denmark': 0.75,
                            'Poland': 0.7,
                            'Slowakei': 0.7,
                            'Czechia': 0.75,
                            'France': 0.8,
                            'LowerAustria': 0.8,
                            'Salzkammergut': 0.85,
                            'Dolomites': 0.85,
                            'Cyprus': 0.85,
                            'Morocco': 0.7,
                            'Lanzarote': 0.85
                        },
                        }
                        # Check if there's a predefined similarity score for the given pair of 'Region' values
                        if b in region_similarity.get(a, {}):
                            similarity = region_similarity[a].get(b, 0)
                        elif b ==a:
                            similarity = 1
                        else:
                            similarity = 0  # Default similarity score if no predefined score found
                    elif attribute == 'Transportation':
                        # Extend Transportation similarity calculations using a nested dictionary
                        transportation_similarity = {
                            'Plane': {
                                'Car': 0.8,
                                'Train': 0.7,
                                'Coach': 0.6,
                            },
                        }
                        # Check if there's a predefined similarity score for the given pair of 'Transportation' values
                        if b in transportation_similarity.get(a, {}):
                            similarity = transportation_similarity[a].get(b, 0)
                        else: similarity = 0  # Default similarity score if no predefined score found
                    elif attribute == 'Duration':
                        # Extend Duration similarity calculations using a nested dictionary
                        duration_similarity = {
                            '14': {
                                '21': 0.8,
                                '7': 0.6,
                                '3': 0.4,
                                '4': 0.4,
                                '8': 0.6,
                                '10': 0.6,
                                '6': 0.4,
                                '9': 0.6,
                            },
                        }
                        # Check if there's a predefined similarity score for the given pair of 'Duration' values
                        if b in duration_similarity.get(a, {}):
                            similarity = duration_similarity[a].get(b, 0)
                        else: similarity = 0  # Default similarity score if no predefined score found
                    elif attribute == 'Accommodation':
                        # Extend Accommodation similarity calculations using a nested dictionary
                        accommodation_similarity = {
                            '1': {
                                '2': 0.7,
                                '3': 0.8,
                                '4': 0.9,
                                '5': 0.8,
                                '6': 0.7,
                            },
                        }
                        # Check if there's a predefined similarity score for the given pair of 'Accommodation' values
                        if b in accommodation_similarity.get(a, {}):
                            similarity = accommodation_similarity[a].get(b, 0)
                        else:
                            similarity = 0 # Default similarity score if no predefined score found
                similarity_points[attribute] = similarity
    return similarity_points

similarity_points = []


# Calculate similarity points for each data record and store in the 'similarity_points' list
for data_record in data_list:
    points = calculate_similarity_points(customer_input,data_record)
    similarity_points.append((data_record, points))

sorted_similarity_points = sorted(similarity_points, key=lambda x: sum(x[1].values()), reverse=True)

# Get the top 4 data records with the highest total similarity points (including those with at least one matching attribute)
top_4_similarity_points = []

for record, points in sorted_similarity_points:
    if sum(points.values()) > 0 and len(top_4_similarity_points) < 4:
        top_4_similarity_points.append((record, points))

# Hardcoded customer input for testing
print("Top 4 Matching Records:")
# Commment out this section if you want to get customer input from the command line
print("Customer Input:", {
    'Recreation': 'Bathing',
    'NumberOfPersons': '2',
    'Region': 'Egypt',
    'Transportation': 'Plane',
    'Duration': '14',
    'Season': '2',
    'Accommodation': '3',
})

# Initialize a dictionary to store the total similarity points for each package
tally_similarity_points = {}

# List to store the modified package details
modified_packages = []

# Iterate through the top 4 matching records
for i, (record, points) in enumerate(top_4_similarity_points, 1):
    package_number = record['PackageNumber']
    price = float(record['Price']) # Convert price to float for calculations
    box_width = 36
    box_top = "+" + "-" * (box_width - 2) + "+"

    print(f"{i}. Package Number: {package_number} - Price: {price}")
    print(box_top)
    print("| Matching Package Details:")

    total_similarity_points = sum(points.values())  # Calculate the total similarity points for the package
    tally_similarity_points[package_number] = total_similarity_points

    # Display details for each attribute
    for attribute in attributes_to_input:
        attribute_value = record[attribute]
        similarity = points[attribute]
        num_spaces = box_width - len(attribute) - len(attribute_value) - 26
        temp = f"{attribute.capitalize()}: {attribute_value}"
        print("| {:<30} |".format(temp))
        
        print("| {:>30} |".format(f"Similarity Points: {similarity:.2f}"))

    box_bottom = "+" + "-" * (box_width - 2) + "+"

    print(box_bottom)

# Ask the user if they want to make modifications
modification_choice = input("Do you want to make modifications? (yes/no): ").lower()

if modification_choice == 'yes':
    print("Choose what to modify:\n 1 - Number of People\n 2 - Duration\n 3 - Both ")

    modification_type = input("Enter your choice (1)(2)(3)): ")

    new_people = 0
    new_duration = 0

    if modification_type == '1':
        new_people = int(input("Enter the new number of people: "))

    elif modification_type == '2':
        new_duration = int(input("Enter the new duration (in days): "))

    elif modification_type == '3':
        new_people = int(input("Enter the new number of people: "))
        new_duration = int(input("Enter the new duration (in days): "))

    for i, (record, points) in enumerate(top_4_similarity_points, 1):
        package_number = record['PackageNumber']
        current_people = int(record['NumberOfPersons'])
        current_duration = int(record['Duration'])
        price = float(record['Price']) 

        print("Original Price:", float(record['Price']))
        print("Modified Price:", price)

        modified_people = new_people if new_people != 0 else current_people
        modified_duration = new_duration if new_duration != 0 else current_duration

        if new_people != 0 and new_people != current_people:
            price += (new_people - current_people) * 50  # Assume an additional cost of $50 per person
            record['NumberOfPersons'] = str(new_people)

        if new_duration != 0 and new_duration != current_duration:
            price += (new_duration - current_duration) * 100  # Assume an additional cost of $100 per extra day
            record['Duration'] = str(new_duration)

        price += (modified_people - current_people) * 50  # Assume an additional cost of $50 per person
        price += (modified_duration - current_duration) * 100  # Assume an additional cost of $100 per extra day

        print("Updated Price:", price)
        print()
        """ 
        # Update the price in the record
        record['Price'] = str(price)
        record['NumberOfPersons'] = str(modified_people)
        record['Duration'] = str(modified_duration) """

        # Store the modified package details
        modified_packages.append({
            'PackageNumber': package_number,
            'CurrentPeople': current_people,
            'NewPeople': new_people,
            'CurrentDuration': current_duration,
            'NewDuration': new_duration,
            'PriceDifference': price - float(record['Price'])
        })


print("\nModified Package Details and Price Differences:")
for modified_package in modified_packages:
    package_number = modified_package['PackageNumber']
    current_people = modified_package['CurrentPeople']
    new_people = modified_package['NewPeople']
    current_duration = modified_package['CurrentDuration']
    new_duration = modified_package['NewDuration']
    price_difference = modified_package['PriceDifference']

    print(f"\nPackage {package_number}")

    
    # Print people change and its price difference
    if new_people != 0:
        people_price_difference = (new_people - current_people) * 50  # Assume an additional cost of $50 per person
        print(f"Changed from {current_people} people to {new_people} people. Price difference for people: {people_price_difference}")

    # Print duration change and its price difference
    if new_duration != 0:
        duration_price_difference = (new_duration - current_duration) * 100  # Assume an additional cost of $100 per extra day
        print(f"Changed from {current_duration} days to {new_duration} days. Price difference for duration: {duration_price_difference}")