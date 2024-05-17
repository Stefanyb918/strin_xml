import re
import xml.etree.ElementTree as ET
import os

def process_xml_file(input_path, output_path, specific_date, specific_msgdefidr):
    # Verificar si el archivo de entrada existe
    if not os.path.isfile(input_path):
        print(f"Error: El archivo {input_path} no existe.")
        return

    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    xml_docs = re.split(r'\n\s*\n', content)

    # Espacios de nombres
    namespaces = {
        'head': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02'
    }

    filtered_xmls = []

    for xml in xml_docs:
        try:
            root = ET.fromstring(xml)

            # Buscar los elementos de fecha y tipo de mensaje en el espacio de nombres correspondiente
            date_element = root.find('.//head:CreDt', namespaces)
            msgdefidr_element = root.find('.//head:MsgDefIdr', namespaces)

            if date_element is not None and msgdefidr_element is not None:
                xml_date = date_element.text.split('T')[0].strip()
                xml_msgdefidr = msgdefidr_element.text.strip()

                if xml_date == specific_date and xml_msgdefidr == specific_msgdefidr:
                    filtered_xmls.append(xml)
        except ET.ParseError:
            continue

    with open(output_path, 'w', encoding='utf-8') as out_file:
        for xml in filtered_xmls:
            compressed_xml = re.sub(r'>\s+<', '><', xml.strip())
            out_file.write(compressed_xml + '\n\n')

# Solicitar la fecha y el tipo de mensaje
specific_date = input("Por favor, ingresa la fecha específica (YYYY-MM-DD): ")
specific_msgdefidr = input("Por favor, ingresa el MsgDefIdr específico: ")

input_path = 'C:/Users/sakur/PycharmProjects/strin/mensajes_raw_1930.xml'
output_path = 'C:/Users/sakur/PycharmProjects/strin/filtrados.xml'

process_xml_file(input_path, output_path, specific_date, specific_msgdefidr)

