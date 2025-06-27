# 🔠 Personal Habit Tracker

A simple, interactive habit tracking web app built with **Streamlit**. Users can log daily habits, monitor progress with charts, and track weekly streaks — all stored in local CSV files.


## 🚀 Features

* 🔐 User-specific login to manage your own data
* 🗕️ Log daily habits with status: `Done` or `Not Done`
* 📊 Interactive charts (bar + pie) to visualize habit progress
* 🔁 Weekly streak tracking to stay consistent
* 🌃 Optional dark mode toggle
* 🗂️ Local CSV-based data storage (not pushed to Git)


## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://gitlab.com/your-username/your-repo-name.git
cd habit-tracker
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the app:**

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
habit-tracker/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignores all user CSVs
├── habits.csv (optional) # Default fallback file
└── habits_<username>.csv # Generated at runtime
```

---

## ❌ .gitignore Notes

This project ignores all user data to keep the repo clean:

```
habits_*.csv
users.csv
```

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Keerthan Reddy**
[GitLab Profile](https://gitlab.com/keerthanreddy1706)
