import networkx as nx
import matplotlib.pyplot as plt
import random
import time

class Enlace:
    def __init__(self):
        self.colisoes = set()

    def verificar_colisao(self, link_id):
        return link_id in self.colisoes

    def adicionar_colisao(self, link_id):
        self.colisoes.add(link_id)

    def limpar_colisoes(self):
        self.colisoes.clear()

class NetworkAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()  # Crie um grafo vazio
        self.enlace = Enlace()

    def add_router(self, router_name):
        self.graph.add_node(router_name)  # Adicione um nó ao grafo

    def add_link(self, router1, router2, link_id, taxa_transmissao, tamanho_max_quadro, latencia, custo):
        self.graph.add_edge(router1, router2, link_id=link_id, taxa_transmissao=taxa_transmissao, tamanho_max_quadro=tamanho_max_quadro, latencia=latencia, custo=custo)

    def transmitir_quadro(self, link_id, quadro):
        if self.enlace.verificar_colisao(link_id):
            print(f"Colisão detectada no link {link_id}. Retransmitindo quadro...")
            self.enlace.limpar_colisoes()
            self.transmitir_quadro(link_id, quadro)
        else:
            print(f"Transmitindo quadro {quadro} pelo link {link_id}")
            self.enlace.limpar_colisoes()

    def simular_colisao(self, link_id):
        if random.random() < 0.5:  # Simula 50% de chance de colisão
            print(f"Colisão detectada no link {link_id}")
            self.enlace.adicionar_colisao(link_id)

    def simular_falha_link(self, link_id):
        print(f"Falha detectada no link {link_id}. Removendo link...")
        for edge in self.graph.edges():
            if self.graph.edges[edge]['link_id'] == link_id:
                self.graph.remove_edge(*edge)

    def run_protocolo_roteamento(self, router_name):
        # Simula a troca de mensagens entre os roteadores para aprender sobre a topologia da rede
        for neighbor in self.graph.neighbors(router_name):
            link_id = self.graph[router_name][neighbor]['link_id']
            latencia = self.graph[router_name][neighbor]['latencia']
            print(f"Roteador {router_name} aprendeu sobre o link {router_name}-{neighbor} (link_id: {link_id}, latência: {latencia})")

    def csma_cd(self, link_id, quadro):
        if self.enlace.verificar_colisao(link_id):
            print(f"Colisão detectada no link {link_id}. Aguardando tempo aleatório para retransmitir...")
            espera = random.uniform(0.1, 1.0)
            time.sleep(espera)
            self.transmitir_quadro(link_id, quadro)
        else:
            self.transmitir_quadro(link_id, quadro)

    def run_ospf(self):
        # Calcula as rotas mais curtas usando o algoritmo Dijkstra
        shortest_paths = nx.single_source_dijkstra_path(self.graph, source="RouterA")

        # Exibe as rotas para cada roteador
        for router, path in shortest_paths.items():
            print(f"Rota para {router}: {' -> '.join(path)}")

        # Adiciona os valores das arestas do caminho mínimo ao grafo
        min_path = shortest_paths["RouterE"]
        min_path_edges = [(min_path[i], min_path[i+1]) for i in range(len(min_path)-1)]
        min_path_graph = nx.Graph()
        min_path_graph.add_edges_from(min_path_edges)

        # Visualizar o grafo do caminho mínimo
        pos = nx.spring_layout(min_path_graph)
        nx.draw(min_path_graph, pos, with_labels=True, node_size=800, font_size=10)
        plt.title("Caminho Mínimo")
        #plt.show()

        #salvando grafico
        #plt.savefig("enlace/static/enlaceapp/images/graph_min.png")
        plt.savefig("C:/Users/franc/OneDrive/Área de Trabalho/enlace-redes/enlace/static/enlaceapp/images/graph_min.png")
    
    def visualize_topology(self, graph=None):
      if graph is None:
          graph = self.graph

      # Desenha a topologia da rede
      pos = nx.spring_layout(graph)
      nx.draw(graph, pos, with_labels=True, node_size=800, font_size=10)

      # Adiciona os valores das arestas como rótulos
      edge_labels = {(router1, router2): attr['custo'] for router1, router2, attr in graph.edges(data=True)}
      nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

      plt.title("Topologia Completa")
      #plt.show()

      #salvando grafico
      #plt.savefig("enlace/static/enlaceapp/images/graph_complet.png")
      plt.savefig("C:/Users/franc/OneDrive/Área de Trabalho/enlace-redes/enlace/static/enlaceapp/images/graph_complet.png")

def links():
    analyzer = NetworkAnalyzer()
    # Adicione roteadores e links à topologia
    analyzer.add_router("RouterA")
    analyzer.add_router("RouterB")
    analyzer.add_router("RouterC")
    analyzer.add_router("RouterD") # Adicionando mais roteadores
    analyzer.add_router("RouterE")
    analyzer.add_router("RouterF")

    # Adicione links com atributos adicionais
    analyzer.add_link("RouterA", "RouterB", link_id=1, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterB", "RouterC", link_id=2, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterC", link_id=3, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterB", "RouterD", link_id=4, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterD", "RouterE", link_id=5, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterC", "RouterF", link_id=6, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterD", link_id=7, taxa_transmissao=1500, tamanho_max_quadro=2000, latencia=4, custo=2)
    analyzer.add_link("RouterB", "RouterE", link_id=8, taxa_transmissao=2500, tamanho_max_quadro=2500, latencia=6, custo=1)
    analyzer.add_link("RouterC", "RouterD", link_id=9, taxa_transmissao=800, tamanho_max_quadro=1800, latencia=7, custo=3)

    # Simula uma falha de link
    analyzer.simular_falha_link(2)

    minimo = analyzer.run_ospf()
    analyzer.visualize_topology()

    return minimo

'''
if __name__ == "__main__":
    analyzer = NetworkAnalyzer()

    # Adicione roteadores e links à topologia
    analyzer.add_router("RouterA")
    analyzer.add_router("RouterB")
    analyzer.add_router("RouterC")
    analyzer.add_router("RouterD") # Adicionando mais roteadores
    analyzer.add_router("RouterE")
    analyzer.add_router("RouterF")

    # Adicione links com atributos adicionais
    analyzer.add_link("RouterA", "RouterB", link_id=1, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterB", "RouterC", link_id=2, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterC", link_id=3, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterB", "RouterD", link_id=4, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterD", "RouterE", link_id=5, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterC", "RouterF", link_id=6, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterD", link_id=7, taxa_transmissao=1500, tamanho_max_quadro=2000, latencia=4, custo=2)
    analyzer.add_link("RouterB", "RouterE", link_id=8, taxa_transmissao=2500, tamanho_max_quadro=2500, latencia=6, custo=1)
    analyzer.add_link("RouterC", "RouterD", link_id=9, taxa_transmissao=800, tamanho_max_quadro=1800, latencia=7, custo=3)

    # Simula uma falha de link
    analyzer.simular_falha_link(2)

    analyzer.run_ospf()
    analyzer.visualize_topology()

    # Executa o protocolo de roteamento de enlace para cada roteador
    for router_name in ["RouterA", "RouterB", "RouterC", "RouterD", "RouterE", "RouterF"]:
        analyzer.run_protocolo_roteamento(router_name)

    # Simula a transmissão de quadros e a retransmissão em caso de colisão
    for link_id in range(1, 7):
        analyzer.csma_cd(link_id, f"Quadro {link_id}")
'''