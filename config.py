DATABASE_PATH = "database.db"

ALLOWED_FILE_TYPES = ["txt", "pdf", "docx"]
ALLOWED_DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
ALLOWED_QUESTION_TYPES = ["Single Correct", "Multiple Correct", "True/False", "No Choice"]

ANTHROPIC_MODEL_NAME = "claude-3-haiku-20240307"

TEXT_CHUNK_SIZE = 4096
TEXT_CHUNK_OVERLAP = 256

QUESTION_GENERATION_SYSTEM_PROMPT = f"""
You are tasked with generating questions based on a given text document. Your goal is to 
create a specified number of questions with a particular difficulty level and of various types. 
Follow these instructions carefully to produce questions in the required XML format.

You can generate only questions of those type: {ALLOWED_QUESTION_TYPES}
You can generate question of those difficulty level: {ALLOWED_DIFFICULTY_LEVELS}

Description and requirements to each question type:
1. 'Single Correct': You should generate exactly the number of options requested with only one answer.

2. 'Multiple Correct': You should generate exactly the number of options requested of options with at least two answers.
   
3. 'True/False': You should generate question that can be simply answered true or false. Provide boolean as answer.

4. 'No Choice': You should generate question without options which can be answered with one word or number. 
Provide answer.

Generate the your response in the following XML format without any additional text:
<questions>
  <question>
    <type>[question type]</type>
    <text>[question text]</text>
    <options>
       <option>[option text]</option>
       <!-- Repeat for each option -->
    </options>
    <answers>
       <answer>[answer text]</answer>
       <!-- Repeat for each answer-->
    </answers>
  </question>
  <!-- Repeat for each question -->
</questions>
"""

QUESTION_GENERATION_REQUEST_PROMPT = """
The difficulty level for these questions should be {difficulty}.
Try to generate question of following types: {question_types}.
You should generate exactly {single_option_number} options for 'Single Correct' questions.
You should generate exactly {multiple_option_number} options for 'Multiple Correct' questions.
You need to generate {question_number} questions based on this text:

<document>
{document}
</document>

Ensure that all questions maintain the specified difficulty level. For higher difficulty levels, 
use more complex concepts, require deeper analysis, or combine multiple ideas from the text.

Before finalizing your output, review all generated questions to ensure they accurately reflect the 
content of the text document, adhere to the specified difficulty level, and follow the correct XML format.

Use strictly XML to structure your response without additional text.  
"""
