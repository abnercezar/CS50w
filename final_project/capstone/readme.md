# Service Control - CS50W Final Project

## Project Description

**Service Control** is a real-world management system developed for Harvard's CS50W. It was designed to support an actual company that provides vehicle tracking services. Its main goal is to register and manage all services performed—tracking both inputs and outputs—categorized by product type and service type. Additionally, the system calculates, on a monthly basis, the number of delivered items and the total amount to be billed for those services.

---

## Distinctiveness and Complexity

This project goes beyond a traditional CRUD application by integrating multiple specialized modules, real-time data visualization, and detailed operational control. Its development required key architectural decisions, such as clearly separating responsibilities between components, integrating JavaScript libraries, and handling complex data logic with Django.

The system stands out by combining multiple interdependent modules and advanced features. It implements:

- **Multiple Django Apps**: Clear separation of responsibilities across modules like Dashboard, Products, Services, Inputs, Outputs, and Users, promoting a modular and scalable architecture.

- **Dynamic Dashboard**: Interactive graphs provide clear and real-time insights into data, allowing quick and efficient analysis of monthly service activity and expected revenue (using Chart.js).

- **Inventory Management**: The system handles product and service inventory, allowing users to register incoming and outgoing items as well as track all services delivered.

- **Authentication and Permissions**: Implements a user authentication system with login and logout capabilities, supporting role-based access (admin and regular users) to ensure security and integrity of data.

- **Responsive Interface and Usability**: The interface is responsive and mobile-friendly, built using Bootstrap, CSS, and JavaScript to deliver a pleasant and intuitive user experience across devices.

---

## File Structure

- `admin/`: Django project settings
- `dashboard/`: App responsible for the dashboard and data visualization
- `entrada/`: Manages input records of products and services
- `saida/`: Manages output records of products and services
- `servicos/`: Tracks services provided
- `usuarios/`: Manages user registration, login, and permissions
- `static/`: Static files (CSS, JavaScript, images)
- `templates/`: HTML templates used globally or per app
- `db.sqlite3`: SQLite database file
- `manage.py`: Django's command-line utility
- `requirements.txt`: Python dependencies required to run the project

---

## Key Features

- Register and manage products and services
- Track and display monthly inputs and outputs
- Automatically calculate monthly totals (quantities and values)
- Visualize data with interactive graphs (Chart.js)
- Login system with role-based access (admin/user)
- Responsive layout for mobile devices (Bootstrap)

---

## How to Run the Application

```bash
# Clone the repository
git clone https://github.com/abnercezar/capstone.git

# Navigate into the project directory
cd capstone

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install the dependencies
pip install -r requirements.txt

# Apply the database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
