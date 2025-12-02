import pandas as pd
import os



def load_ingredients(csv_path: str = None) -> pd.DataFrame:
    """
    Loads cleaned ingredients.csv into a pandas DataFrame.
    Auto-corrects accidental quotes in headers.
    """

    if csv_path is None:
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, "ingredients.csv")

    df = pd.read_csv(csv_path)

    # Clean column names (remove stray quotes or spaces)
    df.columns = df.columns.str.replace('"', '').str.strip()

    print("Dataset loaded:", df.shape, "is the shape")
    return df


# -------------------------------------------------------------------
# FILTERING LOGIC BASED ON GOALS
# -------------------------------------------------------------------

def filter_ingredients(goal: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters ingredient dataset based on user dietary goals.

    Available goals:
        - bulking (high protein)
        - weight_loss (low calorie)
        - vegetarian (plant-based)
    """

    goal = goal.lower().strip()

    # ------------------------
    # 1. Bulking = High Protein
    # ------------------------
    if goal == "bulking":
        return df[df["protein"] >= 20].reset_index(drop=True)

    # ------------------------
    # 2. Weight Loss = Low Calorie
    # ------------------------
    elif goal == "weight_loss":
        return df[df["calories"] <= 120].reset_index(drop=True)

    # ------------------------
    # 3. Vegetarian = Plant-Based
    # ------------------------
    elif goal == "vegetarian":
        plant_keywords = [
            "tofu", "lentils", "quinoa", "brown rice", "broccoli", "spinach",
            "kale", "sweet potato", "oats", "almonds", "black beans",
            "chickpeas"
        ]

        return df[
            df["ingredient"].str.lower().str.contains("|".join(plant_keywords))
        ].reset_index(drop=True)

    else:
        raise ValueError(
            "Invalid goal. Choose from: 'bulking', 'weight_loss', 'vegetarian'."
        )


# -------------------------------------------------------------------
# OPTIONAL: TEST RUN
# -------------------------------------------------------------------

if __name__ == "__main__":
    df = load_ingredients()

    print("\n--- Bulking Ingredients (High Protein) ---")
    print(filter_ingredients("bulking", df))

    print("\n--- Weight Loss (Low Calorie) ---")
    print(filter_ingredients("weight_loss", df))

    print("\n--- Vegetarian (Plant-Based) ---")
    print(filter_ingredients("vegetarian", df))
