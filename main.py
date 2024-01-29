# key = "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"
key = "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"
import openai
import os
from jsonf import work,BodyMassIndex
import streamlit as st
from BMR_calculator import calculate_bmr
import pandas as pd
import plotly.express as px
import tensorflow as tf
from nutritionfoodrecd import normalized_nutrition, Food_name, data1, breakfast, lunch, dinner,food_name_to_index
import numpy as np
from recipe_generator import recommend_recipes
import json
import matplotlib.pyplot as plt
from diseasefooddata import diseasefoodrecmd
from body_mass_index import knn
from disease_precition_model import random, data
# from macronutrition_chart import create_macronutrient_chart

# bg = """" <style>
# [data-testid="stAppViewContainer"]{
# background-image: url("https://imgs.search.brave.com/12qZkMl1K2Sg-DoJh7n-huYCqX9oFX7ttJeSBpbVXEc/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/cHJlbWl1bS1waG90/by9ncnVuZ2UtdGV4/dHVyZS1kYXJrLXdh/bGxwYXBlcl8xMjU4/LTE0MTM3LmpwZz9z/aXplPTYyNiZleHQ9/anBn"),
# background-size:cover;
#
#
# }
# </style>"""
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
# st.markdown(bg, unsafe_allow_html=True)
st.title("PERSONALIZED NUTRITION RECOMMENDATION")
st.write("___________________________________________________________________________________________________")

st.sidebar.title("USER INFORMATION")
# Name Input
name = st.sidebar.text_input("Name")

# Age Input
age = st.sidebar.number_input("Age")

# Gender Input
gender_options = ["Male", "Female"]
gender = st.sidebar.selectbox("Gender", gender_options)

# Height Input
height = st.sidebar.number_input("Height (cm)")

# Weight Input
weight = st.sidebar.number_input("Weight (kg)")

# Activity Level Input
activity_options = ["Sedentary", "Lightly Active", "Moderately Active", "Active", "Very Active"]
activity_level = st.sidebar.multiselect("Activity Level", activity_options)


st.sidebar.title("MEDIICAL CONDITION")
disease = ["Diabetes","Heart Disease","High Blood Pressure","Kidney Disease","Liver Disease"]


# Create the donut chart



disease = st.sidebar.multiselect("Disease",disease)



body_symptoms_options = [
    "itching", "skin_rash", "nodal_skin_eruptions" ,"continuous_sneezing", "shivering","chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting","vomiting", "burning_micturition", "spotting_urination", "fatigue", "weight_gain", "anxiety",
    "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy","patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes",
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin",
    "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation",
    "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes",
    "acute_liver_failure", "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes", "malaise",
    "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure",
    "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate",
    "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus",
    "neck_pain", "dizziness", "cramps", "bruising", "obesity", "swollen_legs",
    "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails",
    "swollen_extremities", "excessive_hunger", "extra_marital_contacts", "drying_and_tingling_lips",
    "slurred_speech", "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck",
    "swelling_joints", "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness",
    "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine",
    "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_(typhos)",
    "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes",
    "increased_appetite", "polyuria", "family_history", "mucoid_sputum", "rusty_sputum",
    "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion",
    "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen",
    "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum",
    "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples",
    "blackheads", "scarring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
    "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"
]
body_symptoms = st.sidebar.multiselect("Body Symptoms", body_symptoms_options)

st.markdown(
    """
    <style>
    .title {
        position: absolute;
        top: 10px;
        left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title("DIET CONDITION")

allergies = ["Nut Allergy", "Oral Allergy Syndrome", "Stone Fruit Allergy", "Insulin Allergy", "Allium Allergy",
             "Histamine Allergy", "Banana Allergy", "Gluten Allergy",
             "Legume Allergy", "Salicylate Allergy", "Broccoli Allergy", "Cruciferous Allergy", "Ragweed Allergy",
             "Milk Allergy / Lactose Intolerance", "Mushroom Allergy",
             "Hypersensitivity", "Alpha-gal Syndrome", "Poultry Allergy", "Ochratoxin Allergy", "Corn Allergy",
             "Seed Allergy", "Shellfish Allergy",
             "Fish Allergy", "Nightshade Allergy", "Sugar Allergy / Intolerance", "LTP Allergy", "Citrus Allergy",
             "Honey Allergy",
             "Beer Allergy", "Potato Allergy", "Lactose Intolerance", "Aquagenic Urticaria", "Peanut Allergy",
             "Mint Allergy", "Rice Allergy", "Pepper Allergy",
             "Soy Allergy", "Tannin Allergy", "Thyroid"]

allergy = st.sidebar.multiselect('Select the allergy type', options=allergies)

veg = ["Vegetarian","Non-vegetarian"]

diet_pref = st.sidebar.multiselect("select diet Preference",options=veg)

st.sidebar.title("JOB SECTOR")

sectors = [
    "IT Sector",
    "Mines",
    "Chemical industries",
    "Decision making",
    "Work labours"
]

job_level = st.sidebar.multiselect("Select your kind of job: ", options=sectors)

st.sidebar.title("DIET GOAL")

pri_goal = ["weight loss","weight gain","maintain","Athletes","High-Intensity Training"]

goal = st.sidebar.multiselect("Select your primary health and nutrition goals: ",options=pri_goal)



fl = []


if st.sidebar.button("Submit"):


    st.title(f"Hello {name},")
    st.title("RECOMMENDED DAILY INTAKE OF CALORIES {:.2f} Kcal".format(calculate_bmr(age, weight, gender, height, activity_level[0],goal[0])))
    st.write("____________________________________________________________________________________________________________________")

    col1,col2 = st.columns((5,3))

    with col1:

        if goal[0] == "maintain":
            labels = ['Carbohydrates', 'Protein', 'Facts']
            sizes = [50, 20, 30]
            data = {'Labels': labels, 'Sizes': sizes}
            df = pd.DataFrame(data)





        elif goal[0] == "weight loss":
            # create_macronutrient_chart(goal[0],45,30,25)
            labels = ['Carbohydrates', 'Protein', 'Facts']
            sizes = [45, 30, 25]
            data = {'Labels': labels, 'Sizes': sizes}
            df = pd.DataFrame(data)


        elif goal[0] == "weight gain":
            # create_macronutrient_chart(goal[0],50,30,20)
            labels = ['Carbohydrates', 'Protein', 'Facts']
            sizes = [50, 30, 20]
            data = {'Labels': labels, 'Sizes': sizes}
            df = pd.DataFrame(data)

        elif goal[0] == "Athletes":
            # create_macronutrient_chart(goal[0],60,15,25)
            labels = ['Carbohydrates', 'Protein', 'Facts']
            sizes = [60,15,25]
            data = {'Labels': labels, 'Sizes': sizes}
            df = pd.DataFrame(data)

        elif goal[0] == "High-Intensity Training":
            # create_macronutrient_chart(goal[0],45,30,25)
            labels = ['Carbohydrates', 'Protein', 'Facts']
            sizes = [45,30,25]
            data = {'Labels': labels, 'Sizes': sizes}
            df = pd.DataFrame(data)
        colors = ['#EC6B56', '#FFC154', '#47B39C']

        fig = px.pie(df, values=sizes, names=labels, color_discrete_sequence=colors)



        st.title("MACRONUTRITION DISTRIBUTION")
        st.plotly_chart(fig)
    with col2:

        st.title("NUTRITION NEED TO INTAKE")


        nutrients_list = work[sectors[0]]

        st.table(nutrients_list)



    st.write("____________________________________________________________________________________________________________________")


    list = []
    symp_col = body_symptoms_options
    for i in range(132):
        if symp_col[i] in body_symptoms:
            list.append(1)
        else:
            list.append(0)

    dis = random.predict([list])[0]
    st.title(f"You may cause due to {dis}")

    # openai.api_key = key
    # bodymas = BodyMassIndex[knn.predict([[0, 1, height, weight]])[0]]
    # bmi_ = knn.predict([[0, 1, height, weight]])[0]
    # l = ''
    # for i in bodymas:
    #     l += i
    #     for j in i:
    #         l += j
    #
    # output = openai.ChatCompletion.create(
    #     model = "gpt-3.5-turbo",
    #     messages = [{"role":"assistant",
    #                      "content":f"generate a 5 points diet plan  report using these for {dis} and i want only point detail only no any other details"}]
    #     )
    # output_content = output.choices[0].message.content
    #
    # st.write(output_content)

    st.write("____________________________________________________________________________________________________________________")

    md = "nutritionfoodred.hdf5"

    loaded_model = tf.keras.models.load_model(md)


    def recommend_similar_foods(food_name, top_k=40):
        bf = []
        lun = []
        din = []
        sna = []
        food_idx = food_name_to_index[food_name]
        food_representation = normalized_nutrition[food_idx].reshape(1, -1)
        similarities = loaded_model.predict(food_representation).flatten()
        similar_food_indices = np.argsort(similarities)[-top_k - 1:-1][::-1]
        similar_food_names = [Food_name[idx] for idx in similar_food_indices]
        for i in similar_food_indices:
            if breakfast[i] == 1:
                bf.append(Food_name[i])
            elif lunch[i] == 1:
                lun.append(Food_name[i])
            elif dinner[i] == 1:
                din.append(Food_name[i])
            else:
                sna.append(Food_name[i])
        return [similar_food_names, bf, lun, din, sna]


    foodlist = diseasefoodrecmd(disease[0])
    breakfastfoodlist = []
    lunchfoodlist = []
    dinnerfoodlist = []
    snacksfoodlist = []

    for i in foodlist[0]:
        fl.append(i)
        if i in Food_name.values:

            recommended_foods = recommend_similar_foods(i)


            for i in recommended_foods[1]:
                if len(breakfastfoodlist) < 25 and (i not in breakfastfoodlist):
                    breakfastfoodlist.append(i)

            for i in recommended_foods[2] :
                if len(dinnerfoodlist) < 25 and (i not in dinnerfoodlist):
                    dinnerfoodlist.append(i)

            for i in recommended_foods[3] :
                if len(lunchfoodlist) < 25 and (i not in lunchfoodlist):
                    lunchfoodlist.append(i)

            for i in recommended_foods[4] :
                if len(snacksfoodlist) < 25 and (i not in snacksfoodlist):
                    snacksfoodlist.append(i)
    col1,col2,col3 = st.columns(3)

    folder_path = 'Image'

    with col1:
        st.title("Fruits")
        for i in range(10):
            # if st.button(foodlist[0][i]):
            #     s = recommend_similar_foods(foodlist[0][i])
            #     st.write(s)
            image_file = foodlist[0][i] + ".jpeg"
            image_path = os.path.join(folder_path, image_file)
            if os.path.exists(image_path):
                st.image(image_path, caption=foodlist[0][i], use_column_width=True)




    with col2:
        st.title("Vegtables")
        for i in range(10):

            image_file = foodlist[1][i] + ".jpeg"
            image_path = os.path.join(folder_path, image_file)

            if os.path.exists(image_path):
                st.image(image_path, caption=foodlist[1][i], use_column_width=True)



    with col3:
        st.title("Food items")
        for i in range(10):

            image_file = foodlist[2][i]+".jpeg"
            image_path = os.path.join(folder_path, image_file)
            if os.path.exists(image_path):
                st.image(image_path, caption= foodlist[2][i], use_column_width=True)
    st.write("_______________________________________________________________________________________")
    c1,c2,c3,c4 = st.columns(4)
    
    with c1:
        st.title("BREAKFAST")

        for i in range(10):
            st.write(breakfastfoodlist[i])

    with c2:
        st.title("LUNCH")

        for i in range(10):
            st.write(lunchfoodlist[i])

    with c3:
        st.title("DINNER")

        for i in range(10):
            st.write(dinnerfoodlist[i])

    with c4:
        st.title("SNACKS")

        for i in range(10):
            st.write(snacksfoodlist[i])


import requests

query = st.sidebar.text_input("Enter the Food items: ")
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'TBGKDHf/kyKcVOm6qPhjsg==zv3jUrtk992mMayM'})
if response.status_code == requests.codes.ok:
    if st.sidebar.button("Find Nutritions"):
        col1, col2 = st.columns(2)

        dictionary = json.loads(response.text)

        for i, (key, value) in enumerate(dictionary[0].items()):
            if i % 2 == 0:
                col1.write(f"{key}: {value}")
            else:
                col2.write(f"{key}: {value}")
    else:
        print("Error:", response.status_code, response.text)


# st.sidebar.title("RECIPE GENERATOR")
# rep = st.sidebar.text_input("SELECT THE FOOD ITEMS")
#
# openai.api_key = key
#
#
# output = openai.ChatCompletion.create(
#     model = "gpt-3.5-turbo",
#     messages = [{"role":"assistant",
#                      "content":f"generate a recipe using {rep} i want only recipe title, incridient, and procedure"}]
#     )
# output_content = output.choices[0].message.content
# if st.button("generate"):
#     st.write(output_content)


