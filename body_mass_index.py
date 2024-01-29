import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


df = pd.read_csv("Datasets/bmi_dataset.csv")

df["Index"] = df["Index"].map({
    0: "Extremely Weak",
    1: "Weak",
    2: "Normal",
    3: "Overweight",
    4: "Obesity",
    5: "Extreme Obesity"
})

gender = pd.get_dummies(df["Gender"], dtype="int")

df = pd.concat([gender, df], axis=1)
df.drop("Gender", axis=1, inplace=True)

X = df.drop("Index", axis=1)
y = df["Index"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
# accuracy_score(y_test, y_pred)