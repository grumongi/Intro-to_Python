# Task 2.5 - Model Updates and Recipe App Enhancement

## Models Review from Exercise 2.3

### Current Models/Tables:

1. **Recipe Model** (`recipes/models.py`)
   - name (CharField, max_length=200)
   - cooking_time (IntegerField, in minutes)
   - difficulty (CharField, choices=['Easy', 'Medium', 'Hard'])
   - created_date (DateTimeField, auto_now_add=True)
   - updated_date (DateTimeField, auto_now=True)
   - user (ForeignKey to User)
   - category (ForeignKey to Category)
   - ingredients (ManyToManyField through RecipeIngredient)

2. **Category Model** (`recipes/models.py`)
   - name (CharField, max_length=100)
   - description (TextField, blank=True, null=True)

3. **Ingredient Model** (`ingredients/models.py`)
   - name (CharField, max_length=100, unique=True)
   - unit_of_measure (CharField, max_length=50, default='grams')

4. **RecipeIngredient Model** (`ingredients/models.py`)
   - recipe (ForeignKey to Recipe)
   - ingredient (ForeignKey to Ingredient)
   - quantity (FloatField, null=True, blank=True)

5. **UserProfile Model** (`users/models.py`)
   - user (OneToOneField to User)
   - bio (TextField, max_length=500, blank=True)
   - location (CharField, max_length=30, blank=True)
   - birth_date (DateField, null=True, blank=True)
   - favorite_cuisine (CharField, max_length=100, blank=True)

## Proposed Model Updates

### Recipe Model Updates:

**ADDITIONS:**
1. **image** (ImageField) - To store recipe images for better visual presentation
   - Reasoning: Visual appeal is crucial for recipe applications
   - Field: `image = models.ImageField(upload_to='recipes/', blank=True, null=True)`

2. **description** (TextField) - To provide recipe overview/description  
   - Reasoning: Users need context about what the recipe is
   - Field: `description = models.TextField(blank=True, null=True)`

3. **instructions** (TextField) - Step-by-step cooking instructions
   - Reasoning: Essential for actually making the recipe
   - Field: `instructions = models.TextField(blank=True, null=True)`

4. **servings** (PositiveIntegerField) - Number of people the recipe serves
   - Reasoning: Important for meal planning and scaling ingredients
   - Field: `servings = models.PositiveIntegerField(default=1)`

**MODIFICATIONS:**
1. **difficulty** field - Change from manual choice to auto-calculated
   - Reasoning: More consistent and objective difficulty assessment
   - Will add method to calculate based on cooking time and ingredient count

### Category Model Updates:

**ADDITIONS:**
1. **image** (ImageField) - Category icon/image
   - Reasoning: Visual categorization improves user experience
   - Field: `image = models.ImageField(upload_to='categories/', blank=True, null=True)`

### No changes needed for:
- **Ingredient Model** - Current structure is sufficient
- **RecipeIngredient Model** - Current structure is sufficient  
- **UserProfile Model** - Current structure is sufficient

## Implementation Plan:

1. Update Recipe model with new fields
2. Update Category model with image field
3. Add automatic difficulty calculation method
4. Create and run migrations
5. Update admin interface to support new fields
6. Test all changes

## Benefits of These Updates:

1. **Enhanced Visual Appeal** - Images for recipes and categories
2. **Complete Recipe Information** - Instructions, descriptions, servings
3. **Better User Experience** - More comprehensive recipe details
4. **Consistent Difficulty Rating** - Automated calculation removes subjectivity
5. **Scalability** - Servings field allows for portion scaling