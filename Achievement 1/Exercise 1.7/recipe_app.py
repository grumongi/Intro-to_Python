
from sqlalchemy import create_engine, Column, Integer, String, and_
from sqlalchemy.orm import declarative_base, sessionmaker

# Part 1: Set up SQLAlchemy and database connection
print("Setting up SQLAlchemy...")

# Database connection details (using the task_database from previous exercise)
username = 'cf-python'
password = 'password'
hostname = 'localhost'
database_name = 'task_database'

# Create engine object to connect to the database
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}')
print("✅ Engine created successfully!")

# Create Session class and bind it to the engine
Session = sessionmaker(bind=engine)

# Initialize session object
session = Session()
print("✅ Session initialized!")

# Part 2: Create Model and Table

# Store declarative base class
Base = declarative_base()

# Define the Recipe model class
class Recipe(Base):
    """Recipe model class that inherits from Base."""
    
    # Set table name
    __tablename__ = 'final_recipes'
    
    # Define table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)
    
    def __repr__(self):
        """Quick representation of the recipe."""
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
    
    def __str__(self):
        """Well-formatted string representation of the recipe."""
        return f"""
{'='*50}
🍽️  RECIPE: {self.name.upper()}
{'='*50}
📋 Recipe ID: {self.id}
🥘 Name: {self.name}
🛒 Ingredients: {self.ingredients}
⏰ Cooking Time: {self.cooking_time} minutes
⭐ Difficulty: {self.difficulty}
{'='*50}
        """
    
    def calculate_difficulty(self):
        """
        Calculate the difficulty of a recipe based on cooking time and number of ingredients.
        Sets the self.difficulty attribute instead of returning the value.
        """
        # Get ingredients as list to count them
        ingredients_list = self.return_ingredients_as_list()
        num_ingredients = len(ingredients_list)
        
        # Access the actual values using getattr to handle SQLAlchemy columns properly
        cooking_time_val = getattr(self, 'cooking_time', 0) or 0
        
        # Calculate difficulty based on time and ingredient count
        if cooking_time_val < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif cooking_time_val < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif cooking_time_val >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:  # cooking_time >= 10 and num_ingredients >= 4
            self.difficulty = "Hard"
    
    def return_ingredients_as_list(self):
        """
        Return the ingredients string as a list.
        
        Returns:
            list: List of ingredients or empty list if no ingredients
        """
        # Get the actual string value using getattr to handle SQLAlchemy columns properly
        ingredients_str = getattr(self, 'ingredients', '') or ''
        
        # Check if ingredients is empty string
        if not ingredients_str or ingredients_str.strip() == "":
            return []
        
        # Split the string by comma and space, then strip each ingredient
        ingredients_list = [ingredient.strip() for ingredient in ingredients_str.split(", ")]
        return ingredients_list

# Create the table in the database
print("\nCreating tables in database...")
Base.metadata.create_all(engine)
print("✅ Tables created successfully!")

print("\n🎉 Recipe Application Setup Complete!")
print("Database: task_database")
print("Table: final_recipes")
print("Session: Active and ready for use")

# Test the Recipe class
print("\n" + "="*60)
print("                    TESTING RECIPE CLASS")
print("="*60)

# Create a test recipe
test_recipe = Recipe(
    name="Spaghetti Carbonara",
    ingredients="spaghetti, eggs, bacon, parmesan cheese, black pepper",
    cooking_time=15
)

# Calculate difficulty
test_recipe.calculate_difficulty()

print("\n📋 Test Recipe Created:")
print(f"Name: {test_recipe.name}")
print(f"Ingredients: {test_recipe.ingredients}")
print(f"Cooking Time: {test_recipe.cooking_time} minutes")
print(f"Difficulty: {test_recipe.difficulty}")

print(f"\n🔍 __repr__ output: {repr(test_recipe)}")
print(f"\n📄 Ingredients as list: {test_recipe.return_ingredients_as_list()}")

print(f"\n📋 __str__ output:")
print(test_recipe)

print("✅ Recipe class testing complete!")

# Part 3: Define Main Operations as Functions

def create_recipe():
    """Function to create a new recipe and add it to the database."""
    print("\n" + "="*50)
    print("           CREATE NEW RECIPE")
    print("="*50)
    
    # Collect recipe name with validation
    while True:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("❌ Recipe name cannot be empty. Please try again.")
        elif len(name) > 50:
            print("❌ Recipe name cannot exceed 50 characters. Please try again.")
        elif not name.replace(' ', '').isalnum():
            print("❌ Recipe name should contain only alphanumeric characters and spaces. Please try again.")
        else:
            break
    
    # Collect cooking time with validation
    while True:
        cooking_time_input = input("Enter cooking time (in minutes): ").strip()
        if not cooking_time_input.isnumeric():
            print("❌ Cooking time should be a number. Please try again.")
        else:
            cooking_time = int(cooking_time_input)
            if cooking_time <= 0:
                print("❌ Cooking time should be a positive number. Please try again.")
            else:
                break
    
    # Collect ingredients
    while True:
        try:
            num_ingredients = input("How many ingredients would you like to enter? ").strip()
            if not num_ingredients.isnumeric():
                print("❌ Please enter a valid number.")
                continue
            num_ingredients = int(num_ingredients)
            if num_ingredients <= 0:
                print("❌ Please enter a positive number of ingredients.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Collect individual ingredients
    ingredients = []
    print(f"\nPlease enter {num_ingredients} ingredients:")
    for i in range(num_ingredients):
        while True:
            ingredient = input(f"Ingredient {i+1}: ").strip()
            if not ingredient:
                print("❌ Ingredient cannot be empty. Please try again.")
            elif not ingredient.replace(' ', '').isalpha():
                print("❌ Ingredient should contain only alphabetical characters. Please try again.")
            else:
                ingredients.append(ingredient)
                break
    
    # Convert ingredients list to string
    ingredients_str = ", ".join(ingredients)
    
    # Create new Recipe object
    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time,
        difficulty=""  # Will be calculated
    )
    
    # Calculate difficulty
    recipe_entry.calculate_difficulty()
    
    # Add to database
    session.add(recipe_entry)
    session.commit()
    
    print(f"\n✅ Recipe '{name}' added successfully!")
    print(f"   Difficulty: {recipe_entry.difficulty}")

def view_all_recipes():
    """Function to display all recipes in the database."""
    print("\n" + "="*50)
    print("           ALL RECIPES")
    print("="*50)
    
    # Retrieve all recipes
    recipes = session.query(Recipe).all()
    
    # Check if any recipes exist
    if not recipes:
        print("❌ No recipes found in the database.")
        return None
    
    # Display all recipes
    print(f"\nFound {len(recipes)} recipe(s):\n")
    for recipe in recipes:
        print(recipe)

def search_by_ingredients():
    """Function to search for recipes by ingredients."""
    print("\n" + "="*50)
    print("         SEARCH BY INGREDIENTS")
    print("="*50)
    
    # Check if table has any entries
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("❌ No recipes found in the database.")
        return None
    
    # Retrieve ingredients column
    results = session.query(Recipe.ingredients).all()
    
    # Initialize list for all ingredients
    all_ingredients = []
    
    # Extract unique ingredients
    for result in results:
        ingredients_str = result[0] if result and result[0] else ""
        ingredient_list = [ing.strip() for ing in ingredients_str.split(", ") if ing.strip()]
        for ingredient in ingredient_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Display ingredients to user
    if not all_ingredients:
        print("❌ No ingredients found.")
        return None
    
    print("\nAvailable ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")
    
    # Get user selection
    print(f"\nEnter the numbers of ingredients to search for (separated by spaces):")
    print(f"Example: 1 3 5")
    
    while True:
        user_input = input("Your selection: ").strip()
        if not user_input:
            print("❌ Please enter at least one number.")
            continue
        
        try:
            selected_numbers = [int(num) for num in user_input.split()]
            
            # Validate selections
            invalid_numbers = [num for num in selected_numbers if num < 1 or num > len(all_ingredients)]
            if invalid_numbers:
                print(f"❌ Invalid numbers: {invalid_numbers}. Please enter numbers between 1 and {len(all_ingredients)}.")
                continue
            
            break
        except ValueError:
            print("❌ Please enter valid numbers separated by spaces.")
    
    # Create search ingredients list
    search_ingredients = [all_ingredients[num-1] for num in selected_numbers]
    
    print(f"\nSearching for recipes containing: {', '.join(search_ingredients)}")
    
    # Create search conditions
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    # Search database with all conditions (AND logic)
    recipes = session.query(Recipe).filter(and_(*conditions)).all()
    
    # Display results
    if recipes:
        print(f"\nFound {len(recipes)} matching recipe(s):\n")
        for recipe in recipes:
            print(recipe)
    else:
        print(f"\n❌ No recipes found containing all selected ingredients.")

def edit_recipe():
    """Function to edit an existing recipe."""
    print("\n" + "="*50)
    print("            EDIT RECIPE")
    print("="*50)
    
    # Check if any recipes exist
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("❌ No recipes found in the database.")
        return None
    
    # Retrieve id and name for each recipe
    results = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    print("\nAvailable recipes:")
    print("-" * 30)
    for recipe_id, recipe_name in results:
        print(f"ID: {recipe_id} | Name: {recipe_name}")
    print("-" * 30)
    
    # Get recipe selection from user
    while True:
        try:
            selected_id = input("Enter the ID of the recipe to edit: ").strip()
            if not selected_id.isnumeric():
                print("❌ Please enter a valid ID number.")
                continue
            
            selected_id = int(selected_id)
            
            # Check if recipe exists
            recipe_to_edit = session.query(Recipe).filter_by(id=selected_id).first()
            if not recipe_to_edit:
                print("❌ Recipe with that ID not found. Please try again.")
                continue
            
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Display current recipe details (editable attributes only)
    print(f"\nCurrent recipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")
    
    # Get attribute to edit
    while True:
        try:
            choice = input("\nWhich attribute would you like to edit? (1-3): ").strip()
            if choice not in ['1', '2', '3']:
                print("❌ Please enter 1, 2, or 3.")
                continue
            choice = int(choice)
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Edit based on choice
    if choice == 1:  # Edit name
        while True:
            new_name = input("Enter new recipe name: ").strip()
            if not new_name:
                print("❌ Recipe name cannot be empty. Please try again.")
            elif len(new_name) > 50:
                print("❌ Recipe name cannot exceed 50 characters. Please try again.")
            elif not new_name.replace(' ', '').isalnum():
                print("❌ Recipe name should contain only alphanumeric characters and spaces. Please try again.")
            else:
                setattr(recipe_to_edit, 'name', new_name)
                print(f"✅ Recipe name updated to '{new_name}'")
                break
    
    elif choice == 2:  # Edit ingredients
        while True:
            try:
                num_ingredients = input("How many ingredients would you like to enter? ").strip()
                if not num_ingredients.isnumeric():
                    print("❌ Please enter a valid number.")
                    continue
                num_ingredients = int(num_ingredients)
                if num_ingredients <= 0:
                    print("❌ Please enter a positive number of ingredients.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Collect new ingredients
        new_ingredients = []
        print(f"\nPlease enter {num_ingredients} ingredients:")
        for i in range(num_ingredients):
            while True:
                ingredient = input(f"Ingredient {i+1}: ").strip()
                if not ingredient:
                    print("❌ Ingredient cannot be empty. Please try again.")
                elif not ingredient.replace(' ', '').isalpha():
                    print("❌ Ingredient should contain only alphabetical characters. Please try again.")
                else:
                    new_ingredients.append(ingredient)
                    break
        
        setattr(recipe_to_edit, 'ingredients', ", ".join(new_ingredients))
        recipe_to_edit.calculate_difficulty()  # Recalculate difficulty
        print(f"✅ Ingredients updated")
        print(f"✅ Difficulty recalculated to '{recipe_to_edit.difficulty}'")
    
    elif choice == 3:  # Edit cooking time
        while True:
            cooking_time_input = input("Enter new cooking time (in minutes): ").strip()
            if not cooking_time_input.isnumeric():
                print("❌ Cooking time should be a number. Please try again.")
            else:
                cooking_time = int(cooking_time_input)
                if cooking_time <= 0:
                    print("❌ Cooking time should be a positive number. Please try again.")
                else:
                    setattr(recipe_to_edit, 'cooking_time', cooking_time)
                    recipe_to_edit.calculate_difficulty()  # Recalculate difficulty
                    print(f"✅ Cooking time updated to {cooking_time} minutes")
                    print(f"✅ Difficulty recalculated to '{recipe_to_edit.difficulty}'")
                    break
    
    # Commit changes
    session.commit()
    print("✅ Changes saved to database!")

def delete_recipe():
    """Function to delete a recipe from the database."""
    print("\n" + "="*50)
    print("           DELETE RECIPE")
    print("="*50)
    
    # Check if any recipes exist
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("❌ No recipes found in the database.")
        return None
    
    # Retrieve id and name for each recipe
    results = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    print("\nAvailable recipes:")
    print("-" * 30)
    for recipe_id, recipe_name in results:
        print(f"ID: {recipe_id} | Name: {recipe_name}")
    print("-" * 30)
    
    # Get recipe selection from user
    while True:
        try:
            selected_id = input("Enter the ID of the recipe to delete: ").strip()
            if not selected_id.isnumeric():
                print("❌ Please enter a valid ID number.")
                continue
            
            selected_id = int(selected_id)
            
            # Check if recipe exists and retrieve it
            recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).first()
            if not recipe_to_delete:
                print("❌ Recipe with that ID not found. Please try again.")
                continue
            
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Confirm deletion
    print(f"\nYou are about to delete:")
    print(f"Recipe: {recipe_to_delete.name}")
    print(f"Ingredients: {recipe_to_delete.ingredients}")
    
    while True:
        confirmation = input("\nAre you sure you want to delete this recipe? (yes/no): ").strip().lower()
        if confirmation in ['yes', 'y']:
            # Delete the recipe
            session.delete(recipe_to_delete)
            session.commit()
            print(f"✅ Recipe '{recipe_to_delete.name}' deleted successfully!")
            break
        elif confirmation in ['no', 'n']:
            print("❌ Deletion cancelled.")
            return None
        else:
            print("❌ Please enter 'yes' or 'no'.")

print("\n🎉 All functions defined successfully!")

# Part 4: Design Your Main Menu

def main_menu():
    """Main menu function that provides user interface for the recipe application."""
    while True:
        print("\n" + "="*60)
        print("                 RECIPE APPLICATION")
        print("="*60)
        print("What would you like to do? Choose from the options below:")
        print()
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print()
        print("Type 'quit' to quit the application")
        print("-" * 60)
        
        # Get user choice
        choice = input("Your choice: ").strip().lower()
        
        # Handle user input with if-elif statements
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit' or choice == 'q':
            print("\n" + "="*60)
            print("                   GOODBYE!")
            print("="*60)
            print("Thank you for using the Recipe Application!")
            print("Closing database connections...")
            
            # Close session and engine
            session.close()
            engine.dispose()
            
            print("✅ Database connections closed successfully!")
            print("👋 Have a great day!")
            break
        else:
            # Handle malformed input
            print("\n❌ Invalid choice! Please select from the options above or type 'quit' to exit.")
            print("   Valid choices: 1, 2, 3, 4, 5, or 'quit'")

# Start the application
if __name__ == "__main__":
    print("\n" + "🍽️"*20)
    print("        Welcome to the Recipe Application!")
    print("🍽️"*20)
    print("\nThis application helps you manage your recipes using a MySQL database.")
    print("You can create, view, search, edit, and delete recipes.")
    print("\nStarting the main menu...")
    
    # Launch the main menu
    main_menu()
