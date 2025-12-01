from sklearn.metrics.pairwise import cosine_similarity
from embeddings import embed_text

def rank_ingredients(goal: str, ingredients:list,top_k:int = 20):

    """
    :param goal:
    :param ingredients:
    :param top_k:

    ingredients would be a list of dicts e.g.
        [
             { "ingredient": "Chicken breast", "protein": 31, "category": "protein", ...},
            ...
        ]
    """

    goal_vector = embed_text(goal)

    scored = []

    for item in ingredients:
        ingredient_desc = f"{item['ingredient']} {item.get('category', '')} {item.get('protein', '')} protein"
        ingredient_vec = embed_text(ingredient_desc)

        score = cosine_similarity([goal_vector], [ingredient_vec])[0][0]

        scored.append((item, score))

    # Sort highest similarity first
    scored.sort(key=lambda x: x[1], reverse=True)


    # Return top K ingredients
    top_items = []
    for item, score in scored[:top_k]:
        top_items.append(item)
    return top_items

