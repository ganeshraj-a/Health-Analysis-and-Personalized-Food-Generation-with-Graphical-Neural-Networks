import pandas as pd
def diseasefoodrecmd(disease):
    if disease == "Diabetes":
        fooddata = pd.read_csv("Datasets/diabetes.csv")
        return [fooddata["Fruits"],fooddata["vegetables"],fooddata["Food"]]
    elif disease == "Heart Disease":
        fooddata = pd.read_csv("Datasets/heart_disease.csv")
        return [fooddata["Fruits"], fooddata["vegetables"], fooddata["Food"]]
    elif disease == "High Blood Pressure":
        fooddata = pd.read_csv("Datasets/high_blood_pressure.csv")
        return [fooddata["Fruits"], fooddata["vegetables"], fooddata["Food"]]
    elif disease == "Kidney Disease":
        fooddata = pd.read_csv("Datasets/kidney_disease.csv")
        return [fooddata["Fruits"], fooddata["vegetables"], fooddata["Food"]]
    elif disease == "Liver Disease":
        fooddata = pd.read_csv("Datasets/Liver_disease.csv")
        return [fooddata["Fruits"], fooddata["vegetables"], fooddata["Food"]]
    else:
        fooddata = pd.read_csv("Datasets/stroke.csv")
        return [fooddata["Fruits"], fooddata["vegetables"], fooddata["Food"]]



