# Exercise 1.4: Recipe Input with Binary File Storage
# Import pickle module to work with binary files
import pickle

def calc_difficulty(cooking_time, ingredients):
    """
    Calculate the difficulty of a recipe based on cooking time and number of ingredients.
    
    Args:
        cooking_time (int): Cooking time in minutes
        ingredients (list): List of ingredients
        
    Returns:
        str: Difficulty level (Easy, Medium, Intermediate, Hard)
    """
    num_ingredients = len(ingredients)
    
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:  # cooking_time >= 10 and num_ingredients >= 4
        return "Hard"

def take_recipe():
    """
    Take recipe information from user and return a recipe dictionary.
    
    Returns:
        dict: Recipe dictionary containing name, cooking_time, ingredients, and difficulty
    """
    # Take recipe name from user
    name = input("Enter the recipe name: ")
    
    # Take cooking time from user
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Take ingredients from user
    print("Enter the ingredients (type 'done' when finished):")
    ingredients = []
    
    while True:
        ingredient = input("Enter an ingredient: ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    
    # Calculate difficulty using calc_difficulty function
    difficulty = calc_difficulty(cooking_time, ingredients)
    
    # Gather all attributes into a dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    return recipe

# Main code
if __name__ == "__main__":
    print("=== Recipe Input System with Binary File Storage ===")
    
    # Ask user for filename
    filename = input("Enter the filename for recipe storage: ")
    
    # Initialize data variable
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
    
    # Try-except-else-finally block to handle file operations
    try:
        # Try to open the file in binary read mode
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        print(f"File '{filename}' loaded successfully!")
        
    except FileNotFoundError:
        # Handle case when file doesn't exist
        print(f"File '{filename}' not found. Creating new data structure.")
        data = {
            'recipes_list': [],
            'all_ingredients': []
        }
        
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}. Creating new data structure.")
        data = {
            'recipes_list': [],
            'all_ingredients': []
        }
        
    else:
        # This runs if no exception occurred in try block
        print("File loaded successfully without errors.")
        
    finally:
        # Extract values from dictionary into separate lists
        recipes_list = data.get('recipes_list', [])
        all_ingredients = data.get('all_ingredients', [])
        
        print(f"Current recipes in file: {len(recipes_list)}")
        print(f"Current ingredients in file: {len(all_ingredients)}")
    
    # Ask user how many recipes they want to enter
    n = int(input("\nHow many recipes would you like to enter? "))
    
    # Loop to collect recipes
    for i in range(n):
        print(f"\n--- Enter Recipe {i + 1} ---")
        
        # Call take_recipe() function and append to recipes_list
        recipe = take_recipe()
        recipes_list.append(recipe)
        
        # Inner loop to scan through recipe's ingredients
        for ingredient in recipe['ingredients']:
            # Add ingredient to all_ingredients if not already there
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
        
        print(f"Recipe '{recipe['name']}' added successfully!")
        print(f"Difficulty: {recipe['difficulty']}")
    
    # Gather updated data into dictionary
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': all_ingredients
    }
    
    # Write data to binary file using pickle
    try:
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
        print(f"\nData successfully saved to '{filename}'!")
        
        # Display summary
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Total recipes saved: {len(recipes_list)}")
        print(f"Total unique ingredients: {len(all_ingredients)}")
        print(f"File: {filename}")
        
        # Display all recipes
        print("\n" + "="*50)
        print("ALL SAVED RECIPES")
        print("="*50)
        for i, recipe in enumerate(recipes_list, 1):
            print(f"\n{i}. {recipe['name']}")
            print(f"   Cooking Time: {recipe['cooking_time']} minutes")
            print(f"   Ingredients: {', '.join(recipe['ingredients'])}")
            print(f"   Difficulty: {recipe['difficulty']}")
            
    except Exception as e:
        print(f"Error saving file: {e}")