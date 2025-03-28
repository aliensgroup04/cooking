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
from typing import List
import os

class Recipe(BaseModel):
    ingredients: List[str] = Field(description="List of ingredients for the dish")
    process: List[str] = Field(description="Steps to prepare the dish")
    varieties: List[str] = Field(description="Similar dish varieties")

# Output parser
output_parser = PydanticOutputParser(pydantic_object=Recipe)

# Load API key
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyCBhbuJbxjlghoZ3X1HQhS_qwuMpSE1wC0")
)
# Prompt Template
prompt_template = ChatPromptTemplate(
    messages=[
        ("system", """You are an AI Chef Assistant.
                      Given a dish name, provide ingredients and step-by-step instructions.
                      Format: {output_format_instructions}"""),
        ("human", "Give me the recipe for {dish_name}."),
    ],
    partial_variables={"output_format_instructions": output_parser.get_format_instructions()},
)

# Chain definition
chain = prompt_template | model | output_parser

# Streamlit UI
st.title("🍽️ Chef Assistant")

# Store recipe data
if "recipe" not in st.session_state:
    st.session_state.recipe = None

# Get main dish recipe
dish_name = st.text_input("Enter a dish name", placeholder="E.g., Pasta, Biryani")

if st.button("Get Recipe") and dish_name:
    with st.spinner("Fetching recipe...⏳"):
        st.session_state.recipe = chain.invoke({"dish_name": dish_name})

# Display recipe
if st.session_state.recipe:
    recipe = st.session_state.recipe
    st.subheader("🥕 Ingredients:")
    st.markdown("\n".join(f"- {i}" for i in recipe.ingredients))

    st.subheader("👨‍🍳 Preparation Steps:")
    st.markdown("\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(recipe.process)))

    # Ask if user wants to try a variety
    if recipe.varieties:
        st.subheader("🍽️ Similar Varieties:")
        st.markdown("\n".join(f"- {v}" for v in recipe.varieties))

        variety_name = st.text_input("Try a variety! Enter a name:", placeholder="E.g., Chicken Biryani")

        if st.button("Get Variety Recipe") and variety_name:
            with st.spinner(f"Fetching recipe for {variety_name}...⏳"):
                variety_recipe = chain.invoke({"dish_name": variety_name})

            # Display variety recipe
            st.subheader(f"🍽️ Recipe for {variety_name}")
            st.subheader("🥕 Ingredients:")
            st.markdown("\n".join(f"- {i}" for i in variety_recipe.ingredients))
            st.subheader("👨‍🍳 Preparation Steps:")
            st.markdown("\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(variety_recipe.process)))

st.markdown("---")
st.markdown("Chef Assistant Made by Suman", unsafe_allow_html=True)
