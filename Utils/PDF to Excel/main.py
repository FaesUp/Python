from PyPDF2 import PdfReader
import re
import pandas as pd
import os
import platform

def extract_pdf_info(pdf_file_path, password = None):

  fecha, sucursal, descripcion, documento, cargo, deposito, saldo = [], [], [], [], [], [], []

  def process_page_text(text):

    lines = text.split("\n")
    regex = r'(\d{2}\/\d{2})([A-Za-z.]+)\s(.*?)\s+(\d+)?\s([\d.]+)?\s+([\d.]+)?' #Each parenthesis is a group in the regex.

    for line in lines:
      match = re.search(regex, line)
      if match:
        fecha.append(match.group(1))
        sucursal.append(match.group(2).strip())
        descripcion.append(match.group(3).strip())
        documento.append(match.group(4) if match.group(4) else "")

        if re.match(r'^\d', match.group(3).strip()):
          cargo.append(0) 
          deposito.append(match.group(5) if match.group(5) else 0)
        else:
          cargo.append(match.group(5) if match.group(5) else 0)
          deposito.append(0)
      
        saldo.append(match.group(6)  if match.group(6) else 0)
  try:

  # Open the PDF File
    with open(pdf_file_path, 'rb') as file:
      if password == None:
        # Create a PDF reader object with password
        pdf_reader = PdfReader(file, False)
      else:
        pdf_reader = PdfReader(file, False, password)
      for page in pdf_reader.pages:
        process_page_text(page.extract_text())


        # use Pandas from generate DF                    
        data = pd.DataFrame(
          { 
            'Fecha' : fecha,
            'Sucursal' : sucursal,
            'Descripción' : descripcion,
            'Documento' : documento,
            'Cargo' : cargo,
            'Depósito' : deposito,
            'Saldo' : saldo
          })
        
        output_file = "processed_invoice/data.xlsx"
        data.to_excel(output_file, index=False) # for use ".to_excel" is necesary => pip install openpyxl
        
        # Abre el archivo generado según el sistema operativo 
        if platform.system() == "Darwin": 
        # macOS 
          os.system(f"open {output_file}") 
        elif platform.system() == "Windows": 
        # Windows 
          os.system(f"start {output_file}") 
        elif platform.system() == "Linux": 
        # Linux 
          os.system(f"xdg-open {output_file}")

  except Exception as e:      
      print(f"Error al procesar el archivo PDF {e}")


extract_pdf_info("invoices/archivo.pdf")