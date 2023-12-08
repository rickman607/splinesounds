# -*- coding: utf-8 -*-
"""Proyecto.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I0HxiSzMcivy2kQf-0NTfeX8riqQTC9W

La eliminación de GAUSS para sistemas tridiagonales:
"""

import numpy as np

def tripiv(a, b, c, d):
  """
    Argumentos:
        a: diagonal inferior (a[0] no se usa)
        b: diagonal principal
        c: diagonal superior (c[-1] no se usa)
        d: lado derecho del sistema Ay=x
    Returns:
        x: solución

    """
  n = len(b)
  x = np.zeros(n)
  fail = 0

  # reordenamiento

  a[0] = b[0]
  b[0] = c[0]
  c[0] = 0

  # eliminación:

  l = 0

  for k in range(0,n):
      q = a[k]
      i = k

      if l < n-1:
          l = l + 1

      for j in range(k+1,l+1):
          q1 = a[j]
          if (np.abs(q1) > np.abs(q)):
              q = q1
              i = j
      if q == 0:
          fail = -1

      if i != k:
          q = d[k]
          d[k] = d[i]
          d[i] = q
          q = a[k]
          a[k] = a[i]
          a[i] = q
          q = b[k]
          b[k] = b[i]
          b[i] = q
          q = c[k]
          c[k] =c[i]
          c[i] = q
      for i in range(k+1,l+1):
          q = a[i]/a[k]
          d[i] = d[i]-q*d[k]
          a[i] = b[i]-q*b[k]
          b[i] = c[i]-q*c[k]
          c[i] = 0



    # sustitución

  x[n-1] = d[n-1]/a[n-1]
  x[n-2] = (d[n-2]-b[n-2]*x[n-1])/a[n-2]

  for i in range(n-3,-1,-1):

      q = d[i] - b[i]*x[i+1]
      x[i] = (q - c[i]*x[i+2])/a[i]

  return x

"""La fución cspline del libro, usando la eliminación de Gauss escrita arriba, lo comentado es del libro pero no funciona y da el mismo resultado que mi función."""

import numpy as np

def cspline(knots,data,x):
  """
  """
  N = np.size(knots-1)
  P = np.size(x)
  h = np.diff(knots)
  D = np.diff(data)/h
  dD3 = 3*np.diff(D)
  a = data[:N]

  # Generar las diagonales de la matriz A
  """
  H = (np.diag(2*(h[:-1]+h[1:]))+np.diag(h[1:-1],1)+np.diag(h[1:-1],-1))
  #print(H)
  """

  A1 = [0]
  A2 = 2*(h[:-1]+h[1:])
  A3 = h[1:-1]
  #for i in range (1,N-2):
   # A1.append(h[i])
    #A3.append(h[i])
  A1 = np.append(A1,A3)
  A3 = np.append(A3,0)
  c = np.zeros(N)
  c[1:N-1]=np.array(tripiv(A1,A2,A3,dD3))
  b = D-h*(c[1:]+2*c[:-1])/3
  d = (c[1:]-c[:1])/(3*h)

  """
  c = np.zeros(N)
  c[1:N-1]=np.linalg.solve(H,dD3)
  b = D-h*(c[1:]+2*c[:-1])/3
  d = (c[1:]-c[:1])/(3*h)
  """
  # Evaluar el spline en x
  s = np.empty(P)
  for i in range(P):
    indices = np.argwhere(x[i]>knots)
    if indices.size>0:
      k = indices.flat[-1]
    elif x[i] == knots[0]:
      k = 0
    else:
      raise ValueError('cspline no da puntos afuera del intervalo de los nodos')
    z=x[i]-knots[k]
    s[i]=a[k]+z*(b[k]+z*(c[k]+z*d[k]))
  return s

"""Implementación (fallida) función raíz cuadrada y función sin^2"""

from matplotlib import pyplot as plt
X = np.array([1 , 4 , 9 , 16 , 25])
Y = np.array([1 , 2 , 3 , 4 , 5])
x = np.arange(1,25,.4)
y = cspline(X,Y,x)
plt.plot(x,y)
plt.show

X = np.linspace(0, 10, 11)
Y = np.sin(X)**2
x = np.arange(0,10,.4)
y = cspline(X,Y,x)
plt.plot(x,y)
plt.show

"""Función nueva que sí funciona para interpolar"""

def cubic_interp1d(x0, x, y):

    x = np.asfarray(x)
    y = np.asfarray(y)

    if np.any(np.diff(x) < 0):
        indexes = np.argsort(x)
        x = x[indexes]
        y = y[indexes]

    size = len(x)

    xdiff = np.diff(x)
    ydiff = np.diff(y)

    Li = np.empty(size)
    Li_1 = np.empty(size-1)
    z = np.empty(size)


    Li[0] = np.sqrt(2*xdiff[0])
    Li_1[0] = 0.0
    B0 = 0.0
    z[0] = B0 / Li[0]

    for i in range(1, size-1, 1):
        Li_1[i] = xdiff[i-1] / Li[i-1]
        Li[i] = np.sqrt(2*(xdiff[i-1]+xdiff[i]) - Li_1[i-1] * Li_1[i-1])
        Bi = 6*(ydiff[i]/xdiff[i] - ydiff[i-1]/xdiff[i-1])
        z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    i = size - 1
    Li_1[i-1] = xdiff[-1] / Li[i-1]
    Li[i] = np.sqrt(2*xdiff[-1] - Li_1[i-1] * Li_1[i-1])
    Bi = 0.0
    z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    i = size-1
    z[i] = z[i] / Li[i]
    for i in range(size-2, -1, -1):
        z[i] = (z[i] - Li_1[i-1]*z[i+1])/Li[i]

    index = x.searchsorted(x0)
    np.clip(index, 1, size-1, index)

    xi1, xi0 = x[index], x[index-1]
    yi1, yi0 = y[index], y[index-1]
    zi1, zi0 = z[index], z[index-1]
    hi1 = xi1 - xi0

    f0 = zi0/(6*hi1)*(xi1-x0)**3 + \
         zi1/(6*hi1)*(x0-xi0)**3 + \
         (yi1/hi1 - zi1*hi1/6)*(x0-xi0) + \
         (yi0/hi1 - zi0*hi1/6)*(xi1-x0)
    return f0

"""Ejemplo con sin^2"""

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x4 = np.linspace(0, 10, 11)
    y4 = np.sin(x4)**2
    plt.scatter(x4, y4)

    x_new = np.linspace(0, 10, 201)
    plt.plot(x_new, cubic_interp1d(x_new, x4, y4))

    plt.show()

"""Usando CubicSpline para un conjunto de datos en 2D que forman la letra D en manuscrita"""

from scipy.interpolate import CubicSpline
t=[i for i in range (1,12)]
x=[1.15,1.22,0.75,0.73,1.6,2.8,3.33,2.75,1.85,1.75,2.18]
y=[3.4,2.4,1,1.6,1.28,1.5,2.88,4.25,4.55,3,0.65]

csx = CubicSpline(t,x)
csy = CubicSpline(t,y)

T=np.linspace(1,11,300)

import csv
with open('dataDx.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(300):
        row = [T[i],csx(T[i])]
        writer.writerow(row)
with open('dataDy.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(300):
        row = [T[i],csy(T[i])]
        writer.writerow(row)
"""
plt.plot(csx(T),csy(T))
plt.axis((0, 4, 0, 5))
plt.show()
"""
fig, (ax1, ax2, ax3) = plt.subplots(1, 3,figsize=(15,5))
fig.suptitle('Splines')


ax1.plot(T, csx(T))
ax1.set_xlabel('spline de t,x')

ax2.plot(T,csy(T))
ax2.set_xlabel('spline de t,y')

ax3.plot(csx(T),csy(T))
ax3.plot(x,y,'ro') #los puntos rojos son los puntos de interpolación
ax3.set_xlabel('spline 2d')
ax3.axis((0,4,0,5))

plt.show()

"""Otro ejemplo con una curva aleatoria"""

from random import random
t=[i for i in range (1,16)]
x=[i for i in range (1,16)]
y=[i for i in range (1,16)]
for i in range(1,16):
  x[i-1]=4*random()
  y[i-1]=4*random()


csx = CubicSpline(t,x)
csy = CubicSpline(t,y)

T=np.linspace(1,15,500)

with open('dataAx.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(500):
        row = [T[i],csx(T[i])]
        writer.writerow(row)
with open('dataAy.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(500):
        row = [T[i],csy(T[i])]
        writer.writerow(row)

"""
plt.plot(csx(T),csy(T))
plt.axis((0, 4, 0, 5))
plt.show()
"""
fig, (ax1, ax2, ax3) = plt.subplots(1, 3,figsize=(15,5))
fig.suptitle('Splines')


ax1.plot(T, csx(T))
ax1.set_xlabel('spline de t,x')

ax2.plot(T,csy(T))
ax2.set_xlabel('spline de t,y')

ax3.plot(csx(T),csy(T))
ax3.plot(x,y,'ro') #los puntos rojos son los puntos de interpolación
ax3.set_xlabel('spline 2d')
ax3.axis((-1,6,-1,6))

plt.show()

"""Portada del álbum Almendra, de Almendra, el famoso "hombre de la tapa". Para los puntos se utilizó el graphic input en la página "https://plotdigitizer.com/app"
"""

from random import random
t=[i for i in range (1,65)]
x = [0.2767052384779938, 0.21879032557386893, 0.2252252340712081, 0.43758040567171363, 0.6177605438334753, 0.85585608585141, 1.0875162284199575, 1.364221712373975, 1.4157014713047367, 1.5250968795676954, 1.5958818549425227, 1.6859720467614157, 1.7245819886974987, 1.6344917968786055, 1.61518658043454, 1.4800515381822248, 1.4607468126902075, 1.4993567546262903, 1.4543114132408201, 1.5186614801183078, 1.5701417300011176, 1.7052767722534325, 1.9498072227687064, 2.284427374150825, 2.6319178334796702, 2.9279280429257053, 3.1209782435581697, 3.1853283104356573, 3.294723718698616, 3.3783785110681213, 3.4298587609509315, 3.635778778578074, 3.9382243874734963, 4.208494471978127, 4.4723296479854175, 4.684685065061948, 4.749035131939436, 4.523809897868228, 4.247104413914211, 3.455598885892337, 3.3140284441906336, 3.2368085603184675, 3.211068435377063, 3.1016735180661525, 2.9086233174336877, 2.992278109803194, 2.95366816786711, 2.779923183678712, 2.741312750790581, 2.6319178334796702, 2.6383527419770094, 2.779923183678712, 2.8507081590535397, 2.966537984861789, 2.9472332593697717, 3.114543335060831, 3.3590737855761046, 3.507078644823098, 3.76447891233305, 3.92535407952677, 4.182754347036722, 4.247104413914211, 4.208494471978127, 4.176319438539383]
y = [0.04070546020609488, 0.2849387390406718, 0.6580730731928881, 0.9226593409295158, 1.0108549360410612, 1.0108549360410612, 1.0922658564532501, 1.2686565290783334, 1.3500679670885307, 1.4043417414973207, 1.4246947303993724, 1.6146537172271502, 1.9267298610702248, 2.096336376593959, 2.3270008236278317, 2.672998529374657, 2.856173617900092, 3.046132863526874, 3.1343284586384197, 3.3649931644712963, 3.907734014147247, 4.199457039688768, 4.423337847219302, 4.592944362743037, 4.599728649243886, 4.464043436824898, 4.233378342793515, 4.090909102672682, 4.0705563725696345, 4.0705563725696345, 4.036635069464888, 4.111261962175231, 4.240162888093369, 4.34192679740761, 4.443690706721851, 4.50474876763149, 4.477612009826599, 4.382632257613705, 4.2808684776989665, 3.9823609068575916, 3.907734014147247, 3.7449119145238647, 3.5142469498919837, 3.113975469736368, 2.8358208877970443, 2.7204884054811043, 2.523745002752974, 2.367706801431935, 2.2320215890129473, 2.1777475558051527, 1.729986458342095, 1.4043417414973207, 1.4314788875007196, 1.3704204383925738, 1.2754406861796803, 1.2279510688722384, 1.078697542250556, 1.078697542250556, 1.11940300245665, 1.0990500135545982, 0.8141112745139273, 0.4274081085610063, 0.13568521241898834, 0.020352471304043145]

csx = CubicSpline(t,x)
csy = CubicSpline(t,y)

T=np.linspace(1,64,1000)
T1=np.linspace(1,64,500)

with open('dataSx.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(500):
        row = [T[i],csx(T[i])]
        writer.writerow(row)
with open('dataSy.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(500):
        row = [T[i],csy(T[i])]
        writer.writerow(row)

"""
plt.plot(csx(T),csy(T))
plt.axis((0, 4, 0, 5))
plt.show()
"""
fig, (ax1, ax2, ax3) = plt.subplots(1, 3,figsize=(16,5))
fig.suptitle('Splines')


ax1.plot(T, csx(T))
ax1.set_xlabel('spline de t,x')

ax2.plot(T,csy(T))
ax2.set_xlabel('spline de t,y')

"fig,  (ax3)=plt.subplots(1,1,figsize=(8,8))"
ax3.plot(csx(T),csy(T))
ax3.plot(x,y,'ro') #los puntos rojos son los puntos de interpolación
ax3.set_xlabel('spline 2d')
ax3.axis((0,5,0,5))

plt.show()

"""Ahora tratemos de convertir esto a música. Para ello usamos scamp"""

t1=[i for i in range (1,12)]
x1=[1.15,1.22,0.75,0.73,1.6,2.8,3.33,2.75,1.85,1.75,2.18]
y1=[3.4,2.4,1,1.6,1.28,1.5,2.88,4.25,4.55,3,0.65]

csx = CubicSpline(t1,x1)
csy = CubicSpline(t1,y1)

import IPython.display as ipd

sr = 22050 # sample rate
T = 12    # seconds
t = np.linspace(0, 12, int(T*sr), endpoint=False) # time variable
xs = csx(t)/4
x = np.array(xs)
print(x)
ipd.Audio(x, rate=sr)

import csv
with open('data1.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    writer.writerow(['x','y'])
    for i in range(1000):
        row = [12*i/1000,csx(12*i/100)]
        writer.writerow(row)

from music21 import *
e1 = note.Note('E')
mary = stream.Stream()
mary.append(e1)
mary.show('midi')

import numpy as np
import soundfile as sf

data = np.random.uniform(-1, 1, 44100)
sf.write('new_file.wav', data, 44100)