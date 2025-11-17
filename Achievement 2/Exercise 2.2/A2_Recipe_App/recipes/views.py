from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

def home(request):
    """Welcome page for the Recipe App"""
    return render(request, 'recipes/recipes_home.html')

def recipe_list(request):
    """Display all recipes with their ingredients"""
    recipes = Recipe.objects.all().select_related('category', 'user').prefetch_related('recipeingredient_set__ingredient')
    return render(request, 'recipes/list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    """Display detailed view of a single recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    # Recalculate difficulty to ensure it's current
    calculated_difficulty = recipe.calculate_difficulty()
    
    context = {
        'recipe': recipe,
        'calculated_difficulty': calculated_difficulty,
        'ingredients_list': recipe.get_ingredients_list(),
    }
    return render(request, 'recipes/detail.html', context)
