If you have docker installed you can spin up MySQL DB with `docker compose up`.
Dependencies of the project are managed by Nix and pipenv.

To start the project install python tooling or use Nix:
```bash
  nix develop
  cd workspace/littlelemon
  pipenv shell
  pipenv install
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```

After running the project feel free to check endpoints created in lab assignments like:

- http://localhost:8000/api/categories/ GET
- http://localhost:8000/api/categories/ POST (as manager)
- http://localhost:8000/api/cart/menu-items/ GET
- http://localhost:8000/api/menu-items/?per_page=10 GET
