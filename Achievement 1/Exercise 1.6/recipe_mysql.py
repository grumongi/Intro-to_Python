import mysql.connector

# Function to calculate recipe difficulty
def calculate_difficulty(cooking_time, ingredients):
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

# Function to create a new recipe
def create_recipe(conn, cursor):
    """Create a new recipe and add it to the database."""
    print("\n=== CREATE NEW RECIPE ===")
    
    # Collect recipe details
    name = input("Enter recipe name: ")
    
    # Get cooking time with input validation
    while True:
        try:
            cooking_time = int(input("Enter cooking time (in minutes): "))
            if cooking_time > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get ingredients
    print("Enter ingredients (type 'done' when finished):")
    ingredients = []
    while True:
        ingredient = input("Ingredient: ").strip()
        if ingredient.lower() == 'done':
            if ingredients:
                break
            else:
                print("Please enter at least one ingredient.")
        elif ingredient:
            ingredients.append(ingredient)
    
    # Calculate difficulty
    difficulty = calculate_difficulty(cooking_time, ingredients)
    
    # Convert ingredients list to comma-separated string
    ingredients_str = ", ".join(ingredients)
    
    # Build and execute SQL query
    query = """
    INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) 
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
        conn.commit()
        print(f"✅ Recipe '{name}' added successfully!")
        print(f"   Difficulty: {difficulty}")
    except mysql.connector.Error as err:
        print(f"❌ Error adding recipe: {err}")

# Function to search for recipes by ingredient
def search_recipe(conn, cursor):
    """Search for recipes containing a specific ingredient."""
    print("\n=== SEARCH RECIPES BY INGREDIENT ===")
    
    # Get all ingredients from the database
    try:
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in the database.")
            return
        
        # Extract unique ingredients
        all_ingredients = []
        for row in results:
            ingredients_str = row[0] if row else ""
            # Split by comma and clean up
            recipe_ingredients = [ing.strip() for ing in ingredients_str.split(",")]
            for ingredient in recipe_ingredients:
                if ingredient and ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        
        if not all_ingredients:
            print("No ingredients found.")
            return
        
        # Display ingredients to user
        print("\nAvailable ingredients:")
        for i, ingredient in enumerate(all_ingredients, 1):
            print(f"{i}. {ingredient}")
        
        # Get user choice
        while True:
            try:
                choice = int(input(f"\nSelect an ingredient (1-{len(all_ingredients)}): "))
                if 1 <= choice <= len(all_ingredients):
                    search_ingredient = all_ingredients[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(all_ingredients)}")
            except ValueError:
                print("Please enter a valid number.")
        
        # Search for recipes containing the ingredient
        search_query = """
        SELECT id, name, ingredients, cooking_time, difficulty 
        FROM Recipes 
        WHERE ingredients LIKE %s
        """
        
        cursor.execute(search_query, (f"%{search_ingredient}%",))
        search_results = cursor.fetchall()
        
        if search_results:
            print(f"\nRecipes containing '{search_ingredient}':")
            print("-" * 80)
            for recipe in search_results:
                print(f"ID: {recipe[0]}")
                print(f"Name: {recipe[1]}")
                print(f"Ingredients: {recipe[2]}")
                print(f"Cooking Time: {recipe[3]} minutes")
                print(f"Difficulty: {recipe[4]}")
                print("-" * 80)
        else:
            print(f"No recipes found containing '{search_ingredient}'.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error searching recipes: {err}")

# Function to update an existing recipe
def update_recipe(conn, cursor):
    """Update an existing recipe in the database."""
    print("\n=== UPDATE RECIPE ===")
    
    try:
        # Display all recipes
        cursor.execute("SELECT id, name, cooking_time, difficulty FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in the database.")
            return
        
        print("\nAvailable recipes:")
        print("-" * 50)
        for recipe in recipes:
            print(f"ID: {recipe[0]} | Name: {recipe[1]} | Time: {recipe[2]}min | Difficulty: {recipe[3]}")
        print("-" * 50)
        
        # Get recipe ID to update
        while True:
            try:
                recipe_id = int(input("Enter the ID of the recipe to update: "))
                # Check if recipe exists
                cursor.execute("SELECT id FROM Recipes WHERE id = %s", (recipe_id,))
                if cursor.fetchone():
                    break
                else:
                    print("Recipe with that ID not found. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get column to update
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Cooking Time")
        print("3. Ingredients")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if choice in [1, 2, 3]:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Handle updates based on choice
        if choice == 1:  # Update name
            new_name = input("Enter new recipe name: ")
            update_query = "UPDATE Recipes SET name = %s WHERE id = %s"
            cursor.execute(update_query, (new_name, recipe_id))
            print(f"✅ Recipe name updated to '{new_name}'")
            
        elif choice == 2:  # Update cooking time
            while True:
                try:
                    new_cooking_time = int(input("Enter new cooking time (in minutes): "))
                    if new_cooking_time > 0:
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Get current ingredients to recalculate difficulty
            cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
            ingredients_str = cursor.fetchone()[0]
            ingredients_list = [ing.strip() for ing in ingredients_str.split(",")]
            
            # Recalculate difficulty
            new_difficulty = calculate_difficulty(new_cooking_time, ingredients_list)
            
            # Update both cooking time and difficulty
            update_query = "UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s"
            cursor.execute(update_query, (new_cooking_time, new_difficulty, recipe_id))
            print(f"✅ Cooking time updated to {new_cooking_time} minutes")
            print(f"✅ Difficulty recalculated to '{new_difficulty}'")
            
        elif choice == 3:  # Update ingredients
            print("Enter new ingredients (type 'done' when finished):")
            new_ingredients = []
            while True:
                ingredient = input("Ingredient: ").strip()
                if ingredient.lower() == 'done':
                    if new_ingredients:
                        break
                    else:
                        print("Please enter at least one ingredient.")
                elif ingredient:
                    new_ingredients.append(ingredient)
            
            # Get current cooking time to recalculate difficulty
            cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
            cooking_time = cursor.fetchone()[0]
            
            # Recalculate difficulty
            new_difficulty = calculate_difficulty(cooking_time, new_ingredients)
            
            # Convert ingredients to string
            ingredients_str = ", ".join(new_ingredients)
            
            # Update both ingredients and difficulty
            update_query = "UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s"
            cursor.execute(update_query, (ingredients_str, new_difficulty, recipe_id))
            print(f"✅ Ingredients updated")
            print(f"✅ Difficulty recalculated to '{new_difficulty}'")
        
        conn.commit()
        
    except mysql.connector.Error as err:
        print(f"❌ Error updating recipe: {err}")

# Function to delete a recipe
def delete_recipe(conn, cursor):
    """Delete a recipe from the database."""
    print("\n=== DELETE RECIPE ===")
    
    try:
        # Display all recipes
        cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in the database.")
            return
        
        print("\nAll recipes:")
        print("-" * 80)
        for recipe in recipes:
            print(f"ID: {recipe[0]}")
            print(f"Name: {recipe[1]}")
            print(f"Ingredients: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Difficulty: {recipe[4]}")
            print("-" * 80)
        
        # Get recipe ID to delete
        while True:
            try:
                recipe_id = int(input("Enter the ID of the recipe to delete: "))
                # Check if recipe exists and get its name
                cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
                result = cursor.fetchone()
                if result:
                    recipe_name = result[0]
                    break
                else:
                    print("Recipe with that ID not found. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{recipe_name}'? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            # Delete the recipe
            delete_query = "DELETE FROM Recipes WHERE id = %s"
            cursor.execute(delete_query, (recipe_id,))
            conn.commit()
            print(f"✅ Recipe '{recipe_name}' deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error deleting recipe: {err}")

# Main menu function
def main_menu(conn, cursor):
    """Display the main menu and handle user choices."""
    while True:
        print("\n" + "="*50)
        print("           RECIPE DATABASE MANAGER")
        print("="*50)
        print("What would you like to do?")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        print("-"*50)
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                create_recipe(conn, cursor)
            elif choice == '2':
                search_recipe(conn, cursor)
            elif choice == '3':
                update_recipe(conn, cursor)
            elif choice == '4':
                delete_recipe(conn, cursor)
            elif choice == '5':
                print("\nExiting...")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    
    # Close the connection when exiting
    try:
        cursor.close()
        conn.close()
        print("✅ Database connection closed")
    except:
        pass

# Step 2: Initialize a connection object called conn
print("Connecting to MySQL server...")
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

if conn.is_connected():
    print("✅ Successfully connected to MySQL server!")
else:
    print("❌ Failed to connect to MySQL server")
    exit(1)

# Step 3: Initialize a cursor object from conn
cursor = conn.cursor()
print("✅ Cursor object initialized")

# Step 4: Create a database called task_database
print("Creating database...")
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
print("✅ Database 'task_database' created (or already exists)")

# Step 5: Access the database with USE statement
cursor.execute("USE task_database")
print("✅ Now using 'task_database'")

# Step 6: Create a table called Recipes with specified columns
print("Creating Recipes table...")
create_table_query = """
CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    ingredients VARCHAR(255) NOT NULL,
    cooking_time INT NOT NULL,
    difficulty VARCHAR(20) NOT NULL
)
"""

cursor.execute(create_table_query)
print("✅ Table 'Recipes' created (or already exists)")

# Verify the table structure
print("\nTable structure:")
cursor.execute("DESCRIBE Recipes")
columns = cursor.fetchall()
for column in columns:
    print(f"  Column: {column}")

print("\n🎉 Database setup complete!")
print("Database: task_database")
print("Table: Recipes")
print("Connection: Active")

# Call the main menu function
main_menu(conn, cursor)
