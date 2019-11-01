#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 17:48:28 2019

@author: hat
"""

class Nodo:
    
    def __init__(self, clave):
        self.id = clave
        self.conectadoA = {} #Hace seguimiento a los nodos que está conectado y su ponderacipon
    
    #Se utiliza para agregar una conexión desde un nodo a otro
    def agregarVecino(self, vecino, ponderacion=0):
        self.conectadoA[vecino] = ponderacion
        
    #Devuelve todos los nodos de la lista de adyacencia, representados por la variable conectadoA
    def obtenerConexiones(self):
        return self.conectadoA.keys()
    
    #Devuelve la ponderación de las aristas del nodo actual al nodo pasado como parametro
    def obtenerPonderacion(self, vecino):
        return self.conectadoA[vecino]
    
    def obtenerId(self):
        return self.id

    def __str__(self):
        return str(self.id) + ' conectadoA: '+ str([x.id for x in self.conectadoA])
    
    
class Grafo:
    
    def __init__(self):
        self.listaNodos = {}
        self.numNodos = 0
    
    def agregarNodo(self,clave):
        self.numNodos = self.numNodos + 1
        nuevoNodo = Nodo(clave)
        self.listaNodos[clave] = nuevoNodo
        return nuevoNodo
    
    def obtenerNodo(self,n):
        if n in self.listaNodos:
            return self.listaNodos[n]
        else:
            return None
        
    def __contains__(self,n):
        return n in self.listaNodos
        
    def agregarArista(self,de,a,costo=0):
        if de not in self.listaNodos:
            nv = self.agregarNodo(de)
        if a not in self.listaNodos:
            nv = self.agregarNodo(a)
        self.listaNodos[de].agregarVecino(self.listaNodos[a], costo)
    
    

        
    
    
    
    