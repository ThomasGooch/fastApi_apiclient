# fastapi-apiclient

A FastAPI project for FHIR R4 Patient CRUD operations with PostgreSQL and external FHIR API integration.

## Features
- FastAPI-based REST API
- FHIR R4 Patient resource support (using `fhir.resources` and `fhirclient`)
- PostgreSQL integration (async, via SQLAlchemy/asyncpg)
- External FHIR backend integration with resiliency (retries, circuit breaker)
- Poetry for dependency management
- Environment variable configuration via `.env`
- Unit tests with pytest

## Endpoints
| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | `/patients`           | Create a FHIR Patient      |
| GET    | `/patients/{id}`      | Get a FHIR Patient by ID   |
| PUT    | `/patients/{id}`      | Update a FHIR Patient      |
| DELETE | `/patients/{id}`      | Delete a FHIR Patient      |

## Quickstart
1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd fastApi_apiclient
   ```
2. **Install dependencies**
   ```sh
   poetry install
   ```
3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   BACKENDURL=http://your-fhir-backend-url
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   EXTERNAL_API_URL=https://external-api.example.com
   EXTERNAL_API_KEY=your_api_key_here
   ```
4. **Run the application**
   ```sh
   poetry run uvicorn app.main:app --reload
   ```
5. **Access the API docs**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## Testing
Run all tests with:
```sh
poetry run pytest
```

## Example Patient JSON
```json
{
  "resourceType": "Patient",
  "name": [
    {
      "family": "Doe",
      "given": ["John"]
    }
  ],
  "gender": "male",
  "birthDate": "1980-01-01",
  "address": [
    {
      "line": ["123 Main St"],
      "city": "Anytown",
      "state": "CA",
      "postalCode": "12345"
    }
  ]
}
```

## Notes
- The application expects a running FHIR backend at the URL specified in `BACKENDURL`.
- Circuit breaker and retry logic are implemented for external API calls.
- The service strips non-standard fields like `meta.createdAt` from FHIR responses for compatibility.
- Update the `.env` file with your actual configuration.

---
*Workspace-specific Copilot instructions are in `.github/copilot-instructions.md`.*