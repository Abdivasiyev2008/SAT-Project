# SAT Test Preparation Project

This project is a web application designed to assist users in preparing for the SAT (Scholastic Assessment Test). Built on the Django framework, it provides interactive features for students to test their knowledge, review their progress, and improve their scores.

## Features

- **User Authentication**: Sign-up, login, and logout functionalities to provide personalized user experience.
- **SAT Practice Tests**: A wide variety of practice questions covering all SAT sections (Math, Reading, and Writing).
- **Progress Tracking**: Analyze performance over time through detailed analytics and reports.
- **Admin Dashboard**: Manage questions, monitor user activity, and view statistics.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (optionally with frameworks like Bootstrap for styling)
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL for production)

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Abdivasiyev2008/SAT-Project/
   cd SAT-Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application in your browser at `http://127.0.0.1:8000/`.

## Environment Variables

Create a `.env` file in the project root to store sensitive information:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, feel free to reach out:
- **Email**: abdivasiyevsunnatillo2008@gmail.com
- **GitHub**: [Abdivasiyev2008](https://github.com/Abdivasiyev2008)

