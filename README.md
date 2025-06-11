Local PostgREST stack (PostgreSQL, Swagger UI and JWT auth)

This project sets up a PostgREST environment with:
- PostgreSQL for data storage
- PostgREST for RESTful API generation
- Swagger UI for exploring the API
- JWT-based authentication

Requirements:
- docker
- docker-compose
  
Steps:

1. Start the stack

```
docker compose -f docker-compose.yml up 
```
This launches PostgreSQL, PostgREST API at http://localhost:3000, and Swagger UI at http://localhost:8080.

2. Connect to PostgreSQL

```
docker exec -ti postgrest-playground-db-1 psql -U superset -d everse -h localhost
```
3. Create API Schema
```
CREATE SCHEMA IF NOT EXISTS api;
```
4. Create Tables, roles and Permissions
```
CREATE TABLE api.assessment (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT,
  url TEXT,
  identifier TEXT,
  checks JSONB
);

CREATE ROLE web_anon NOLOGIN;

GRANT USAGE ON SCHEMA api TO web_anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON api.assessment TO web_anon;
GRANT USAGE, SELECT ON SEQUENCE api.assessment_id_seq TO web_anon;

ALTER TABLE api.assessment ENABLE ROW LEVEL SECURITY;

CREATE POLICY api_user_policy ON api.assessment
  FOR ALL
  TO web_anon
  USING (true);

```

5. Generate JWT Token

```
JWT_SECRET="xlIjoid2ViX2Fub24iLCJ1c2VyX2lkIjoxL" python scripts/generate_jwt.py
```

6. Populate table via API
    

```
curl -X POST http://localhost:3000/assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoid2ViX2Fub24iLCJ1c2VyX2lkIjoxLCJpYXQiOjE3NDk2MzQyNjAsImV4cCI6MTc0OTYzNzg2MH0.wzFA_HappOplWhtNa2WINMKmfDocHW5ngppQvvyaTk8" \
  -d '{
    "name": "software_1",
    "version": "1.0.0",
    "url": "https://example.org/f-uji/test_15",
    "identifier": "https://everse.software/some_checker_identifier_ZZ",
    "checks": {
      "hasPermissiveLicense": {
        "output": true,
        "evidence": "found MIT license (OPTIONAL)",
        "passed": true
      },
      "licenseName": {
        "output": "Apache 2.0",
        "evidence": "Found the license name in LICENSE file in the repository root (OPTIONAL)",
        "passed": true
      }
    }
  }'

```
Replace <your-jwt-token> with the one generated in step 5.


7. Query table with and without token
```
curl http://localhost:3000/assessment \
  -H "Authorization: Bearer <your-jwt-token>"

```
