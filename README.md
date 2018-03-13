# Electric Guitar Pickup Simulator - v1

Librerías necesarias:

    -Time
    -PyQt4
    -PyAudio
    -Librosa
    -Soundfile
    -Sounddevice
    -Scipy
    -Tempfile
    -IO
    -Threading
    -Functools
    -OS
    
El código fue realizado utilizando Python 2.7 como interpreter.

El algoritmo consta de tres archivos principales:

- audio_module.py
- egps_window.py
- config.py

En el archivo audio_module.py se encuentran los métodos pertenecientes al procesamiento de audio de la señal. Dentro de audio_module.py estan definidos los métodos para grabar, reproducir, interrumpir y procesar una señal. 

    - El método REC permite al usuario grabar una muestra de audio a través del driver de entrada de audio que se esté utilizando. El mismo, guarda un archivo .wav al directorio temporal del sistema, con el formato y sample rate indicado.
    
    - El método PLAY reproduce el archivo de audio del directorio que se eligió, o también aquel archivo .wav que fue generado durante el proceso de la grabacin. A través de abrir un stream de datos lo reproduce en el driver de salida de audio predeterminado.
    
    -El procesamiento de ese archivo de audio se lleva a cabo al invocar la funcin lfilter. 
    
    Posteriormente, se implementa una doble aplicación de funciones transferencia al archivo; sería como un "doble filtrado". En primer lugar, se aplica una función transferencia inversa a la función transferencia del transductor con el que se grabó la señal: 1/H(z) = a/b. Este sistema existe únicamente si la ROC de la función transferencia del transductor converje, o se la hace converger. Luego, se aplica una función de transferencia H2(z) referida a la función de transferencia de otro de los transductores; particularmente, en la versión del algoritmo v1 se implementa la función H(z) = b/a, para comprobar que el filtrado está funcionando. De esta manera, al aplicarle a la señal x(t) las funciones de transferencia 1/H(z) y H(z), la señal de salida y(t) es equivalente a la señal de entrada x(t), con lo cual se comprueba que es posible deshacer el efecto de una función transferencia con su sistema inverso (siempre que la ROC converja). En teoría, esta operación es el equivalente al proceso de deconvolución, pero realizada en el dominio z: es por esto que está en comentarios un método similar para realizar con la función deconvolución de scipy (se comprobó que el resultado era equivalente).   
    Además se exporta un archivo denominado "recfile_filtered", el cuál es resultado de todo este proceso. 
    
    La idea es que al aplicar el método process, el mismo pueda realizar el procesamiento de datos de la señal de entrada con cada una de las funciones de transferencia de cada transductor, y almacenarlas en los botones de play del lado derecho de la ventana gráfica. De esta manera, se puede acceder rápidamente a cada simulación.
    

Dentro de egps_window.py, se encuentra la realización de una interfaz gráfica para la interacción con el usuario. Dentro de la misma, se definen botones, sus íconos y acciones/métodos que ejecutan, así como también las listas para la creacin de los mismos.
