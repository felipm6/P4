PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

  · sox: transforma de WAV a i16.
  
  · x2x: cambia el formato de los datos, en nuestro caso de i16 a f32.
  
  · frame: corta en distintos frames el fichero, con -l y -p asignamos el desplazamiento y el tamaño del mismo.
  
  · window: enventana los frames anteriores.
  
  . lpc: calcula los coeficientes lpc del frame enventanado.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 51 del script `wav2lp.sh`).
  
  · En primer lugar buscamos el numero de columnas y filas que tendra nuestro fichero, estos valores los calculamos anteriormente. Una vez preparados, pasamos de ascii a unit32 `-aI` y creamos un fichero con dichas columnas y filas para poder observar los datos de una manera mas comoda y visual. 

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

  · De esta manera ya almacenamos los datos en formato unit32 y no requieren combersiones para verlos. Solo tenemos que añadir una cabecera para que funcione.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
  
  ```.sh
  # Main command for feature extration
   sox $inputfile -t raw -e signed -b 16 - |
   $X2X +sf | 
   $FRAME -l 240 -p 80 | 
   $WINDOW -l 240 -L 240 |
 	 $LPC -l 240 -m $lpc_order | 
   $LPCC -m $lpc_order -M $lpcc_order > $base.lpcc || exit 1
  ```
 


- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
  
  ```.sh
  # Main command for feature extration
   sox $inputfile -t raw -e signed -b 16 - | 
   $X2X +sf | 
   $FRAME -l 240 -p 80 | 
   $WINDOW -l 240 -L 240 |
	 $MFCC -l 240 -s 8 -w 0 -m $mfcc_order -n $mel_filter_bank_order > $base.mfcc || exit 1
   ```

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    
    · Primero necesitamos obtener los ficheros de texto con los diferentes coeficientes. En nuestro caso hemos escojido el locutor 22 del bloque 2.
    · Codigo coefs `lp`:
    ```
    fmatrix_show work/lp/BLOCK02/SES022/*.lp | egrep '^\[' | cut -f4,5 > lpout.txt
    ```
    
    · Codigo coefs `lpcc`:
    ```
    fmatrix_show work/lpcc/BLOCK02/SES022/*.lpcc | egrep '^\[' | cut -f4,5 > lpccout.txt
    ```
    
    · Codigo coefs `mfcc`:
    ```
    fmatrix_show work/mfcc/BLOCK02/SES022/*.mfcc | egrep '^\[' | cut -f4,5 > mfccout.txt
    ```
    
    · A continuación solo tenemos que representar los datos, para eso hemos realizado un simple programa en python:
    
    ```.py
    import matplotlib.pyplot as plt

	# coeficientes LP
	X, Y = [], []
	for line in open('lpout.txt', 'r'):
	  values = [float(s) for s in line.split()]
 	 X.append(values[0])
	  Y.append(values[1])
	plt.figure(1)
	plt.plot(X, Y, 'b*', markersize=4)
	plt.title('LP',fontsize=18)
	plt.xlabel('coef 1')
	plt.ylabel('coef 2')
	plt.savefig('lpout.png')
	plt.show()

	# coeficientes LPCC
	X, Y = [], []
	for line in open('lpccout.txt', 'r'):
	  values = [float(s) for s in line.split()]
	  X.append(values[0])
	  Y.append(values[1])
	plt.figure(2)
	plt.plot(X, Y, 'b*', markersize=4)
	plt.title('LPCC',fontsize=18)
	plt.xlabel('coef 1')
	plt.ylabel('coef 2')
	plt.savefig('lpccout.png')
	plt.show()

	# coeficientes MFCC
	X, Y = [], []
	for line in open('mfccout.txt', 'r'):
	  values = [float(s) for s in line.split()]
	  X.append(values[0])
	  Y.append(values[1])
	plt.figure(3)
	plt.plot(X, Y, 'b*', markersize=4)
	plt.title('MFCC',fontsize=18)
	plt.xlabel('coef 1')
	plt.ylabel('coef 2')
	plt.savefig('mfccout.png')
	plt.show()
	```
    · Coeficientes LP
    ![lpout](https://user-images.githubusercontent.com/113842807/210063643-46a44d16-1b04-46be-9092-fb9361bbdd68.png)
    
    . Coeficientes LPCC
    ![lpccout](https://user-images.githubusercontent.com/113842807/210063690-d51dac6f-e2ac-4138-868c-a68eaba94783.png)
    
    . Coeficientes MFCC
    ![mfccout](https://user-images.githubusercontent.com/113842807/210063694-996a7fd9-bcaa-4e19-9f1d-7764a6c48244.png)

    
  + ¿Cuál de ellas le parece que contiene más información?
  
  · La que tiemes mas información es la LPCC ya que los coeficientes estan mejor distribuidos por el plano lo que elimina dependencias y correlaciones. El caso contrario seria el LP que practicamente siguen una funcion lineal y nos aporta menos información.

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |   -0.683414   |   0.286001   |   0.31916   |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
  · Como podemos ver LP (en valor absoluto), nos da una rho mucho mas alta, eso significa que estan mas correlados los coeficientes. En cambio con LPCC y MFCC tenemos rhos mucho mas pequeñas, lo que era de esperar viendo las. gràficas anteriores.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

  · La teoria nos dice que para speaker recognition se usan un minimo de 24 coeficientes, nosotros de momento estamos usando 20/30 para probar que nos da mejores resultados.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
  
![s22](https://user-images.githubusercontent.com/113842807/210066388-d3b702bb-17cf-4b74-b239-7efa32565017.png)

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.
  
<img width="677" alt="Captura de pantalla 2022-12-30 a les 12 55 52" src="https://user-images.githubusercontent.com/113842807/210067768-2d764d3c-23fe-4369-9e76-673b887b8770.png">

· En este caso es un poco dificil diferenciar las regiones de un locutor y de otro ya que son muy parecidas, pero basicamente para que se reconozca como uno u otro tienen que coincidir proporcionalmente las regiones con el numero de puntos que hay en ellos. Como podemos ver cuando usamos el modelo correcto las regiones coinciden con los porcentajes.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | tasa de error |   9.68%  |   3.69%  |   14.65%   |

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
  

 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
