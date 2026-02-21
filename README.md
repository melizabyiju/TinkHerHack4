
# Tink-Her-Hack-4.0
Proposing RiverClean - A web application that enables community-driven detection of river pollution using AI-powered image analysis.
<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# RiverClean 

## Basic Details

### Team Member: Meliza Mariya Byiju(Individual)

### Project Description
RiverClean is an AI-powered web platform that detects river pollution using image-based analysis. Users upload images of polluted rivers, and the system uses computer vision to detect waste and classify pollution severity. Authorities receive geo-tagged alerts for faster cleanup and accountability.

### The Problem statement
India faces severe river pollution due to:
- Illegal waste dumping
- Lack of real-time monitoring
- Slow response from authorities
- No structured reporting mechanism

Manual monitoring is inefficient, expensive, and non-scalable.

### The Solution
RiverClean provides:
- 📸 Crowd-powered pollution reporting
- 🤖 AI-based waste detection
- 📍 Geo-tagged complaint logging
- 🏛️ Authority dashboard for tracking & action
- 🎁 Incentive-based reporting model

This creates a scalable, transparent, and tech-driven river protection ecosystem.

---

## Technical Details

### Technologies/Components Used

**For Software:**
- **Languages used:** Python, HTML, CSS, JavaScript
- **Frameworks used:** Flask (Python backend), Custom CSS (Frontend templates)
- **Libraries used:** TensorFlow, Werkzeug, NumPy, Pillow, SQLite3
- **Tools used:** VS Code, Git

---

## Features

List the key features of your project:
- **Feature 1: AI Pollution Detection** - Leverages a custom TensorFlow/Keras deep learning model (DepthwiseConv2D) to analyze uploaded images and classify them as 'Clean' or 'Polluted'.
- **Feature 2: User & Authority Dashboards** - Separate interfaces for regular citizens (tracking their reports and earned points) and admins/authorities (viewing and managing polluted river reports).
- **Feature 3: Geo-tagged Reporting** - Captures the location of the report to inform authorities accurately of where cleanup is needed.
- **Feature 4: Incentive System** - Users receive points for verified reports of pollution, encouraging community engagement.

---

## Implementation

### For Software:

#### Installation
```bash
# Clone the repository (if applicable)
git clone https://github.com/melizabyiju/TinkHerHack4.git
cd TinkHerHack4

# Install required Python dependencies
pip install -r requirements.txt
```

#### Run
```bash
# Run the Flask application
python app.py
```
*The app will be available at http://127.0.0.1:5000*

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

![Screenshot1](docs/screenshot_1.png)
*Shows the file upload and location input for detecting pollution.*

![Screenshot2](docs/screenshot_2.png)
*Allows users to track their past reports and accumulated reward points.*

![Screenshot3](docs/screenshot_3.png)
*Enables authorities to review submitted 'Polluted' reports and mark them as 'Done'.*

#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)
*Explain your system architecture: Users upload images -> Flask server -> TensorFlow Model predicts status -> Results and Location saved in SQLite database -> Authorities view actionable reports in Admin Panel.*

**Application Workflow:**

![Workflow](docs/workflow.png)
*Add caption explaining your workflow: Registration/Login -> Upload image & enter location -> AI Processing -> Display result -> If Polluted: Alert Admin & Add point to user -> Admin reviews & resolves issue.*

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `http://127.0.0.1:5000` (Local)

##### Endpoints

**POST /detect**
- **Description:** Analyzes an uploaded image using the AI model and logs the report.
- **Parameters (Form Data):**
  - `photo` (File): Image of the river (png, jpg, jpeg)
  - `location` (string): The geographical location of the river
- **Response:**
```json
{
  "category": "Polluted",
  "location": "Kerala",
  "authorities_notified": true
}
```

**POST /update_status/<report_id>**
- **Description:** Admin endpoint to update the status of a specific pollution report to 'Done'.
- **Response:**
```json
{
  "success": true
}
```

**GET /dashboard**
- **Description:** Returns the user dashboard showing their submitted reports and current score.
- **Response:** HTML Page rendering `dashboard.html`

**GET /admin**
- **Description:** Returns the admin dashboard listing all 'Polluted' reports for action.
- **Response:** HTML Page rendering `admin.html`

[Authentication endpoints (`/login`, `/register`, `/logout`) are also available using standard GET/POST methods.]

---


## Project Demo

### Video
https://drive.google.com/file/d/1l8R2NQI2_LGh-ud-sRmlpaX6mqTwGXsO/view?usp=sharing
---

## AI Tools Used

**Tool Used:** GitHub Copilot,Gemini, ChatGPT

**Purpose:** [What you used it for]
Debugging support for model loading and prediction pipeline.
Designed database schema (SQLite) for storing reports and user data.
Code review and optimization suggestions for frontend–backend communication.

**Key Prompts Used:**
“Provide technical implementation for RiverClean AI-based river pollution detection system.”
“Explain how to integrate a TensorFlow model with Flask backend.”
“Generate workflow for image upload → AI prediction → database storage → admin alert.”
“Debug model loading error in Flask application.”

**Percentage of AI-generated code:** 50%

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

=======
