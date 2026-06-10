# domain/value_objects/crm.py
# Value Object CRM — valida e representa o CRM do médico no AgendaMed

import re  # módulo de expressões regulares para validar o formato


class CRM:
    """
    Value Object que representa o CRM de um médico.
    Formato aceito: 6 dígitos numéricos + barra + sigla do estado (ex: 123456/SP).
    """

    # Padrão esperado: 6 dígitos, barra, 2 letras maiúsculas do estado
    _FORMATO_VALIDO = re.compile(r"^\d{6}/[A-Z]{2}$")

    def __init__(self, valor: str) -> None:
        # Remove espaços extras antes de validar
        valor_limpo = valor.strip().upper()

        # Valida o formato — levanta erro se não bater com o padrão
        if not self._FORMATO_VALIDO.match(valor_limpo):
            raise ValueError(
                f"CRM inválido: '{valor}'. "
                "Formato esperado: 6 dígitos + estado (ex: 123456/SP)"
            )

        self._valor = valor_limpo

    # ── Propriedade de leitura ──

    @property
    def valor(self) -> str:
        """Retorna o CRM formatado: 123456/SP"""
        return self._valor

    @property
    def numero(self) -> str:
        """Retorna só os dígitos do CRM: 123456"""
        return self._valor.split("/")[0]

    @property
    def estado(self) -> str:
        """Retorna só a sigla do estado: SP"""
        return self._valor.split("/")[1]

    # ── Métodos especiais para comparação e representação ──

    def __eq__(self, outro: object) -> bool:
        """Dois CRMs são iguais se tiverem o mesmo valor — isso é Value Object."""
        if not isinstance(outro, CRM):
            return False
        return self._valor == outro._valor

    def __hash__(self) -> int:
        """Permite usar CRM em sets e como chave de dicionários."""
        return hash(self._valor)

    def __repr__(self) -> str:
        """Representação legível para debug."""
        return f"CRM({self._valor})"