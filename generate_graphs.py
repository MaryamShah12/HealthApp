import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'healthapp'
}

# Function to connect and fetch data
def fetch_data(table_name, user_id):
    conn = mysql.connector.connect(**db_config)
    if table_name == 'meals':
        query = "SELECT timestamp, id, user_id, food_name, calories, carbs, protein, fat FROM meals WHERE user_id = %s"
    elif table_name == 'exercise':
        query = "SELECT timestamp, id, user_id, activity, duration_mins, calories_b FROM exercise WHERE user_id = %s"
    elif table_name == 'sleep':
        query = "SELECT date AS timestamp, id, user_id, hours, quality_rating FROM sleep WHERE user_id = %s"
    elif table_name == 'water':
        query = "SELECT timestamp, id, user_id, amount_ml AS liters FROM water WHERE user_id = %s"
    elif table_name == 'mood':
        query = "SELECT date AS timestamp, id, user_id, rating, note FROM mood WHERE user_id = %s"
    else:
        raise ValueError(f"Unknown table: {table_name}")
    
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    print(f"{table_name} DataFrame columns: {df.columns.tolist()}")
    return df

# Example user_id
user_id = 5  # Replace with session['user_id'] later

# Fetch data
meals_df = fetch_data('meals', user_id)
exercise_df = fetch_data('exercise', user_id)
sleep_df = fetch_data('sleep', user_id)
water_df = fetch_data('water', user_id)
mood_df = fetch_data('mood', user_id)

# Check if DataFrames are empty
if meals_df.empty or exercise_df.empty or sleep_df.empty or water_df.empty or mood_df.empty:
    print("Warning: One or more DataFrames are empty. Ensure data exists for user_id =", user_id)
    if meals_df.empty:
        print("No meals data found. Please add data via the 'Add Today's Data' form.")
    if exercise_df.empty:
        print("No exercise data found. Please add data via the 'Add Today's Data' form.")
    if sleep_df.empty:
        print("No sleep data found. Please add data via the 'Add Today's Data' form.")
    if water_df.empty:
        print("No water data found. Please add data via the 'Add Today's Data' form.")
    if mood_df.empty:
        print("No mood data found. Please add data via the 'Add Today's Data' form.")
else:
    # Convert timestamps to datetime objects (keep as datetime for filtering)
    meals_df['timestamp'] = pd.to_datetime(meals_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    exercise_df['timestamp'] = pd.to_datetime(exercise_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    sleep_df['timestamp'] = pd.to_datetime(sleep_df['timestamp'], format='%Y-%m-%d')
    water_df['timestamp'] = pd.to_datetime(water_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    mood_df['timestamp'] = pd.to_datetime(mood_df['timestamp'], format='%Y-%m-%d')

    # Dashboard Chart 1: Sleep Trend (Last 7 Days)
    last_7_days_sleep = sleep_df[sleep_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    plt.figure(figsize=(10, 6))
    plt.plot(last_7_days_sleep['timestamp'].dt.strftime('%a, %b %d'), last_7_days_sleep['hours'], 
             marker='o', color='#ff9800', label='Hours Slept')
    plt.title('Sleep Trend (Last 7 Days)', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Hours', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('dashboard_sleep_trend.png')
    plt.close()

    # Dashboard Chart 2: Calories In vs Out (Last 7 Days)
    last_7_days_meals = meals_df[meals_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    last_7_days_exercise = exercise_df[exercise_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    daily_calories = last_7_days_meals.groupby(last_7_days_meals['timestamp'].dt.strftime('%a, %b %d'))['calories'].sum()
    daily_burned = last_7_days_exercise.groupby(last_7_days_exercise['timestamp'].dt.strftime('%a, %b %d'))['calories_b'].sum()
    common_dates = daily_calories.index.union(daily_burned.index)
    daily_calories = daily_calories.reindex(common_dates, fill_value=0)
    daily_burned = daily_burned.reindex(common_dates, fill_value=0)
    plt.figure(figsize=(10, 6))
    plt.bar(daily_calories.index, daily_calories.values, color='#007bff', label='Calories In', alpha=0.7)
    plt.bar(daily_burned.index, daily_burned.values, color='#28a745', label='Calories Burned', alpha=0.7, bottom=daily_calories.values)
    plt.title('Calories In vs Out (Last 7 Days)', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Calories', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('dashboard_calories_in_out.png')
    plt.close()

    # Graph 3: Sleep Quality Trend
    sleep_quality_map = {'Poor': 1, 'Fair': 2, 'Good': 3, 'Excellent': 4}
    sleep_df['quality_score'] = sleep_df['quality_rating'].map(sleep_quality_map).fillna(0)  # Default to 0 if not mapped
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(sleep_df['timestamp'].dt.strftime('%a, %b %d'), sleep_df['quality_score'], 
             marker='o', color='#ff9800', label='Quality Score')
    ax1.set_title('Sleep Quality and Hours Trend', fontsize=14, color='white')
    ax1.set_xlabel('Date', color='white')
    ax1.set_ylabel('Quality Score (0=Unrated, 1=Poor, 2=Fair, 3=Good, 4=Excellent)', color='#ff9800')
    ax1.tick_params(axis='y', labelcolor='#ff9800')
    ax1.set_xticks(ax1.get_xticks())  # Ensure all dates are shown
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(sleep_df['timestamp'].dt.strftime('%a, %b %d'), sleep_df['hours'], 
             marker='s', color='#2196f3', label='Hours Slept')
    ax2.set_ylabel('Hours Slept', color='#2196f3')
    ax2.tick_params(axis='y', labelcolor='#2196f3')
    ax2.legend(loc='upper right')

    plt.xticks(rotation=45, ha='right')
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('sleep_quality.png')
    plt.close()

    # Graph 4: Mood Frequency (Pie Chart with Insights)
    mood_counts = mood_df['rating'].value_counts()
    # Categorize notes into sentiment themes
    mood_df['note_sentiment'] = mood_df['note'].str.lower().apply(lambda x: 'positive' if 'great' in x or 'fun' in x else 
                                                                 'negative' if 'tough' in x or 'sad' in x else 'neutral')
    note_sentiment_counts = mood_df['note_sentiment'].value_counts()

    plt.figure(figsize=(10, 10))
    plt.pie(mood_counts.values, labels=mood_counts.index, colors=['#f44336', '#ffeb3b', '#4caf50'], 
            autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    plt.title('Mood Frequency Distribution with Sentiment Insight', fontsize=14, color='white')
    plt.axis('equal')

    # Add sentiment insight as text annotations
    plt.text(0, -1.2, f"Sentiment Breakdown:\n{note_sentiment_counts.to_string()}", 
             fontsize=10, color='white', ha='center', va='center')
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('mood_frequency.png')
    plt.close()

    # Graph 5: Exercise Duration Trend
    plt.figure(figsize=(10, 6))
    plt.plot(exercise_df['timestamp'].dt.strftime('%a, %b %d'), exercise_df['duration_mins'], 
             marker='o', color='#6a1b9a', label='Minutes')
    avg_duration = exercise_df['duration_mins'].mean()
    plt.axhline(y=avg_duration, color='red', linestyle='--', label=f'Avg: {avg_duration:.1f} mins')
    plt.title('Exercise Duration Trend', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Minutes', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('exercise_duration.png')
    plt.close()

    print("Graphs saved as PNG files: dashboard_sleep_trend.png, dashboard_calories_in_out.png, sleep_quality.png, mood_frequency.png, exercise_duration.png")