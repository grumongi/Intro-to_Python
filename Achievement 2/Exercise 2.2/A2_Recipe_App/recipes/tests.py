from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import Client
from .models import Category, Recipe

class CategoryModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Italian",
            description="Traditional Italian cuisine"
        )
    
    def test_category_creation(self):
        """Test category creation with valid data"""
        self.assertEqual(self.category.name, "Italian")
        self.assertEqual(self.category.description, "Traditional Italian cuisine")
        self.assertTrue(isinstance(self.category, Category))
    
    def test_category_str_representation(self):
        """Test string representation of category"""
        self.assertEqual(str(self.category), "Italian")
    
    def test_category_verbose_name_plural(self):
        """Test the verbose name plural"""
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")

class RecipeModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Italian",
            description="Traditional Italian cuisine"
        )
        self.recipe = Recipe.objects.create(
            name="Spaghetti Carbonara",
            description="Classic Italian pasta dish",
            cooking_time=30,
            difficulty="Medium",
            servings=4,
            instructions="Cook pasta, mix with eggs and cheese",
            user=self.user,
            category=self.category
        )
    
    def test_recipe_creation(self):
        """Test recipe creation with valid data"""
        self.assertEqual(self.recipe.name, "Spaghetti Carbonara")
        self.assertEqual(self.recipe.description, "Classic Italian pasta dish")
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.difficulty, "Medium")
        self.assertEqual(self.recipe.servings, 4)
        self.assertEqual(self.recipe.user, self.user)
        self.assertEqual(self.recipe.category, self.category)
        self.assertTrue(isinstance(self.recipe, Recipe))
    
    def test_recipe_str_representation(self):
        """Test string representation of recipe"""
        self.assertEqual(str(self.recipe), "Spaghetti Carbonara")
    
    def test_recipe_default_difficulty(self):
        """Test default difficulty level"""
        recipe_no_difficulty = Recipe.objects.create(
            name="Test Recipe",
            description="Test description",
            cooking_time=15,
            servings=2,
            instructions="Test instructions",
            user=self.user
        )
        self.assertEqual(recipe_no_difficulty.difficulty, "Easy")
    
    def test_recipe_difficulty_choices(self):
        """Test difficulty choices validation"""
        valid_difficulties = ['Easy', 'Medium', 'Hard']
        for difficulty in valid_difficulties:
            recipe = Recipe.objects.create(
                name=f"Test Recipe {difficulty}",
                description="Test description",
                cooking_time=15,
                difficulty=difficulty,
                servings=2,
                instructions="Test instructions",
                user=self.user
            )
            self.assertEqual(recipe.difficulty, difficulty)
    
    def test_recipe_ordering(self):
        """Test recipe ordering by created_date"""
        # Create another recipe
        recipe2 = Recipe.objects.create(
            name="Pizza Margherita",
            description="Classic pizza",
            cooking_time=25,
            servings=2,
            instructions="Make dough, add toppings, bake",
            user=self.user,
            category=self.category
        )
        
        # Check ordering (newest first)
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0], recipe2)  # Most recent first
        self.assertEqual(recipes[1], self.recipe)
    
    def test_recipe_timestamps(self):
        """Test automatic timestamp creation"""
        self.assertIsNotNone(self.recipe.created_date)
        self.assertIsNotNone(self.recipe.updated_date)
    
    def test_recipe_without_category(self):
        """Test recipe creation without category"""
        recipe_no_category = Recipe.objects.create(
            name="Simple Recipe",
            description="No category recipe",
            cooking_time=10,
            servings=1,
            instructions="Simple instructions",
            user=self.user
        )
        self.assertIsNone(recipe_no_category.category)


class RecipeViewsTest(TestCase):
    """Test cases for Recipe views and URL functionality"""
    
    def setUp(self):
        """Set up test data for view tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Italian",
            description="Traditional Italian cuisine"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            description="A test recipe for testing",
            cooking_time=25,
            difficulty="Medium",
            servings=4,
            instructions="Test instructions for recipe",
            user=self.user,
            category=self.category
        )
    
    def test_home_view_status_code(self):
        """Test that home view returns 200 status code"""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Test that home view uses correct template"""
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')
    
    def test_recipe_list_view_status_code(self):
        """Test that recipe list view returns 200 status code"""
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_list_view_template(self):
        """Test that recipe list view uses correct template"""
        response = self.client.get(reverse('recipes:list'))
        self.assertTemplateUsed(response, 'recipes/list.html')
    
    def test_recipe_list_view_context(self):
        """Test that recipe list view contains recipes in context"""
        response = self.client.get(reverse('recipes:list'))
        self.assertIn('recipes', response.context)
        self.assertIn(self.recipe, response.context['recipes'])
    
    def test_recipe_detail_view_status_code(self):
        """Test that recipe detail view returns 200 status code"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view_template(self):
        """Test that recipe detail view uses correct template"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertTemplateUsed(response, 'recipes/detail.html')
    
    def test_recipe_detail_view_context(self):
        """Test that recipe detail view contains correct context"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertIn('recipe', response.context)
        self.assertIn('calculated_difficulty', response.context)
        self.assertIn('ingredients_list', response.context)
        self.assertEqual(response.context['recipe'], self.recipe)
    
    def test_recipe_detail_view_404_for_nonexistent_recipe(self):
        """Test that recipe detail view returns 404 for non-existent recipe"""
        response = self.client.get(reverse('recipes:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_list_view_contains_recipe_links(self):
        """Test that recipe list view contains links to recipe details"""
        response = self.client.get(reverse('recipes:list'))
        detail_url = reverse('recipes:detail', args=[self.recipe.pk])
        self.assertContains(response, detail_url)


class RecipeModelEnhancedTest(TestCase):
    """Test cases for enhanced Recipe model functionality"""
    
    def setUp(self):
        """Set up test data for enhanced model tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test category description"
        )
    
    def test_calculate_difficulty_easy(self):
        """Test difficulty calculation for easy recipes"""
        easy_recipe = Recipe.objects.create(
            name="Easy Recipe",
            description="Quick and simple",
            cooking_time=10,
            servings=2,
            instructions="Simple instructions",
            user=self.user,
            category=self.category
        )
        # Add 2 ingredients (less than 5)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredient1 = Ingredient.objects.create(name="Salt", unit_of_measure="tsp")
        ingredient2 = Ingredient.objects.create(name="Pepper", unit_of_measure="tsp")
        
        RecipeIngredient.objects.create(recipe=easy_recipe, ingredient=ingredient1, quantity=1.0)
        RecipeIngredient.objects.create(recipe=easy_recipe, ingredient=ingredient2, quantity=0.5)
        
        difficulty = easy_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Easy")
    
    def test_calculate_difficulty_medium(self):
        """Test difficulty calculation for medium recipes"""
        medium_recipe = Recipe.objects.create(
            name="Medium Recipe",
            description="Moderately complex",
            cooking_time=45,  # Over 30 minutes
            servings=4,
            instructions="Moderate instructions",
            user=self.user,
            category=self.category
        )
        # Add 7 ingredients (more than 5 but less than 10)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredients = []
        for i in range(7):
            ingredient = Ingredient.objects.create(name=f"Ingredient {i+1}", unit_of_measure="cups")
            ingredients.append(ingredient)
            RecipeIngredient.objects.create(recipe=medium_recipe, ingredient=ingredient, quantity=float(i+1))
        
        difficulty = medium_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Medium")
    
    def test_calculate_difficulty_hard(self):
        """Test difficulty calculation for hard recipes"""
        hard_recipe = Recipe.objects.create(
            name="Hard Recipe",
            description="Complex dish",
            cooking_time=75,  # Over 60 minutes
            servings=6,
            instructions="Complex instructions",
            user=self.user,
            category=self.category
        )
        # Add 12 ingredients (more than 10)
        from ingredients.models import Ingredient, RecipeIngredient
        
        ingredients = []
        for i in range(12):
            ingredient = Ingredient.objects.create(name=f"Complex Ingredient {i+1}", unit_of_measure="units")
            ingredients.append(ingredient)
            RecipeIngredient.objects.create(recipe=hard_recipe, ingredient=ingredient, quantity=float(i+1))
        
        difficulty = hard_recipe.calculate_difficulty()
        self.assertEqual(difficulty, "Hard")
    
    def test_automatic_difficulty_calculation_on_save(self):
        """Test that difficulty is automatically calculated when saving recipe"""
        recipe = Recipe.objects.create(
            name="Auto Difficulty Recipe",
            description="Test auto calculation",
            cooking_time=15,
            servings=2,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        # The difficulty should be automatically set to Easy (default for recipes with few ingredients and short time)
        self.assertEqual(recipe.difficulty, "Easy")
    
    def test_get_ingredients_list_method(self):
        """Test get_ingredients_list method returns correct format"""
        recipe = Recipe.objects.create(
            name="Ingredients Test Recipe",
            description="Test ingredients display",
            cooking_time=20,
            servings=3,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        
        from ingredients.models import Ingredient, RecipeIngredient
        
        # Add some ingredients
        ingredient1 = Ingredient.objects.create(name="Flour", unit_of_measure="cups")
        ingredient2 = Ingredient.objects.create(name="Sugar", unit_of_measure="cups")
        
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1, quantity=2.0)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2, quantity=1.0)
        
        ingredients_list = recipe.get_ingredients_list()
        self.assertIn("2.0 cups of Flour", ingredients_list)
        self.assertIn("1.0 cups of Sugar", ingredients_list)
        self.assertEqual(len(ingredients_list), 2)


class URLPatternsTest(TestCase):
    """Test URL patterns and routing"""
    
    def setUp(self):
        """Set up test data for URL tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.recipe = Recipe.objects.create(
            name="URL Test Recipe",
            description="Recipe for URL testing",
            cooking_time=20,
            servings=4,
            instructions="URL test instructions",
            user=self.user
        )
    
    def test_home_url_resolves_to_home_view(self):
        """Test that home URL resolves to correct view"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_list_url_resolves_to_list_view(self):
        """Test that list URL resolves to correct view"""
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_resolves_to_detail_view(self):
        """Test that detail URL resolves to correct view"""
        url = reverse('recipes:detail', args=[self.recipe.pk])
        self.assertEqual(url, f'/recipe/{self.recipe.pk}/')
    
    def test_all_urls_accessible(self):
        """Test that all URLs are accessible and return appropriate status codes"""
        urls_to_test = [
            reverse('recipes:home'),
            reverse('recipes:list'),
            reverse('recipes:detail', args=[self.recipe.pk]),
        ]
        
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 301, 302], f"URL {url} returned status code {response.status_code}")


class RecipeModelFieldsTest(TestCase):
    """Test enhanced recipe model fields"""
    
    def setUp(self):
        """Set up test data for field tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )
    
    def test_recipe_with_description_field(self):
        """Test that recipe can have description"""
        recipe = Recipe.objects.create(
            name="Recipe with Description",
            description="This is a detailed description of the recipe",
            cooking_time=30,
            servings=4,
            instructions="Detailed cooking instructions",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.description, "This is a detailed description of the recipe")
    
    def test_recipe_with_instructions_field(self):
        """Test that recipe can have instructions"""
        recipe = Recipe.objects.create(
            name="Recipe with Instructions",
            description="Test description",
            cooking_time=25,
            servings=3,
            instructions="Step 1: Prepare ingredients. Step 2: Cook. Step 3: Serve.",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.instructions, "Step 1: Prepare ingredients. Step 2: Cook. Step 3: Serve.")
    
    def test_recipe_with_servings_field(self):
        """Test that recipe servings field works correctly"""
        recipe = Recipe.objects.create(
            name="Recipe with Servings",
            description="Test description",
            cooking_time=20,
            servings=6,
            instructions="Test instructions",
            user=self.user,
            category=self.category
        )
        self.assertEqual(recipe.servings, 6)
    
    def test_recipe_blank_fields_allowed(self):
        """Test that optional fields can be left blank"""
        recipe = Recipe.objects.create(
            name="Minimal Recipe",
            cooking_time=15,
            servings=2,
            user=self.user
        )
        self.assertEqual(recipe.name, "Minimal Recipe")
        self.assertEqual(recipe.cooking_time, 15)
        self.assertEqual(recipe.servings, 2)
        # Optional fields should be empty or have defaults
        self.assertIsNone(recipe.category)
