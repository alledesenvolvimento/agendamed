# domain/value_objects/status_consulta.py
# Value Object StatusConsulta — define os estados possíveis de uma consulta

from enum import Enum  # importa a classe base para criar Enums no Python


class StatusConsulta(Enum):
    """
    Value Object do tipo Enum que representa o status de uma consulta no AgendaMed.
    Uma consulta só pode estar em um destes três estados.
    """

    AGENDADA = "AGENDADA"      # consulta foi marcada e está confirmada
    CANCELADA = "CANCELADA"    # consulta foi desmarcada — não pode ser revertida
    REALIZADA = "REALIZADA"    # consulta aconteceu — não pode ser revertida

    def pode_cancelar(self) -> bool:
        """Retorna True apenas se a consulta puder ser cancelada."""
        return self == StatusConsulta.AGENDADA

    def pode_realizar(self) -> bool:
        """Retorna True apenas se a consulta puder ser marcada como realizada."""
        return self == StatusConsulta.AGENDADA

    def __repr__(self) -> str:
        """Representação legível para debug."""
        return f"StatusConsulta.{self.value}"