# CREDY - Assignment

## About request count
I have currently implemented it using middleware and celery. However the current approach can be optimized. I was thinking of storing the request count in cache and schedule a daily task to update the request count in the database.

By this appoach we can reduce the number of sql queries running. I would love to discuss the idea with you and learn more about it.

### Follow this documentation to install Redis
<a href="https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/">https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/</a>

### Setup

1. **Clone the repository**
    ```
    git clone https://github.com/arunkumar02042002/credy.git
    cd credy
    ```

2. **Create and activate a virtual environment**
    ```
    virtualenv venv
    source venv/bin/activate
    ```

3. **Add Environments varibales**
    ```
    Create a .env file and set all the variables mentioned in .env-sample
    ```

4. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

5. **Configure PostgreSQL**

    ```
    Create a PostgreSQL database named ' credy_db'
    ```

6. **Run migrations**
    ```sh
    python manage.py migrate
    ```

7. **Create a superuser**
    ```sh
    python manage.py createsuperuser
    ```

8. **Configure Redis and Celery**

    Run the redis server
    ```
    redis-server
    ```

    Open another terminal run the following command:
    ```
    $ redis-cli
    127.0.0.1:6379> ping
    PONG
    127.0.0.1:6379>
    ```

    The "PONG" represents success.

9. **Start the Celery worker**
    ```sh
    celery -A core worker -l INFO --pool=solo
    ```

10. **Run Test**
    ```
    python manage.py test
    ```
    Check every test pass and look for errors.

11. **Run the development server**
    ```sh
    python manage.py runserver
    ```
12. **API Docs**
    ```sh
    http://127.0.0.1:8000/swagger
    ```

Please feel free to contact me on arun.kumar.2403gg@gmail.com
