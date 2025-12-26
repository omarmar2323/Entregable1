from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.tasks_router import router as tasks_router
from app.core.config import get_settings

settings = get_settings()

# Inicialización de la aplicación FastAPI principal
app = FastAPI(
	title=settings.app_name,
	version=settings.app_version,
	description=settings.app_description,
)

# Handler global para errores de validación: campos requeridos faltantes
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	# Intentar leer el cuerpo enviado para identificar qué campos faltan
	try:
		payload = await request.json()
		if not isinstance(payload, dict):
			payload = {}
	except Exception:
		payload = {}

	# Nombre del parámetro del body en el endpoint de creación
	body_param = "task_input"
	body_data = payload if body_param not in payload else payload.get(body_param, {})
	if not isinstance(body_data, dict):
		body_data = {}

	# Campos requeridos según el modelo
	from app.models.task_model import task as TaskModel
	# Considerar todos los campos del modelo excepto 'id' como requeridos
	required_fields = [name for name in TaskModel.model_fields.keys() if name != "id"]

	missing_fields = [f for f in required_fields if f not in body_data]

	# Detectar errores específicos del campo effort_hours (no numérico / <= 0)
	invalid_msgs: list[str] = []
	for err in exc.errors():
		loc = err.get("loc", [])
		type_name = str(err.get("type", "")).lower()
		msg_text = str(err.get("msg", "")).lower()
		if isinstance(loc, (list, tuple)) and "effort_hours" in loc:
			if type_name == "greater_than" or "greater than" in msg_text:
				invalid_msgs.append("effort_hours debe ser mayor a 0")
			elif "valid number" in msg_text or "parsing" in type_name or "float" in type_name or "int" in type_name:
				invalid_msgs.append("effort_hours debe ser numérico")
		elif isinstance(loc, (list, tuple)) and "priority" in loc:
			# Mensaje claro para prioridad inválida
			from typing import get_args
			from app.models.task_model import task as TaskModel
			allowed = ", ".join(get_args(TaskModel.model_fields["priority"].annotation))
			invalid_msgs.append(f"priority debe ser uno de: {allowed}")
		elif isinstance(loc, (list, tuple)) and "status" in loc:
			# Mensaje claro para status inválido
			from typing import get_args
			from app.models.task_model import task as TaskModel
			allowed = ", ".join(get_args(TaskModel.model_fields["status"].annotation))
			invalid_msgs.append(f"status debe ser uno de: {allowed}")
		# Caso JSON inválido: intentar inferir errores de formato por valores sin comillas
		elif type_name == "json_invalid":
			try:
				import re
				raw = (await request.body()).decode("utf-8", errors="ignore")
				# Detectar valores string sin comillas para todos los campos string del esquema
				string_fields = ["title", "description", "priority", "status", "assigned_to"]
				for field in string_fields:
					m = re.search(rf'"{field}"\s*:\s*(.+)', raw)
					if m:
						after = m.group(1).lstrip()
						if after and not after.startswith('"'):
							invalid_msgs.append(f"{field} tiene formato inválido: debe ser texto entre comillas dobles")

				# Para effort_hours: solo marcar numérico cuando el token no está entre comillas y no es número
				m_eh = re.search(r'"effort_hours"\s*:\s*([^,}\]\s]+)', raw)
				if m_eh:
					val = m_eh.group(1).strip()
					# Ignorar si comienza con comillas (no decidir aquí) 
					if val and not val.startswith('"'):
						# ¿Es numérico válido? (enteros/decimales con notación científica)
						is_numeric = re.fullmatch(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?', val) is not None
						if not is_numeric:
							invalid_msgs.append("effort_hours debe ser numérico")
			except Exception:
				pass

	# Construir mensaje priorizando claridad para effort_hours numérico
	parts: list[str] = []
	if invalid_msgs:
		# Si detectamos errores de formato (json inválido) o numéricos de effort_hours, no mezclar con faltantes
		if any(m.startswith("effort_hours debe ser numérico") for m in invalid_msgs) or any("formato inválido" in m for m in invalid_msgs):
			parts.append("; ".join(invalid_msgs))
		else:
			if missing_fields:
				parts.append("Faltan los siguientes campos requeridos: " + ", ".join(missing_fields))
			parts.append("; ".join(invalid_msgs))
	elif missing_fields:
		parts.append("Faltan los siguientes campos requeridos: " + ", ".join(missing_fields))

	msg = " ".join(parts) if parts else "Datos incompletos o inválidos."

	return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"msg": msg, "detail": exc.errors()})

# Incluye el router principal para gestión de tareas (modular)
app.include_router(tasks_router)

__all__ = ["app"]



