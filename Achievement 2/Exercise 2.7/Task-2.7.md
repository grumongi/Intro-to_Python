# Task 2.7 - Recipe Search and Data Visualization

## Search Implementation Planning

### Search Criteria for Users
Users should be able to search recipes based on:

1. **Recipe Name**: Full or partial recipe names (e.g., "Pizza", "Choc", "Bread")
2. **Ingredients**: Search by ingredient names (e.g., "tomato", "cheese", "chicken")
3. **Difficulty Level**: Filter by Easy, Medium, or Hard
4. **Cooking Time**: Filter by time ranges (e.g., <30 min, 30-60 min, >60 min)
5. **Category**: Filter by recipe categories

### Search Features
- **Wildcard Search**: Partial matches using contains lookups
- **Case Insensitive**: Search should work regardless of case
- **Multiple Criteria**: Allow combining multiple search filters
- **Show All Option**: View all recipes without filters

### Output Format
- **Table Display**: Search results shown in a clean table format
- **Clickable Results**: Each recipe name links to its detail page
- **Result Count**: Display number of results found
- **Sorting Options**: Allow sorting by name, difficulty, cooking time

### Search Form Fields
1. Recipe Name (text input)
2. Ingredients (text input) 
3. Difficulty (dropdown: Any, Easy, Medium, Hard)
4. Cooking Time (dropdown: Any, <30min, 30-60min, >60min)
5. Search Button
6. Show All Button

## Data Analysis

### Visualization Requirements

#### 1. Bar Chart - Recipes by Difficulty Level
- **Purpose**: Show distribution of recipes across difficulty levels
- **X-axis**: Difficulty levels (Easy, Medium, Hard)
- **Y-axis**: Number of recipes
- **Labels**: Count of recipes for each difficulty
- **Display**: Always visible on analytics page

#### 2. Pie Chart - Recipes by Cooking Time Ranges
- **Purpose**: Show proportion of recipes in different time categories
- **Categories**: Quick (<30 min), Medium (30-60 min), Long (>60 min)
- **Labels**: Percentage and count for each category
- **Display**: User can toggle view on analytics page

#### 3. Line Chart - Recipe Creation Trend Over Time
- **Purpose**: Show how recipe additions trend over months
- **X-axis**: Months (last 12 months)
- **Y-axis**: Number of recipes created
- **Labels**: Month names and recipe counts
- **Display**: Available on analytics dashboard for admin users

### Implementation Strategy
1. Create analytics views with matplotlib charts
2. Convert Django QuerySets to pandas DataFrames for analysis
3. Generate charts as base64 encoded images for web display
4. Provide interactive filters for chart customization
5. Cache chart data for better performance