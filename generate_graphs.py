import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'healthapp'
}

# connect and fetch data
def fetch_data(table_name, user_id):
    conn = mysql.connector.connect(**db_config)
    if table_name == 'meals':
        query = "SELECT timestamp, id, user_id, food_name, calories, carbs, protein, fat FROM meals WHERE user_id = %s"
    elif table_name == 'exercise':
        query = "SELECT timestamp, id, user_id, activity, duration_mins, calories_b FROM exercise WHERE user_id = %s"
    elif table_name == 'sleep':
        query = "SELECT date AS timestamp, id, user_id, hours, quality_rating FROM sleep WHERE user_id = %s"
    elif table_name == 'water':
        query = "SELECT timestamp, id, user_id, amount_ml FROM water WHERE user_id = %s"
    elif table_name == 'mood':
        query = "SELECT date AS timestamp, id, user_id, rating, note FROM mood WHERE user_id = %s"
    else:
        raise ValueError(f"Unknown table: {table_name}")
    
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    print(f"{table_name} DataFrame columns: {df.columns.tolist()}")
    return df


user_id = 5  

# Fetching the data through the method.
meals_df = fetch_data('meals', user_id)
exercise_df = fetch_data('exercise', user_id)
sleep_df = fetch_data('sleep', user_id)
water_df = fetch_data('water', user_id)
mood_df = fetch_data('mood', user_id)


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
    # Convert timestamps to datetime objects
    meals_df['timestamp'] = pd.to_datetime(meals_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    exercise_df['timestamp'] = pd.to_datetime(exercise_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    sleep_df['timestamp'] = pd.to_datetime(sleep_df['timestamp'], format='%Y-%m-%d')
    water_df['timestamp'] = pd.to_datetime(water_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    mood_df['timestamp'] = pd.to_datetime(mood_df['timestamp'], format='%Y-%m-%d')

    # Dashboard Chart 1: Sleep Trend (Last 7 Days)
    last_7_days_sleep = sleep_df[sleep_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.bar(last_7_days_sleep['timestamp'].dt.strftime('%a, %b %d'), last_7_days_sleep['hours'], 
            color='#ff9800', label='Hours Slept', width=0.5)
    plt.title('Sleep Trend (Last 7 Days)', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Hours', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('dashboard_sleep_trend.png')
    plt.close()

    # Dashboard Chart 2: Calories In vs Out (Last 7 Days)
    last_7_days_meals = meals_df[meals_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    last_7_days_exercise = exercise_df[exercise_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    daily_calories = last_7_days_meals.groupby(last_7_days_meals['timestamp'].dt.date).agg({'calories': 'sum'}).reindex(
        pd.date_range(start=(pd.Timestamp.now() - pd.Timedelta(days=7)).date(), end=pd.Timestamp.now().date(), freq='D'),
        fill_value=0
    )
    daily_burned = last_7_days_exercise.groupby(last_7_days_exercise['timestamp'].dt.date).agg({'calories_b': 'sum'}).reindex(
        pd.date_range(start=(pd.Timestamp.now() - pd.Timedelta(days=7)).date(), end=pd.Timestamp.now().date(), freq='D'),
        fill_value=0
    )
    daily_calories.index = daily_calories.index.strftime('%a, %b %d')
    daily_burned.index = daily_burned.index.strftime('%a, %b %d')
    net_calories = daily_calories['calories'] - daily_burned['calories_b']
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(daily_calories))
    # Plot Calories In and Burned side by side
    plt.bar([i - bar_width/2 for i in index], daily_calories['calories'], bar_width, label='Calories In', color='#007bff', alpha=0.7)
    plt.bar([i + bar_width/2 for i in index], daily_burned['calories_b'], bar_width, label='Calories Burned', color='#28a745', alpha=0.7)
    # Plot Net Calories as a line for clarity
    plt.plot(index, net_calories, marker='o', color='#ff4444', label='Net Calories', linewidth=2)
    for i, v in enumerate(net_calories):
        if v < 0:
            plt.text(i, v, f'{v:.1f}', ha='center', va='bottom', color='white', fontsize=10)
        elif v > 0:
            plt.text(i, v, f'{v:.1f}', ha='center', va='top', color='white', fontsize=10)
    plt.xlabel('Date', color='white')
    plt.ylabel('Calories', color='white')
    plt.title('Calories In vs Out (Last 7 Days)', fontsize=14, color='white')
    plt.xticks(index, daily_calories.index, rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('dashboard_calories_in_out.png')
    plt.close()

    # Graph 3: Sleep Quality Trend 
    max_days = min(30, (pd.Timestamp.now() - sleep_df['timestamp'].min()).days)
    last_n_days_sleep = sleep_df[sleep_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    sleep_quality_map = {'Poor': 1, 'Fair': 2, 'Good': 3, 'Excellent': 4}
    last_n_days_sleep['quality_score'] = last_n_days_sleep['quality_rating'].map(sleep_quality_map).fillna(0)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(last_n_days_sleep['timestamp'].dt.strftime('%a, %b %d'), last_n_days_sleep['quality_score'], 
             marker='o', color='#ff9800', label='Quality Score')
    ax1.set_title('Sleep Quality and Hours Trend', fontsize=14, color='white')
    ax1.set_xlabel('Date', color='white')
    ax1.set_ylabel('Quality Score (0=Unrated, 1=Poor, 2=Fair, 3=Good, 4=Excellent)', color='#ff9800')
    ax1.tick_params(axis='y', labelcolor='#ff9800')
    ax1.grid(True, linestyle='--', alpha=0.7, color='gray')
    ax1.legend(loc='upper left')
    ax1.set_xticks(ax1.get_xticks())
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(last_n_days_sleep['timestamp'].dt.strftime('%a, %b %d'), last_n_days_sleep['hours'], 
             marker='s', color='#2196f3', label='Hours Slept')
    ax2.set_ylabel('Hours Slept', color='#2196f3')
    ax2.tick_params(axis='y', labelcolor='#2196f3')
    ax2.legend(loc='upper right')

    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('sleep_quality.png')
    plt.close()

    # Graph 4: Mood Frequency (Simplified Pie Chart, Last 30 days or available data)
    max_days = min(30, (pd.Timestamp.now() - mood_df['timestamp'].min()).days)
    last_n_days_mood = mood_df[mood_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    mood_counts = last_n_days_mood['rating'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(mood_counts.values, labels=None, colors=['#f44336', '#ffeb3b', '#4caf50', '#ff9800', '#9C27B0', '#2196F3'], 
            autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    plt.title('Mood Overview', fontsize=14, color='white')
    plt.axis('equal')
    plt.legend(mood_counts.index, loc='best', bbox_to_anchor=(1, 0.5), frameon=False, title='Moods')
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('mood_frequency.png')
    plt.close()

    # Graph 5: Exercise Duration Trend 
    max_days = min(30, (pd.Timestamp.now() - exercise_df['timestamp'].min()).days)
    last_n_days_exercise = exercise_df[exercise_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    plt.figure(figsize=(10, 6))
    plt.plot(last_n_days_exercise['timestamp'].dt.strftime('%a, %b %d'), last_n_days_exercise['duration_mins'], 
             marker='o', color='#6a1b9a', label='Minutes')
    avg_duration = last_n_days_exercise['duration_mins'].mean()
    plt.axhline(y=avg_duration, color='red', linestyle='--', label=f'Avg: {avg_duration:.1f} mins')
    plt.title('Exercise Duration Trend', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Minutes', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('exercise_duration.png')
    plt.close()

    # Graph 6: Water Intake Trend 
    max_days = min(30, (pd.Timestamp.now() - water_df['timestamp'].min()).days)
    last_n_days_water = water_df[water_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    plt.figure(figsize=(10, 6))
    plt.plot(last_n_days_water['timestamp'].dt.strftime('%a, %b %d'), last_n_days_water['amount_ml'], 
             marker='o', color='#00BCD4', label='Water Intake (ml)')
    avg_water = last_n_days_water['amount_ml'].mean()
    plt.axhline(y=avg_water, color='red', linestyle='--', label=f'Avg: {avg_water:.1f} ml')
    plt.title('Water Intake Trend', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Water Intake (ml)', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('water_intake.png')
    plt.close()

    # Graph 7: Calorie Balance 
    max_days = min(30, (pd.Timestamp.now() - meals_df['timestamp'].min()).days)
    last_n_days_meals = meals_df[meals_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    last_n_days_exercise = exercise_df[exercise_df['timestamp'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
    daily_calories = last_n_days_meals.groupby(last_n_days_meals['timestamp'].dt.strftime('%a, %b %d'))['calories'].sum()
    daily_burned = last_n_days_exercise.groupby(last_n_days_exercise['timestamp'].dt.strftime('%a, %b %d'))['calories_b'].sum()
    common_dates = daily_calories.index.union(daily_burned.index)
    daily_calories = daily_calories.reindex(common_dates, fill_value=0)
    daily_burned = daily_burned.reindex(common_dates, fill_value=0)
    net_calories = daily_calories - daily_burned
    plt.figure(figsize=(10, 6))
    plt.plot(net_calories.index, net_calories.values, marker='o', color='#ff4444', label='Net Calories')
    plt.axhline(y=0, color='gray', linestyle='--', label='Balance Point')
    plt.title('Calorie Balance ', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Net Calories (In - Burned)', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.savefig('calorie_balance.png')
    plt.close()

    print("Graphs saved as PNG files: dashboard_sleep_trend.png, dashboard_calories_in_out.png, sleep_quality.png, mood_frequency.png, exercise_duration.png, water_intake.png, calorie_balance.png")