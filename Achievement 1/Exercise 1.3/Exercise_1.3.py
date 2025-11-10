# Initialize empty lists
recipes_list = []
ingredients_list = []

def take_recipe():
    """
    Function to take recipe input from user and create a recipe dictionary.
    Takes input for name, cooking_time, and ingredients.
    Returns a recipe dictionary.
    """
    
    # Get recipe name from user
    name = input("Enter the recipe name: ")
    
    # Get cooking time from user (convert to int)
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Get ingredients from user
    print("Enter the ingredients (type 'done' when finished):")
    ingredients = []
    
    while True:
        ingredient = input("Enter an ingredient: ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    
    # Create recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe

def determine_difficulty(cooking_time, num_ingredients):
    """
    Determine recipe difficulty based on cooking time and number of ingredients.
    """
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"

def display_recipe(recipe):
    """
    Display a recipe with its difficulty level.
    """
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    
    # Calculate difficulty
    difficulty = determine_difficulty(recipe['cooking_time'], len(recipe['ingredients']))
    print(f"Difficulty: {difficulty}")
    print("-" * 40)

# Main section of the code
if __name__ == "__main__":
    print("=== Recipe Collection System ===")
    
    # Ask user how many recipes they would like to enter
    n = int(input("How many recipes would you like to enter? "))
    
    # Run for loop n times to collect recipes
    for i in range(n):
        print(f"\n--- Enter Recipe {i + 1} ---")
        
        # Run take_recipe() and store output in recipe variable
        recipe = take_recipe()
        
        # Run another for loop to iterate through recipe's ingredients
        for ingredient in recipe['ingredients']:
            # Check if ingredient is not in ingredients_list, then add it
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)
        
        # Append recipe to recipes_list
        recipes_list.append(recipe)
    
    print("\n" + "="*50)
    print("ALL RECIPES WITH DIFFICULTY LEVELS")
    print("="*50)
    
    # Run for loop that iterates through recipes_list
    for recipe in recipes_list:
        display_recipe(recipe)
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total recipes collected: {len(recipes_list)}")
    print(f"All ingredients used: {', '.join(ingredients_list)}")
    print(f"Total unique ingredients: {len(ingredients_list)}")