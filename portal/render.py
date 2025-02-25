import os
import json
import random
from google.cloud import storage

from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from onramp_workaround import get_next_region


def render_assignment_page(assignment: str):
    try:
        region=get_next_region()
        llm = VertexAI(model_name="gemini-2.0-flash-001", location=region)
        input_msg = HumanMessage(content=[f"Here the assignment {assignment}"])
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        """
                        As a frontend developer, create HTML to display a student assignment with a creative look and feel. Include the following navigation bar at the top:
                        ```
                        <nav>
                            <a href="/">Home</a>
                            <a href="/quiz">Quizzes</a>
                            <a href="/courses">Courses</a>
                            <a href="/assignment">Assignments</a>
                        </nav>
                        ```
                        Also include these links in the <head> section:
                        ```
                        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
                        <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">

                        ```
                        Do not apply inline styles to the navigation bar. 
                        The HTML should display the full assignment content. In its CSS, be creative with the rainbow colors and aesthetic. 
                        Make it creative and pretty
                        The assignment content should be well-structured and easy to read.
                        respond with JUST the html file
                        """
                    )
                ),
                input_msg,
            ]
        )

        prompt = prompt_template.format()
        
        response = llm.invoke(prompt)

        response = response.replace("```html", "")
        response = response.replace("```", "")
        with open("templates/assignment.html", "w") as f:
            f.write(response)


        print(f"response: {response}")

        return response
    except Exception as e:
        print(f"Error sending message to chatbot: {e}") # Log this error too!
        return f"Unable to process your request at this time. Due to the following reason: {str(e)}"
