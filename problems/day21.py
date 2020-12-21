from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass(frozen=True)
class Recipe:
    ingredients: List[str]
    allergens: List[str]   


def parse_recipe(line: str) -> Recipe:
    splt = line.split('(contains ')
    ingredients = splt[0].strip().split(' ')
    allergens = splt[1].split(')')[0].strip().split(', ')
    return Recipe(ingredients, allergens)


def parse_input(lines: List[str]) -> List[Recipe]:
    return [parse_recipe(line.strip()) for line in lines]


def find_allergen_mappings(recipes: List[Recipe]) -> Dict[str, Set[str]]:
    allergen_to_recipes = defaultdict(list)

    # Find all recipes that have each allergen
    for recipe in recipes:
        for allergen in recipe.allergens:
            allergen_to_recipes[allergen].append(recipe)

    # Find ingredients that are in the intersection of all recipes for each allergen
    allergen_to_ingredients = defaultdict(list)
    for allergen, recipes in allergen_to_recipes.items():
        possible_ingredients = set(recipes[0].ingredients)
        for r in recipes:
            possible_ingredients.intersection_update(r.ingredients)
        allergen_to_ingredients[allergen] = possible_ingredients
    
    return allergen_to_ingredients


def part1(recipes: List[Recipe]) -> int:
    allergen_mapping = find_allergen_mappings(recipes)
    print(allergen_mapping)
    possibly_allergen_ingredients = {v for s in allergen_mapping.values() for v in s}
    non_allergen_count = 0
    for recipe in recipes:
        non_allergen_count += len([i for i in recipe.ingredients if i not in possibly_allergen_ingredients])
    return non_allergen_count


def part2(data: List[Recipe]) -> int:
    pass