# Student Quiz Performance Insights 🎓📊

## Project Overview

This project analyzes student quiz performance and provides detailed insights based on the data. It leverages **Python (FastAPI)** for backend processing and **React** for the frontend. The goal is to  identify patterns in student performance by topics, difficulty levels, and response accuracy and present visualizations such as score progression, score distribution, score trends, and mistake correction heatmaps, all of which help in understanding student performance. 

A key feature of this project is the use of **AI-driven insights** and **Large Language Models (LLMs)** to generate teacher-like responses based on quiz performance data. By analyzing the data, the AI produces weak areas, improvement trends, and performance gaps for a given user, encouraging feedback and actionable recommendations for improvement.

## Key Features ✨

- **File Upload**: Upload your quiz data (in JSON format) for analysis.
- **Insights Generation**: Generate insights such as average score, score progression, and trends over time.
- **Visualizations**: Interactive charts such as score distribution, score trends, score ranges, and more.
- **AI-Generated Feedback**: Leverage LLMs to generate teacher-like responses based on insights derived from the data.
- **Actionable Recommendations**: Get detailed suggestions on how students can improve based on their quiz performance.

## Technologies Used 🔧

- **Frontend**: React.js, Axios, marked.js
- **Backend**: FastAPI, Python, Pandas, Matplotlib, Seaborn, OpenAI API
- **Database**: No database used (works with the uploaded data)
- **Visualizations**: Matplotlib, Seaborn
- **AI/LLM**: OpenAI GPT-4o-mini model
- **Deployment**: Can be deployed locally using `uvicorn` and `npm start`

## How AI is Used 🤖

AI, specifically **Large Language Models (LLMs)** like **GPT-4o-mini**, play a crucial role in providing natural, motivational feedback to students. Once the quiz data is processed and analyzed, the insights are passed to the AI model, which generates a response that mimics a teacher's feedback. 

### The AI Process:
1. **Data Insights**: The system processes the quiz data to generate insights such as:
   - Total number of quizzes taken.
   - Average score across all quizzes.
   - Score progression over time.
   - Mistakes corrected over multiple attempts.
   - Score trend analysis over time.
   
2. **Teacher-like Response Generation**: After generating the insights, the **OpenAI GPT-4 model** is used to interpret the data and provide a personalized, encouraging response. This AI-generated feedback includes:
   - **Strengths and Weaknesses**: The AI highlights the student's strengths and areas where they can improve.
   - **Actionable Suggestions**: Based on performance gaps, the AI suggests ways to improve, such as focusing on certain topics or improving accuracy on specific question types.
   - **Performance Analysis**: Although it is very difficult to predict ranks from the scores in the given data,the AI uses historical trends to predict potential performance in future exams (e.g., NEET in India).

The AI model ensures that the feedback is not only relevant and insightful but also motivational, helping students stay engaged and focused on areas that need improvement.

## Setup Instructions ⚙️

### Prerequisites
- **Node.js** (for frontend)
- **Python** (for backend)
- **FastAPI** and **Uvicorn** (for backend server)
- **Axios** and **React** (for frontend)
- **OpenAI API Key** (for LLM-powered feedback)

### Backend Setup (Python)
1. Clone the repository:
    ```bash
    git clone <https://github.com/HimanshuBhosale25/AI-insightful-quiz-analytics.git>
    cd backend
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key (for AI-driven insights):
    - Create a `.env` file in the `backend` directory and add your API key:
    ```bash
    OPENAI_API_KEY=your-api-key
    ```

4. Start the FastAPI backend server:
    ```bash
    uvicorn main:app --reload
    ```

### Frontend Setup (React)
1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Start the React development server:
    ```bash
    npm start
    ```

4. The app should now be running at `http://localhost:3000`.

## Usage 📝

1. On the frontend, select a JSON file containing student quiz data.
2. The system will process the file, generate insights, and provide visualizations of quiz scores, progress, and trends.
3. View detailed charts and AI-generated teacher-like feedback based on the student's quiz performance.

## Approach 🔍

### Data Processing:
The backend processes the uploaded JSON data using **Pandas**, ensuring proper formatting and generating valuable insights:
- **Score Progression**: Tracks score changes over time.
- **Mistakes Corrected**: Analyzes the correction patterns of mistakes.
- **Score Range Distribution**: Visualizes the distribution of scores in various ranges (e.g., Poor, Average, Good, Excellent).

### Visualizations:

- **Score Progression Chart**: Line chart showing the evolution of scores across different topics.
  
- **Score Distribution**: Bar chart showing average scores per topic.

- **Score Trend Over Time**: Line chart showing the average score trend over submission times.

- **Score Range Distribution**: Pie chart showing the distribution of scores across different ranges.

- **Score Improvement Over Time**: Scatter plot showing the improvement of scores over time for individual students.

- **Mistake Correction Heatmap**: Heatmap that displays patterns of mistake correction across quizzes and attempts.


### AI-Generated Teacher Feedback:
Using the **OpenAI GPT-4o-mini model**, the system generates natural, motivational feedback based on the data. The AI analyzes performance gaps, trends, and areas of strength, and generates feedbacks.
This AI-driven feedback is personalized for each student based on their performance, making the learning experience more engaging and effective.

## Screenshots 📸

### 1. **File Upload**
![File Upload](images/Screenshot%202025-01-31%20224618.png)

### 2. **Insights**
![Insights](images/Screenshot%202025-01-31%20225038.png)

### 3. **Score Progression by Topic Line Chart**
![Score Progression by Topic](images/Screenshot%202025-01-31%20225337.png)

### 4. **Score Distribution Bar Chart**
![Score Distribution Bar Chart](images/Screenshot%202025-01-31%20225351.png)

### 5. **Score Trend Chart**
![Score Trend Scatterplot](images/Screenshot%202025-01-31%20225730.png)

### 6. **Score Range Distribution Pie Chart**
![Score Range Distribution Pie Chart](images/Screenshot%202025-01-31%20225211.png)

### 7. **Score Improvement Scatterplot**
![Score Improvement Scatterplot](images/Screenshot%202025-01-31%20225259.png)

### 8. **Mistake Correction Heatmap**
![Mistake Correction Heatmap](images/Screenshot%202025-01-31%20225247.png)

## Future Improvements 🚀

- Add Chatbot functionality where the user can directly ask general questions and get guidance.
- Implement user authentication for saving data and insights.
- Enable multi-file upload for batch processing.
- Improve performance for larger datasets.


Happy coding! 😊
