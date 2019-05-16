import pandas as pd

def get_corresponding_recipes(final_results, chefkoch_rezepte_csv):
    chefkoch_rezepte_result = pd.DataFrame()
    for recipe_id_single in final_results:
        chefkoch_rezepte_result = chefkoch_rezepte_result.append(chefkoch_rezepte_csv.query('recipe_id in @recipe_id_single[2]'), ignore_index=True)
    return chefkoch_rezepte_result
