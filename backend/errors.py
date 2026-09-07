class ServiceError(Exception):
    """Error de negocio levantado por la Service Layer.

    El Controller no necesita capturarlo: test_app.py registra un
    errorhandler que lo traduce a la respuesta JSON {"ok": False, ...}.
    """

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
