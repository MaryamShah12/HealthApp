# HealthTrack 🌟

Hey there! Welcome to **HealthTrack** 🚀, my favorite project that I poured my heart into! It’s a web app that helps you take control of your wellness by tracking your meals 🍽️, workouts 💪, sleep 😴, water 💧, and mood 😊. With some cool data science tricks using Pandas and Matplotlib, it turns your health data into beautiful, easy-to-understand charts. Built with Flask and SQLAlchemy, this app is all about making health tracking fun and insightful! 📊

## Table of Contents
- [Why HealthTrack Rocks](#why-healthtrack-rocks) 😎
- [Tech Stack](#tech-stack) 🛠️
- [How to Set It Up](#how-to-set-it-up) ⚡
- [How to Use It](#how-to-use-it) 📱
- [Database Details](#database-details) 🗄️
- [Project Structure](#project-structure) 📂
- [Want to Contribute?](#want-to-contribute) 🤝
- [License](#license) 📜

## Why HealthTrack Rocks 😎
This isn’t just any app—it’s like having a health buddy in your pocket! Here’s what makes it special:
- **Safe & Secure**: Sign up and log in with peace of mind, thanks to bcrypt password protection. 🔒
- **Track Your Journey**: Log meals (with calories and macros), exercise, sleep, water, and mood, all timestamped. 🕒
- **Quick Dashboard**: See your latest health stats at a glance—calories, sleep, water, and mood. 📈
- **Awesome Visuals**: Check out charts like:
  - Sleep trends for the last 7 days 😴
  - Calories in vs. calories burned 🔥
  - Sleep quality and hours over 30 days 🌙
  - Mood breakdown in a colorful pie chart 😊
  - Macronutrient split (carbs, protein, fat) 🥗
  - Water intake trends 💦
  - Net calorie balance ⚖️
- **Data Science Vibes**: Uses Pandas for number-crunching and Matplotlib for stunning graphs. 📊

## Tech Stack 🛠️
Here’s the tech that powers HealthTrack:
- **Backend**: Flask, Python, SQLAlchemy 🐍
- **Database**: MySQL 🗄️
- **Data Science**: Pandas for data magic, Matplotlib for charts 📈
- **Frontend**: HTML with Tailwind CSS for a clean, modern look 🎨
- **Security**: bcrypt to keep passwords safe 🔐
- **Extras**: Base64 and BytesIO to handle graph rendering 🖼️

## How to Set It Up ⚡
Excited to try HealthTrack? Here’s how to get it running on your machine:

1. **Grab the Code**:
   ```bash
   git clone <repository-url>
   cd HealthTrack
   ```

2. **Install the Goodies**:
   ```bash
   pip install flask sqlalchemy mysql-connector-python pandas matplotlib bcrypt
   ```

3. **Set Up MySQL**:
   - Make sure MySQL is installed and running.
   - Create a database called `healthapp`:
     ```sql
     CREATE DATABASE healthapp;
     ```
   - If your MySQL username or password is different, update the `mysql_url` in `app.py`:
     ```python
     mysql_url = 'mysql+mysqlconnector://<username>:<password>@localhost/healthapp'
     ```

4. **Add a Secret Key**:
   - In `app.py`, swap out `'your_secret_key_here'` with something super secure:
     ```python
     app.secret_key = '<your-secure-random-string>'
     ```

5. **Fire It Up**:
   ```bash
   python app.py
   ```
   - Open your browser to `http://127.0.0.1:5000` and start exploring! 🚀

## How to Use It 📱
1. **Sign Up**: Create an account with a username, email, and password. ✍️
2. **Log In**: Jump into your personal dashboard. 🔑
3. **Log Your Data**: Go to "Log Today's Data" to add meals, workouts, sleep, water, or mood. 📝
4. **Check Your Dashboard**: Get a quick peek at your latest health stats. 👀
5. **Dive Into Graphs**: Explore detailed charts of your health trends. 📊
6. **Log Out**: Keep your data safe when you’re done. 🚪

## Database Details 🗄️
HealthTrack uses a MySQL database with these tables:
- **users**: Stores your info (id, username, email, password_hash). 🧑‍💻
- **meals**: Tracks what you eat (food_name, calories, carbs, protein, fat, timestamp). 🍽️
- **exercise**: Logs your workouts (activity, duration_mins, calories_b, timestamp). 🏋️
- **sleep**: Records sleep info (hours, quality_rating, date). 😴
- **water**: Keeps track of hydration (amount_ml, timestamp). 💧
- **mood**: Captures how you’re feeling (rating, note, date). 😊

All tables (except `users`) link back to `users` with a `user_id`.

## Project Structure 📂
Here’s how the project is organized:
```
HealthTrack/
├── app.py                # The heart of the app with Flask logic 🐍
├── templates/
│   ├── login.html        # Sign-up and login page 🔐
│   ├── dashboard.html    # Your health snapshot 📈
│   ├── add_data.html     # Form for logging data 📝
│   ├── graphs.html       # Cool health charts 📊
├── static/               # CSS, images, and other goodies 🎨
├── README.md             # This file, yay! 😄
```

## Want to Contribute? 🤝
Love HealthTrack and want to make it even better? I’d love your help! Here’s how:
1. Fork the repo. 🍴
2. Create a new branch (`git checkout -b my-cool-feature`). 🌟
3. Commit your changes (`git commit -m "Added something awesome"`). 💾
4. Push it up (`git push origin my-cool-feature`). 🚀
5. Open a pull request. 🎉

Please keep your Python code PEP 8-friendly and add tests if you can. 🙌

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more info.

---

Made with tons of 💖 by a data science nerd! Let’s make health tracking fun, insightful, and totally awesome! 🌈