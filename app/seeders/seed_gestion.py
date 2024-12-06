from app.models.gestion import Gestion
from app.models.periodo import Periodo
from app import db

gestiones_data = [
    {"id": 1, "gestion": "2020"},
    {"id": 2, "gestion": "2021"},
    {"id": 3, "gestion": "2022"},
    {"id": 4, "gestion": "2023"},
    {"id": 5, "gestion": "2024"},
]


def seed_gestion():
    # Crear gestiones
    gestiones = []
    for gestion in gestiones_data:
        gestiones.append(Gestion(
            id=gestion["id"],
            gestion=gestion["gestion"],
        ))

    db.session.add_all(gestiones)
    db.session.commit()

    print("Datos de prueba de la tabla Gestion agregados correctamente.")


def seed_periodos():
    # Crear períodos para cada gestión
    # gestiones = {
    #     1: '2021',
    #     2: '2022',
    #     3: '2023',
    #     4: '2024'
    # }

    for gestion in gestiones_data:
        periodos = [
            Periodo(nombre=f'1er Bimestre {gestion["gestion"]}', fecha_inicio=f'{gestion["gestion"]}-01-01',
                    fecha_fin=f'{gestion["gestion"]}-03-31', gestion_id=gestion["id"]),
            Periodo(nombre=f'2do Bimestre {gestion["gestion"]}', fecha_inicio=f'{gestion["gestion"]}-04-01',
                    fecha_fin=f'{gestion["gestion"]}-06-30', gestion_id=gestion["id"]),
            Periodo(nombre=f'3er Bimestre {gestion["gestion"]}', fecha_inicio=f'{gestion["gestion"]}-07-01',
                    fecha_fin=f'{gestion["gestion"]}-09-30', gestion_id=gestion["id"]),
            Periodo(nombre=f'4to Bimestre {gestion["gestion"]}', fecha_inicio=f'{gestion["gestion"]}-10-01',
                    fecha_fin=f'{gestion["gestion"]}-12-31', gestion_id=gestion["id"])
        ]

        # Agregar los períodos de la gestión actual
        db.session.add_all(periodos)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    print("Datos de prueba de la tabla Periodo agregados correctamente.")
