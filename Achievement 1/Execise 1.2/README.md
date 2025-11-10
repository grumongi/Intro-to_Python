# Recipe Management System

## Data Structure Choice for recipe_1

I chose a **dictionary** for the recipe_1 structure because it provides key-value pairs that perfectly match the recipe attributes (name, cooking_time, ingredients). Dictionaries offer fast lookups, clear semantic meaning through descriptive keys, and flexible data type storage - allowing strings for names, integers for time, and lists for ingredients. This structure is intuitive, easily extensible, and follows Python best practices for representing structured data with mixed types.

## IPython Shell Implementation

To create the recipe_1 structure in IPython shell, run these commands:

```python
# Start IPython shell and execute:
recipe_1 = {
    'name': 'Tea',
    'cooking_time': 5,
    'ingredients': ['Tea leaves', 'Sugar', 'Water']
}

# Verify the structure
print(recipe_1)
print(f"Recipe name: {recipe_1['name']}")
print(f"Cooking time: {recipe_1['cooking_time']} minutes")
print(f"Ingredients: {recipe_1['ingredients']}")
```

## Data Structure Choice for all_recipes

I chose a **list** for the all_recipes outer structure because it's designed to contain multiple recipe dictionaries. Here's my justification:

### Why List over Other Data Structures?

**List Benefits:**
- **Ordered Collection**: Maintains the sequence recipes were added, which is useful for displaying them chronologically or by preference
- **Index Access**: Easy access to specific recipes using `all_recipes[0]`, `all_recipes[1]`, etc.
- **Dynamic Growth**: Can easily add new recipes using `.append()` without declaring size beforehand
- **Iteration-Friendly**: Simple to loop through all recipes with `for recipe in all_recipes`
- **Mutable**: Can modify, add, or remove recipes as needed

**Why Not Dictionary?**
- Recipes don't need unique keys as identifiers
- Sequential access is more natural than key-based lookup for recipe collections

**Why Not Tuple?**
- Need mutability to add/remove recipes dynamically
- Tuples are immutable which would require recreating the entire collection

### IPython Implementation

```python
# Create the outer structure and add recipe_1
all_recipes = []
all_recipes.append(recipe_1)

# Verify the structure
print(f"Container type: {type(all_recipes).__name__}")
print(f"Number of recipes: {len(all_recipes)}")
print(f"First recipe: {all_recipes[0]}")
```

The complete implementation can be found in `all_recipes_structure.py`.
