"""Configuração centralizada de logging da aplicação."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Cria ou recupera um logger configurado para a aplicação."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    return logging.getLogger(name)