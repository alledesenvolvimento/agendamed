# tests/test_value_objects.py
# Testes dos Value Objects do domínio do AgendaMed

import pytest

from domain.value_objects.cpf import CPF
from domain.value_objects.crm import CRM
from domain.value_objects.status_consulta import StatusConsulta


# ══════════════════════════════════════════════════════
#  TESTES DO CPF
# ══════════════════════════════════════════════════════

class TestCPF:

    def test_cpf_valido_com_formatacao(self):
        """CPF com pontos e traço deve ser aceito e armazenado sem formatação."""
        cpf = CPF("529.982.247-25")
        assert cpf.numero_limpo == "52998224725"

    def test_cpf_valido_sem_formatacao(self):
        """CPF só com dígitos também deve ser aceito."""
        cpf = CPF("52998224725")
        assert cpf.numero == "529.982.247-25"

    def test_cpf_formatado_corretamente(self):
        """A propriedade numero deve devolver o CPF com pontos e traço."""
        cpf = CPF("52998224725")
        assert cpf.numero == "529.982.247-25"

    def test_cpf_invalido_levanta_value_error(self):
        """Um CPF inválido deve lançar ValueError imediatamente."""
        with pytest.raises(ValueError):
            CPF("123.456.789-00")

    def test_cpf_com_todos_digitos_iguais_e_invalido(self):
        """CPF com todos os dígitos iguais (ex: 111.111.111-11) deve ser rejeitado."""
        with pytest.raises(ValueError):
            CPF("111.111.111-11")

    def test_dois_cpfs_iguais_sao_equivalentes(self):
        """Dois CPFs com o mesmo número são iguais — comportamento de Value Object."""
        cpf1 = CPF("529.982.247-25")
        cpf2 = CPF("52998224725")  # mesmo número, sem formatação
        assert cpf1 == cpf2

    def test_dois_cpfs_diferentes_nao_sao_equivalentes(self):
        """CPFs com números diferentes não são iguais."""
        cpf1 = CPF("529.982.247-25")
        cpf2 = CPF("111.444.777-35")
        assert cpf1 != cpf2


# ══════════════════════════════════════════════════════
#  TESTES DO CRM
# ══════════════════════════════════════════════════════

class TestCRM:

    def test_crm_valido(self):
        """CRM no formato correto deve ser aceito."""
        crm = CRM("123456/SP")
        assert crm.valor == "123456/SP"

    def test_crm_com_letras_minusculas_e_aceito(self):
        """CRM com estado em minúsculas deve ser normalizado para maiúsculas."""
        crm = CRM("123456/sp")
        assert crm.valor == "123456/SP"

    def test_crm_retorna_numero_corretamente(self):
        """A propriedade numero deve retornar só os dígitos do CRM."""
        crm = CRM("123456/SP")
        assert crm.numero == "123456"

    def test_crm_retorna_estado_corretamente(self):
        """A propriedade estado deve retornar só a sigla do estado."""
        crm = CRM("123456/SP")
        assert crm.estado == "SP"

    def test_crm_invalido_sem_estado_levanta_value_error(self):
        """CRM sem a sigla do estado deve ser rejeitado."""
        with pytest.raises(ValueError):
            CRM("123456")

    def test_crm_invalido_com_poucos_digitos_levanta_value_error(self):
        """CRM com menos de 6 dígitos deve ser rejeitado."""
        with pytest.raises(ValueError):
            CRM("1234/SP")

    def test_dois_crms_iguais_sao_equivalentes(self):
        """Dois CRMs com o mesmo valor são iguais — comportamento de Value Object."""
        crm1 = CRM("123456/SP")
        crm2 = CRM("123456/SP")
        assert crm1 == crm2

    def test_dois_crms_diferentes_nao_sao_equivalentes(self):
        """CRMs com valores diferentes não são iguais."""
        crm1 = CRM("123456/SP")
        crm2 = CRM("654321/RJ")
        assert crm1 != crm2


# ══════════════════════════════════════════════════════
#  TESTES DO STATUS CONSULTA
# ══════════════════════════════════════════════════════

class TestStatusConsulta:

    def test_consulta_agendada_pode_ser_cancelada(self):
        """Status AGENDADA deve permitir cancelamento."""
        assert StatusConsulta.AGENDADA.pode_cancelar() is True

    def test_consulta_cancelada_nao_pode_ser_cancelada_novamente(self):
        """Status CANCELADA não deve permitir novo cancelamento."""
        assert StatusConsulta.CANCELADA.pode_cancelar() is False

    def test_consulta_realizada_nao_pode_ser_cancelada(self):
        """Status REALIZADA não deve permitir cancelamento."""
        assert StatusConsulta.REALIZADA.pode_cancelar() is False

    def test_consulta_agendada_pode_ser_realizada(self):
        """Status AGENDADA deve permitir marcar como realizada."""
        assert StatusConsulta.AGENDADA.pode_realizar() is True

    def test_consulta_cancelada_nao_pode_ser_realizada(self):
        """Status CANCELADA não deve permitir marcar como realizada."""
        assert StatusConsulta.CANCELADA.pode_realizar() is False

    def test_consulta_realizada_nao_pode_ser_realizada_novamente(self):
        """Status REALIZADA não deve permitir nova realização."""
        assert StatusConsulta.REALIZADA.pode_realizar() is False

    def test_status_tem_valor_string_correto(self):
        """O .value de cada status deve retornar a string correspondente."""
        assert StatusConsulta.AGENDADA.value == "AGENDADA"
        assert StatusConsulta.CANCELADA.value == "CANCELADA"
        assert StatusConsulta.REALIZADA.value == "REALIZADA"