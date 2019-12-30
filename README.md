
     _______  _______  _______  ___      ___   _  _______  ______
    |       ||       ||   _   ||   |    |   | | ||       ||    _ |
    |  _____||_     _||  |_|  ||   |    |   |_| ||    ___||   | ||
    | |_____   |   |  |       ||   |    |      _||   |___ |   |_||_
    |_____  |  |   |  |       ||   |___ |     |_ |    ___||    __  |
     _____| |  |   |  |   _   ||       ||    _  ||   |___ |   |  | |
    |_______|  |___|  |__| |__||_______||___| |_||_______||___|  |_|                                                  


# stalker

software de captura de  datos, para investigación en el doctorado en educación en ciencia y tecnología.

## introducción

STALKER es un pequeño IDE (Integrated development environment) diseñado para enseñar el lenguaje python, y como herramienta de recolección de datos para el trabajo de campo que estoy haciendo en el **doctorado en educación en ciencia y tecnología** (FAMAF - UNC).

Este programa esta diseñado para capturar todas las interacciones de teclado que un usuario haga dentro del entorno (digamos que es básicamente un Keylogger). STALKER genera un archivo .py con el proyecto que los estudiantes ejecuten y un .csv (Comma Separated Values) con cada tecla presionada por el usuario (incluyendo teclas especiales como SUPR , CTRL, LSHIFT, de forma que podemos obtener no solo el archivo final del trabajo del estudiante, sino las auto correcciones que estos van escribiendo a medida que aprenden a programar.
Podemos hablar de 3 etapas de análisis sobre un proyecto de software, en primer lugar tenemos el código fuente final, lo que el alumno nos muestra como resultado de su trabajo. En segundo lugar algunos sistemas (mediante GIT por ejemplo) permiten analizar cada vez que el usuario ejecuta su programa, y usa la técnica de prueba-error. Sin embargo, estas dos etapas no nos dejan ver una tercera posibilidad de análisis, donde veremos cuales son los puntos donde el estudiante corrigió su propio código antes de ejecutarlo, y así analizar su razonamiento.
STALKER ademas, captura un video con el micrófono de la computadora y el escritorio, permitiendo ver todo el proceso que los estudiantes van haciendo y comentando mientras trabajan

## ADVERTENCIAS

STALKER **no es un software para uso corriente**, ni para trabajar en el aula, es ** una herramienta de laboratorio** diseñada para investigación en un espacio regulado y controlado, donde los participantes saben todo el tiempo que la computadora esta grabando la sesión de trabajo y sus voces.
La idea es poder tener datos para una análisis de enfoque imperativo cualitativo, donde mediante entrevistas de auto confrontación y análisis de código fuente (mediante STALKER) poder estudiar las posibilidades de una didáctica de la programación.




