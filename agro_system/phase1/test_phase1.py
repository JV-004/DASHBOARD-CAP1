import unittest
import sys
import os

# Adiciona a pasta phase1 ao path para importar os módulos
sys.path.append(os.path.dirname(__file__))

from main import adicionar_dados, listar_dados, calcular_manejo, executar_analise

class TestPhase1(unittest.TestCase):

    def setUp(self):
        """Limpa os dados antes de cada teste"""
        from main import fase1_instance
        fase1_instance.plantio = []

    def test_adicionar_dados_cafe(self):
        """Testa adição de dados de café"""
        resultado, mensagem = adicionar_dados("café", "fosfato", largura=10, comprimento=20)
        
        self.assertEqual(mensagem, "Dados adicionados com sucesso")
        self.assertEqual(resultado["cultura"], "café")
        self.assertEqual(resultado["area"], 200.0)
        self.assertEqual(resultado["insumo"], "fosfato")

    def test_adicionar_dados_milho(self):
        """Testa adição de dados de milho"""
        resultado, mensagem = adicionar_dados("milho", "ureia", raio=10)
        
        self.assertEqual(mensagem, "Dados adicionados com sucesso")
        self.assertEqual(resultado["cultura"], "milho")
        self.assertAlmostEqual(resultado["area"], 314.0)
        self.assertEqual(resultado["insumo"], "ureia")

    def test_listar_dados(self):
        """Testa listagem de dados"""
        # Adiciona um dado primeiro
        adicionar_dados("café", "fosfato", largura=5, comprimento=10)
        
        dados = listar_dados()
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["cultura"], "café")

    def test_calcular_manejo_cafe(self):
        """Testa cálculo de manejo para café"""
        adicionar_dados("café", "fosfato", largura=10, comprimento=20)
        
        resultado = calcular_manejo(0)
        self.assertEqual(resultado["cultura"], "Café")
        self.assertEqual(resultado["quantidade_insumos"], 100.0)

    def test_calcular_manejo_posicao_invalida(self):
        """Testa cálculo com posição inválida"""
        resultado = calcular_manejo(999)
        self.assertEqual(resultado["erro"], "Posição inválida")

    def test_executar_analise_r(self):
        """Testa execução da análise R (requer R instalado)"""
        adicionar_dados("café", "fosfato", largura=10, comprimento=20)
        
        resultado = executar_analise()
        self.assertIsInstance(resultado, str)
        # Verifica se retornou algum resultado (pode ser erro ou sucesso)
        self.assertTrue(len(resultado) > 0)

if __name__ == '__main__':
    # Executa os testes
    unittest.main(verbosity=2)