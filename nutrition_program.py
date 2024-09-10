#Emily Tan 2230693
#Computer Applications
#Prof. Robert Vincent
#May 2nd 2024


#*** Due to the website that provides the nutritional values of various different kinds of food,
#some food's nutritional values cannot be determined or are not accurate enough to be assessed. It is only an approximation.***
#SO DO NOT TAKE THIS PROGRAM VERY SERIOUSLY!!!

import requests

#welcome message
print(
"""
Hi, fellow user. Welcome to the best nutrition program in the country! Here, we will be able
to evaluate your overall fitness levels and your diet and recommend you nutritional goals to achieve. Please take the time
to answer a few questions in order for us to get to know you better. 
"""
)
# User input
age = int(input("How old are you? "))
sex = input("What sex are you? M/F: ")
activity = input("How active are you? (Non Active, Moderate, Active): ")
foods = input("State all the foods you ate today(separated by commas): ").split(',')
dict_nut = {"Protein": 0, "Carbohydrate, by difference": 0, "Fiber, total dietary": 0,"Sodium, Na": 0}

# nutrients information using API keys and food nutrients website
def get_nutrients(food_name,dict_nut):
    """get nutrient information for a food item"""
    API_KEY = '7AHzoweeJyrYNYpDNl1vADshrg4XxecWIcZNnfgM' #api key
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={API_KEY}" #food website
    response = requests.get(url)
    data = response.json()
    print(f"\n{food_name} :")
    if data.get('foods'):
        food_data = data['foods'][0] #assuming the first one is the most relevant one
        for key in dict_nut:
            for nutrient in food_data['foodNutrients']:
                if nutrient['nutrientName'] == key:
                    print(f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}") #print nutrients for every food
                    dict_nut[key] += float(nutrient['value'])  # update dictionary #sodium mg, else in g
        return dict_nut
    else:
        return None
def diet_index(age,sex,activity):
    """get the diet_index to access the recommendation in database"""
    if sex == "M": #male
        sex_index = 12 #in database.txt, male recommendation starts at 12
    else: #"F" for female
        sex_index = 1 #in database.txt, female recommendation starts at 1

    age_groups = [[1, 6], [6, 12], [12, 19], [19, 36], [36, 56], [56, 120]] #age categories
    activity_levels = ["Non Active", "Moderate", "Active"]
    age_group_index = -1
    for a in range(len(age_groups)): #determine the age group index
        range_age_group = range(min(age_groups[a]), max(age_groups[a]))
        if age in range_age_group:
            age_group_index = a
            break

    #case where the age_index == 0 or 1 #baby/toddler and child have no activity level to be measured
    if age_group_index == 0 or 1: #baby [1-5] or child[6-11]
        diet_index = sex_index + age_group_index
    if 1 < age_group_index < 5 :  #age groups [12,19], [19,36] or [36,56]
        diet_index = sex_index + age_group_index + activity_levels.index(activity)
    else: #age_group [56+], no activity levels measured
        diet_index = sex_index + age_group_index
    return diet_index #any number between 1-24 in the first column of database.txt

#diet recommendation
def diet_recommendation(fp, diet_index):
    """Get the diet recommendation based on the provided database"""
    for line in fp:
        diet_info = line.strip().split()
        if int(diet_info[0]) == diet_index:
            return diet_info[1:]

# Function to check if current nutrients meet recommendations
def criterias_checker(current_nutrients, recomm_nutrients, dict_nut):
    """Check if the current user's nutrients satisfy the recommendations"""
    comparison = {}
    dict_nut = list(dict_nut.keys())
    recomm_nutrients = recomm_nutrients[1:]  # Skip the first value in recomm_nutrients
    for food, nutrients in current_nutrients.items():
        total_intake = {nutrient: 0 for nutrient in range(len(recomm_nutrients))}
        for index, nut in enumerate(nutrients):
            total_intake[index] += float(nut)
        # Compare with recommended
        for index, value in enumerate(total_intake.values()):
            recomm_value = recomm_nutrients[index]
            if value > float(recomm_value) * 1.1:
                comparison[dict_nut[index]] = f"You consume too much of nutrient {dict_nut[index]}."
            elif value < float(recomm_value) * 0.9:
                comparison[dict_nut[index]] = f"You need more of nutrient {dict_nut[index]}."
            else:
                comparison[dict_nut[index]] = f"You have satisfied the amount of nutrient {dict_nut[index]}."
    return comparison

# Get nutrient information for each food
nutrient_info_all = {}
for food in foods:
    nutrient_info = get_nutrients(food, dict_nut)
    if nutrient_info:
        nutrient_info_all[food] = list(nutrient_info.values())

# Calculate diet index and get diet recommendation
diet_ind = diet_index(age, sex, activity)
recommendation = diet_recommendation(open("Database.txt"), diet_ind)

# Compare current nutrients with recommendations
comparison_results = criterias_checker(nutrient_info_all, recommendation, dict_nut)

print("\nDiet Recommendation:")
print("Based on your age, sex, and activity levels, you would need to satisfy these criterias:")
print(f"- {recommendation[0]} calories")
print(f"- {recommendation[1]}g of protein")
print(f"- {recommendation[2]}g of fiber")
print(f"- {recommendation[3]}g of carbs")
print(f"- {recommendation[4]}mg of sodium")

print("\nBased on the diet recommendation, we have determined that:")
for nutrient, result in comparison_results.items():
    print(result)

#an example for you to try for fun :)
# 25
# F
# Non Active
# Orange,Big Mac,Banana,Apple Juice,rice,curry,bread,milk


