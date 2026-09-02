class BrapiClientError(Exception):
    """Exceção base para erros gerados pelo cliente HTTP brapi."""


class BrapiRequestError(BrapiClientError):
    """Gerada quando a comunicação com a API brapi falha."""


class BrapiResponseError(BrapiClientError):
    """Gerada quando a API brapi retorna uma resposta inválida."""