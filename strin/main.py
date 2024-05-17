import re
import xml.etree.ElementTree as ET

def process_xml_file(input_path, output_path, specific_date, specific_msgdefidr, folios):
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    xml_docs = re.split(r'\n\s*\n', content)

    # Espacios de nombres
    namespaces = {
        'head': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
        'doc': 'urn:iso:std:iso:20022:tech:xsd:sese.025.001.09'
    }

    # Convertir la cadena de folios en una lista
    folios_list = [folio.strip() for folio in folios.split(',')]

    filtered_xmls = []

    for xml in xml_docs:
        try:
            root = ET.fromstring(xml)

            # Buscar elementos en el espacio de nombres correspondiente
            date_element = root.find('.//head:CreDt', namespaces)
            msgdefidr_element = root.find('.//head:MsgDefIdr', namespaces)
            cmonid_element = root.find('.//doc:CmonId', namespaces)

            if date_element is not None and msgdefidr_element is not None and cmonid_element is not None:
                xml_date = date_element.text.split('T')[0].strip()
                xml_msgdefidr = msgdefidr_element.text.strip()
                xml_cmonid = cmonid_element.text.strip()

                if xml_date == specific_date and xml_msgdefidr == specific_msgdefidr and xml_cmonid in folios_list:
                    filtered_xmls.append(xml)
        except ET.ParseError:
            continue

    with open(output_path, 'w', encoding='utf-8') as out_file:
        for xml in filtered_xmls:
            compressed_xml = re.sub(r'>\s+<', '><', xml.strip())
            out_file.write(compressed_xml + '\n\n')

# Solicitar los datos
specific_date = input("Por favor, ingresa la fecha específica (YYYY-MM-DD): ")
specific_msgdefidr = input("Por favor, ingresa el MsgDefIdr específico: ")
folios = input("Por favor, ingresa los folios (separados por comas, sin espacios): ")

input_path = 'C:/Users/sakur/PycharmProjects/strin/mensajes_bo_1830.xml'
output_path = 'C:/Users/sakur/PycharmProjects/strin/filtrados.xml'

process_xml_file(input_path, output_path, specific_date, specific_msgdefidr, folios)



