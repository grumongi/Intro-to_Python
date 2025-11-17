from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe

# Create your views here.

def home(request):
    """Welcome page for the Recipe App"""
    return render(request, 'recipes/recipes_home.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or the page they were trying to access
            next_url = request.GET.get('next', 'recipes:list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'recipes/login.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return render(request, 'recipes/success.html')

@login_required
def recipe_list(request):
    """Display all recipes with their ingredients - Protected view"""
    recipes = Recipe.objects.all().select_related('category', 'user').prefetch_related('recipeingredient_set__ingredient')
    return render(request, 'recipes/list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, pk):
    """Display detailed view of a single recipe - Protected view"""
    recipe = get_object_or_404(Recipe, pk=pk)
    # Recalculate difficulty to ensure it's current
    calculated_difficulty = recipe.calculate_difficulty()
    
    context = {
        'recipe': recipe,
        'calculated_difficulty': calculated_difficulty,
        'ingredients_list': recipe.get_ingredients_list(),
    }
    return render(request, 'recipes/detail.html', context)
