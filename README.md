Local PostgREST stack with PostgreSQL and Swagger UI.

Requirements:
- docker
- docker-compose
  
Steps:

1. Run docker compose
```
docker compose -f docker-compose.yml up 
```
2. Create database for API
```
docker exec -ti postgrest-playground-db-1 psql -U superset -d everse -h localhost
```
3. Create a named schema for the database objects which will be exposed in the API.
```
create schema api;
```
4. Create a table, roles and permissions
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

5. Populate table
   
```
curl -X POST http://localhost:3000/assessment \
  -H "Content-Type: application/json" \
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

6. Check
```
curl http://localhost:3000/assessment

```
For a visual overview of API go to http://localhost:8080/. Also access both the database and PostgREST via http://localhost:3000/
