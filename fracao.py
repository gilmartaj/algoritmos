#!/usr/bin/env python
# coding: utf-8

import math
class Fracao:
    def __init__(self, numerador, denominador = 1):
        if denominador == 0:
            raise Exception("Denominador não pode ser 0.")
        self._numerador = numerador
        self._denominador = denominador
        
    def __add__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return Fracao(numerador1 + numerador2, mmc)
    
    def __abs__(self):
        numerador = self._numerador if self._numerador >= 0 else -self._numerador
        denominador = self._denominador if self._denominador > 0 else -self._denominador
        return Fracao(numerador, denominador)
    
    def __ceil__(self):
        numerador = self.numerador
        if numerador > 0:
            while numerador % self.denominador != 0:
                numerador += 1
        else:
            while numerador % self.denominador != 0:
                numerador -= 1
        return Fracao(numerador, self.denominador)
        
    def __complex__(self):
        return complex(self._numerador / self._denominador)
    
    def __eq__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 == numerador2
        
    def __float__(self):
        return self._numerador / self._denominador
    
    def __floor__(self):
        numerador = self.numerador
        if numerador > 0:
            while numerador % self.denominador != 0:
                numerador -= 1
        else:
            while numerador % self.denominador != 0:
                numerador += 1
        return Fracao(numerador, self.denominador)
    
    def __floordiv__(self, other):
        numerador = self.numerador * other.denominador
        denominador = self.denominador * other.numerador
        if numerador > 0:
            while numerador % denominador != 0:
                numerador -= 1
        else:
            while numerador % denominador != 0:
                numerador += 1
        return Fracao(numerador, denominador)
    
    def __ge__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 >= numerador2
    
    def __gt__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 > numerador2
    
    def __int__(self):
        return int(self._numerador / self._denominador)

    def __le__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 <= numerador2
    
    def __lt__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 < numerador2
    
    def __mdcCalc(a, b):
        if b == 0:
            return a
        return Fracao.__mdcCalc(b, a % b)
    
    def __mmcCalc(a, b):
        a = abs(a)
        b = abs(b)
        maior = a if a > b else b
        menor = a if maior == b else b
        mmc = menor
        while mmc % maior != 0:
            mmc += menor
            
        return mmc
    
    def __mod__(self, other):
        div = math.floor(self / other)
        return self - div * other
    
    def __mul__(self, other):
        return Fracao(self.numerador * other.numerador, self.denominador * other.denominador)
    
    def __ne__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return numerador1 != numerador2
    
    def __neg__(self):
        return Fracao(-self._numerador, self._denominador)
    
    def __pos__(self):
        return Fracao(self._numerador, self._denominador)
    
    def __pow__(self, other):
        return Fracao.fromNumber(pow(self.numerador / self.denominador, other.numerador / other.denominador))
    
    def __round__(self, ndigits = None):
        return round(self._numerador / self._denominador, ndigits)
        
    def __str__(self):
        return "{0:d}/{1:d}".format(self._numerador, self._denominador)
    
    def __sub__(self, other):
        mmc = Fracao.__mmcCalc(self.denominador, other.denominador)
        numerador1 = mmc // self.denominador * self.numerador
        numerador2 = mmc // other.denominador * other.numerador
        return Fracao(numerador1 - numerador2, mmc)
    
    def __truediv__(self, other):
        return Fracao(self.numerador * other.denominador, self.denominador * other.numerador)
    
    def __trunc__(self):
        numerador = self.numerador
        if numerador > 0:
            while numerador % self.denominador != 0:
                numerador -= 1
        else:
            while numerador % self.denominador != 0:
                numerador += 1
        return Fracao(numerador, self.denominador)
    
    def fromNumber(number):
        numerador = number
        denominador = 1
        
        for i in range(0, 10):
            if numerador % 1 == 0:
                break
            numerador *= 10
            denominador *= 10
        return Fracao(int(numerador), denominador)
    
    def fromString(string):
        parts = string.split("/")
        numerador = int(parts[0].strip())
        denominador = int(parts[1].strip()) if len(parts) > 1 else 1
        return Fracao(numerador, denominador)
    
    def simplify(self):
        mdc = Fracao.__mdcCalc(self.numerador, self.denominador)
        return Fracao(self.numerador // mdc, self.denominador // mdc)
    
    @property
    def numerador(self):
        return self._numerador
    
    @property
    def denominador(self):
        return self._denominador