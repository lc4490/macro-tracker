import tkinter as tk
from tkinter import *
import os
import subprocess

root = tk.Tk()
root.title("Macro Tracker")
recipes=[]
ingr = []
canvas = tk.Canvas(root, height=500, width = 500, bg = "black")
canvas.pack()
color = "#ececec"

cmd = 'defaults read -g AppleInterfaceStyle'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
if bool(p.communicate()[0]):
    color = "#343434"


#Recipe class that holds list of ingredients
class Recipe:
    def __init__(self, name):
        self.name=name
        self.ingredients=[]
        
    def addIngredient(self, ingr):
        self.ingredients.append(ingr)

#Ingredients class that holds ratios
class Ingredient:
    def __init__(self, name, calories,protein, carb, fats):
        self.name=name
        self.calories = calories
        self.protein = protein
        self.carb = carb
        self.fats = fats
    
    def setCalories(self, newCalories):
        self.calories=newCalories
    
    def setProtein(self, newProtein):
        self.protein=newProtein
    
    def setCarb(self, newCarb):
        self.carb = newCarb
        
    def setFats(self, newFats):
        self.fats = newFats


#Fills out ingr list with Ingredient objects from ingredients.txt
if os.path.isfile("ingredients.txt"):
    with open("ingredients.txt","r") as j:
        temp = j.read()
        tempIngr = temp.split(":")
        for i in tempIngr:
            if i.strip():
                ingrParts = i.split(",")
                tempI = Ingredient(ingrParts[0],ingrParts[1],ingrParts[2],ingrParts[3],ingrParts[4])
                ingr.append(tempI)


#Fills out recipes list with Recipe objects from recipes.txt
if os.path.isfile("recipes.txt"):
    with open("recipes.txt", "r") as f:
        temp = f.read()
        tempRecipe = temp.split(":")
        for i in tempRecipe:
            if i.strip():
                recipeParts = i.split(",")
                tempR = Recipe(recipeParts[0])
                for j in recipeParts[1:]:
                    for k in range(len(ingr)):
                        index=0
                        if(j==ingr[k].name):
                            index=k
                            tempR.addIngredient(ingr[index])
                recipes.append(tempR)
        
#Creates a Recipe object with the input from Entry entry
#Appends object to recipes list
#Displays buttons of all current Recipe in recipes
def addRecipe():  
    for widget in framed.winfo_children():
        widget.pack_forget()
    recipe = Recipe(entry.get())
    recipes.append(recipe)
    title = tk.Label(framed, text="Recipes:")
    title.pack()
    for r in recipes:
        button = tk.Button(framed, text=r.name, command = lambda r=r: viewIngr(framed, r))
        button.pack()
    
#@param previous Frame (in order to delete it), Recipe object
# Creates a new frame on activation
#Displays Recipe name
#Displays list of ingredients as buttons
#Creates buttons to Add Ingredient, Delete Recipe, or Back 
def viewIngr(prevFrame, recipe):
    # prevFrame.destroy()
    frame = tk.Frame(fra, bg= color)
    frame.place(relwidth=1,relheight=1, relx=0, rely= 0)
    title = tk.Label(frame, text= recipe.name)
    title.pack()
    addButt = tk.Button(frame, text="Add Ingredient", command = lambda: addIngr(frame, recipe))
    addButt.pack()
    delButt = tk.Button(frame, text="Delete Recipe", command = lambda: delRec(frame, recipe))
    delButt.pack()
    calcButt = tk.Button(frame, text="Calculate", command = lambda: calculate(frame, recipe))
    calcButt.pack()
    exit = tk.Button(frame, text= "Back", command = lambda: deleteFrame(frame))
    exit.pack()
    label = tk.Label(frame, text= "Ingredient List:")
    label.pack()
    for i in recipe.ingredients:
        button = tk.Button(frame, text=i.name, command = lambda i =i: viewMacro(frame, recipe, i))
        button.pack()

#@param previous Frame, Recipe object
#Creates a new frame on activation
#Parses through recipe.ingredients, stores input into list called entries
#Creates button Calculate to take information and calculate out total macros
def calculate(prevFrame, recipe):
    frame = tk.Frame(fra, bg= color)
    frame.place(relwidth=1,relheight=1,relx=0,rely=0)
    entries = []
    for i in recipe.ingredients:
        label = tk.Label(frame, text="Amount of " +i.name+ " in grams")
        label.pack()
        entry = tk.Entry(frame, width=10)
        entry.pack()
        entries.append(entry)
    button = tk.Button(frame, text="Calculate", command = lambda: calculate2(frame, recipe, entries))
    button.pack()

#@param previous Frame (in order to delete it), Recipe object, entries list
#Parses through recipe.ingredients, adds calories, protein, carbs, fats to total counters
#Displays label with all information
def calculate2(prevFrame, recipe, entries):
    calories,protein,carbs,fats=0,0,0,0
    
    for i in range(len(recipe.ingredients)):
        if not recipe.ingredients[i].calories == "":
            calories = calories + (float(recipe.ingredients[i].calories)/100)*float(entries[i].get())
        if not recipe.ingredients[i].protein == "":
            protein = protein + (float(recipe.ingredients[i].protein)/100)*float(entries[i].get())
        if not recipe.ingredients[i].carb == "":
            carbs = carbs + (float(recipe.ingredients[i].carb)/100)*float(entries[i].get())
        if not recipe.ingredients[i].fats == "":
            fats = fats + (float(recipe.ingredients[i].fats)/100)*float(entries[i].get())
    label = tk.Label(prevFrame, text= "Calories: " +str(calories)+"\nProtein: "+str(protein)+"\nCarbs: "+str(carbs)+"\nFats: "+str(fats))
    label.pack()
    backButton = tk.Button(prevFrame, text="Back", command=lambda: deleteFrame(prevFrame))
    backButton.pack()
    

#@param previous Frame (in order to delete it), Recipe object
# Creates a new frame on activation
#Takes input from Entry name (name of ingredient)
#Calls addMacros function
#Destroys previous frame
def addIngr(prevFrame, recipe):
    
    frame = tk.Frame(fra, bg= color)
    frame.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)
    name = tk.Entry(frame, width=10)
    name.pack()
    button = tk.Button(frame, text="Enter Ingredient Name", command = lambda: addMacros(frame,recipe, name))
    button.pack()
    prevFrame.destroy()

#@param previous Frame (in order to delete it), Recipe object, Name of Ingredient
# Creates new frame on activation
#Checks if name of ingredient is in ingr list
#If it is, Call createIngr to add ingredient to Recipe
#If not, takes input from Entries protein, carbs, fats (protein %, carbs %, fats %)
#Sends name, protein, carbs, fats to createIngr and Calls it
def addMacros(prevFrame,recipe, name):
    n= name.get()
    for i in range(len(ingr)):
        if ingr[i].name == n:
            createIngr(prevFrame, recipe, ingr[i].name, ingr[i].calories, ingr[i].protein, ingr[i].carb,ingr[i].fats)
            return
    
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1, relx=0, rely=0)
    labelTitle = tk.Label(frame, text="Please enter values per 100g")
    labelCa = tk.Label(frame, text="Calories: ")
    labelP = tk.Label(frame, text="Protein:")
    labelC = tk.Label(frame, text="Carbs:")
    labelF = tk.Label(frame, text="Fats:")
    
    calories = tk.Entry(frame, width=10)
    protein = tk.Entry(frame, width=10)
    carbs = tk.Entry(frame, width=10)
    fats = tk.Entry(frame, width=10)
    
    labelTitle.pack()
    labelCa.pack()
    calories.pack()
    labelP.pack()
    protein.pack()
    labelC.pack()
    carbs.pack()
    labelF.pack()
    fats.pack()
        
    button = tk.Button(frame, text="Enter Macroingredients", command = lambda: createIngr(frame,recipe, n, calories.get(), protein.get(), carbs.get(), fats.get()))
    button.pack()
    prevFrame.destroy()

#@param previous Frame (in order to delete it), Recipe object, components of Ingredient object
# Creates ingredient with name, protein, carbs, fats
#Checks if ingredient is already in ingredients list 
#If it is not in the list, append ingredient to ingr
#Adds ingredient to Recipe object   
def createIngr(prevFrame,recipe, name, calories, protein, carbs, fats):
    i = Ingredient(name, calories, protein, carbs, fats)
    exists=False
    for j in range(len(ingr)):
        if ingr[j].name == i.name:
            exists=True
    if(exists ==False):
        ingr.append(i)
    recipe.addIngredient(i)
    prevFrame.destroy()
    # framed.destroy()

#@param previous Frame (in order to delete it), Recipe object
#Deletes recipe from recipes
#Forgets all widgets in framed
#Repacks current recipes to Framed
def delRec(prevFrame, recipe):
    del recipes[recipes.index(recipe)]
    for widget in framed.winfo_children():
        widget.pack_forget()
    title = tk.Label(framed, text="Recipes:")
    title.pack()
    for r in recipes:
        button = tk.Button(framed, text=r.name, command = lambda r=r: viewIngr(framed, r))
        button.pack()
    prevFrame.destroy()
        
#@param previous Frame
#Destroys it
def deleteFrame(f):
    f.destroy()

#@param previous Frame (in order to delete it), Recipe object, Ingredient object
#Creates new Frame on activation
#Displays Protein, Carbs, Fats percentages
#Creates buttons Remove Ingredient, Delete Ingredient, Back
def viewMacro(prevFrame, recipe, ingredient):
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1, relx=0, rely= 0)
    
    titleLabel = tk.Label(frame, text="Values per 100g")
    caloriesLabel = tk.Button(frame, text= "Calories: "+ingredient.calories, command=lambda:editCalories(frame,recipe,ingredient))
    proteinLabel = tk.Button(frame, text = "Protein: "+ ingredient.protein, command = lambda:editProtein(frame,recipe,ingredient))
    carbsLabel = tk.Button(frame, text = "Carbs: "+ ingredient.carb, command = lambda:editCarb(frame, recipe,ingredient))
    fatsLabel = tk.Button(frame, text = "Fats: "+ ingredient.fats, command=lambda: editFats(frame, recipe,ingredient))
    
    titleLabel.pack()
    caloriesLabel.pack()
    proteinLabel.pack()
    carbsLabel.pack()
    fatsLabel.pack()
    remButt = tk.Button(frame, text="Remove Ingredient", command = lambda: remMac(frame, recipe, ingredient))
    remButt.pack()
    delButt = tk.Button(frame, text="Delete Ingredient", command = lambda: delMac(prevFrame,frame, ingredient))
    delButt.pack()
    
    exit = tk.Button(frame, text= "Back", command = lambda: deleteFrame(frame))
    exit.pack()
    
def editCalories(prevFrame, recipe, ingredient):
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1,relx=0,rely=0)
    
    entry = tk.Entry(frame, width=10)
    entry.pack()
    button = tk.Button(frame, text="Change Calories",command=lambda:editCalories2(frame, recipe, ingredient,entry.get()))
    button.pack()
    prevFrame.destroy()

def editCalories2(prevFrame, recipe, ingredient,new):
    ingredient.setCalories(new)
    prevFrame.destroy()

def editProtein(prevFrame, recipe, ingredient):
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1,relx=0,rely=0)
    
    entry = tk.Entry(frame, width=10)
    entry.pack()
    button = tk.Button(frame, text="Change Protein",command=lambda:editProtein2(frame, recipe, ingredient,entry.get()))
    button.pack()
    prevFrame.destroy()

def editProtein2(prevFrame, recipe, ingredient,new):
    ingredient.setProtein(new)
    prevFrame.destroy()

def editCarb(prevFrame, recipe, ingredient):
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1,relx=0,rely=0)
    
    entry = tk.Entry(frame, width=10)
    entry.pack()
    button = tk.Button(frame, text="Change Carbs",command=lambda:editCarbs2(frame, recipe, ingredient,entry.get()))
    button.pack()
    prevFrame.destroy()

def editCarbs2(prevFrame, recipe, ingredient,new):
    ingredient.setCarb(new)
    prevFrame.destroy()
    
def editFats(prevFrame, recipe, ingredient):
    frame = tk.Frame(fra, bg=color)
    frame.place(relwidth=1,relheight=1,relx=0,rely=0)
    
    entry = tk.Entry(frame, width=10)
    entry.pack()
    button = tk.Button(frame, text="Change Fats",command=lambda:editFats2(frame, recipe, ingredient,entry.get()))
    button.pack()
    prevFrame.destroy()

def editFats2(prevFrame, recipe, ingredient,new):
    ingredient.setFats(new)
    prevFrame.destroy()
    

#@param previous Frame (in order to delete it), Recipe object, Ingredient object
#Removes ingredient from recipe
def remMac (prevFrame, recipe, ingredient):
    del recipe.ingredients[recipe.ingredients.index(ingredient)]
    prevFrame.destroy()

#@param previous Frame (in order to delete it), Recipe object, Ingredient object
#Removes ingredient from recipe
#Deletes ingredient from ingr   
def delMac(prevFrame, frame, ingredient):
    del ingr[ingr.index(ingredient)]
    for rec in recipes:
        for ingredientss in rec.ingredients:
            if ingredientss==ingredient:
                del rec.ingredients[rec.ingredients.index(ingredientss)]
    prevFrame.destroy()
    frame.destroy()
    
 

    


fra = tk.Frame(root, bg= color)
fra.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)
framed = tk.Frame(root, bg=color)
framed.place(relwidth=1, relheight=0.5, relx= 0, rely=0.5)

entry = tk.Entry(fra, width = 50)
entry.pack()

button = tk.Button(fra, text="Add Recipe", command=addRecipe)
button.pack()

title = tk.Label(framed, text="Recipes:")
title.pack()
for r in recipes:
    button = tk.Button(framed, text=r.name, command = lambda r = r: viewIngr(framed, r))
    button.pack()

root.mainloop()

with open('ingredients.txt','w') as j:
    for i in ingr:
        j.write(i.name +"," +i.calories+","+i.protein+ ","+ i.carb + ","+i.fats + ":")

with open('recipes.txt','w') as f:
    for recipe in recipes:
        ret = ""
        for ingredient in recipe.ingredients:
            ret = ret + "," + ingredient.name
        f.write(recipe.name+ret+":")