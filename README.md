Agents and Networks Model in Python
==============================

[![](https://img.youtube.com/vi/zIRMNPTBESc/0.jpg)](https://www.youtube.com/watch?v=zIRMNPTBESc)

## Summary

This is an implementation of the [GMU-Social Model](https://github.com/abmgis/abmgis/blob/master/Chapter08-Networks/Models/GMU-Social/README.md) in Python, using [Mesa](https://github.com/projectmesa/mesa) and [Mesa-Geo](https://github.com/Corvince/mesa-geo).

In this model, buildings are randomly assigned to agents as their home and work places, and the buildings' nearest road vertices are used as their entrances. Agents' commute routes can be found as the shortest path between entrances of their home and work places. These commute routes are segmented according to agents' walking speed. In this way, the movements of agents are constrained on the road network.

### GeoSpace

The GeoSpace contains multiple vector layers, including buildings, lakes, and a road network. More specifically, the road network is constructed from the polyline data and implemented by two underlying data structures: a topological network and a k-d tree. First, by treating road vertices as nodes and line segments as links, a topological network is created using the NetworkX and momepy libraries. NetworkX also provides several methods for shortest path computations (e.g., Dijkstra, A-star). Second, a k-d tree is built for all road vertices through the Scikit-learn library for the purpose of nearest vertex searches.

### GeoAgent

The commuters are the GeoAgents.

## How to run

### Paso 1: Preparación

Si usas Windows, te recomiendo instalar el [Windows Subsystem for Linux](https://docs.microsoft.com/es-es/windows/wsl/install-win10). Puede ser la versión 1 o 2 (recomiendo WSL2). Como distribución te recomiendo Ubuntu 22.04 (es la que uso yo). 

Abre la consola (_shell_) de Ubuntu y ejecuta el siguiente comando:

```sh
sudo apt install make libxcursor1 libgdk-pixbuf2.0-dev libxdamage-dev osmctools gcc
```

Esto instalará algunas bibliotecas que son necesarias para el funcionamiento de `aves` (particularmente de `graph-tool` que es usada por aves).

Además, para administrar el entorno de ejecución de aves necesitas una instalación de `conda` ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) es una buena alternativa) y de `mamba`. Primero debes instalar `conda`, y una vez que la tengas, puedes ejecutar:

```sh
conda install mamba
```

¿Por qué `mamba`? Es una versión más eficiente de `conda`. ¡Te ahorrará muchos minutos de instalación!


### Paso 2: Creación del Entorno

Después de descargar o clonar el repositorio (utilizando el comando `git clone`), debes instalar el entorno de `conda` con los siguientes comandos:

```sh
make conda-create-env
make install-package
```

Ello creará un entorno llamado `zorzim` que puedes utilizar a través del comando `conda activate zorzim`.

```sh
conda activate zorzim
```

Luego, puedes ejecutar la simulación con:

```bash
python scripts/run.py --campus ub
```

Reemplaza `ub` a `gmu` para ver un campus distinto.

Abre [http://127.0.0.1:8521/](http://127.0.0.1:8521/) en tu navegador y haz click en `Start`.

### Paso 3: Ejecución en Jupyter

El principal modo de uso de aves es a través de los notebooks de Jupyter.

Es posible que ya tengas un entorno de `conda` en el que ejecutes Jupyter. En ese caso, puedes agregar el entorno de `aves` como _kernel_ ejecutando este comando desde el entorno que contiene Jupyter:

```sh
make install-kernel
```

Así quedará habilitado acceder al entorno de aves desde Jupyter.


## Actualización de Dependencias

Para añadir o actualizar dependencias:

1. Agrega el nombre (y la versión si es necesaria) a la lista en `environment.yml`.
2. Ejecuta `conda env update --name aves --file environment.yml  --prune`.
3. Actualiza el archivo `environment.lock.yml` ejecutando `conda env export > environment.lock.yml`.
