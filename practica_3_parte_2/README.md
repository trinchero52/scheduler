# Práctica 3

## Nos ordenamos

En primer lugar nos vamos a encontrar con que el código en este TP difiere un poco del que veníamos trabajando. Vamos a encontrar que los archivos se transformaron en carpetas, y ahora hay un archivo para cada clase (casi), además de modificar un poquito la forma en la que programamos algunas cosas para ser más prolijos.

Como las veces anteriores, partimos del mismo lugar en donde estabamos, al final de la práctica 2.

## MMU

También vamos a encontrar en el hardware un nuevo componente, la MMU,que se va a encargar de acceder a la memoria. En principio el componente tiene un modelo de acceso directo a la memoria, pero pronto lo deberemos extender con memoria virtual.

## Paginación con bloques de tamaño estático

Contando con el MMU, podemos empezar a pensar en gestionar la memoria de forma un poco más interesante, y necesitamos entonces poder paginarla, como vimos en la teoría.

Vamos a cargar los programas en una memoria paginada, liberar páginas, y todo realizando diversas estrategias.

## Lo que tenemos que hacer es:

- **1:** Primero, entender la nueva organización del código, donde estamos parados, ver como funcionan los programas nuevos y cómo se cargan los programas con el MMU como intermediario. Notar que el main solo carga programas, sin ejecutarlos.

- **2:** Vamos a crear un nuevo componente **MemoryManager** que será el encargado de administrar la memoria en términos del sistema operativo. El sistema operativo no va a acceder a la memoria de ninguna forma por fuera de este componente. A este componente le vamos a pedir que pueda:

  - Cargar un proceso completo en memoria.
  - Liberar la memoria asociada a un proceso.
  - Darnos la información que hay en una determinada posición de memoria.

- **3:** Ahora el **MMU** debe entender la idea de página y va a tener un tamaño de página (digamos que por defecto son 4 lugares de memoria). El **MemoryManager** tiene que poder cargar un programa en varias páginas de tamaño fijo, para poder tener programas en espacios no contiguos, aunque por ahora no los tengamos. El **MMU** deberá recordar las páginas asignadas, y las posiciones de memoria asociadas, de forma que ahora leer y escribir en la memoria implica dos argumentos, la página y la dirección relativa a la misma. Hagamos que el **MMU** pueda en principio decirnos la dirección fisica asociada a una página y su offset.
