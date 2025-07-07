import bcrypt
from flask import Flask, redirect, render_template, request, url_for, session, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Force non-GUI backend (must be set BEFORE importing pyplot)
import matplotlib.pyplot as plt
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import Session
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random string in production

# Database 
mysql_url = 'mysql+mysqlconnector://root:@localhost/healthapp'
engine = create_engine(mysql_url)
Base = declarative_base()

# models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    meals = relationship("Meal", back_populates="user")
    moods = relationship("Mood", back_populates="user")
    sleeps = relationship("Sleep", back_populates="user")
    waters = relationship("Water", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_name = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    carbs = Column(DECIMAL(5, 2))
    protein = Column(DECIMAL(5, 2))
    fat = Column(DECIMAL(5, 2))
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="meals")

class Mood(Base):
    __tablename__ = 'mood'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(String(50))
    date = Column(DateTime)
    note = Column(Text)

    user = relationship("User", back_populates="moods")

class Sleep(Base):
    __tablename__ = 'sleep'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hours = Column(DECIMAL(4, 2))
    date = Column(DateTime)
    quality_rating = Column(String(50), nullable=False)

    user = relationship("User", back_populates="sleeps")

class Water(Base):
    __tablename__ = 'water'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount_ml = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="waters")

class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity = Column(String(100), nullable=False)
    duration_mins = Column(Integer, nullable=False)
    calories_b = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="exercises")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

def fetch_data(table_name, user_id):
    if table_name == 'meals':
        query = db_session.query(Meal).filter_by(user_id=user_id)
    elif table_name == 'exercise':
        query = db_session.query(Exercise).filter_by(user_id=user_id)
    elif table_name == 'sleep':
        query = db_session.query(Sleep).filter_by(user_id=user_id)
    elif table_name == 'water':
        query = db_session.query(Water).filter_by(user_id=user_id)
    elif table_name == 'mood':
        query = db_session.query(Mood).filter_by(user_id=user_id)
    else:
        raise ValueError(f"Unknown table: {table_name}")
    
    df = pd.read_sql(query.statement, db_session.bind, params={'user_id': user_id})
    print(f"{table_name} DataFrame columns: {df.columns.tolist()}")
    return df

# Function to calculate stats (most recent entries)
def calculate_stats(user_id):
    stats = {}
    
    # Most recent sleep hours and quality
    sleep_data = db_session.query(Sleep).filter_by(user_id=user_id).order_by(Sleep.date.desc()).first()
    if sleep_data:
        stats['sleep_hours'] = sleep_data.hours
        stats['sleep_quality'] = sleep_data.quality_rating
    else:
        stats['sleep_hours'] = 0
        stats['sleep_quality'] = 'Unrated'

    # Most recent water intake
    water_data = db_session.query(Water).filter_by(user_id=user_id).order_by(Water.timestamp.desc()).first()
    if water_data:
        stats['water_intake'] = water_data.amount_ml
    else:
        stats['water_intake'] = 0

    # Most recent calorie intake (from meals)
    meal_data = db_session.query(Meal).filter_by(user_id=user_id).order_by(Meal.timestamp.desc()).first()
    if meal_data:
        stats['calories'] = meal_data.calories
    else:
        stats['calories'] = 0

    # Most recent mood
    mood_data = db_session.query(Mood).filter_by(user_id=user_id).order_by(Mood.date.desc()).first()
    if mood_data:
        stats['mood'] = mood_data.rating
    else:
        stats['mood'] = 'Unrated'

    return stats


def generate_graphs(user_id, dashboard_only=False):
    # Fetch data
    meals_df = fetch_data('meals', user_id)
    exercise_df = fetch_data('exercise', user_id)
    sleep_df = fetch_data('sleep', user_id)
    water_df = fetch_data('water', user_id)
    mood_df = fetch_data('mood', user_id)

    if meals_df.empty or exercise_df.empty or sleep_df.empty or water_df.empty or mood_df.empty:
        print(f"Warning: One or more DataFrames are empty for user_id = {user_id}")
        return {}

    # Convert timestamps to datetime objects
    meals_df['timestamp'] = pd.to_datetime(meals_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    exercise_df['timestamp'] = pd.to_datetime(exercise_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    sleep_df['date'] = pd.to_datetime(sleep_df['date'], format='%Y-%m-%d')
    water_df['timestamp'] = pd.to_datetime(water_df['timestamp'], format='%Y-%m-%d %H:%M:%S')
    mood_df['date'] = pd.to_datetime(mood_df['date'], format='%Y-%m-%d')

    graphs = {}

    # Dashboard Chart 1: Sleep Trend (Last 7 Days)
    last_7_days_sleep = sleep_df[sleep_df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.bar(last_7_days_sleep['date'].dt.strftime('%a, %b %d'), last_7_days_sleep['hours'], 
            color='#ff9800', label='Hours Slept', width=0.5)
    plt.title('Sleep Trend (Last 7 Days)', fontsize=14, color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Hours', color='white')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.legend()
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphs['sleep_trend'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
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
    plt.bar([i - bar_width/2 for i in index], daily_calories['calories'], bar_width, label='Calories In', color='#007bff', alpha=0.7)
    plt.bar([i + bar_width/2 for i in index], daily_burned['calories_b'], bar_width, label='Calories Burned', color='#28a745', alpha=0.7)
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
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphs['calories_in_out'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    if not dashboard_only:
        # Graph 3: Sleep Quality Trend 
        max_days = min(30, (pd.Timestamp.now() - sleep_df['date'].min()).days)
        last_n_days_sleep = sleep_df[sleep_df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
        sleep_quality_map = {'Poor': 1, 'Fair': 2, 'Good': 3, 'Excellent': 4}
        last_n_days_sleep['quality_score'] = last_n_days_sleep['quality_rating'].map(sleep_quality_map).fillna(0)
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(last_n_days_sleep['date'].dt.strftime('%a, %b %d'), last_n_days_sleep['quality_score'], 
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
        ax2.plot(last_n_days_sleep['date'].dt.strftime('%a, %b %d'), last_n_days_sleep['hours'], 
                 marker='s', color='#2196f3', label='Hours Slept')
        ax2.set_ylabel('Hours Slept', color='#2196f3')
        ax2.tick_params(axis='y', labelcolor='#2196f3')
        ax2.legend(loc='upper right')

        plt.style.use('dark_background')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphs['sleep_quality'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

        # Graph 4: Mood Frequency
        max_days = min(30, (pd.Timestamp.now() - mood_df['date'].min()).days)
        last_n_days_mood = mood_df[mood_df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=max_days))]
        mood_counts = last_n_days_mood['rating'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(mood_counts.values, labels=None, colors=['#f44336', '#ffeb3b', '#4caf50', '#ff9800', '#9C27B0', '#2196F3'], 
                autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
        plt.title('Mood Overview', fontsize=14, color='white')
        plt.axis('equal')
        plt.legend(mood_counts.index, loc='best', bbox_to_anchor=(1, 0.5), frameon=False, title='Moods')
        plt.style.use('dark_background')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphs['mood_frequency'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

        # Graph 5: Macronutrient Split
        total_carbs = meals_df['carbs'].sum()
        total_protein = meals_df['protein'].sum()
        total_fat = meals_df['fat'].sum()
        macronutrients = {'Carbs': total_carbs, 'Protein': total_protein, 'Fat': total_fat}
        plt.figure(figsize=(8, 8))
        plt.pie(macronutrients.values(), labels=macronutrients.keys(), colors=['#4caf50', '#2196f3', '#ff9800'], 
                autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
        plt.title('Macronutrient Split', fontsize=14, color='white')
        plt.axis('equal')
        plt.style.use('dark_background')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphs['macronutrient_split'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
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
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphs['water_intake'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
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
        plt.title('Calorie Balance', fontsize=14, color='white')
        plt.xlabel('Date', color='white')
        plt.ylabel('Net Calories (In - Burned)', color='white')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7, color='gray')
        plt.legend()
        plt.style.use('dark_background')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphs['calorie_balance'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

    return graphs

@app.route('/')
def loginpage():
    if 'user_id' in session:
        generate_graphs(session['user_id'], dashboard_only=True)
        return redirect(url_for('dashboard'))
    return render_template("login.html", error=None)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('login.html', error='Password does not match!')
    
    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        new_user = User(username=username, email=email, password_hash=pass_hash)
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('loginpage'))
    except Exception as err:
        db_session.rollback()
        if 'Duplicate entry' in str(err):
            error_msg = 'Username or email already exists'
        else:
            error_msg = "An error occurred: " + str(err)
        return render_template('login.html', error=error_msg)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = db_session.query(User).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session['user_id'] = user.id
            generate_graphs(session['user_id'], dashboard_only=True)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid username or password")
    except Exception as err:
        return render_template('login.html', error="An error occurred: " + str(err))
    finally:
        db_session.close()

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    graphs = generate_graphs(session['user_id'], dashboard_only=True)
    stats = calculate_stats(session['user_id'])
    return render_template('dashboard.html', user_id=session['user_id'], stats=stats, graphs=graphs)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    if request.method == 'POST':
        data_type = request.form['type']
        try:
            if data_type == 'meals':
                new_entry = Meal(user_id=session['user_id'], food_name=request.form['food_name'], 
                                calories=request.form['calories'], carbs=request.form['carbs'], 
                                protein=request.form['protein'], fat=request.form['fat'], 
                                timestamp=datetime.now())
            elif data_type == 'exercise':
                new_entry = Exercise(user_id=session['user_id'], activity=request.form['activity'], 
                                   duration_mins=request.form['duration_mins'], 
                                   calories_b=request.form['calories_burned'], 
                                   timestamp=datetime.now())
            elif data_type == 'sleep':
                new_entry = Sleep(user_id=session['user_id'], hours=request.form['hours'], 
                                quality_rating=request.form['quality_rating'], 
                                date=datetime.now())
            elif data_type == 'water':
                new_entry = Water(user_id=session['user_id'], amount_ml=request.form['liters'], 
                                timestamp=datetime.now())
            elif data_type == 'mood':
                new_entry = Mood(user_id=session['user_id'], rating=request.form['rating'], 
                               note=request.form['note'], date=datetime.now())
            db_session.add(new_entry)
            db_session.commit()
            return redirect(url_for('add_data'))
        except Exception as err:
            db_session.rollback()
            return render_template('add_data.html', error="An error occurred: " + str(err))
    return render_template('add_data.html', error=None)

@app.route('/graphs')
def graphs():
    if 'user_id' not in session:
        return redirect(url_for('loginpage'))
    graphs = generate_graphs(session['user_id'])
    return render_template('graphs.html', user_id=session['user_id'], graphs=graphs)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('loginpage'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    print(f"Attempting to serve static file: {filename}")
    full_path = os.path.join('static', filename)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return "Static file not found", 404
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)