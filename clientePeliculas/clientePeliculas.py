import json
from time import sleep

import requests


class ClienteHttp():

    def __init__(self,url,retry=0 , retry_codes=[]):
        self.url=url
        self.retry= retry
        self.retry_codes=retry_codes

    def get(self,  payload = {}, headers = {}) -> dict:
      peliculasFecha={}
      titulo= input("Ingrese  la palabra clave por la que quiere buscar:")
      page=1
      params={
          "Title":titulo,
          "page":page
      }
      peliculasEncontradas=[]
      fechas=[]
      response = requests.request("GET", self.url, headers=headers,
                              data=payload,params=params)
      total= response.json().get("total_pages")
      for i in range(0,total):
        newParams={
            "Title":titulo,
            "page":i+1
        }
        response = requests.request("GET", self.url, headers=headers,
                              data=payload,params=newParams)
        peliculas=response.json().get("data")
        for pelicula in peliculas:
          fecha= pelicula.get("Year")
          fechas.append(fecha)
          peliculasEncontradas.append(pelicula)
      fechasSinRepetir= list(set(fechas))
      for fechaLlave in fechasSinRepetir:
       lista=[]
       for peliculaGuardar in peliculasEncontradas:
          fechaComparar= peliculaGuardar.get("Year")
          if fechaComparar== fechaLlave:
             lista.append(peliculaGuardar)
             peliculasFecha[fechaLlave]=lista
      print("Fechas sin repetir:"+"\n")
      print(fechasSinRepetir)
      print("\n"+"Peliculas ordenadas por año")
      print(peliculasFecha)

      print(f'{i},{response.status_code}')
      if response.status_code == 200 \
                or response.status_code not in self.retry_codes:
            return response.json()



if __name__ == '__main__':
    cliente=ClienteHttp('https://jsonmock.hackerrank.com/api/movies/search/',50,[500,503,301])
    cliente.get()
