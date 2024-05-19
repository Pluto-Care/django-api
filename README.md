# Backend API

## Running the server

1. Use Linux or WSL.
2. Make sure you have `make` installed.
3. Run the following command to install the dependencies and setup the database:

    ```bash
    make getready
    ```

4. Run the following command to start the server:

    ```bash
    make run
    ```

## Superuser

To create a superuser, run the following command:

```bash
make superuser
```

Access the admin panel at <http://localhost:8000/admin/>.

## Read Documentation

Set up the documentation by following the instructions in the documentation repository.
<https://github.com/Pluto-Care/documentation>
