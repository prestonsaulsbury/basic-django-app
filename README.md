# Setting Up a Django Project from GitHub (No Python Experience Required)

Welcome! This guide will walk you through setting up a Django project hosted on GitHub. Follow these steps carefully, even if you have no prior experience with Python. By the end, you'll have everything running on your local machine.

## Prerequisites

Before you start, make sure you have the following installed:
**Python (3.x)** – Required for running Django.
    - [Install Python](https://www.python.org/downloads/)

## Step 1: Clone the GitHub Repository
1. Clone the project from GitHub:

    ```bash
    git clone https://github.com/prestonsaulsbury/basic-django-app.git
    ```

2. Navigate into the project directory:

    ```bash
    cd basic-django-app
    ```

## Step 2: Set Up a Virtual Environment (Recommended)

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On **Windows**:

        ```bash
        venv\Scripts\activate
        ```

    - On **Mac/Linux**:

        ```bash
        source venv/bin/activate
        ```

3. Your terminal should now show `(venv)` before the prompt, indicating that the virtual environment is active.

## Step 3: Install Project Dependencies

1. Make sure you are in the project directory (where the `requirements.txt` file is located).
2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

   This command reads the `requirements.txt` file and installs all the necessary Python packages.

## Step 4: Set Up the Database
1. Go to the mysite folder
   ```bash
   cd main/mysite
   ```
2. Apply the Django migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

   This command will set up the necessary database tables.

## Step 5: Create a Superuser (Admin Account)

1. To create an admin user, run the following command:

    ```bash
    python manage.py createsuperuser
    ```

2. Follow the prompts to enter a username, email, and password for the admin account.

## Step 6: Run the Django Development Server

1. Start the development server by running:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and navigate to:

    ```
    http://127.0.0.1:8000/
    ```

   You should see the Django welcome page or the project’s homepage.

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Python Documentation](https://docs.python.org/3/)
- [Git Documentation](https://git-scm.com/doc)

## Troubleshooting

- **Issue:** `pip` or `python` not recognized
  - **Solution:** Make sure Python and Git are installed and added to your system's PATH.
- **Issue:** Database errors
  - **Solution:** Double-check that you’ve run the migrations and installed dependencies properly.

## Next Steps

You are now all set up! Explore the project, make your changes, or start developing your own features.

Happy coding!