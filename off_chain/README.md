poetry add pandas  # Instala Pandas
poetry add numpy   # Instala Numpy
poetry show


Crear el nuevo módulo - Git Bash o PowerShell
mkdir -p src/my_new_package

Crear el nuevo archivo - Git Bash o PowerShell
touch src/my_new_package/__init__.py
touch src/my_new_package/module.py
touch .gitignore


#poetry 
poetry --version
#--step 0
#configura poetry
poetry init

#--step 1: Verifica si el entorno virtual de Poetry está activado
#Poetry maneja su propio entorno virtual separado
poetry env info
#--step 2: Habilitar la Creación de Entorno Virtual en Poetry
#Esto obliga a Poetry a crear un entorno virtual en lugar de usar el Python global.
poetry config virtualenvs.create true
#--step 3: Crear/Reconfigurar el Entorno Virtual
#Si sigue sin detectar un entorno virtual, puedes forzar a Poetry a crear uno con:
poetry env use python
#--step 4: Instalar las Dependencias
#Esto instalará todas las dependencias de pyproject.toml y activará el entorno virtual correcto
#Instala todas las dependencias asegurando que coincidan con pyproject.toml
poetry install


###### Eliminar y Regenerar el Entorno Virtual de Poetry
#....Elimina el entorno virtual actual de Poetry.
#Eliminar entornos virtuales
poetry env remove python

#....Limpia cualquier caché que esté causando conflictos.
#Limpiar caché
poetry cache clear pypi --all

#....Instala dependencias sin empaquetar off_chain/.
#instala dependencias sin empaquetar los módulos
poetry install --no-root

###### Verificar la Configuración
#....Para comprobar si ahora Poetry reconoce la configuración correctamente, ejecuta:
poetry check

###### Solución: Regenerar poetry.lock
#Regenera el poetry.lock sin cambiar versiones de dependencias
poetry lock --no-update
poetry lock



###### ejecutar clases

python off_chain/tests/test_connection.py

python -m off_chain.tests.test_settings

#Cómo Ejecutar Scripts con Poetry
#Para ejecutar scripts usando las dependencias del entorno virtual de Poetry, usa poetry run
poetry run python off_chain/tests/test_settings.py




