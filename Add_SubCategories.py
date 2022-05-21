import requests,json

url = "http://localhost:8000/api/CreateSubCategories"

list_subCat = [
  [
    'Acc. para Carros y Camionetas',"Acc. para Motos y Cuatrimotos","Accesorios Náuticos",'Accesorios para Camiones',
    'Audio para Vehículos','GNV','Herramientas','Limpieza de Vehículos','Llantas','Motos','Navegadores GPS para Vehículos',
    'Performance','Repuestos Carros y Camionetas','Repuestos de Línea Pesada','Repuestos Motos y Cuatrimotos','Repuestos Náuticos',
    'Rines','Seguridad Vehicular','Service Programado','Tuning','Otros'
  ],
  [
    'Animales','Generadores de Energía','Infraestructura Rural','Insumos Agrícolas','Insumos Ganaderos','Máquinas y Herramientas','Repuestos Maquinaria Agrícola','Otros'
  ],
  [
    'Almacén','Bebidas','Comida Preparada','Congelados','Frescos','Kéfir','Otros'
  ],
  [
    'Aves','Caballos','Conejos','Gatos','Insectos','Peces','Perros','Reptiles y Anfibios','Roedores','Otros'
  ],
  [
    'Antigüedades','Banderas','Billetes y Monedas','Coleccionables de Deportes','Esculturas','Filatelia','Militaría y Afines','Posters','Otros'
  ],
  [
    'Arte y Manualidades','Espejos Mosaicos','Mercería','Papelería','Otros'
  ],
  [
    'Artículos de Bebés para Baños','Artículos de Maternidad','Caminadores y Correpasillos','Chupetes y Mordedores','Comida para Bebés','Corrales para Bebé','Cuarto del Bebé',
  'Higiene y Cuidado del Bebé','Juegos y Juguetes para Bebés','Lactancia y Alimentación','Paseo del Bebé','Ropa para Bebés','Salud del Bebé','Seguridad para Bebés',
  'Otros'
  ],
  [
    'Artefactos para el Cabello','Artículos de Peluquería','Barbería','Cuidado de la Piel','Cuidado del Cabello','Depilación','Farmacia','Higiene Personal',
    'Manicure y Pedicure','Maquillaje','Perfumes y Fragancias','Tratamientos de Belleza','Otros'
  ],
  [
    'Accesorios para Celulares','Celulares y Smartphones','Gafas de Realidad Virtual','Radios y Handies','Repuestos de Celulares','Smartwatches y Accesorios',
    'Tarificadores y Cabinas','Telefonía Fija e Inalámbrica','Telefonía IP','Otros'
  ],
  [
    'Accesorios de Antiestática','Accesorios para PC Gaming','Almacenamiento','Cables y Hubs USB','Componentes de PC','Conectividad y Redes','Estabilizadores y UPS',
    'Impresión','Lectores y Scanners','Limpieza y Cuidado de PCs','Monitores y Accesorios','Palms, Agendas y Accesorios','PC de Escritorio','Periféricos de PC',
    'Portátiles y Accesorios','Software','Tablets y Accesorios','Video Beams y Pantallas','Otros'
  ],
  [
    'Accesorios para Consolas','Accesorios para PC Gaming','Consolas','Pinballs y Máquinas de Juego','Repuestos para Consolas','Videojuegos','Otros'
  ],
  [
    'Aberturas, Puertas y Ventanas','Accesorios de Construcción','Baños y Sanitarios','Electricidad','Maquinarias para Construcción','Materiales de Obra','Mobiliario para Cocinas',
    'Pinturería','Pisos y Recubrimientos','Plomería','Otros'
  ],
  [
    'Bádminton','Baloncesto','Balonmano','Boxeo y Artes Marciales','Buceo','Camping, Caza y Pesca','Canoas, Kayaks e Inflables','Ciclismo','Equitación y Polo','Esgrima',
    'Esqui y Snowboard','Fitness y Musculación','Fútbol','Fútbol Americano','Golf','Hockey','Juegos de Salón','Kitesurf','Monopatines y Scooters','Montañismo y Trekking',
    'Natación','Paintball','Parapente','Patín y Skateboard','Pulsómetros y Cronómetros','Ropa Deportiva','Rugby','Slackline','Softball y Beisbol','Suplementos y Shakers',
    'Surf y Bodyboard','Tenis','Tenis, Padel y Squash','Tiro Deportivo','Voleibol','Wakeboard y Esqui Acuático','Windsurf','Yoga y Pilates','Otros'
  ],
  [
    'Artefactos de Cuidado Personal','Climatización','Cocción','Dispensadores y Purificadores','Lavado','Pequeños Electrodomésticos','Refrigeración','Otros'
  ],
  [
    'Accesorios Audio y Video','Accesorios para TV','Audio','Cables','Componentes Electrónicos','Controles Remotos','Drones y Accesorios','Fundas y Bolsos',
    'Media Streaming','Pilas y Cargadores','Repuestos TV','Televisores','Video','Video Beams y Pantallas','Otros'
  ],
  [
    'Accesorios para Herramientas','Cajas y Organizadores','Herramientas Eléctricas','Herramientas Industriales','Herramientas Manuales','Herramientas Neumáticas',
    'Herramientas para Jardín','Instrumentos de Medición','Otros'
  ],
  [
    'Adornos y Decoración del Hogar','Baños','Camas, Colchones y Accesorios','Cocina','Cuidado del Hogar y Lavandería','Iluminación para el Hogar','Jardin y Aire Libre',
    'Muebles para el Hogar','Organización para el Hogar','Seguridad para el Hogar','Textiles de Hogar y Decoración','Otros'
  ],
  [
    'Arquitectura y Diseño','Embalaje y Logística','Equipamiento Médico','Equipamiento para Comercios','Equipamiento para Oficinas','Gastronomía y Hotelería','Gráfica e Impresión',
    'Herramientas Industriales','Publicidad y Promoción','Seguridad Laboral','Textil y Calzado','Uniformes y Ropa de Trabajo','Otros'
  ],
  [
    'Apartamentos','Bodegas','Casas','Consultorio','Edificios','Fincas','Habitaciones','Haciendas','Hoteles y Resorts','Locales','Negocios','Oficinas',
    'Parcelas de Cementerio','Terrenos y Lotes','Otros Inmuebles'
  ],
  [
    'Baterías y Percusión','Equipos de DJ y Accesorios','Estudio de Grabación','Instrumentos de Cuerdas','Instrumentos de Viento','Metrónomos','Micrófonos y Amplificadores',
    'Parlantes','Partituras y Letras','Pedales y Accesorios','Teclados y Pianos','Otros'
  ],
  [
    'Arte y Manualidades'
  ],
  [
    'Accesorios para Cosplay','Artículos para Fiestas','Decoración para Fiestas','Desechables para Fiestas','Disfraces','Espuma, Serpentina y Confeti','Kits Imprimibles para Fiestas',
    'Props para Photo Booths','Recuerdos','Tarjetas de Invitación','Otros'
  ],
  [
    'Abrigos','Accesorios de Moda','Bermudas y Pantalonetas','Blusas','Calzado','Camisas','Camisetas','Enterizos','Equipaje, Bolsos y Carteras','Faldas','Indumentaria Laboral y Escolar',
    'Kimonos','Leggings','Pantalones y Jeans','Ropa Deportiva','Ropa Interior y de Dormir','Ropa para Bebés','Ropa por Mayor','Trajes','Vestidos','Vestidos de Baño','Otros'
  ],
  [
    'Cuidado de la Salud','Equipamiento Médico','Masajes','Movilidad','Ortopedia','Suplementos Alimenticios','Terapias Alternativas','Otros'
  ],
  [
    'Belleza e Higiene Personal','Cursos y Clases','Fiestas y Eventos','Hogar','Mantenimiento de Vehículos','Medicina y Salud','Profesionales','Reparaciones e Instalaciones',
    'Ropa e Indumentaria','Servicios para Mascotas','Transporte','Viajes y Turismo','Otros'
  ],
  [
    'Ácido Clorhídrico','Adultos','Artículos para Fumadores','Coberturas Extendidas','Criptomonedas','Esoterismo','Giftcards','Hornos Crematorios','Insumos para Tatuajes',
    'Kits de Criminalística','Licencias para Taxis','Mangas de Viento','Otros'
  ]



]


for i in range(len(list_subCat)):
  for j in list_subCat[i]:
    value = i + 1
    payload = json.dumps({
      "name": str(j),
      "id_category": str(value)
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)





