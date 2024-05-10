# <center>Restaurant Menu API</center>

This REST API provides different endpoints for managing restaurant menu items. It allows users to perform operations related to menu items, ingredients, and options, making it a versatile tool for restaurant management systems.

## Getting Started

1. Installation: Clone the repository from GitHub.

```bash
git clone https://github.com/anitdevrim/anitdevrim-akdeniz-otsimo-internship-task-2024
```

2. In order to run the program, go to the directory.

```bash
cd anitdevrim-akdeniz-otsimo-internship-task-2024
```

3. Configuration: This REST API will run on the port 8080 on the localhost. You can change host and port by doing some changes in .env file.

```bash
nano .env
```

4. To run the REST API in the localhost use the command,

```bash
python3 server.py
```

## Usage

There is 8 different endpoints that can be used. Both GET and POST methods can be accessed by terminal using curl commands.

## Endpoints

1. <ins>Listing the Menu</ins>:
   This endpoint lists the whole menu items and their ingredients with options to filter some criteria such as vegan or vegetarian. Following line can be used for making request.

```bash
$ curl http://localhost:8080/listMeals
```

or

```bash
$ curl http://localhost:8080/listMeals?is_vegan=true
```

2.<ins>Getting an item from the menu</ins>:
This endpoint takes an integer as meal_id and outputs the menu item that corresponds to that certain meal_id. Output of this endpoint includes name, ingredients and ingredient options of that menu item. Following line can be used for making request.

```bash
$ curl http://localhost:8080/getMeal?id=2
```

3. <ins>Quality Calculation with Ingredient Qualities</ins>:
   This endpoint takes an integer as meal_id and option for the quality of the ingredients and calculates the quality number of that menu item. If there is no parameter passed for an ingredient, quality of that ingredient is marked as 'high'. Following line can be used for making request.

```bash
$ curl -d "meal_id=1&garlic=high&chicken=low" -X POST http://localhost:8080/quality
```

4. <ins>Price Calculation With Ingredient Qualities</ins>:
   This endpoint takes an integer as meal_id and option for the quality of the ingredients and calculates the price of that menu item. If there is no parameter passed for an ingredient, quality of that ingredient is marked as 'high'. Following line can be used for making request.

```bash
$ curl -d "meal_id=1&garlic=high&chicken=low" -X POST http://localhost:8080/price
```

5. <ins>I'm Feeling Lucky</ins>:
   This endpoint takes an integer as budget and outputs a random meal to a user without exceeding the budget. The parameter budget is optional and if there is no entry for the budget, the budget is assigned to '+inf'. Following line can be used for making request.

```bash
$ curl -d "budget=42.42" -X POST http://localhost:8080/random
```

6. <ins>Searching For a Meal</ins>:
   This endpoint takes a string(text) and checks is there any item that contains that text. Following line can be used for making request.

```bash
$ curl http://localhost:8080/search?query=beer
```

7. <ins>Finding the Highest Quality Meal For Given Budget</ins>:
   This endpoint takes an integer as budget and gives the highest quality meal that can be bought within the given budget. User also can select whether item is a vegan or vegetarian. Following line can be used for making request.

```bash
$ curl -d "budget=42.42&is_vegetarian=false&is_vegan=false" -X POST http://localhost:8080/findHighest
```

8. <ins>Finding the Highest Quality Version of a Meal For Given Budget</ins>:
   This endpoint takes two integer values as meal_id and budget and outputs the best quality version of that given menu item within the given budget. Following line can be used for making request.

```bash
$ curl -d "budget=42.42&meal_id=2&is_vegan=false" -X POST http://localhost:8080/findHighestOfMeal
```
