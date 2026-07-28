from data.mock_pantry import MOCK_RECIPES, MOCK_PANTRY

def calories_matcher(target_amount, amounts):
    closest_amount = min(amounts, key=lambda i: abs(i - target_amount))

    return closest_amount


def grocery_list(ingredients, pantry):
    missing_ingredients = []
    for i in ingredients:
        if i not in pantry:
            missing_ingredients.append(i)

    return missing_ingredients


def find_suitable_meal(calorie_target):
    calories = []

    for meal in MOCK_RECIPES:
        calories.append(meal["calories"])

    """Select the closest to the target amount"""
    meal_calories = calories_matcher(calorie_target, calories)

    """Select the dictionary for the meal"""
    selected_meal = next((item for item in MOCK_RECIPES if item['calories'] == meal_calories), None)

    """Build grocery list"""
    meal_ingredients = selected_meal["ingredients"]
    missing_ingredients = grocery_list(meal_ingredients, MOCK_PANTRY)

    return {
        "status": "success",
        "meal_name": selected_meal["name"],
        "total_calories": selected_meal["calories"],
        "meal_protein": selected_meal["protein"],
        "meal_carbs": selected_meal["carbs"],
        "meal_fat": selected_meal["fat"],
        "grocery_list": missing_ingredients if missing_ingredients else "All ingredients already in the kitchen!"
    }