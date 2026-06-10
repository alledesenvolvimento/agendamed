# domain/value_objects/cpf.py
# Value Object CPF — valida e representa o CPF do paciente no AgendaMed


class CPF:
    """
    Value Object que representa o CPF de um paciente.
    Garante que nenhum CPF inválido exista no domínio do AgendaMed.
    """

    def __init__(self, numero: str) -> None:
        # Remove pontos e traços antes de validar
        numero_limpo = self._limpar(numero)

        # Se não passar na validação, lança um erro imediatamente
        if not self._e_valido(numero_limpo):
            raise ValueError(f"CPF inválido: {numero}")

        # Guarda o número limpo (só dígitos)
        self._numero = numero_limpo

    # ── Propriedade de leitura — não permite alterar o valor após criação ──

    @property
    def numero(self) -> str:
        """Retorna o CPF formatado com pontos e traço: 123.456.789-09"""
        return (
            f"{self._numero[:3]}."
            f"{self._numero[3:6]}."
            f"{self._numero[6:9]}-"
            f"{self._numero[9:]}"
        )

    @property
    def numero_limpo(self) -> str:
        """Retorna o CPF sem formatação: 12345678909"""
        return self._numero

    # ── Métodos internos de validação ──

    @staticmethod
    def _limpar(numero: str) -> str:
        """Remove pontos, traços e espaços do CPF."""
        return numero.replace(".", "").replace("-", "").replace(" ", "")

    @staticmethod
    def _e_valido(numero: str) -> bool:
        """
        Valida o CPF usando o algoritmo dos dígitos verificadores.
        Rejeita CPFs com todos os dígitos iguais (ex: 111.111.111-11).
        """
        # CPF deve ter exatamente 11 dígitos numéricos
        if len(numero) != 11 or not numero.isdigit():
            return False

        # Rejeita sequências inválidas como 000.000.000-00
        if numero == numero[0] * 11:
            return False

        # Cálculo do primeiro dígito verificador
        soma = sum(int(numero[i]) * (10 - i) for i in range(9))
        primeiro_digito = (soma * 10 % 11) % 10
        if primeiro_digito != int(numero[9]):
            return False

        # Cálculo do segundo dígito verificador
        soma = sum(int(numero[i]) * (11 - i) for i in range(10))
        segundo_digito = (soma * 10 % 11) % 10
        if segundo_digito != int(numero[10]):
            return False

        return True

    # ── Métodos especiais para comparação e representação ──

    def __eq__(self, outro: object) -> bool:
        """Dois CPFs são iguais se tiverem o mesmo número — isso é Value Object."""
        if not isinstance(outro, CPF):
            return False
        return self._numero == outro._numero

    def __hash__(self) -> int:
        """Permite usar CPF em sets e como chave de dicionários."""
        return hash(self._numero)

    def __repr__(self) -> str:
        """Representação legível para debug."""
        return f"CPF({self.numero})"