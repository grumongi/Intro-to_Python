# Exercise 1.4: Recipe Search System
# Import pickle module to work with binary files
import pickle

def display_recipe(recipe):
    """
    Display a recipe with all its attributes.
    
    Args:
        recipe (dict): Recipe dictionary containing name, cooking_time, ingredients, and difficulty
    """
    print("\n" + "="*50)
    print(f"Recipe: {recipe['name']}")
    print("="*50)
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Difficulty: {recipe['difficulty']}")
    print(f"Ingredients:")
    
    # Display ingredients as a numbered list
    for i, ingredient in enumerate(recipe['ingredients'], 1):
        print(f"  {i}. {ingredient}")
    
    print("="*50)

def search_ingredient(data):
    """
    Search for recipes containing a specific ingredient.
    
    Args:
        data (dict): Dictionary containing recipes_list and all_ingredients
    """
    # Get all ingredients from data
    all_ingredients = data['all_ingredients']
    recipes_list = data['recipes_list']
    
    # Show all available ingredients with numbers
    print("\nAll available ingredients:")
    print("-" * 30)
    
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i}. {ingredient}")
    
    print("-" * 30)
    
    # Try block for user input
    try:
        # Get user input for ingredient selection
        choice = int(input(f"\nPick an ingredient by number (0-{len(all_ingredients)-1}): "))
        
        # Use the number as index to get the ingredient
        ingredient_searched = all_ingredients[choice]
        
    except (ValueError, IndexError):
        # Handle incorrect input (non-integer or out of range)
        print("Error: Please enter a valid number from the list!")
        return
        
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        return
    
    else:
        # Search for recipes containing the ingredient
        print(f"\nRecipes containing '{ingredient_searched}':")
        print("=" * 60)
        
        found_recipes = []
        
        # Go through every recipe in recipes_list
        for recipe in recipes_list:
            # Check if the searched ingredient is in this recipe
            if ingredient_searched in recipe['ingredients']:
                found_recipes.append(recipe)
                display_recipe(recipe)
        
        # Show results summary
        if found_recipes:
            print(f"\nFound {len(found_recipes)} recipe(s) containing '{ingredient_searched}'")
        else:
            print(f"\nNo recipes found containing '{ingredient_searched}'")

# Main code
if __name__ == "__main__":
    print("=== Recipe Search System ===")
    
    # Ask user for the filename
    filename = input("Enter the filename that contains your recipe data: ")
    
    # Try to open and load the file
    try:
        # Open the file in binary read mode
        with open(filename, 'rb') as file:
            # Extract contents using pickle
            data = pickle.load(file)
        
        print(f"Successfully loaded data from '{filename}'!")
        
        # Display summary of loaded data
        recipes_count = len(data.get('recipes_list', []))
        ingredients_count = len(data.get('all_ingredients', []))
        
        print(f"Found {recipes_count} recipe(s) and {ingredients_count} unique ingredient(s)")
        
    except FileNotFoundError:
        # Handle file not found
        print(f"Error: File '{filename}' not found!")
        print("Please make sure the file exists and try again.")
        print("Hint: You need to run recipe_input.py first to create a recipe file.")
        
    except Exception as e:
        # Handle other exceptions (corrupt file, etc.)
        print(f"Error loading file: {e}")
        print("The file might be corrupted or in the wrong format.")
        
    else:
        # Call search_ingredient function if file loaded successfully
        search_ingredient(data)