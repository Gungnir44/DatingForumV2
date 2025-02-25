Dating Forum V2
A Django-based dating forum web application that includes user profiles, messaging, blogs, notifications, and geolocation-based search.

Getting Started:


How to Run the Project
Ensure you have Python installed (Recommended: Python 3.10+).

Activate the virtual environment:
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate  # Windows

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Collect static files:
python manage.py collectstatic --noinput

Run the development server:
python manage.py runserver

Access the website:
Open a web browser and go to:
http://127.0.0.1:8000/users/login/
(This is the starting URL for testing)

Features Implemented
✅ User Registration & Login
✅ Profile Editing with Geolocation
✅ Friend Requests & Messaging System
✅ Blog Posts with Comments
✅ User Search with Map Integration
✅ Notifications & Privacy Settings
✅ Admin Panel for Moderation