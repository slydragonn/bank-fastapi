# 🚀 FastAPI MongoDB Bank API

Este es un proyecto base para construir APIs RESTful para un banco utilizando **FastAPI**, **MongoDB (PyMongo)** y **Docker**, organizado bajo principios de **Clean Architecture**

---

## 🧠 Arquitectura

Se aplica una arquitectura **Clean Architecture (Hexagonal)**, que separa responsabilidades en capas bien definidas:

```

Presentation (FastAPI routers)
└── Service Layer (lógica de negocio)
└── Repository Layer (acceso a datos)
└── MongoDB (almacenamiento)

```

### 🧩 Estructura del Proyecto

```

app/
├── api/              # Endpoints organizados por versión (v1)
│   └── v1/user.py
├── core/             # Configuración de base de datos
├── models/           # Modelos Pydantic
├── repositories/     # Lógica de acceso a datos (Repository Pattern)
├── services/         # Lógica de negocio (Service Layer Pattern)
├── main.py           # App principal

````

---

## 🧰 Patrones de desarrollo utilizados

| Patrón / Arquitectura     | Descripción |
|---------------------------|-------------|
| **Repository Pattern**    | Aisla el acceso a MongoDB desde el resto de la app. |
| **Service Layer Pattern** | Encapsula la lógica de negocio entre routers y repositorios. |
| **Dependency Injection**  | Usado con `Depends()` de FastAPI para inyectar servicios. |
| **DTO con Pydantic**      | Define contratos de entrada/salida. |
| **API Versioning**        | La API se organiza por versiones (`/api/v1/`). |

---

## 🚀 Cómo correr el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/slydragonn/bank-fastapi.git
cd bank-fastapi
````

### 2. Crea el archivo `.env`

```env
MONGO_URI=mongodb://admin:example@mongo:27017
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=example
TESTING=0
PYTHONPATH=.
```

### 3. Levanta los servicios con Docker

```bash
docker compose up --build
```

Modo de desarrollo:

```bash
docker compose watch
```

La API estará disponible en: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

---

## 📬 Endpoints principales

* `POST /api/v1/accounts/` → Crear una cuenta
* `PATCH /api/v1/accounts/{account_id}` → Cantidad a agregar o restar al saldo de la cuenta
* `GET /api/v1/accounts` → Listar todas las cuentas
* `GET /api/v1/accounts/{account_id}` → Obtener cuenta por ID
* `DELETE /api/v1/accounts/{account_id}` → Elimar cuenta por ID

---

## 🧪 Cómo correr los tests

### Crea el archivo .env.test

```env
MONGO_URI=mongodb://admin:example@mongo:27017
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=example
TESTING=1
PYTHONPATH=.
```

### Ejecuta los tests

```bash
docker compose run --rm test
```

## 🛠 Tecnologías utilizadas

* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
* [PyMongo](https://pymongo.readthedocs.io/)
* [Docker](https://www.docker.com/)
* [Pytest](https://docs.pytest.org/)
