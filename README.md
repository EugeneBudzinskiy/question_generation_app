# Quiz Generation App

This application is built using Streamlit and integrates with the Anthropic LLM to generate quizzes from 
user-uploaded documents. The application allows users to specify parameters such as the number of questions, 
difficulty level, and question types. The generated quizzes are stored in a database and can be accessed later 
using a unique UUID.

## Features

- Upload various file types: **DOCX**, **PDF**, or **TXT** files
- Configure quiz parameters:
  - **Quiz Name**: Customize the title of your quiz
  - **Number of Questions**: Select from 1 to 100
  - **Difficulty Level**: Choose from Easy, Medium, or Hard
  - **Question Types**:
    - Single Correct Answer
    - Multiple Correct Answers 
    - True/False 
    - No Choice (Text Input)
  - **Number of Options** for "Single Correct" and "Multiple Correct" answer types
- Generates the quiz in **XML** format for easy import/export
- Stores the generated quiz with a unique UUID, allowing access via a shareable URL.


## Installation

1. Clone the repository to your local machine.
    ```
    git clone https://github.com/EugeneBudzinskiy/question_generation_app
    ```

2. Install the necessary dependencies from the requirements.txt file. 
    ```
    pip install -r requirements.txt
    ```

3. Run the Streamlit app.
    ```
    streamlit run main.py
    ```

4. Start generate!


## Usage

1. **Upload a document**: Choose a file from your computer (supported formats: **DOCX**, **PDF**, **TXT**).
2. **Set quiz parameters**:
   - Name the quiz
   - Specify the number of questions (1–100)
   - Choose the difficulty level (Easy, Medium, Hard)
   - Select the type of questions
   - For "Single Correct" or "Multiple Correct" types, specify the number of answer options
3. Generate the quiz: After validation, the parameters will be passed to the Anthropic LLM to generate the quiz. 
4. View your quiz: The generated quiz is stored as an XML file in the database and assigned a unique UUID. You can access the quiz later using a URL with this UUID.

## Example

After generating the quiz, the URL might look like this:


```
http://name-of-your-app/quiz?key=123e4567-e89b-12d3-a456-426614174000
```

You can share this URL to access the quiz XML data.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
