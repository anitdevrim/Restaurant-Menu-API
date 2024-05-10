import json
import itertools

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from funcs import *

import random

with open('dataset.json', 'r') as file:
    json_data = json.load(file)

meal_list = json_data['meals']
ingredients_list = json_data['ingredients']


class RESTHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        # listMeals
        if parsed_url.path == '/listMeals':
            list_meals_json = []
            is_vegetarian = False
            is_vegan = False

            if 'is_vegetarian' in query:
                if (query['is_vegetarian'][0].lower()) == 'true':
                    is_vegetarian = True
                else:
                    is_vegetarian = False

            if 'is_vegan' in query:
                if (query['is_vegan'][0].lower()) == 'true':
                    is_vegan = True
                else:
                    is_vegan = False

            for meal in meal_list:
                if is_vegan and check_vegan(meal,ingredients_list) == False:
                    continue
                if is_vegetarian and check_vegetarian(meal,ingredients_list) == False:
                    continue

                result = {
                    'id': meal['id'],
                    'name': meal['name'],
                    'ingredients': [ingredient['name'] for ingredient in meal['ingredients']]
                }

                list_meals_json.append(result)

            response_json = json.dumps(list_meals_json)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))

        # getMeal
        elif parsed_url.path == '/getMeal':
            meal_id = int(query.get('id', [None])[0])
            requested_meal = get_meal_with_id(meal_id, meal_list)

            if requested_meal is not None:
                meal_ingredients = get_ingredients_with_id(meal_id,meal_list)

                ingredient_parts = []
                for ingredient_name in meal_ingredients:
                    for ingredient in ingredients_list:
                        if ingredient['name'].lower() == ingredient_name.lower():
                            ingredient_parts.append(ingredient)
                            break
            
                requested_meal['ingredients'] = ingredient_parts
                response_json = json.dumps(requested_meal)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_error(404, 'There is no such meal in the menu!')
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

        # search
        elif parsed_url.path == '/search':
            params = parse_qs(parsed_url.query)
            search_query = params['query'][0]
            return_meals = get_meal_with_query(search_query,meal_list)
            if return_meals is not None:
                result_list = []
                for meal in return_meals:
                    result_json = {
                        'id' : meal['id'],
                        'name' : meal['name'],
                        'ingredients' : [ingredient['name'] for ingredient in meal['ingredients']]
                    }
                    result_list.append(result_json)
                response_json = json.dumps(result_list)
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_error(404,'There is no such meal with the given name!')
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

        # If there is no true endpoint
        else:
            self.send_error(404, 'There is no such endpoint')
            self.send_response(404)
            self.send_header('Content-type','application/json')
            self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)

        # quality
        if parsed_url.path == '/quality':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            post_params = parse_qs(post_data)
            meal_id = int(post_params.get("meal_id", [None])[0])
            requested_meal = get_meal_with_id(meal_id, meal_list)

            parameters = {}
            for key, value in post_params.items():
                if key != "meal_id":
                    parameters[key] = value[0]

            if requested_meal is not None:
                meal_ingredients = get_ingredients_with_id(meal_id,meal_list)
                total_cost = get_quality_score(parameters,meal_ingredients)

                result_json = {
                    'quality': total_cost
                }
                response_json = json.dumps(result_json)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_error(404,'There is no such meal with the given id!')
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

        # price
        elif parsed_url.path == '/price':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            post_params = parse_qs(post_data)
            meal_id = int(post_params.get("meal_id", [None])[0])
            requested_meal = get_meal_with_id(meal_id, meal_list)

            parameters = {}
            values_dict = {}

            for key, value in post_params.items():
                if key != "meal_id":
                    parameters[key] = value[0]
            
            if requested_meal is not None:
                meal_ingredients = get_ingredients_with_id(meal_id,meal_list)
                quantities = get_quantity_with_id(meal_id,meal_list)
                for ingredient in meal_ingredients:
                    ingredient = ingredient.lower()
                    if ingredient in parameters:
                        values_dict[ingredient] = parameters[ingredient]
                    else:
                        values_dict[ingredient] = 'high'
            else:
                self.send_error(404, 'There is no such meal with the given id!')
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()

            total_price = calculate_price(values_dict,ingredients_list,quantities)

            result_json = {
                'price' : total_price
            }

            response_json = json.dumps(result_json)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
        
        # random
        elif parsed_url.path == '/random':
            content_length = self.headers['Content-Length']

            if content_length is None:
                budget = float('inf')
            else:
                content_length = int(content_length)
                post_data = self.rfile.read(content_length)
                post_data = post_data.decode('utf-8')
                post_params = parse_qs(post_data)
                budget = post_params.get('budget', [None])[0]
            
            qualities = ['high', 'medium', 'low']

            while True:
                random_meal_id = random.randint(1,len(meal_list))
                random_meal = get_meal_with_id(random_meal_id,meal_list)
                random_meal_ingredients = get_ingredients_with_id(random_meal_id, meal_list)
                random_qualities_dict = {}

                for ingredient in random_meal_ingredients:
                    random_qualities_dict[ingredient] = random.choice(qualities)

                quantities = get_quantity_with_id(random_meal_id,meal_list)
                total_price = calculate_price(random_qualities_dict,ingredients_list,quantities)
                random_qualities_dict = {key.lower(): value for key, value in random_qualities_dict.items()}
                quality_score = round(get_quality_score(random_qualities_dict,random_meal_ingredients), 2)

                if float(total_price) <= float(budget):
                    break
                else:
                    pass

            random_meal_json = {
                'id' : random_meal_id,
                'name' : random_meal['name'],
                'price' : total_price,
                'quality_score' : quality_score,
                'ingredients': [ingredient['name'] for ingredient in random_meal['ingredients']],
                'ingredients' : [{'name': ingredient, 'quality': random_qualities_dict.get(ingredient.lower())} for ingredient in random_meal_ingredients]
            }

            response_json = json.dumps(random_meal_json)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))

        # findHighest
        elif parsed_url.path == '/findHighest':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            post_params = parse_qs(post_data)
            budget = float(post_params.get('budget', [None])[0])

            if budget is not None:
                qualities = ['high','medium','low']
                highest_quality_score = 0
                best_combination = None
                final_price = 0

                if 'is_vegetarian' in post_params:
                    if (post_params['is_vegetarian'][0].lower()) == 'true':
                        is_vegetarian = True
                    else:
                        is_vegetarian = False
                else:
                    is_vegetarian = False

                if 'is_vegan' in post_params:
                    if (post_params['is_vegan'][0].lower()) == 'true':
                        is_vegan = True
                    else:
                        is_vegan = False
                else:
                    is_vegan = False

                for meal in meal_list:
                    if is_vegan and check_vegan(meal,ingredients_list) == False:
                        continue
                    if is_vegetarian and check_vegetarian(meal,ingredients_list) == False:
                        continue
                    
                    all_combinations = []
                    meal_id = meal['id']
                    meal_ingredients = get_ingredients_with_id(meal_id,meal_list)
                    quantities = get_quantity_with_id(meal_id,meal_list)

                    quality_combinations = itertools.product(qualities, repeat=len(meal_ingredients))
                    
                    for comb in quality_combinations:
                        combination_dict = {ingredient.lower():quality.lower() for ingredient, quality in zip(meal_ingredients, comb)}
                        all_combinations.append(combination_dict)

                    
                    for combination in all_combinations:
                        quality_score = get_quality_score(combination,meal_ingredients)
                        total_price = calculate_price(combination,ingredients_list,quantities)

                        if total_price <= budget:
                            if quality_score > highest_quality_score:
                                highest_quality_score = quality_score
                                best_combination = combination
                                final_price = total_price
                                final_meal_ingredients = meal_ingredients
                                final_meal_id = meal_id
                                final_meal_name = meal['name']
                            elif quality_score == highest_quality_score:
                                if total_price > final_price:
                                    highest_quality_score = quality_score
                                    best_combination = combination
                                    final_price = total_price
                                    final_meal_ingredients = meal_ingredients
                                    final_meal_id = meal_id
                                    final_meal_name = meal['name']
                                elif final_price >= total_price:
                                    continue
                        

                if best_combination is not None:
                    result_json = {
                        'id' : final_meal_id,
                        'name': final_meal_name,
                        'price': final_price,
                        'quality_score' : highest_quality_score,
                        'ingredients': [{'name' : ingredient, 'quality': best_combination.get(ingredient.lower()) } for ingredient in final_meal_ingredients ]
                    }

                    response_json = json.dumps(result_json)
                    self.send_response(200)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(response_json.encode('utf-8'))
                else:
                    self.send_error(400,'There is no such possible meal with the given id!')
                    self.send_response(400)
                    self.send_header('Content-type','application/json')
                    self.end_headers()


            else:
                self.send_error(404, 'Budget is not given!')
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

        # findHighestOfMeal
        elif parsed_url.path == '/findHighestOfMeal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            post_params = parse_qs(post_data)
            meal_id = int(post_params.get('meal_id', [None])[0])
            budget = float(post_params.get('budget', [None])[0])

            meal = get_meal_with_id(meal_id,meal_list)
            qualities = ['high','medium','low']
            all_combinations = []

            if meal is not None:
                meal_ingredients = get_ingredients_with_id(meal_id,meal_list)
                quantities = get_quantity_with_id(meal_id,meal_list)

                quality_combinations = itertools.product(qualities, repeat=len(meal_ingredients))
                for combination in quality_combinations:
                    combination_dict = {ingredient.lower():quality for ingredient, quality in zip(meal_ingredients, combination)}
                    all_combinations.append(combination_dict)
                
                highest_quality_score = 0
                best_combination = None
                final_price = 0

                for combination in all_combinations:
                    quality_score = get_quality_score(combination,meal_ingredients)
                    total_price = calculate_price(combination,ingredients_list,quantities)

                    if total_price <= budget and quality_score >= highest_quality_score:
                        highest_quality_score = quality_score
                        best_combination = combination
                        final_price = total_price
                
                if best_combination is not None:
                    result_json = {
                        'id' : meal_id,
                        'name': meal['name'],
                        'price': final_price,
                        'quality_score' : highest_quality_score,
                        'ingredients': [{'name' : ingredient, 'quality': best_combination.get(ingredient.lower()) } for ingredient in meal_ingredients ]
                    }

                    response_json = json.dumps(result_json)
                    self.send_response(200)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(response_json.encode('utf-8'))

                else:
                    self.send_error(400, 'There is no such possible meal with the given id!')
                    self.send_response(400)
                    self.send_header('Content-type','application/json')
                    self.end_headers()

            
            else:
                self.send_error(404, 'There is no such meal in the menu with the given id!')
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()

        # If there is no true endpoint
        else:
            self.send_error(404,'There is no such endpoint!')
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
