<<<<<<< HEAD
# Practica_TaskTracker
A simple task managing and tracking program.
=======
Descrierea aplicației

    Aplicația este un Task Manager dezvoltat în Python folosind FastAPI și SQLite.
    Permite gestionarea sarcinilor printr-un API REST și include funcționalități de:
    
    Creare, citire, actualizare și ștergere task-uri (CRUD)
    
    Filtrare task-uri după status sau deadline
    
    Exportul listei de sarcini în CSV sau JSON
    
    (Optional) autentificare simpla prin header user
Fiecare task are următoarele câmpuri:

| Camp        | Tip      | Descriere                      |
|-------------| -------- | ------------------------------ |
| id          | int      | ID unic task                   |
| title       | string   | Titlul task-ului               |
| description | string   | Descriere task                 |
| status      | string   | `to-do`, `in-progress`, `done` |
| deadline    | date     | Data limită (opțional)         |
| owner       | string   | User asociat task-ului         |
| created\_at | datetime | Data creării                   |
| updated\_at | datetime | Data ultimei modificări        |

Pași pentru instalare și rulare

    1.Cloneaza repository-ul:
        git clone <URL_REPO>
        cd Practica_TaskTracker


    2.Creează un mediu virtual si instalează dependentele:
        python -m venv venv
        # Linux/Mac
        source venv/bin/activate
        # Windows
        venv\Scripts\activate
        
        pip install -r requirements.txt

    3.Rulează serverul FastAPI:
        uvicorn app.main:app --reload

    4.Accesează Swagger UI pentru testare rapida:
        http://127.0.0.1:8000/docs

Exemple API:

    !!HEADER OBLIGATORIU!!
        Key: X-User
        Value: testuser

    Create task:
        curl -X POST "http://127.0.0.1:8000/tasks" \
        -H "Content-Type: application/json" \
        -H "X-User: testuser" \
        -d '{
          "title": "Invata FastAPI",
          "description": "Fac CRUD + SQLite",
          "status": "to-do",
          "deadline": "2025-09-30"
        }'
    
    Afisarea tuturor taskurilor:
        curl -X GET "http://127.0.0.1:8000/tasks" -H "X-User: testuser"
    
    *Filtrare dupa status: 
        curl -X GET "http://127.0.0.1:8000/tasks?status=done" -H "X-User: testuser"
    *Filtrare dupa deadline: 
        curl -X GET "http://127.0.0.1:8000/tasks?due_before=2025-09-30" -H "X-User: testuser"
    *Filtrare dupa status si deadline:
        curl -X GET "http://127.0.0.1:8000/tasks?status=to-do&due_before=2025-09-30" -H "X-User: testuser"

    Actualizare task:
        curl -X PUT "http://127.0.0.1:8000/tasks/1" \
        -H "Content-Type: application/json" \
        -H "X-User: testuser" \
        -d '{
          "status": "in-progress"
        }'

    Stergere task:
        curl -X DELETE "http://127.0.0.1:8000/tasks/1" -H "X-User: testuser"

    Export task:
        Format csv:
            curl -X GET "http://127.0.0.1:8000/tasks/export?format=csv" -H "X-User: testuser"
       Format json:
            curl -X GET "http://127.0.0.1:8000/tasks/export?format=json" -H "X-User: testuser"

>>>>>>> 716934f (Initial commit: setup FastAPI Task Manager)
