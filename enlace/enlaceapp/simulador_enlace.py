import random

class EnlaceDadosSimulator:
    def __init__(self):
        self.frame_size = 64  # Tamanho fixo do quadro em bytes
        self.crc_polynomial = 0b110101  # Polinômio CRC (CRC-6)

    def encapsulate_frame(self, data, dest_mac, src_mac):
        frame = bytearray()
        if isinstance(data, str):
            frame.extend(data.encode())
        elif isinstance(data, bytes):
            frame.extend(data)
        else:
            print("Formato de dados não suportado.")
            return None

        # Adicione campos de endereço MAC
        frame.extend(dest_mac)
        frame.extend(src_mac)

        crc = self.calculate_crc(frame)
        frame.append(crc)
        return frame

    def decapsulate_frame(self, frame):
        received_crc = frame[-1]
        calculated_crc = self.calculate_crc(frame[:-1])
        if received_crc != calculated_crc:
            print("Erro de CRC! Quadro corrompido.")
            return None

        # Remova os campos de endereço MAC e o CRC
        data = frame[0:-1]
        return data

    def calculate_crc(self, data):
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= self.crc_polynomial
                else:
                    crc >>= 1
        return crc

def generate_random_mac():
    mac = [random.randint(0, 255) for _ in range(6)]
    return bytes(mac)

'''
if __name__ == "__main__":
    enlace_simulator = EnlaceDadosSimulator()
    input_data = input("Digite os dados a serem encapsulados: ")

    dest_mac = generate_random_mac()
    src_mac = generate_random_mac()

    encapsulated_frame = enlace_simulator.encapsulate_frame(input_data, dest_mac, src_mac)

    print("\nQuadro encapsulado:\n")
    print("+-------------------+-------------------+-------------------+-------------------+")
    print("|  Endereço de Destino (MAC)  |  Endereço de Origem (MAC)  |  Dados  | Dados Hex | CRC  |")
    print("+-------------------+-------------------+-------------------+-------------------+")
    print(f"| {dest_mac.hex()}           | {src_mac.hex()}            |  {input_data}  | {encapsulated_frame.hex()} | {encapsulated_frame[-1]:02X}  |")
    print("+-------------------+-------------------+-------------------+-------------------+")
'''