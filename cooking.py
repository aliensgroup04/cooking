# -*- coding: utf-8 -*-
"""cooking.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EZKm1yMTM1n8IhHb5SaE6iJwGisqZORi
"""

!pip install langchain_google_genai

!pip install streamlit

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field,ValidationError
class recipe(BaseModel):
  ingredients:list = Field(description="List of ingredients for preparing dish")
  process: list = Field(description="Steps to follow for preparing dish")
output_parser=PydanticOutputParser(pydantic_object=recipe)
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyBMCc42a-cWcpnG1TfCC830kbHG20dAqpo")
prompt_template = ChatPromptTemplate(
    messages=[
        (
            "system",
            """You are a helpful AI Chef Assistant.
            Given a dish name by user, yoy provide the process of preparation step by step alnog with ingredients.
            Output Format Instructions:
            {output_format_instructions}""",
        ),
        ("human", "Give me the recipe and step by step instruction for cooking {dish_name}."),
    ],
    partial_variables={
        "output_format_instructions": output_parser.get_format_instructions()
    },
)
chain = prompt_template | model | output_parser
input = st.text_input(" Enter your dish name:")
input_data = {"dish_name": input}
# Instead of invoke, use stream to get the output in chunks
st.title("Chef Assistant")
user_input = st.text_area(label="Enter dish name", placeholder="Write dish name")
btn_click=st.button("Enter")

if st.button("Dish Name"):
    if input:
        with st.spinner("Getting the recipe...⏳"):
            for chunk in chain.stream(input_data):
              try:
                  # Access the parsed output directly from the chunk
                  intermediate_recipe = chunk
                  print("Ingredients (so far):")
                  for ingredient in intermediate_recipe.ingredients:
                      print(f"- {ingredient}")
                  print("\nProcess (so far):")
                  for step in intermediate_recipe.process:
                      print(f"- {step}")
                  print("---")

              except ValidationError:  # Use ValidationError directly
                  # Handle cases where the intermediate output isn't a valid recipe yet
                  print(chunk.content, end="", flush=True)