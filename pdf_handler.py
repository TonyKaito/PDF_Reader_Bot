import requests
import fitz
import io


def pdf_to_img(url, page_no):
  request = requests.get(url)
  filestream = io.BytesIO(request.content)
  
  dpi = 300  # choose desired dpi here
  zoom = dpi / 72  # zoom factor, standard: 72 dpi
  magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
  doc = fitz.open(stream=filestream)  # open document
  
  pix = doc.get_page_pixmap(page_no, matrix=magnify)
  data = io.BytesIO(pix.tobytes())
  return data

def get_page_count(url):

  request = requests.get(url)
  filestream = io.BytesIO(request.content)

  doc = fitz.open(stream=filestream)
  return doc.page_count