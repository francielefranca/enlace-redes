from django.shortcuts import render
from django.http import HttpResponse
from enlaceapp.simulador_enlace import EnlaceDadosSimulator, generate_random_mac
from enlaceapp.ospf import links
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
    graph = links()

    context = {}
    context['graph_min'] = graph

    return render(request, 'enlaceapp/ospf.html', context)

def sobre(request):
    return render(request, 'enlaceapp/sobre.html')

def contato(request):
    return render(request, 'enlaceapp/contato.html')