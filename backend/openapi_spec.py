"""Genera un spec OpenAPI a partir de las rutas registradas en la app Flask."""
import re

CONVERTER_TYPES = {
    "integer": "integer",
    "float": "number",
    "unicode": "string",
    "any": "string",
    "path": "string",
    "uuid": "string",
}

HIDDEN_ENDPOINTS = {"static"}
HIDDEN_RULE_PREFIXES = ("/docs", "/openapi.json")
JSON_BODY_METHODS = {"POST", "PUT", "PATCH"}

GENERIC_JSON_BODY = {
    "required": True,
    "content": {"application/json": {"schema": {"type": "object"}}},
}

OK_RESPONSE = {
    "type": "object",
    "properties": {
        "ok": {"type": "boolean"},
        "message": {"type": "string"},
    },
}


def array_of(item_schema):
    return {"type": "array", "items": item_schema}


def doc(body=None, response=None, summary=None):
    """Decorador para anotar una vista de Flask con su request/response body.

    `body` y `response` son JSON Schemas (dict). Se guardan como atributo
    en la función de vista y build_spec los usa para completar el spec,
    ya que Flask por si solo no expone el "shape" de un request.get_json().
    """
    def decorator(func):
        spec = getattr(func, "_openapi", {})
        if body is not None:
            spec["requestBody"] = {
                "required": True,
                "content": {"application/json": {"schema": body}},
            }
        if response is not None:
            spec["response_schema"] = response
        if summary is not None:
            spec["summary"] = summary
        func._openapi = spec
        return func
    return decorator


def _path_params(rule):
    params = []
    for name, converter in rule._converters.items():
        type_name = CONVERTER_TYPES.get(
            converter.__class__.__name__.replace("Converter", "").lower(), "string"
        )
        params.append({
            "name": name,
            "in": "path",
            "required": True,
            "schema": {"type": type_name},
        })
    return params


def build_spec(app, title="Gestion NG API", version="1.0.0"):
    paths = {}

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if rule.endpoint in HIDDEN_ENDPOINTS:
            continue
        if rule.rule.startswith(HIDDEN_RULE_PREFIXES):
            continue

        methods = rule.methods - {"HEAD", "OPTIONS"}
        if not methods:
            continue

        openapi_path = re.sub(r"<[^:>]+:([^>]+)>", r"{\1}", rule.rule)
        openapi_path = re.sub(r"<([^>]+)>", r"{\1}", openapi_path)

        view = app.view_functions.get(rule.endpoint)
        module = getattr(view, "__module__", "") or ""
        tag = module.rsplit(".", 1)[-1] if module else "default"
        extra = getattr(view, "_openapi", {}) if view else {}

        responses = {"200": {"description": "OK"}}
        if extra.get("response_schema") is not None:
            responses["200"]["content"] = {
                "application/json": {"schema": extra["response_schema"]}
            }

        path_item = paths.setdefault(openapi_path, {})
        for method in methods:
            operation = {
                "tags": [tag],
                "summary": extra.get("summary")
                or ((view.__doc__ or rule.endpoint).strip().splitlines()[0]
                    if view and view.__doc__ else rule.endpoint),
                "operationId": rule.endpoint,
                "parameters": _path_params(rule),
                "responses": responses,
            }

            if method in JSON_BODY_METHODS:
                operation["requestBody"] = extra.get("requestBody", GENERIC_JSON_BODY)

            path_item[method.lower()] = operation

    return {
        "openapi": "3.0.3",
        "info": {"title": title, "version": version},
        "paths": paths,
    }
