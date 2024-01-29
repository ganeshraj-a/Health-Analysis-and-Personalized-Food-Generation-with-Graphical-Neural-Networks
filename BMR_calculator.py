def calculate_bmr(age, weight, gender, height, activity, need):
    if gender.lower() == "male":
        bmr = 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)
    elif gender.lower() == "female":
        bmr = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")

    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9,
        "maintain": 1.0,                 # Add maintenance activity level
        "athletes": 1.9,                    # Add athletes activity level
        "high-intensity training": 2.3      # Add high-intensity training activity level
    }

    if activity.lower() not in activity_factors:
        raise ValueError(
            "Invalid activity level. Please choose from: sedentary, lightly active, moderately active, very active, extra active, maintenance, athletes, high-intensity training.")

    bmr *= activity_factors[activity.lower()]

    need_factors = {
        "weight loss": -500,      # Subtract 500 calories for weight loss
        "weight gain": 500,       # Add 500 calories for weight gain
        "maintain": 0,         # No changes for maintenance
        "athletes": 1000,         # Add 1000 calories for athletes
        "high-intensity training": 1200  # Add 1200 calories for high-intensity training
    }

    if need.lower() not in need_factors:
        raise ValueError(
            "Invalid goal. Please choose from: weight loss, weight gain, maintenance, athletes, high-intensity training.")

    bmr += need_factors[need.lower()]

    return bmr