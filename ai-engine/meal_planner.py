from openai import OpenAI
import json
import os
from ranker import rank_ingredients

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_meal_plan(goal: str, ingredients: list):

    # 1. Rank the ingredients using embeddings
    ranked = rank_ingredients(goal,ingredients,top_k=30)

    # 2. Convert to readable list
    ingredient_names = []
    for item in ranked:
        ingredient_names.append(item["ingredient"])

    # 3. Create prompt for LLM
    prompt = """
    You are an expert nutritionist and meal-planning AI.

    The user goal is:
    "{goal}"

    The available ingredients (ranked and filtered) are:
    {ingredients}

    Your tasks:
    1. Create a structured 5-day meal plan (Day 1 → Day 5).
    2. Each day must contain EXACTLY:
       - breakfast
       - lunch
       - dinner
    3. For EACH meal:
       - Provide a short descriptive meal name (no recipes).
       - List the ingredients used for that meal in "ingredients_used".
       - Only choose ingredients from the available list.
    4. If any required ingredient is NOT in the available list, add it to "missing_items".
    5. Do NOT include cooking steps or portion sizes.
    6. Output MUST be valid JSON. Return ONLY the JSON.

    Use this exact JSON structure:

    {{
      "meal_plan": {{
        "Day 1": {{
          "breakfast": {{
            "meal": "",
            "ingredients_used": []
          }},
          "lunch": {{
            "meal": "",
            "ingredients_used": []
          }},
          "dinner": {{
            "meal": "",
            "ingredients_used": []
          }}
        }},
        "Day 2": {{
          "breakfast": {{
            "meal": "",
            "ingredients_used": []
          }},
          "lunch": {{
            "meal": "",
            "ingredients_used": []
          }},
          "dinner": {{
            "meal": "",
            "ingredients_used": []
          }}
        }},
        "Day 3": {{
          "breakfast": {{
            "meal": "",
            "ingredients_used": []
          }},
          "lunch": {{
            "meal": "",
            "ingredients_used": []
          }},
          "dinner": {{
            "meal": "",
            "ingredients_used": []
          }}
        }},
        "Day 4": {{
          "breakfast": {{
            "meal": "",
            "ingredients_used": []
          }},
          "lunch": {{
            "meal": "",
            "ingredients_used": []
          }},
          "dinner": {{
            "meal": "",
            "ingredients_used": []
          }}
        }},
        "Day 5": {{
          "breakfast": {{
            "meal": "",
            "ingredients_used": []
          }},
          "lunch": {{
            "meal": "",
            "ingredients_used": []
          }},
          "dinner": {{
            "meal": "",
            "ingredients_used": []
          }}
        }}
      }},
      "missing_items": []
    }}

    Rules:
    - All keys must remain EXACTLY as shown.
    - "ingredients_used" must contain ingredient names only.
    - Output must be valid JSON that can be parsed.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # 4. Parse JSON returned by LLM
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"error": "Failed to parse LLM output"}


