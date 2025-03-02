# -*- coding: utf-8 -*-
"""cooking.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EZKm1yMTM1n8IhHb5SaE6iJwGisqZORi
"""
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError

# Define Recipe Schema
class Recipe(BaseModel):
    ingredients: list = Field(description="List of ingredients for preparing the dish")
    process: list = Field(description="Steps to follow for preparing the dish")

# Output parser
output_parser = PydanticOutputParser(pydantic_object=Recipe)

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyCBhbuJbxjlghoZ3X1HQhS_qwuMpSE1wC0")

# Prompt Template
prompt_template = ChatPromptTemplate(
    messages=[
        (
            "system",
            """You are a helpful AI Chef Assistant.
            Given a dish name by the user, you provide the process of preparation step by step along with ingredients.
            Output Format Instructions:
            {output_format_instructions}""",
        ),
        ("human", "Give me the recipe and step-by-step instructions for cooking {dish_name}."),
    ],
    partial_variables={
        "output_format_instructions": output_parser.get_format_instructions()
    },
)

# Chain definition
chain = prompt_template | model | output_parser

# Streamlit UI
st.title("Chef Assistant 🍽️")
user_input = st.text_input("Enter your dish name", placeholder="E.g., Pasta, Biryani")

if st.button("Get Recipe"):
    if user_input:
        with st.spinner("Fetching recipe...⏳"):
            input_data = {"dish_name": user_input}

            # Streamlit placeholders for real-time updates
            ingredients_placeholder = st.empty()
            process_placeholder = st.empty()

            try:
                recipe = Recipe(ingredients=[], process=[])  # Initialize an empty recipe

                for chunk in chain.stream(input_data):
                    if isinstance(chunk, Recipe):  # Ensure it's a valid Recipe object
                        recipe.ingredients.extend(chunk.ingredients)
                        recipe.process.extend(chunk.process)

                        # Update Ingredients List
                        with ingredients_placeholder.container():
                            st.subheader("🥕 Ingredients:")
                            st.markdown("\n".join(f"- {i}" for i in recipe.ingredients))

                        # Update Preparation Steps
                        with process_placeholder.container():
                            st.subheader("👨‍🍳 Preparation Steps:")
                            st.markdown("\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(recipe.process)))

            except ValidationError as e:
                st.error("Error parsing the response. Try again!")
                st.write(str(e))  # Display error details for debugging
    else:
        st.warning("Please enter a dish name!")
st.markdown("<h5 style='color: gray;'>Chef Assistant made by Suman</h5>", unsafe_allow_html=True)
