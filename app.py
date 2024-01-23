from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import sys


from dotenv import load_dotenv

load_dotenv()


def read_file_into_string(file_path):
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"The file at '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


quiz_bank = read_file_into_string("quiz_bank.txt")

delimiter = "####"

system_message = f"""
Write a quiz for the category the user requests.

## Steps to create a quiz

Step 1:{delimiter} First identify the category user is asking about. Allowed categories are:
* Art
* Science
* Geography

If a user asks about another category respond: "I can only generate quizzes for Art, Science, or Geography"

Step 2:{delimiter} Based on the category, select the facts to generate questions about from the following list:

{quiz_bank}

Step 3:{delimiter} Generate a quiz with three questions for the user.

Use the following format:
Question 1:{delimiter} <question 1>

Question 2:{delimiter} <question 2>

Question 3:{delimiter} <question 3>
"""


def assistant_chain():
    human_template = "{question}"

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", human_template),
        ]
    )
    return (
        chat_prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )


def main():
    question = sys.argv[1]
    assistant = assistant_chain()
    result = assistant.invoke({"question": question})
    print(result)


if __name__ == "__main__":
    main()
