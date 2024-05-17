import sys
import pyperclip
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# API endpoints configuration
openai_api_url = "https://api.openai.com/v1/chat/completions"
groq_base_url = "https://api.groq.com/openai/v1"

# Function to generate a comment using Groq API 8b Llama model.
def fetch_initial_comment():
    text = pyperclip.paste()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                You are an insightful 'Comment Creator' assistant. Your task is to analyze an input article, blog post, or video (usually YouTube) and generate a concise yet thought-provoking comment of 150 tokens or less (approximately 600 characters).

                Instructions:
                - Carefully read the input article, which will be a summary from a lower quality language model.
                - Choose one key aspect of the article to focus your comment on. This could be an especially insightful point, a key takeaway you would apply in the future, or an intriguing topic you'd like to explore further in discussion.
                - Craft a unique, 'bursty' comment that is direct in addressing the article's author. Be concise but avoid generic or predictable language.
                - Don't start the comment with the author's name, but reference them directly if contextually appropriate.
                - Critically analyze the article and respectfully point out any inaccuracies or issues. Don't simply agree with everything.
                - After drafting your comment, reflect on whether it sounds distinctively human or more like generic AI output. If the latter, generate a second alternative comment.
                - Utilize the extra context on top of the initial comment to further refine the final product.

                Your final output should only display the final comment. It will be copy-pasted. Make no mention of your instructions, just complete the task.
                """
            },
            {
                "role": "user",
                "content": text
            }
        ],
        model="llama3-8b-8192",
        max_tokens=506,
        n=1,
        stop=None,
        temperature=1,
    )
    comment = chat_completion.choices[0].message.content.strip()
    return comment

# New function to refine the comment using OpenAI GPT-4 model.
def refine_comment_with_openai(text):
    response = requests.post(
        openai_api_url,
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": """
                    Follow this step-by-step process with examples to refine the comment:

                    #### 1. Identify Key Points:
                    - Extract the main ideas from the original text.
                    - Key Points:
                      - Emphasis on daily writing.
                      - The challenge of daily writing.
                      - The myth of instant genius.
                      - Writing as a process that rewards persistence.
                      - Reframing focus on progress over perfection.

                    #### 2. Simplify Sentence Structure:
                    - Break down complex sentences into simpler, shorter ones.
                    - Combine related ideas for brevity without losing meaning.

                    #### 3. Remove Redundancies:
                    - Eliminate repetitive phrases and unnecessary words.
                    - Ensure each sentence adds new information or perspective.

                    #### 4. Use Conversational Tone:
                    - Write as if speaking to a friend.
                    - Use contractions and informal language where appropriate.

                    #### 5. Maintain Original Meaning:
                    - Ensure the core message and intent remain intact.
                    - Preserve the emphasis on daily writing and debunking the myth of instant genius.

                    ### Detailed Steps Applied:

                    #### Original Text:
                    "I'm intrigued by your emphasis on writing daily. It's a daunting task, but your anecdotes and arguments convinced me of its necessity. Perhaps it's the myth of instant genius that holds us back. Your article boldly confronts this misconception, reminding us that writing is a slow-burning flame of creativity that rewards persistence. What if we reframed our approach to focus on progress, not perfection?"

                    #### Step 1: Identify Key Points
                    - Daily writing importance.
                    - Challenges of daily writing.
                    - Myth of instant genius.
                    - Writing rewards persistence.
                    - Focus on progress over perfection.

                    #### Step 2: Simplify Sentence Structure
                    - "Your push for daily writing really struck a chord with me."
                    - "It seems tough, but your stories and points make it clear why it's important."
                    - "Maybe it's the myth of instant genius that trips us up."
                    - "You challenge this idea well, showing that writing is a slow, steady process that pays off with persistence."
                    - "What if we focused more on progress than perfection?"

                    #### Step 3: Remove Redundancies
                    - "It's a daunting task, but your anecdotes and arguments convinced me of its necessity." → "It seems tough, but your stories and points make it clear why it's important."
                    - Combine sentences where logical: "Perhaps it's the myth of instant genius that holds us back." and "Your article boldly confronts this misconception, reminding us that writing is a slow-burning flame of creativity that rewards persistence." → "Maybe it's the myth of instant genius that trips us up. You challenge this idea well, showing that writing is a slow, steady process that pays off with persistence."

                    #### Step 4: Use Conversational Tone
                    - "Your push for daily writing really struck a chord with me."
                    - "It seems tough, but your stories and points make it clear why it's important."
                    - "Maybe it's the myth of instant genius that trips us up."
                    - "You challenge this idea well, showing that writing is a slow, steady process that pays off with persistence."
                    - "What if we focused more on progress than perfection?"

                    #### Step 5: Maintain Original Meaning
                    - Ensure the final version retains the essence of the original text, emphasizing daily writing, debunking the myth of instant genius, and shifting focus to progress.

                    ### Final Revised Text
                    The final output should always be only a comment. You are commenting as 'Nerdsaver' Example: "Your push for daily writing really struck a chord with me. It seems tough, but your stories and points make it clear why it's important. Maybe it's the myth of instant genius that trips us up. You challenge this idea well, showing that writing is a slow, steady process that pays off with persistence. What if we focused more on progress than perfection?"                    
                    """
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "max_tokens": 350,
            "temperature": 1.0
        }
    )
    return response.json()['choices'][0]['message']['content'].strip()

# Function to further refine the comment using Groq API 70b Llama model.
def refine_comment_further(text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a world-class writer tasked with refining a comment you just wrote. Your goal is to enhance the comment's quality by improving its clarity, conciseness, and impact while preserving its original meaning and tone.

                Instructions:
                - Focus on improving the comment's clarity and readability. Ensure that the language is precise and easy to understand.
                - Enhance the comment's conciseness by removing any unnecessary words or phrases without sacrificing meaning.
                - Amplify the comment's impact by refining the language and structure to make it more engaging and memorable.
                - Maintain the original tone and intention of the comment. Do not introduce any new ideas or alter the comment's overall message.
                - Double check you reference the author by saying 'Your writing' when appropriate or 'this post' or this 'article' when the author is not directly addressed.
                but make sure the choice you make is contextually sound.

                Output:
                Provide the refined comment, ensuring that it is clear, concise, impactful, and faithful to the original. Make sure to remove purple prose and unnecessary verbosity, and focus on enhancing the comment's core message.
            """
            },
            {
                "role": "user",
                "content": text
            }
        ],
        model="llama3-70b-8192",
        max_tokens=8192
    )
    return chat_completion.choices[0].message.content.strip()

class CommentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.textEdit1 = QTextEdit()
        initial_comment = fetch_initial_comment()
        self.textEdit1.setText(initial_comment)
        layout.addWidget(self.textEdit1)

        self.textEdit2 = QTextEdit()
        second_comment = refine_comment_with_openai(initial_comment)  # Refine with GPT-4
        self.textEdit2.setText(second_comment)
        layout.addWidget(self.textEdit2)

        refineButton = QPushButton('Refine Further', self)
        refineButton.clicked.connect(self.refineCommentFurther)
        layout.addWidget(refineButton)

        closeButton = QPushButton('Close', self)
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton)

        self.setLayout(layout)
        self.setWindowTitle('Comment Refinement Tool')
        self.setGeometry(300, 300, 350, 250)

    def refineCommentFurther(self):
        initial_comment = self.textEdit1.toPlainText()
        refined_comment = refine_comment_with_openai(initial_comment)  # Refine with GPT-4
        further_refined_comment = refine_comment_further(refined_comment)  # Further refine with Groq
        self.textEdit2.setText(further_refined_comment)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommentWindow()
    ex.show()
    sys.exit(app.exec_())
