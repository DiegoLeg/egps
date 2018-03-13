# Electric Guitar Pickup Simulator - v1

Librerías necesarias:

    -Wave
    -PyQt4
    -PyAudio
    -Librosa
    -Sounddevice
    -SWHear
    
El código fue realizado utilizando Python 2.7 como interpreter, ya que tenía problemas con algunas librerías
si utilizaba una versión más reciente.

El algoritmo consta de dos archivos principales:

- audio_module.py
- qtesis.py

En el archivo audio_module.py se encuentran los métodos pertenecientes al procesamiento de audio de la señal.
Al principio iba a implementar una ventana gráfica para este módulo, es por eso que puede haber quedado algo de código remanente de Qt que no se esté utilizando.

Dentro de audio_module.py estánd definidos los métodos para grabar, reproducir y procesar una señal. Se intentó implementar un método para frenar el stream de grabación de datos, pero no se pudo realizar de manera efectiva, por lo que se opta por dejar una libre elección al usuario de la cantidad de segundos que desee grabar (creo que puedo lograr hacerlo andar pero precisaría entender un poco más sobre cómo correr procesos en background. Necesitaría correr REC o PLAY en background para poder usar STOP al mismo tiempo que se estén ejecutando. No me pareció correcto dedicarle mucho más tiempo a ese método ya que no era algo central del trabajo de tesis)

    - El método REC permite al usuario grabar una muestra de audio (actualmente está seteado a 7 segundos pero se va a dejar librado a elección del usuario) a través del driver de entrada de audio que se esté utilizando. El mismo, guarda un archivo llamado "rec_file.wav" al directorio de ejecución del código, con el formato y sample rate indicado.
    
    - El método PLAY levanta el archivo "rec_file.wav" del directorio, y a través de abrir un stream de datos lo reproduce en el driver de salida de audio predeterminado.
    
    - El método PROCESS realiza el procesamiento de ese archivo de audio. En primera instancia, levanta el archivo que fue grabado ("rec_file.wav") utilizando librosa; de esta manera, el archivo ya es transformado también en float32, lo cual permite que sea manipulado con otras funciones y variables sin tener que realizar una conversión de bytes a samples.
    
    Posteriormente, se implementa una doble aplicación de funciones transferencia al archivo; sería como un "doble filtrado". En primer lugar, se aplica una función transferencia inversa a la función transferencia del transductor con el que se grabó la señal: 1/H(z) = a/b. Este sistema existe únicamente si la ROC de la función transferencia del transductor converje, o se la hace converger. Luego, se aplica una función de transferencia H2(z) referida a la función de transferencia de otro de los transductores; particularmente, en la versión del algoritmo v1 se implementa la función H(z) = b/a, para comprobar que el filtrado está funcionando. De esta manera, al aplicarle a la señal x(t) las funciones de transferencia 1/H(z) y H(z), la señal de salida y(t) es equivalente a la señal de entrada x(t), con lo cual se comprueba que es posible deshacer el efecto de una función transferencia con su sistema inverso (siempre que la ROC converja). En teoría, esta operación es el equivalente al proceso de deconvolución, pero realizada en el dominio z: es por esto que está en comentarios un método similar para realizar con la función deconvolución de scipy (se comprobó que el resultado era equivalente).
    
    Finalmente, el método PROCESS exporta un archivo denominado "recfile_filtered", el cuál es resultado de todo este proceso. Se deberían implementar uno para cada uno de los transductores, y que los mismos puedan ser reproducidos desde los botones de play de la parte derecha de la ventana gráfica (esto se encuentra en proceso)
    
    La idea es que al aplicar el método process, el mismo pueda realizar el procesamiento de datos de la señal de entrada con cada una de las funciones de transferencia de cada transductor, y almacenarlas en los botones de play del lado derecho de la ventana gráfica. De esta manera, se puede acceder rápidamente a cada simulación.
    

Dentro de qtesis.py, se encuentra la realización de una interfaz gráfica para la interacción con el usuario. Dentro de la misma, se definen botones, sus íconos y acciones/métodos que ejecutan.

    - Los radio buttons están únicamente para obtener el string de datos sobre cuál fue seleccionado; de esta manera, se pretende enviar este string en un if para que se realice el procesamiento necesario (no está realizao todavía completamente, pero debería poder hacerse rápidamente)
    - Los botones de REC y PLAY graban y reproducen una señal de audio. Para este trabajo de tesis, se utiliza la librería SWHear, la cual permite detectar automáticamente qué driver de audio se está utilizando, e imprimir esa información al ejecutar el código.
    - El boton de PROCESAR que se explica anteriormente qué es lo que realiza.
    - Una barra de progreso que no está conectada a ningún método; si se puede realizar en un breve período de tiempo se dejará, sino no se utilizará.
    - Botones de play, y save para escuchar y guardar los archivos .wav de las simulaciones.
    - Boton de STOP, que no se pudo realizar y probablemente no se realice para este trabajo de tesis.
    
Si bien el código funciona y realiza la parte principal de manera eficiente, se entiende que podría realizarse de una manera más optimizada y eficaz. Entiendo que se pueden estar sobreescribiendo ciertos métodos o funciones; pero es mi primera aproximación con PyQt, y mi primera aplicación a una escala mayor en Python, con lo cual voy aprendiendo todo el tiempo como poder mejorarlo.

De todas maneras, el código puede grabar un archivo de audio, reproducirlo y además procesarlo, lo cuál considero que es lo central en este trabajo de tesis. Además se diseñó una ventana gráfica, que probablemente no sea algo central pero considero que facilita la interacción con la aplicación.

Faltan cargar las funciones de transferencia del resto de los transductores, pero están todas almacenadas en un código de MATLAB. Para la obtención de las mismas, se utilizó el método ARMAX de identificación de sistemas, aplicado a un sistema digital o simulado en LTSpice. Fue la manera más conveniente y menos complicada de obtener las funciones transferencia de manera aproximada de cada transductor. Una vez cargadas, se completará el algoritmo para cada transductor.


