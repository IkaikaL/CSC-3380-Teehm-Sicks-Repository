from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import SearchToolForm, RecipeSubmissionForm, MealPlanForm, SearchEngine
import shutil
import re
from .meal_plan import daily_plan
#from .SearchEngine import SearchEngine

def Homepage(request):
    return render(request,'display/homepage.html/')

def SearchTool(request):
    form = SearchToolForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            price_range = form['price_filter'].data
            name = form['name'].data
            ingredients = form['ingredients'].data

            if price_range == 'under_5':
                price_range = 5
            elif price_range == '5_10':
                price_range = 10
            else:
                price_range = 15

            obj = SearchEngine()
            obj.changePrice(price_range)
            obj.changeName(name)
            obj.addIngredients(ingredients)
            obj.printEverything()
            recipes = obj.searchFilters()
            #print(recipes)
            #print(FindRecipeDetails(recipes))
            
            #once we have the list of recipes, go read the ingredients for each one
            #for i in range (0,len(recipes)):
            #    print(recipes[i])
            #    print(FindRecipeDetailsForOneRecipe(recipes[i]))
            
            #print(recipes)
            return render(request,'display/search_tool.html/', {
                'form': form,
                'recipes': json.dumps(recipes)
            })
    return render(request,'display/search_tool.html/', {
        'form':form
    })

def FindRecipeDetailsForOneRecipe (recipe):
    #read = open("display/DataBase.txt", "r")

    with open('display/DataBase.txt') as f:
        for line in f:
            
            if recipe in line:
                ingredients = next(f).strip('& ')
                cost = next(f).strip('$ ')
                instructions = next(f).strip(': ')
                return [ingredients.strip('\n'),cost.strip('\n'),instructions.strip('\n')]

def FindRecipeDetails(recipes):
    i = 0
    read = open("display/DataBase.txt", "r")
    for line in read:
        if '*' in line:
            if line.strip('* ').strip('\n') in recipes[i] and i < 3:
                outputDetails = open('display/Output.txt', 'a')
                outputDetails.write(line.strip('* '))
                outputDetails.write(next(read).strip('& '))
                outputDetails.write(next(read).strip('$ '))
                outputDetails.write(next(read).strip(': '))
                outputDetails.write('\n')
                outputDetails.close()
                read.seek(0,0)
                i += 1
    read.close()
    #print(outputDetails)



def RecipeSubmission(request):
    form = RecipeSubmissionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cost = form['cost'].data
            name = form['name'].data
            ingredients = form['ingredients'].data
            direction = form['direction'].data
            RecipeSubmissionProcess(cost, name, ingredients, direction)
    return render(request,'display/recipe_submission.html/', {'form':form})

def MealPlan(request):
    form = MealPlanForm(request.POST or None)
    #test = SearchEngine("hello","hello","hello")
    #print(test._price)
    if request.method == 'POST':
        if form.is_valid():
            name = form['name'].data
            day = form['day'].data
            AddToMealPlan(name, day)
            daily_plan[day] = name
            
    return render(request, 'display/meal_plan.html/', {
        'form': form,
        'mon': daily_plan['Monday'],
        'tue': daily_plan['Tuesday'],
        'wed': daily_plan['Wednesday'],
        'thu': daily_plan['Thursday'],
        'fri': daily_plan['Friday'],
        'sat': daily_plan['Saturday'],
        'sun': daily_plan['Sunday'],
    })

def RecipeSubmissionProcess(cost, name, ingredients, direction):
    #form = RecipeSubmissionForm()
    recipeSubmit = open("display/DataBase.txt", "a")
    recipeSubmit.write('\n* ')
    recipeSubmit.write(name)
    recipeSubmit.write('\n& ')
    recipeSubmit.write(ingredients)
    recipeSubmit.write("\n$ ")
    recipeSubmit.write(cost)
    recipeSubmit.write("\n: ")
    recipeSubmit.write(direction)
    recipeSubmit.close()

def AddToMealPlan(name, day):
    comp = day + ":\n"
    i = 0
    mealPlan = open("display/MealPlanTemplate.txt", "r")
    allLines = mealPlan.readlines()
    size = len(allLines)
    #print(name)
    #print(allLines[0])
    while i < size-1:
        line = allLines[i]
        #print(comp)
       #print(line)
        if line == comp:
            
            allLines[i+1] = name + "\n"
        i += 1
    mealPlan.close()
    #print(allLines)
    mealPlan = open("display/MealPlanTemplate.txt", "w")
    mealPlan.writelines(allLines)
    mealPlan.close()
    
