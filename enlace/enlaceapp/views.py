from django.shortcuts import render
from django.http import HttpResponse
from enlaceapp.simulador_enlace import EnlaceDadosSimulator, generate_random_mac
from enlaceapp.ospf import NetworkAnalyzer
from enlaceapp.EnlaceForm import EnlaceForm
from .models import Enlace
import os

# Create your views here.

def home(request):
    return render(request, 'enlaceapp/home.html')

def simulador_enlace(request):
    form = EnlaceForm()
    return render(request, 'enlaceapp/simulador_enlace.html', {'form': form})

def resultado_simulador(request):
    if request.method == 'POST':
        form = EnlaceForm(request.POST)
        if form.is_valid():
            input_text = request.POST.get('input_text')

            print(input_text)

            encapsulatedd_simulator = EnlaceDadosSimulator()

            src_mac = generate_random_mac()
            dest_mac = generate_random_mac()

            encap_frame = encapsulatedd_simulator.encapsulate_frame(input_text, dest_mac, src_mac)

            crc = f"{encap_frame[-1]:02X}"

            print("source mac:", src_mac)
            print("destin mac:", dest_mac)
            print("encap_frame:", encap_frame)
            print("encap_frame_hex:", encap_frame.hex())
            print("crc:", crc)

            context = {}
            context['src_mac'] = src_mac
            context['dest_mac'] = dest_mac
            context['input_text'] = input_text
            context['encapsulated_frame'] = encap_frame.hex()
            context['crc'] = crc
            
            return render(request, 'enlaceapp/resultado_simulador.html', context)
        else:
            form = EnlaceForm

    return render(request, 'simulador_enlace.html', {'form':form})

def ospf(request):
    explanation = "Open Shortest Path First (OSPF) é um protocolo de roteamento \
        de estado de link que é usado para encontrar o melhor caminho entre o roteador \
            de origem e o destino usando seu próprio algoritmo Shortest Path First (SPF)."
    return render(request, 'enlaceapp/ospf.html', {'explanation': explanation})

def resultado_ospf(request):
    # Inicializa o NetworkAnalyzer
    analyzer = NetworkAnalyzer()

    # Adiciona roteadores e links à topologia
    analyzer.add_router("RouterA")
    analyzer.add_router("RouterB")
    analyzer.add_router("RouterC")
    analyzer.add_router("RouterD") # Adicionando mais roteadores
    analyzer.add_router("RouterE")
    analyzer.add_router("RouterF")

    # Adiciona links com atributos adicionais
    analyzer.add_link("RouterA", "RouterB", link_id=1, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterB", "RouterC", link_id=2, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterC", link_id=3, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterB", "RouterD", link_id=4, taxa_transmissao=1000, tamanho_max_quadro=1500, latencia=5, custo=1)
    analyzer.add_link("RouterD", "RouterE", link_id=5, taxa_transmissao=2000, tamanho_max_quadro=2000, latencia=8, custo=3)
    analyzer.add_link("RouterC", "RouterF", link_id=6, taxa_transmissao=500, tamanho_max_quadro=1000, latencia=3, custo=2)
    analyzer.add_link("RouterA", "RouterD", link_id=7, taxa_transmissao=1500, tamanho_max_quadro=2000, latencia=4, custo=2)
    analyzer.add_link("RouterB", "RouterE", link_id=8, taxa_transmissao=2500, tamanho_max_quadro=2500, latencia=6, custo=1)
    analyzer.add_link("RouterC", "RouterD", link_id=9, taxa_transmissao=800, tamanho_max_quadro=1800, latencia=7, custo=3)

    # Execute o OSPF e coleta a saída
    ospf_output = analyzer.run_ospf()
    #graph_min = ospf_output.savefig("C:/Users/franc/OneDrive/Área de Trabalho/enlace-redes/enlace/static/enlaceapp/images/graph_min.png")


    # Visualizar a topologia completa e salvar a imagem
    graph_output = analyzer.visualize_topology()
    #graph_output_path = os.path.join(settings.MEDIA_ROOT, 'enlaceapp/images/topologia_completa.png')
    #graph_output.save(graph_output_path)
    #graph_complet = graph_output.savefig("C:/Users/franc/OneDrive/Área de Trabalho/enlace-redes/enlace/static/enlaceapp/images/graph_complet.png")

    # Lista para armazenar a saída do protocolo de roteamento de enlace para cada roteador
    protocol_output = []

    # Executa o protocolo de roteamento de enlace para cada roteador e coleta a saída
    for router_name in ["RouterA", "RouterB", "RouterC", "RouterD", "RouterE", "RouterF"]:
        output = analyzer.run_protocolo_roteamento(router_name)
        protocol_output.append(output)


    print("saida po",protocol_output)

    context = {}
    context['graph_min'] = ospf_output
    context['graph_complet'] = graph_output
    context['protocol_output'] = protocol_output

    # Renderiza o template com as saídas coletadas
    return render(request, 'enlaceapp/resultado_ospf.html', context)

def sobre(request):
    return render(request, 'enlaceapp/sobre.html')

def contato(request):
    return render(request, 'enlaceapp/contato.html')
