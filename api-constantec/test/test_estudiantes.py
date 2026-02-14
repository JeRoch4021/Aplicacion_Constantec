from fastapi import status
from models.factories import EstudiantesFactory
from models.tables import Estudiantes

def test_get_estudiante(client, session):
    # 1. ARRANGE: Create a real record in the Postgres test DB with one line!
    estudiante = EstudiantesFactory()
    
    # 2. Take the user and password of endpoint data
    breakpoint()
    login_data = {"usuario": estudiante.nombre, "password": "test"}
    response = client.post("/v1/login/", data=login_data)

    # 3. Extract the token
    breakpoint()
    token = response.json().get("token")
    
    # 4. ACT: Call the API endpoint
    breakpoint()
    auth_headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/v1/estudiantes/{estudiante.no_control}", headers=auth_headers)

    # 5. ASSERT: 
    # Check if the API responded successfully
    breakpoint()
    assert response.status_code == status.HTTP_200_OK
    api_data = response.json()

    # 6. DATABASE COMPARISON:
    # Fetch the record directly from Postgres to verify
    breakpoint()
    db_record = session.query(Estudiantes).filter(Estudiantes.id == estudiante.id).first()

    # Compare API response against the Database record
    assert api_data["id"] == db_record.id
    assert api_data["no_control"] == db_record.no_control
    assert api_data["nombre"] == db_record.nombre
    assert api_data["apellidos"] == db_record.apellidos