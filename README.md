# RiverClean Application (Latest Version)

RiverClean is an AI-powered web platform designed to detect river pollution using community-driven image uploads. This `Latest` directory serves as the main codebase for the fully integrated application, actively containing both the **Frontend** and **Backend** infrastructures.

---

## 🏗️ Project Architecture

### 1. Backend (Python/Flask)
The core of the application logic resides in `app.py`. It is responsible for:
- Routing all web requests (`/`, `/dashboard`, `/admin`, etc.)
- User authentication and session management
- Accessing the SQLite database (`database.db`) for storing users, reward points, and pollution reports
- AI Model Inference: Loading a pre-trained TensorFlow/Keras deep learning model (`model.h5` using a custom `DepthwiseConv2D` layer) to classify images as 'Clean' or 'Polluted'.
- Secure file handling using `werkzeug` for the uploaded image assets stored in the `uploads/` directory.

#### Key Endpoints:
- `POST /detect` - Accepts an image upload and location, processes it via the AI model, logs the report, and awards points if pollution is detected.
- `POST /update_status/<report_id>` - (Admin only) Updates a polluted report's cleanup status to 'Done'.

### 2. Frontend (HTML, CSS, JS)
The frontend relies essentially on Jinja2 templates served by the Flask backend, specifically located inside the `templates/` folder:
- `index.html` & `detect.html`: Clean, responsive interfaces where users can upload geo-tagged images of rivers to be analyzed.
- `dashboard.html`: User-specific dashboard allowing regular citizens to track their report history and overall reward points.
- `admin.html`: A specialized panel for users designated as administrators to view and manage all submitted 'Polluted' reports.
- `login.html` & `result.html`: Form handling and result presentations.
*(The frontend utilizes Bootstrap and custom CSS classes for modern styling, ensuring cross-platform usability).*

### 3. Database
- `database.db` (SQLite3) instances a scalable schema housing the `users` table (ID, username, password hash, points, is_admin status) and `reports` table (user reference, photo filename, category, location, timestamp, and status).

---

## ⚙️ Setup and Installation

### Prerequisites
- Python 3.8+ installed locally.

### Installation Steps

1. **Navigate to the Latest directory:**
   ```bash
   cd Latest
   ```

2. **Install the dependencies:**
   Make sure to install the required Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask Development Server:**
   ```bash
   python app.py
   ```
   *The application will now be accessible locally at `http://127.0.0.1:5000`*

---

## 👥 Role Management (Admin vs. User)

- **Regular Users**: Can register, login, upload images, earn points, and view their dashboard.
- **Admin Users**: The very first user registering under the username strictly set as **`admin`** will automatically be elevated to administrator status. This grants them access to the `/admin` path where actionable backend queries concerning polluted locations can be viewed.

---

## 📄 License
This codebase is fully licensed under the standard [MIT License](LICENSE) provisions.
