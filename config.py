# config.py

# Colores de la app
PRIMARY_BLUE = "#355C9A"
ACCENT_YELLOW = "#FADD7F"
WHITE = "#FFFFFF"

# CATEGORÍAS (cámbialas aquí por nombres reales)
CATEGORIES = [
    "El(la) más colaborador(a)",
    "El(la) más comunicativo(a) ",
    "El(la) más guapo(a)",
    "El(la) que siempre tiene hambre",
    "El(la) que le pone más optimismo a cada situación",
    "El(la) que llega tarde a todo",
    "El(la) más sexy",
    "El(la) más buena vibra",
]

CATEGORY_DESCRIPTIONS = [
    "Siempre está listo(a) para ayudar… incluso sin que se lo pidan.",
    "Habla mucho, a veces más de la cuenta, pero siempre se hace entender. Si no sabes lo último, allí tienes la fuente",
    "No solo vino a trabajar… también vino a imponer presencia.",
    "Acaba de comer… y ya está pensando en la siguiente.",
    "Puede estar todo en llamas… y aún así sonríe.",
    "Llega tarde, pero llega con estilo.",
    "No lo intenta… simplemente pasa y lo confirma.",
    "La energía que necesitas cuando el día va cuesta arriba.",
]

# CANDIDATOS (cámbialos aquí por nombres reales)
CANDIDATES = [
     "Alejandro Urbina",
     "Carolina Sánchez",
     "Danilo Quintero",
     "Diana Ruiz",
     "Duvan Bacca",
     "Gibson Rodríguez",
     "Harold Rueda",
     "Kevin Toro",
     "Kevin Vergel",
     "Lorena Grimaldo",
     "Mayra Gutiérrez",
     "Mónica Monsalve",
     "Nicol López",
     "Oscar Bayona",
     "Ricardo Alvear",
     "Sarhid Sarmiento",
     "Sebastian Bermón",
     "Stella Salinas",
]

# USUARIOS DE AUTENTICACIÓN (20 usuarios normales)
USERS = [
    {"username": "usuario1", "password": "Rasi_165"},
    {"username": "usuario2", "password": "Rasi_927"},
    {"username": "usuario3", "password": "Rasi_304"},
    {"username": "usuario4", "password": "Rasi_479"},
    {"username": "usuario5", "password": "Rasi_123"},
    {"username": "usuario6", "password": "Rasi_644"},
    {"username": "usuario7", "password": "Rasi_219"},
    {"username": "usuario8", "password": "Rasi_891"},
    {"username": "usuario9", "password": "Rasi_708"},
    {"username": "usuario10", "password": "Rasi_038"},
    {"username": "usuario11", "password": "Rasi_909"},
    {"username": "usuario12", "password": "Rasi_806"},
    {"username": "usuario13", "password": "Rasi_893"},
    {"username": "usuario14", "password": "Rasi_766"},
    {"username": "usuario15", "password": "Rasi_620"},
    {"username": "usuario16", "password": "Rasi_913"},
    {"username": "usuario17", "password": "Rasi_285"},
    {"username": "usuario18", "password": "Rasi_399"},
    {"username": "usuario19", "password": "Rasi_432"},
    {"username": "usuario20", "password": "Rasi_525"},
    {"username": "usuario21", "password": "Rasi_583"},
]

# USUARIO ADMIN PARA VER RESULTADOS DETALLADOS
ADMIN_USER = {
    "username": "admin",
    "password": "Ras!Leg3nd/.$26",  # contraseña más segura
}

# Cada usuario puede enviar su voto completo máximo 2 veces
# (voto inicial + 1 vez para cambiarlo)
MAX_SUBMISSIONS_PER_USER = 2

# Archivos de datos (JSON plano)
USERS_FILE = "users.json"
VOTES_FILE = "votes.json"

VOTING_OPEN = False  # True = se puede votar / False = votación cerrada

