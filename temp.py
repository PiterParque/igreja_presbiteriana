from PIL import Image
import pytesseract

# Caminho da imagem (ajuste conforme o local do arquivo)
image_path = "C:/Users/lanca/Downloads/nomes.png"

# Carregar a imagem
image = Image.open(image_path)

# Extrair texto com OCR em português
extracted_text = pytesseract.image_to_string(image, lang="por")

# Mostrar o texto extraído
print(extracted_text)
