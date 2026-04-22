# Chaski

Aplicación de mensajería en tiempo real inspirada en los mensajeros del imperio inca.

Permite crear canales y enviar mensajes instantáneamente utilizando WebSockets, combinando una API REST documentada con comunicación en vivo.

---

## 🚀 Demo

- Home: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- Schema OpenAPI: http://127.0.0.1:8000/api/schema/

---

## 🖼️ Capturas

![Captura 1 - Chat](screenshots/1.png)

![Captura 2 - API / UI](screenshots/2.png)

---

## ✨ Características principales

- Chat en tiempo real con WebSockets (Django Channels)
- API REST completa para canales y mensajes
- Documentación automática con OpenAPI (Swagger + ReDoc)
- Soporte para usuarios autenticados y anónimos
- Persistencia de mensajes en base de datos
- Frontend simple para demostración rápida

---

## 🛠️ Stack técnico

**Backend**
- Django 6
- Django REST Framework
- Django Channels
- Daphne (ASGI server)

**Documentación**
- DRF Spectacular (OpenAPI 3)

**Base de datos**
- SQLite (desarrollo)

**Frontend**
- Django Templates
- Tailwind CSS (CDN)

---

## ⚙️ Arquitectura (resumen)

- `apps/chat/models.py`: modelos de canales y mensajes  
- `apps/chat/views.py`: API REST (ViewSets)  
- `apps/chat/consumers.py`: lógica WebSocket  
- `config/asgi.py`: configuración ASGI + Channels  
- `config/routing.py`: rutas de WebSocket  
- `templates/`: interfaz básica para demo  

---

## 🔌 API REST

### Canales

- `GET /api/channels/` → listar canales  
- `POST /api/channels/` → crear canal  
- `GET /api/channels/{slug}/` → detalle de canal  

### Mensajes

- `GET /api/channels/{slug}/messages/` → mensajes de un canal  
- `POST /api/channels/{slug}/messages/` → enviar mensaje  
- `GET /api/messages/` → listado global  
- `GET /api/messages/{id}/` → detalle  

---

## ⚡ WebSocket

- URL:
```
ws://127.0.0.1:8000/ws/chat/{slug}/
```

### Payload esperado

```json
{
  "content": "Hola equipo",
  "nickname": "visitante"
}
```

### Flujo

1. El cliente se conecta al WebSocket del canal  
2. Envía un mensaje en formato JSON  
3. El servidor:
   - procesa el mensaje  
   - lo guarda en base de datos (si aplica)  
   - lo transmite a todos los clientes conectados  
4. Los usuarios reciben el mensaje en tiempo real  

---

## 🔐 Autenticación

La aplicación soporta dos modos de uso:

### Usuario autenticado
- Mensajes asociados a un usuario real  
- Uso de session auth o basic auth  

### Usuario anónimo
- Requiere `nickname` para enviar mensajes  
- `created_by_name` para identificar creador del canal  

---

## 🧪 Tests

Incluye pruebas base para:

- Creación anónima de canales  
- Publicación de mensajes con nickname  

Ejecutar:

```bash
source .venv/bin/activate
python manage.py test
```

---

## 🖥️ Ejecutar en local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📌 Roadmap

- [ ] Indicador de usuario escribiendo  
- [ ] Estado online/offline  
- [ ] Notificaciones en tiempo real  
- [ ] Mejoras en UI  
- [ ] Soporte para mensajes privados (1 a 1)  

---

## 🧠 Notas

Chaski toma su nombre de los mensajeros del imperio inca, conocidos por transmitir información de forma rápida a través de largas distancias.

Este proyecto busca reflejar esa idea mediante comunicación en tiempo real usando tecnologías modernas.