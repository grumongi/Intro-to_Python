
class Recipe:
    """
    A class to represent a recipe with ingredients, cooking time, and difficulty level.
    """
    
    # Class variable to keep track of all ingredients across all recipes
    all_ingredients = []
    
    def __init__(self, name):
        """
        Initialize a new Recipe object.
        
        Args:
            name (str): The name of the recipe
        """
        self._name = name
        self._cooking_time = 0
        self._ingredients = []
        self._difficulty = None
    
    # Getter and setter methods for name
    def get_name(self):
        """Get the recipe name."""
        return self._name
    
    def set_name(self, name):
        """Set the recipe name."""
        self._name = name
    
    # Getter and setter methods for cooking_time
    def get_cooking_time(self):
        """Get the cooking time."""
        return self._cooking_time
    
    def set_cooking_time(self, cooking_time):
        """Set the cooking time and recalculate difficulty."""
        self._cooking_time = cooking_time
        self._difficulty = None  # Reset difficulty to trigger recalculation
    
    def add_ingredients(self, *ingredients):
        """
        Add ingredients to the recipe.
        
        Args:
            *ingredients: Variable-length arguments for ingredients
        """
        for ingredient in ingredients:
            self._ingredients.append(ingredient)
        
        # Update all_ingredients class variable
        self.update_all_ingredients()
        
        # Reset difficulty to trigger recalculation
        self._difficulty = None
    
    def get_ingredients(self):
        """Get the list of ingredients."""
        return self._ingredients
    
    def calculate_difficulty(self):
        """
        Calculate and set the difficulty based on cooking time and number of ingredients.
        """
        num_ingredients = len(self._ingredients)
        
        if self._cooking_time < 10 and num_ingredients < 4:
            self._difficulty = "Easy"
        elif self._cooking_time < 10 and num_ingredients >= 4:
            self._difficulty = "Medium"
        elif self._cooking_time >= 10 and num_ingredients < 4:
            self._difficulty = "Intermediate"
        elif self._cooking_time >= 10 and num_ingredients >= 4:
            self._difficulty = "Hard"
    
    def get_difficulty(self):
        """
        Get the difficulty level, calculating it if not already done.
        
        Returns:
            str: The difficulty level (Easy, Medium, Intermediate, Hard)
        """
        if self._difficulty is None:
            self.calculate_difficulty()
        return self._difficulty
    
    def search_ingredient(self, ingredient):
        """
        Search for a specific ingredient in the recipe.
        
        Args:
            ingredient (str): The ingredient to search for
            
        Returns:
            bool: True if ingredient is found, False otherwise
        """
        return ingredient in self._ingredients
    
    def update_all_ingredients(self):
        """
        Update the class variable all_ingredients with ingredients from this recipe.
        """
        for ingredient in self._ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    
    def __str__(self):
        """
        String representation of the recipe.
        
        Returns:
            str: Formatted string showing all recipe details
        """
        # Ensure difficulty is calculated
        difficulty = self.get_difficulty()
        
        # Format ingredients list
        ingredients_str = ", ".join(self._ingredients)
        
        # Create formatted string
        recipe_str = f"""
{'='*50}
Recipe: {self._name}
{'='*50}
Cooking Time: {self._cooking_time} minutes
Difficulty: {difficulty}
Ingredients: {ingredients_str}
{'='*50}
        """
        return recipe_str.strip()
    
    @staticmethod
    def recipe_search(data, search_term):
        """
        Search for recipes containing a specific ingredient.
        
        Args:
            data (list): List of Recipe objects to search through
            search_term (str): The ingredient to search for
        """
        print(f"\nRecipes containing '{search_term}':")
        print("=" * 60)
        
        found_recipes = []
        
        for recipe in data:
            if recipe.search_ingredient(search_term):
                found_recipes.append(recipe)
                print(recipe)
                print()
        
        if not found_recipes:
            print(f"No recipes found containing '{search_term}'")
        else:
            print(f"Found {len(found_recipes)} recipe(s) containing '{search_term}'")
        
        print("=" * 60)
    
    @staticmethod
    def interactive_search(recipes_list):
        """
        Interactive ingredient search function for use in IPython.
        
        Args:
            recipes_list (list): List of Recipe objects to search through
        """
        print("=== Interactive Recipe Search ===")
        print("Available ingredients:")
        print(f"{', '.join(Recipe.all_ingredients)}")
        print()
        
        while True:
            try:
                search_term = input("Enter an ingredient to search for (or 'quit' to exit): ").strip()
                
                if search_term.lower() == 'quit':
                    break
                
                if search_term == '':
                    print("Please enter a valid ingredient name.")
                    continue
                    
                Recipe.recipe_search(recipes_list, search_term)
                print()
                
            except KeyboardInterrupt:
                print("\n\nExiting recipe search...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        print("Search session ended.")


# Main code
if __name__ == "__main__":
    print("=== Recipe Object-Oriented Programming Demo ===")
    print()
    
    # Create Tea recipe
    print("Creating Tea recipe...")
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)
    print()
    
    # Create Coffee recipe
    print("Creating Coffee recipe...")
    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print(coffee)
    print()
    
    # Create Cake recipe
    print("Creating Cake recipe...")
    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    print(cake)
    print()
    
    # Create Banana Smoothie recipe
    print("Creating Banana Smoothie recipe...")
    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print(banana_smoothie)
    print()
    
    # Wrap recipes into a list and make it globally accessible
    recipes_list = [tea, coffee, cake, banana_smoothie]
    globals()['recipes_list'] = recipes_list  # Make accessible from IPython
    
    print(f"Created {len(recipes_list)} recipes total.")
    print(f"All ingredients used: {', '.join(Recipe.all_ingredients)}")
    print(f"Total unique ingredients: {len(Recipe.all_ingredients)}")
    print()
    
    # Interactive ingredient search
    print("=== Interactive Recipe Search ===")
    print("Available ingredients:")
    print(f"{', '.join(Recipe.all_ingredients)}")
    print()
    
    while True:
        try:
            search_term = input("Enter an ingredient to search for (or 'quit' to exit): ").strip()
            
            if search_term.lower() == 'quit':
                break
            
            if search_term == '':
                print("Please enter a valid ingredient name.")
                continue
                
            Recipe.recipe_search(recipes_list, search_term)
            print()
            
        except KeyboardInterrupt:
            print("\n\nExiting recipe search...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print("=== Recipe OOP Demo Complete ===")