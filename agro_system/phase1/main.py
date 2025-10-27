import csv
import subprocess
import os

class Phase1:
    def __init__(self):
        self.plantio = []
        # CORREÇÃO: Usar caminho absoluto baseado no diretório do arquivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_path = os.path.join(current_dir, "plantio.csv")
    
    def adicionar_dados_streamlit(self, cultura, insumo, largura=None, comprimento=None, raio=None):
        if cultura.lower() in ["café", "cafe"]:
            area = largura * comprimento
        elif cultura.lower() == "milho":
            area = 3.14 * (raio ** 2)
        else:
            return None, "Cultura inválida"

        novo_dado = {"cultura": cultura, "area": area, "insumo": insumo}
        self.plantio.append(novo_dado)
        
        # CORREÇÃO: Salvar CSV imediatamente após adicionar
        self.salvar_csv()
        
        return novo_dado, "Dados adicionados com sucesso"

    def get_dados(self):
        return self.plantio

    def calcular_manejo_streamlit(self, posicao):
        if posicao < 0 or posicao >= len(self.plantio):
            return {"erro": "Posição inválida"}
        
        cultura = self.plantio[posicao]["cultura"]
        area = self.plantio[posicao]["area"]
        insumo = self.plantio[posicao]["insumo"]

        if cultura.lower() in ["café", "cafe"]:
            quantidade_insumos = area * 0.5
            return {
                "cultura": "Café",
                "area": area,
                "insumo": insumo,
                "quantidade_insumos": quantidade_insumos,
                "unidade": "litros"
            }
        elif cultura.lower() == "milho":
            raio_original = (area / 3.14) ** 0.5
            ruas_somadas = sum(2 * 3.14 * (raio_original - i) for i in range(int(raio_original)))
            quantidade_insumos = ruas_somadas * 0.5
            return {
                "cultura": "Milho",
                "area": area,
                "insumo": insumo,
                "quantidade_insumos": quantidade_insumos,
                "unidade": "litros"
            }

    def executar_analise_r(self):
        try:
            # CORREÇÃO: Garantir que o CSV existe antes de executar R
            if not os.path.exists(self.csv_path):
                return "Erro: Nenhum dado encontrado. Adicione dados primeiro."
            
            # CORREÇÃO: Usar diretório correto para execução R
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            r_script = """
            plantio <- read.csv("plantio.csv")
            if (nrow(plantio) > 0) {
                media <- mean(plantio$area)
                desvio <- sd(plantio$area)
                cat(paste("Média das áreas:", round(media, 2), "m²\\n"))
                cat(paste("Desvio padrão:", round(desvio, 2), "m²\\n"))
                cat(paste("Total de registros:", nrow(plantio), "\\n"))
            } else {
                cat("Nenhum dado para análise.\\n")
            }
            """
            
            result = subprocess.run(["Rscript", "-e", r_script], 
                                capture_output=True, text=True, cwd=current_dir)
            
            # CORREÇÃO: Combinar stdout e stderr para melhor debug
            output = result.stdout
            if result.stderr:
                output += f"\nErros R: {result.stderr}"
                
            return output
        except Exception as e:
            return f"Erro na análise R: {e}"

    def salvar_csv(self):
        """Salva dados em CSV - CORRIGIDO para usar caminho absoluto"""
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as arquivo:
                campos = ['cultura', 'area', 'insumo']
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                if self.plantio:
                    escritor.writerows(self.plantio)
            return True
        except Exception as e:
            print(f"Erro ao salvar CSV: {e}")
            return False

# Instância global para integração
fase1_instance = Phase1()

def adicionar_dados(cultura, insumo, **kwargs):
    return fase1_instance.adicionar_dados_streamlit(cultura, insumo, **kwargs)

def listar_dados():
    return fase1_instance.get_dados()

def calcular_manejo(posicao):
    return fase1_instance.calcular_manejo_streamlit(posicao)

def executar_analise():
    return fase1_instance.executar_analise_r()

# Função para verificar se o CSV existe (debug)
def verificar_arquivo_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "plantio.csv")
    return os.path.exists(csv_path)