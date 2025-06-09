Local PostgREST stack with PostgreSQL and Swagger UI.

Requirements:
- docker
- docker-compose
  
Steps:

1. Start the stack

```
docker compose -f docker-compose.yml up 
```
This starts PostgreSQL, PostgREST API at http://localhost:3000, and Swagger UI at http://localhost:8080.

2. Connect to PostgreSQL

```
docker exec -ti postgrest-playground-db-1 psql -U superset -d everse -h localhost
```
3. Create API Schema
```
create schema api;
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
```

5. Generate JWT Token

```
docker compose run --rm jwtgen --role web_anon --user-id 123 --expire 30
```

6. Populate table via API
   
```
curl -X POST http://localhost:3000/assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
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
Replace <your-jwt-token> with the one generated in previous step.

7. Query table
```
curl http://localhost:3000/assessment \
  -H "Authorization: Bearer <your-jwt-token>"

```
