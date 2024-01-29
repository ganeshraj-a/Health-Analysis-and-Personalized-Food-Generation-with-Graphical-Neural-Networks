# apikey = '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'
# apikey2 = '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'

import matplotlib.pyplot as plt
import streamlit1 as st

def create_macronutrient_chart(category, carbohydrate, protein, fat):
    labels = ['Carbohydrates', 'Protein', 'Fat']
    sizes = [carbohydrate, protein, fat]
    colors = ['#ff9999','#66b3ff','#99ff99']
    explode = (0.1, 0, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(category + " Macronutrient Distribution")

    st.pyplot(fig)

# Example usage
