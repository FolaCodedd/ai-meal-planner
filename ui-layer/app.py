# app.py
import streamlit as st
import pandas as pd

# === IMPORT BACKEND LOGIC (from Person 1 & 2) ===
# Make sure these files and functions exist:
#   - data_layer.py  -> load_ingredients, filter_ingredients
#   - ai_layer.py    -> generate_meal_plan
from data_layer import load_ingredients, filter_ingredients
from ai_layer import generate_meal_plan


# ---------- Helper: nice rendering of a single day's meals ----------
def render_day(day_data: dict):
    """
    Expects structure like:
    {
        "day": 1,
        "meals": {
            "breakfast": {"name": "...", "ingredients": ["..", ".."]},
            "lunch": {"name": "...", "ingredients": [...]},
            "dinner": {"name": "...", "ingredients": [...]}
        }
    }
    """
    day_number = day_data.get("day", "")
    meals = day_data.get("meals", {})

    st.subheader(f"Day {day_number}")

    for meal_name in ["breakfast", "lunch", "dinner"]:
        meal = meals.get(meal_name)
        if not meal:
            continue

        with st.expander(meal_name.capitalize()):
            st.markdown(f"**Meal:** {meal.get('name', 'N/A')}")
            ingredients = meal.get("ingredients", [])
            if ingredients:
                st.markdown("**Ingredients:**")
                for item in ingredients:
                    st.write(f"- {item}")
            instructions = meal.get("instructions")
            if instructions:
                st.markdown("**Instructions:**")
                st.write(instructions)


# ---------- Streamlit App ----------
def main():
    st.set_page_config(
        page_title="Smart Meal Planner",
        page_icon="🥗",
        layout="wide"
    )

    st.title("🥗 Smart Meal Planner")
    st.write("Generate a 5-day meal plan based on your fitness goal.")

    # === Sidebar (Settings) ===
    st.sidebar.header("Settings")

    goal_options = [
        "High protein (bulking)",
        "Low calorie (weight loss)",
        "Vegetarian (plant-based)"
    ]

    selected_goal_label = st.sidebar.selectbox(
        "Select your primary goal",
        goal_options
    )

    # A free-text input for extra details
    user_goal_text = st.text_area(
        "Describe your goal / preferences (optional)",
        placeholder="e.g., I want to gain muscle, I can cook 2 meals per day, no dairy..."
    )

    st.markdown("---")

    # === Button to generate plan ===
    if st.button("✨ Generate 5-Day Meal Plan"):
        try:
            # 1. Load ingredients (Person 1)
            df = load_ingredients("ingredients.csv")

            # 2. Map UI label to internal goal string for filter_ingredients()
            if "bulking" in selected_goal_label.lower():
                goal_internal = "bulking"
            elif "weight loss" in selected_goal_label.lower():
                goal_internal = "weight_loss"
            else:
                goal_internal = "vegetarian"

            # 3. Filter ingredients (Person 1)
            filtered_df = filter_ingredients(goal_internal, df)

            if filtered_df.empty:
                st.error("No ingredients found matching this goal. Check your CSV or filters.")
                return

            # 4. Build full goal text sent to AI (Person 2)
            full_goal_text = selected_goal_label
            if user_goal_text.strip():
                full_goal_text += " | " + user_goal_text.strip()

            # 5. Generate meal plan with AI (Person 2)
            result = generate_meal_plan(full_goal_text, filtered_df)

            # result is expected to be a dict with "days" and "missing_items"
            days = result.get("days", [])
            missing_items = result.get("missing_items", [])

            # === Display the plan ===
            st.success("Meal plan generated successfully!")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.header("📅 5-Day Plan")
                if not days:
                    st.warning("AI did not return any days in the plan.")
                else:
                    for day_data in days:
                        render_day(day_data)
                        st.markdown("---")

            with col2:
                st.header("🛒 Missing Items")
                if not missing_items:
                    st.info("No missing items – you seem to have everything you need!")
                else:
                    st.write("You may need to buy:")
                    for item in missing_items:
                        st.write(f"- {item}")

            # === Optional: show filtered ingredients table ===
            with st.expander("🔍 See filtered ingredient list"):
                st.dataframe(filtered_df.reset_index(drop=True))

        except FileNotFoundError:
            st.error("`ingredients.csv` not found. Please make sure it is in the project folder.")
        except Exception as e:
            st.error(f"Something went wrong while generating the plan: {e}")


if __name__ == "__main__":
    main()
