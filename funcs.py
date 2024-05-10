
def get_meal_with_id(meal_id,meal_list):
    for meal in meal_list:
        if meal_id == meal['id']:
            requested_meal = meal
            break
        else:
            requested_meal = None
    return requested_meal


def get_ingredients_with_id(meal_id,meal_list):
    meal_ingredients = []
    for meal in meal_list:
        if meal_id == meal['id']:
            for ingredient in meal['ingredients']:
                meal_ingredients.append(ingredient['name'])
    return meal_ingredients

def get_quantity_with_id(meal_id,meal_list):
    quantities = []
    for meal in meal_list:
        if meal_id == meal['id']:
            for ingredient in meal['ingredients']:
                quantities.append(ingredient['quantity'])
    return quantities

def get_meal_with_query(search_query,meal_list):
    return_meals = []
    for meal in meal_list:
        if (search_query.lower() in meal['name'].lower()):
            return_meals.append(meal)
    if return_meals == []:
        return None
    else:
        return return_meals

def check_vegetarian(meal,ingredients_list):
    for ingredient in meal['ingredients']:
        ingredient_name = ingredient['name']
        for ingredient in ingredients_list:
            if ingredient_name == ingredient['name']:
                if 'vegetarian' not in ingredient['groups'] and 'vegan' not in ingredient['groups']:
                    return False
    return True

def check_vegan(meal,ingredients_list):
    for ingredient in meal['ingredients']:
        ingredient_name = ingredient['name']
        for ingredient in ingredients_list:
            if ingredient_name == ingredient['name']:
                if 'vegan' not in ingredient['groups']:
                    return False
    return True


def get_quality_score(parameters,meal_ingredients):
    values_dict = {}
    for ingredient in meal_ingredients:
        ingredient = ingredient.lower()
        if ingredient in parameters:
            values_dict[ingredient] = parameters[ingredient]
        else:
            values_dict[ingredient] = 'high'
    
    cost_dict = {'high' : 10, 'medium' : 5, 'low': 1}
    total_cost = float(sum(cost_dict[item_cost] for item_cost in values_dict.values()) / len(values_dict))
    return total_cost

def calculate_price(values_dict,ingredients_list,quantities):
    total_price = 0
    degraded_cost = 0

    for i,(item, quality) in enumerate(values_dict.items()):
        for ingredient in ingredients_list:
            if ingredient['name'].lower() == item.lower():
                for option in ingredient['options']:
                    if quality.lower() == option['quality']:
                        if i < len(quantities):
                            quantity = quantities[i]
                            item_price = 0
                            item_price = (quantity * option['price']) / 1000
                            total_price = total_price + item_price
                            total_price = round(total_price, 2)
                        break
                break
    for quality in values_dict.values():
        if quality == 'low':
            degraded_cost = degraded_cost + 0.1
        elif quality == 'medium':
            degraded_cost = degraded_cost + 0.05
        else:
            pass
    total_price = total_price - degraded_cost
    
    return total_price