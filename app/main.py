# Python


# SqlAlchemy
from typing import List
from sqlalchemy.orm import Session

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi.param_functions import Path

# Modelos locales
from . import database, models, schemas

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()

# Models

@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    summary='Home',
    tags=['Home']
)
def home():
    """
    Pagina de inicio

    Muestra un calido saludo de bienvenida

    Parametros:
        - Request body parameter:

    Retorna un JSON con el saludo del programador
    """
    return {
        'Hello':'World'
    }

## Dogs

### Obtener listado
@app.get(
    path='/api/dogs',
    tags=['Dogs']
)
def api_dogs(db:Session=Depends(get_db)):
    """
    Obtener Listado
    
    Muestra los perros que han sido registrados en la DB

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna un JSON con los datos ingresados en la base de datos como:
        - ID: int
        - name: String
        - Picture: String
        - is_adopted: Boolean
        - Created_date: Datetime
    """
    registration = db.query(models.Dogs).all()
    return registration


### Obtener todo el listado de perros adoptados
@app.get(
    path='/api/dogs/is_adopted',
    tags=['Dogs']
)
def api_dogs_is_adopted(db:Session=Depends(get_db)):
    """
    Obtener Listado
    
    Muestra los perros que han sido adoptados

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna un JSON con los datos de cada uno de los perros adoptados
    """
    registration = db.query(models.Dogs).filter(models.Dogs.is_adopted == True).all()
    return registration


### Obtener la información de un perro
@app.get(
    path='/api/dogs/{name}',
    response_model=schemas.Dogs,
    tags=['Dogs']
)
def api_dogs_information(name: str, db: Session = Depends(get_db)):
    """
    Obtener una entrada apartir del nombre
    
    Muestra el perro registrado con dicho nombre, en caso de no encontrarse ese nombre se devolvera una excepción

    Parametros:
        - Request body parameter
            - name: str
            - Valores de la DB

    Retorna un JSON con los datos del perro seleccionado
    """
    db_dog = db.query(models.Dogs).filter(models.Dogs.name == name).first()
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    return db_dog


### Crear nuevo registro
@app.post(
    path='/api/dogs/created',
    tags=['Dogs']
)
def api_dogs_create(
    dogs: schemas.DogsBase,
    db: Session = Depends(get_db)
):
    """
    Guardar un registro
    
    Nuevo registro de un perro en la BD

    Parametros:
        - Request body parameter
            - dogs: Datos DogsBase
            - Valores de la DB

    Retorna la solicitud realizada a la BD
    """
    verification = db.query(models.Dogs).filter(models.Dogs.name == dogs.name).first()
    if verification:
        raise HTTPException(status_code=400, detail="Este perro ya se encuentra registrado")
    register = models.Dogs(
        name = dogs.name,
        picture = dogs.picture,
        is_adopted = dogs.is_adopted,
        create_date = dogs.create_date,
        id_user = dogs.id_user
    )
    db.add(register)
    db.commit()
    db.refresh(register)
    return register


### Actualizar un registro
@app.put(
    path='/api/dogs/{name}',
    response_model=schemas.Dogs,
    tags=['Dogs']
)
def api_dogs_update(
    name: str,
    dogs:schemas.DogsUpdate,
    db:Session=Depends(get_db)
):
    """
    Actualizar un registro según el nombre
    
    Actualizar los datos de un perro seleccionado atravez de su nombre

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna la solicitud de los cambios realizados
    """
    update = db.query(models.Dogs).filter(models.Dogs.name == name).first()
    if update is None:
        raise HTTPException(status_code=400, detail="No se ha encontrado registro del perro ingresado")
    update.picture = dogs.picture
    update.is_adopted = dogs.is_adopted
    update.create_date = dogs.create_date
    update.id_user = dogs.id_user
    db.commit()
    db.refresh(update)
    return update


### Eliminar un registro
@app.delete(
    path='/api/dogs/{name}',
    response_model=schemas.Respuesta,
    tags=['Dogs']
)
def api_dogs_delete(
    name: str,
    db:Session=Depends(get_db)
):
    """
    Borrar un registro según el nombre
    
    Eliminar un registro de un canino registrado anteriormente

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna la solicitud de la eliminación
    """
    delete_dog = db.query(models.Dogs).filter(models.Dogs.name == name).first()
    if delete_dog is None:
        raise HTTPException(status_code=400, detail="No se ha encontrado registro del perro ingresado")
    db.delete(delete_dog)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminación exitosa")
    return respuesta

## Users

### Crear Usuario
@app.post(
    path='/api/user/create',
    tags=['Users']
)
def api_user_create(
    users: schemas.UserBase,
    db: Session = Depends(get_db)
):
    """
    Crear usuario
    
    Crear un usuario apartir de cirta información, el manejo de uno a muchos se maneja directamente desde dog

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna un JSON con los datos ingresados en la base de datos como:
        - name = str,
        - last_name = str,
        - email = str,
    """

    register = models.User(
        name = users.name,
        last_name = users.last_name,
        email = users.email,
    )
    db.add(register)
    db.commit()
    db.refresh(register)
    return register


### Leer usuarios
@app.get(
    path='/api/users',
    response_model=List[schemas.User],
    tags=['Users']
)
def api_user_read(db:Session=Depends(get_db)):
    """
    Obtener Listado
    
    Mostrar listado de los usuarios registrados en la BD

    Parametros:
        - Request body parameter
            - Valores de la DB

    Retorna un archivo JSON con los usuarios registrados mostrando los siguientes datos
        - id
        - name
        - last_name
        - email
        - dogs
    """
    registration = db.query(models.User).all()
    return registration


### Leer un usuario
@app.get(
    path='/api/user/{id}',
    response_model=schemas.User,
    tags=['Users']
)
def api_user_a_read(id: int, db: Session = Depends(get_db)):
    """
    Obtener Listado
    
    Mostrar un usuario 

    Parametros:
        - Request body parameter
            - Valores de la DB
            - ID

    Retorna un archivo JSON con el usuario registrado con el ID ingresado, mostrando los siguientes datos
        - id
        - name
        - last_name
        - email
        - dogs
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_user

    
### Actualizar Usuario
@app.put(
    path='/api/user/update/{id}',
    response_model=schemas.User,
    tags=['Users']
)
def api_user_update(
    id: int,
    users: schemas.UserUpdate,
    db:Session=Depends(get_db)
):
    """
    Actualizar Usuario
    
    Actualizar los datos ingresados de un usuario

    Parametros:
        - Request body parameter
            - Valores de la DB
            - ID

    Retorna el valor de la nueva informacion de la DB
    """
    update = db.query(models.User).filter(models.User.id == id).first()
    if update is None:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    update.name = users.name
    update.last_name = users.last_name
    update.email = users.email
    db.commit()
    db.refresh(update)
    return update


### Eliminar usuario
@app.delete(
    path='/api/user/delete/{id}',
    response_model=schemas.Respuesta,
    tags=['Users']
)
def api_user_delete(
    id: int,
    db:Session=Depends(get_db)
):
    """
    Eliminar Usuario
    
    Eliminar un usuario creado anteriormente

    Parametros:
        - Request body parameter
            - ID

    Retorna mensaje de aprobación de la solicitud enviada
    """
    delete_user = db.query(models.Dogs).filter(models.User.id == id).first()
    if delete_user is None:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    db.delete(delete_user)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminación exitosa")
    return respuesta