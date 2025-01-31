from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import io
import base64
import openai
import os
import seaborn as sns

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development purposes)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/process_data/")
async def process_data(file: UploadFile = File(...)):
    # Read the uploaded file
    content = await file.read()
    # Decode bytes to string
    json_data = content.decode("utf-8")
    
    # Parse JSON into a pandas DataFrame
    df = pd.read_json(StringIO(json_data))

    # Sort data by the timestamp (submitted_at) to ensure chronological order
    df['submitted_at'] = pd.to_datetime(df['submitted_at'])
    df = df.sort_values(by='submitted_at')

    # Process the data and generate insights
    insights = generate_insights(df)
    
    # Visualizations
    score_progression_chart = create_score_progression_chart(df)
    score_distribution_chart = create_score_distribution_chart(df)
    score_trend_chart = create_score_trend_chart(df)
    score_range_pie_chart = create_score_range_pie_chart(df)
    mistake_correction_heatmap = create_mistake_correction_heatmap(df)
    score_improvement_plot = create_scatter_plot(df)


    # Generate a more natural, teacher-like response using OpenAI
    natural_response = generate_teacher_like_response(insights)

    return {
        "insights": insights,
        "natural_response": natural_response,
        "score_progression_chart": score_progression_chart,
        "score_distribution_chart": score_distribution_chart,
        "score_trend_chart": score_trend_chart,
        "score_range_pie_chart": score_range_pie_chart,
        "mistake_correction_heatmap": mistake_correction_heatmap,
        "score_improvement_plot": score_improvement_plot,
    }

# Function to generate insights
def generate_insights(df):
    insights = {}
    
    # 1. Summary of total quizzes (Topics & Titles)
    insights['total_quizzes'] = df['quiz'].apply(lambda x: x['title']).nunique()
    
    # 2. Average score across quizzes
    insights['avg_score'] = df['score'].mean()
    
    # 3. Score progression (grouped by title)
    insights['score_progression'] = df.groupby(df['quiz'].apply(lambda x: x['title']))['score'].apply(list).to_dict()

    # 4. Score trend over time (average score by submission time)
    insights['score_trend'] = df.groupby('submitted_at')['score'].mean().to_dict()

    return insights

# OpenAI function to generate a teacher-like response
def generate_teacher_like_response(insights):
    prompt =f"""
    You are an AI tutor analyzing a student's quiz performance data. Based on the following insights:

    1. Total Quizzes: {insights['total_quizzes']}
    2. Average Score: {insights['avg_score']}
    3. Score Progression by Topic (Title): {insights['score_progression']}
    4. Score Trend Over Time: {insights['score_trend']}

    Please provide a short, clear, and encouraging response. Focus on:
    - The student's strengths,weaknesses and areas of improvement (in a positive tone).
    - Key insights that will help them improve their future performance.
    - Highlight performance gaps.
    - Propose actionable steps for the student to improve, such as suggested topics, question types, or difficulty levels to focus on.
    - Analyze and define the student persona based on patterns in the data.
    - Give the expected result that the student might get in the actual NEET exam taken in India based on the insights.
    - Keep the response to a few sentences with bullet points and make important words **bold**, avoiding overwhelming detail.

    Make sure to keep the language simple and motivational.
    """ 

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response['choices'][0]['message']['content']

# Function to create score progression chart (line chart)
def create_score_progression_chart(df):
    plt.figure(figsize=(10, 6))

    # Plot the scores by title
    for title, group in df.groupby(df['quiz'].apply(lambda x: x['title'])):
        plt.plot(group['submitted_at'], group['score'], marker='o', label=f"Topic: {title}", linestyle='--', markersize=6)

    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the plot as a base64 string to send to frontend
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close()  # Close the plot to avoid it showing on the server

    return img_b64

# Function to create score distribution chart (bar chart)
def create_score_distribution_chart(df):
    plt.figure(figsize=(10,8))
    
    # Create a bar chart for scores distribution per title
    score_counts = df.groupby(df['quiz'].apply(lambda x: x['title']))['score'].mean().sort_values(ascending=False)  # Average score per topic
    score_counts.plot(kind='barh', color=score_counts.apply(lambda x: 'green' if x > 80 else ('orange' if x > 60 else 'red')))
    for i, v in enumerate(score_counts):
        plt.text(i, v + 1, f'{v:.2f}', ha='center', va='bottom')

    plt.xlabel('Topic Title', fontsize=12)
    plt.ylabel('Average Score', fontsize=12)
    plt.xticks(rotation=0)
    plt.subplots_adjust(left=0.4) 
   

    # Save the plot as a base64 string to send to frontend
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close()

    return img_b64

# Function to create score trend chart (line chart)
def create_score_trend_chart(df):
    plt.figure(figsize=(15, 6))

    # Plot the average score trend over time with moving average
    avg_score_by_time = df.groupby('submitted_at')['score'].mean().rolling(window=7).mean()  # 7-day moving average
    plt.plot(avg_score_by_time.index, avg_score_by_time.values, marker='o', color='green')

    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Score', fontsize=12)
    plt.xticks(rotation=45)

    # Save the plot as a base64 string to send to frontend
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close()

    return img_b64

def create_mistake_correction_heatmap(df):
    # Extract quiz title from the dictionary in the 'quiz' column
    df['quiz_title'] = df['quiz'].apply(lambda x: x['title'])

    # Create the 'attempt' column based on ranking submission times per quiz title
    df['attempt'] = df.groupby('quiz_title')['submitted_at'].rank().astype(int)

    # Create the pivot table: Sum of 'mistakes_corrected' grouped by 'quiz_title' and 'attempt'
    pivot_df = df.pivot_table(values='mistakes_corrected', 
                              index='quiz_title',  # Use extracted title as index
                              columns='attempt',   # Use attempt column
                              aggfunc='sum',       # Sum the corrected mistakes
                              fill_value=0)        # Fill missing values with 0

    # Create the heatmap
    plt.figure(figsize=(12, 8))  # Adjust size as needed
    sns.heatmap(pivot_df, annot=True, cmap='YlGnBu', fmt='g', cbar=True, linewidths=0.5)
    
    plt.title('Mistake Correction Trends Across Quizzes')
    plt.ylabel('Quiz Title')
    plt.xlabel('Attempt Number')
    
    # Save the heatmap as a base64 image
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
    
    plt.close()  # Close the plot to avoid it showing on the server
    
    return img_b64

# Function to create score range pie chart
def create_score_range_pie_chart(df):
    # Define score ranges
    bins = [0, 40, 60, 80, 100]
    labels = ['Poor (0-40)', 'Average (40-60)', 'Good (60-80)', 'Excellent (80-100)']
    
    # Categorize scores into the defined ranges
    df['score_range'] = pd.cut(df['score'], bins=bins, labels=labels, right=False)
    
    # Calculate the distribution of scores across the ranges
    score_range_distribution = df['score_range'].value_counts()

    plt.figure(figsize=(8, 8))

    # Create a pie chart with improved colors and labels
    plt.pie(score_range_distribution, labels=score_range_distribution.index, autopct='%1.1f%%', startangle=90, colors=['#FF4C4C', '#FFB74D', '#FFEB3B', '#388E3C'], wedgeprops={'edgecolor': 'black'})

    # Save the plot as a base64 string to send to frontend
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close()

    return img_b64

def create_scatter_plot(df):
    plt.figure(figsize=(12, 6))
    plt.scatter(df['submitted_at'], df['score'], color='purple', alpha=0.5)
    plt.xlabel('Submission Time')
    plt.ylabel('Score')
    plt.xticks(rotation=45)

    # Save and return as base64
    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    plt.close()
    return img_b64

# Run the API with: uvicorn main:app --reload
