# Practica_TaskTracker
A simple task managing and tracking program.
=======
Descrierea aplicatiei

    Aplicatia este un Task Manager dezvoltat in Python folosind FastAPI si SQLite.
    Permite gestionarea sarcinilor printr-un API REST si include functionalitati de:
    
    Creare, citire, actualizare si stergere task-uri (CRUD)
    
    Filtrare task-uri dupa status sau deadline
    
    Exportul listei de sarcini in CSV sau JSON
    
    (Optional) autentificare simpla prin header user
Fiecare task are urmatoarele campuri:

| Camp        | Tip      | Descriere                      |
|-------------| -------- | ------------------------------ |
| id          | int      | ID unic task                   |
| title       | string   | Titlul task-ului               |
| description | string   | Descriere task                 |
| status      | string   | `to-do`, `in-progress`, `done` |
| deadline    | date     | Data limita (optional)         |
| owner       | string   | User asociat task-ului         |
| created\_at | datetime | Data crearii                   |
| updated\_at | datetime | Data ultimei modificari        |

Pasi pentru instalare si rulare

    1.Cloneaza repository-ul:
        git clone <URL_REPO>
        cd Practica_TaskTracker


    2.Creeaza un mediu virtual si instaleaza dependentele:
        python -m venv venv
        # Linux/Mac
        source venv/bin/activate
        # Windows
        venv\Scripts\activate
        
        pip install -r requirements.txt

    3.Ruleaza serverul FastAPI:
        uvicorn app.main:app --reload

    4.Acceseaza Swagger UI pentru testare rapida:
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

    Tehnologii:
        - Python 3.12
        - FastAPI
        - SQLite
        - HTML / JavaScript (frontend simplu)

    Interfata Web (HTML)

Aplicatia include un frontend simplu in HTML/JavaScript (index.html) care permite interactiunea cu API-ul:
    
    Adaugarea de task-uri (titlu, descriere, status, deadline)
    Listarea tuturor task-urilor
    Filtrarea task-urilor dupa status si deadline
    Stergerea task-urilor
    Header-ul X-User este trimis automat pentru a putea folosi autentificarea simpla.
    Pagina poate fi deschisa direct in browser sau cu un Live Server (de exemplu in VSCode).

Exemplu utilizare:

    Deschide index.html in browser.

    Completeaza titlu, descriere, deadline si apasa Adauga.

    Task-urile apar in lista de mai jos, unde le poti filtra sau sterge.

Structura proiectului:

    - app
        - main.py         # aplicatia FastAPI
        - models.py       # modelele SQLAlchemy
        - schemas.py      # Pydantic schemas
        - crud.py         # functii CRUD
        - db.py           # configurare baza de date
        - utils.py        # functii auxiliare 
    - index.html          # frontend simplu
    - requirements.txt    # dependinte Python
    - README.md


>>>>>>> 716934f (Initial commit: setup FastAPI Task Manager)
