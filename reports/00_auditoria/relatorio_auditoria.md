# Relatório de Auditoria de Qualidade - Hackathon Seazone

> **Modo:** READ-ONLY | **Data:** gerado por `analysis/audit.py` | **Sem JOIN, sem receita, sem recomendação**
> **Decisões:** nulo = "" ou espaços | placeholder <NA>/não informado separado | 0/0.0 mantido e sinalizado

## Resumo Executivo

- **Details_Itapema.csv**: 4441 linhas de dados, 35 colunas, 0 linhas 100% duplicadas
- **Hosts_ids_Itapema.csv**: 4440 linhas de dados, 11 colunas, 0 linhas 100% duplicadas
- **Mesh_Ids_Data_Itapema.csv**: 4441 linhas de dados, 8 colunas, 0 linhas 100% duplicadas
- **Price_AV_Itapema.csv**: 118839 linhas de dados, 4 colunas, 0 linhas 100% duplicadas
- **VivaReal_Itapema.csv**: 8329 linhas de dados, 22 colunas, 35 linhas 100% duplicadas

**Compatibilidade de chaves (recomputada):**
- `Details vs Mesh` (`airbnb_listing_id`): interseção 4441 | só Details 0 | só Mesh 0 | 100% compatível
- `Details vs Price` (`airbnb_listing_id`): interseção 999 | só Details 3442 | só Price 6 | Cobertura parcial: 999/4441 (22.5%) de Details têm preço; 6 ids em Price não existem em Details
- `Mesh vs Price` (`airbnb_listing_id`): interseção 999 | só Mesh 3442 | só Price 6 | 999 em comum; 6 em Price sem Mesh
- `Details vs Hosts` (`owner_id`): Details distintos 3057 | Hosts distintos 3057 | interseção 3057 | só Details 0 | só Hosts 0 | Verificar 1 a 1

---
## ARQUIVO: `Details_Itapema.csv`

* **Linhas (dados, sem header, via csv):** 4441
* **Colunas:** 35
* **Colunas listadas:** `airbnb_listing_id`, `url`, `ad_name`, `ad_description`, `space`, `house_rules`, `amenities`, `safety_features`, `number_of_bathrooms`, `number_of_bedrooms`, `number_of_beds`, `latitude`, `longitude`, `check_in`, `check_out`, `number_of_guests`, `number_of_reviews`, `cleaning_fee`, `owner_id`, `aquisition_date`, `star_rating`, `picture_count`, `min_nights`, `guest_satisfaction_overall`, `listing_type`, `can_instant_book`, `is_professional`, `accuracy_rating`, `checkin_rating`, `cleanliness_rating`, `communication_rating`, `location_rating`, `value_rating`, `is_new_listing`, `is_guest_favorite`
* **Linhas 100% duplicadas:** 0

### Tipos inferidos
- `airbnb_listing_id`: numérico (inteiro)
- `url`: string/categórico
- `ad_name`: string/categórico
- `ad_description`: string/categórico
- `space`: string/categórico
- `house_rules`: string/categórico
- `amenities`: string/categórico
- `safety_features`: string/categórico
- `number_of_bathrooms`: numérico (inteiro)
- `number_of_bedrooms`: numérico (inteiro)
- `number_of_beds`: numérico (inteiro)
- `latitude`: numérico (inteiro)
- `longitude`: numérico (inteiro)
- `check_in`: string/categórico
- `check_out`: string/categórico
- `number_of_guests`: numérico (inteiro)
- `number_of_reviews`: numérico (inteiro)
- `cleaning_fee`: numérico (inteiro)
- `owner_id`: numérico (inteiro)
- `aquisition_date`: data/datetime (string)
- `star_rating`: numérico (float)
- `picture_count`: numérico (inteiro)
- `min_nights`: numérico (inteiro)
- `guest_satisfaction_overall`: numérico (inteiro)
- `listing_type`: string/categórico
- `can_instant_book`: booleano (string)
- `is_professional`: booleano (string)
- `accuracy_rating`: numérico (float)
- `checkin_rating`: numérico (float)
- `cleanliness_rating`: numérico (float)
- `communication_rating`: numérico (float)
- `location_rating`: numérico (float)
- `value_rating`: numérico (float)
- `is_new_listing`: booleano (string)
- `is_guest_favorite`: booleano (string)

### Nulos ("" ou espaços) e Placeholders (<NA>/não informado) por coluna

| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |
|---|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `url` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `ad_name` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `ad_description` | 54 | 1.22% | 0 | 0.00% | 54 | 1.22% | 0 | 0.00% |
| `space` | 2527 | 56.90% | 0 | 0.00% | 2527 | 56.90% | 0 | 0.00% |
| `house_rules` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `amenities` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `safety_features` | 0 | 0.00% | 3137 | 70.64% | 0 | 0.00% | 0 | 0.00% |
| `number_of_bathrooms` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 65 | 1.46% |
| `number_of_bedrooms` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 56 | 1.26% |
| `number_of_beds` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 64 | 1.44% |
| `latitude` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 4441 | 100.00% |
| `longitude` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 4441 | 100.00% |
| `check_in` | 0 | 0.00% | 446 | 10.04% | 0 | 0.00% | 0 | 0.00% |
| `check_out` | 0 | 0.00% | 842 | 18.96% | 0 | 0.00% | 0 | 0.00% |
| `number_of_guests` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `number_of_reviews` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `cleaning_fee` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 939 | 21.14% |
| `owner_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `aquisition_date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `star_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `picture_count` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1729 | 38.93% |
| `min_nights` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 4441 | 100.00% |
| `guest_satisfaction_overall` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `listing_type` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `can_instant_book` | 0 | 0.00% | 355 | 7.99% | 0 | 0.00% | 0 | 0.00% |
| `is_professional` | 355 | 7.99% | 0 | 0.00% | 355 | 7.99% | 0 | 0.00% |
| `accuracy_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `checkin_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `cleanliness_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `communication_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `location_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `value_rating` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 1540 | 34.68% |
| `is_new_listing` | 874 | 19.68% | 0 | 0.00% | 874 | 19.68% | 0 | 0.00% |
| `is_guest_favorite` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

_*Vazios = mesma definição de nulos._

### IDs
- **`airbnb_listing_id`**: únicos `4441` / duplicados `0` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{19: 2129, 18: 944, 8: 1342, 6: 1, 7: 25}`
  - Exemplos: `['828307537051457546', '985445004274818605', '1048785577617228176']`
- **`owner_id`**: únicos `3057` / duplicados `1384` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{9: 3856, 8: 537, 7: 45, 6: 3}`
  - Exemplos: `['587657794', '446793136', '668234945']`

### Numéricas (min, max, mediana, média, qtd zero)

| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |
|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 4441 | 822704.0 | 1.3297872953081106e+18 | 9.8189445944595e+17 | 7.466437614346395e+17 | 0 | 0.0% |
| `number_of_bathrooms` | 4441 | 0.0 | 19.0 | 2.0 | 2.15 | 65 | 1.46% |
| `number_of_bedrooms` | 4441 | 0.0 | 16.0 | 3.0 | 2.51 | 56 | 1.26% |
| `number_of_beds` | 4441 | 0.0 | 50.0 | 3.0 | 3.44 | 64 | 1.44% |
| `latitude` | 4441 | 0.0 | 0.0 | 0.0 | 0.0 | 4441 | 100.0% |
| `longitude` | 4441 | 0.0 | 0.0 | 0.0 | 0.0 | 4441 | 100.0% |
| `number_of_guests` | 4441 | 1.0 | 16.0 | 6.0 | 6.64 | 0 | 0.0% |
| `number_of_reviews` | 4441 | 0.0 | 504.0 | 2.0 | 9.01 | 1540 | 34.68% |
| `cleaning_fee` | 4441 | 0.0 | 1200.0 | 250.0 | 210.43 | 939 | 21.14% |
| `owner_id` | 4441 | 614119.0 | 669723189.0 | 268455389.0 | 301997457.63 | 0 | 0.0% |
| `star_rating` | 4441 | 0.0 | 5.0 | 4.820000171661377 | 3.17 | 1540 | 34.68% |
| `picture_count` | 4441 | 0.0 | 195.0 | 12.0 | 13.91 | 1729 | 38.93% |
| `min_nights` | 4441 | 0.0 | 0.0 | 0.0 | 0.0 | 4441 | 100.0% |
| `guest_satisfaction_overall` | 4441 | 0.0 | 5.0 | 4.0 | 2.97 | 1540 | 34.68% |
| `accuracy_rating` | 4441 | 0.0 | 5.0 | 4.829999923706055 | 3.17 | 1540 | 34.68% |
| `checkin_rating` | 4441 | 0.0 | 5.0 | 4.929999828338623 | 3.21 | 1540 | 34.68% |
| `cleanliness_rating` | 4441 | 0.0 | 5.0 | 4.769999980926514 | 3.14 | 1540 | 34.68% |
| `communication_rating` | 4441 | 0.0 | 5.0 | 4.940000057220459 | 3.21 | 1540 | 34.68% |
| `location_rating` | 4441 | 0.0 | 5.0 | 4.860000133514404 | 3.18 | 1540 | 34.68% |
| `value_rating` | 4441 | 0.0 | 5.0 | 4.71999979019165 | 3.13 | 1540 | 34.68% |

### Categóricas (qtd categorias, top, inconsistentes)
- **`url`**: 4441 categorias (non-null 4441)
  - Top: `https://www.airbnb.com.br/rooms/1018938592594574382`:1, `https://www.airbnb.com.br/rooms/991407580891691701`:1, `https://www.airbnb.com.br/rooms/41074064`:1, `https://www.airbnb.com.br/rooms/54177663`:1, `https://www.airbnb.com.br/rooms/51975323`:1
  - Inconsistentes: Nenhum problema encontrado
- **`ad_name`**: 4209 categorias (non-null 4441)
  - Top: `Apartamento em Meia Praia`:25, `Apartamento em Itapema`:21, `Apartamento Meia Praia`:18, `Apartamento quadra mar`:10, `Apartamento em meia praia`:7
  - **Inconsistentes:** `{'apartamento em meia praia': ['Apartamento em meia praia', 'Apartamento em Meia Praia'], 'apartamento meia praia': ['Apartamento Meia Praia', 'Apartamento Meia praia', 'Apartamento meia praia'], 'apartamento com vista para o mar': ['Apartamento com vista para o mar', 'Apartamento com vista para o Mar'], 'apartamento aconchegante': ['Apartamento Aconchegante', 'Apartamento aconchegante'], 'apartamento pé na areia': ['Apartamento pé na Areia', 'Apartamento Pé na Areia', 'Apartamento Pé na areia', 'Apartamento pé na areia'], 'apartamento meia praia itapema': ['Apartamento meia praia Itapema', 'Apartamento Meia Praia Itapema', 'Apartamento meia praia itapema', 'apartamento meia praia itapema'], 'apartamento em itapema': ['Apartamento em Itapema', 'Apartamento em itapema'], 'apartamento 02 suítes - meia praia': ['Apartamento 02 suítes - Meia Praia', 'Apartamento 02 Suítes - Meia Praia'], 'apartamento em itapema-sc': ['Apartamento em Itapema-SC', 'apartamento em Itapema-SC'], 'apartamento': ['Apartamento', 'apartamento'], 'apartamento beira mar itapema': ['Apartamento Beira Mar Itapema', 'Apartamento beira mar itapema'], 'apartamento itapema': ['Apartamento itapema', 'Apartamento Itapema', 'apartamento itapema', 'apartamento Itapema'], 'apartamento novo 3 suítes': ['Apartamento novo 3 suítes', 'Apartamento novo 3 Suítes', 'Apartamento NOVO 3 suítes'], 'apartamento praia centro itapema': ['Apartamento praia centro itapema', 'Apartamento Praia Centro Itapema'], 'apartamento  meia praia': ['Apartamento  Meia Praia', 'Apartamento  meia praia'], 'apartamento itapema meia praia': ['Apartamento Itapema Meia Praia', 'Apartamento Itapema meia praia'], 'apartamento quadra mar': ['Apartamento quadra mar', 'Apartamento Quadra Mar', 'apartamento quadra mar'], 'apartamento na meia praia': ['Apartamento na Meia Praia', 'Apartamento na meia praia', 'Apartamento na Meia praia'], 'apartamento em meia praia itapema': ['Apartamento em Meia Praia Itapema', 'Apartamento em meia praia itapema', 'Apartamento em Meia praia Itapema'], 'apartamento em meia praia - itapema': ['Apartamento em Meia Praia - Itapema', 'Apartamento em meia praia - Itapema'], 'lindo apartamento frente mar': ['Lindo Apartamento frente mar', 'Lindo Apartamento Frente Mar'], 'ótimo apartamento em itapema': ['Ótimo Apartamento em Itapema', 'Ótimo apartamento em Itapema'], 'cobertura quadra mar em meia praia': ['Cobertura quadra mar em Meia Praia', 'Cobertura Quadra Mar em Meia Praia'], 'apartamento bem localizado': ['Apartamento bem localizado', 'Apartamento Bem Localizado'], 'apto no coração da meia praia': ['Apto no coração da meia praia', 'Apto no coração da Meia Praia'], 'apto quadra mar meia praia': ['Apto Quadra Mar Meia Praia', 'apto quadra mar meia praia', 'Apto quadra mar meia praia'], 'apartamento itapema pé na areia': ['Apartamento Itapema Pé na Areia', 'Apartamento Itapema pé na areia'], 'apartamento na praia': ['Apartamento na Praia', 'Apartamento na praia'], 'quarto em itapema': ['Quarto em itapema', 'Quarto em Itapema'], 'aluguel de temporada itapema': ['Aluguel de Temporada Itapema', 'Aluguel de temporada Itapema'], 'apartamento frente mar meia praia': ['Apartamento frente mar meia praia', 'Apartamento Frente Mar Meia Praia'], 'apartamento quadra do mar': ['Apartamento Quadra do Mar', 'Apartamento quadra do mar'], 'apartamento a 100m da praia': ['Apartamento a 100m da praia', 'Apartamento a 100m da Praia'], 'casa para temporada': ['Casa para temporada', 'CASA PARA TEMPORADA'], 'apartamento no centro de itapema': ['Apartamento no Centro de Itapema', 'Apartamento no centro de Itapema'], 'lindo apto meia praia': ['Lindo APTO meia praia', 'Lindo Apto Meia Praia'], 'apartamento 3 suítes': ['Apartamento 3 Suítes', 'Apartamento 3 suítes'], 'kitnet em itapema': ['Kitnet em itapema', 'Kitnet em Itapema'], 'excelente apartamento frente mar': ['Excelente Apartamento Frente Mar', 'Excelente apartamento frente mar'], 'lindo apartamento quadra mar': ['Lindo apartamento quadra mar', 'Lindo Apartamento Quadra Mar'], 'chacara em cidade de praia': ['Chacara em cidade de praia', 'chacara em cidade de praia'], 'casa na praia': ['Casa na Praia', 'casa na praia'], 'apto centro de itapema': ['Apto centro de Itapema', 'Apto Centro de Itapema'], 'apartamento novo em meia praia': ['Apartamento NOVO em MEIA PRAIA', 'Apartamento novo em Meia Praia', 'Apartamento novo em meia praia'], 'apto meia praia frente mar': ['Apto Meia Praia Frente Mar', 'Apto Meia Praia frente mar'], 'apartamento em itapema perto da praia': ['APARTAMENTO EM ITAPEMA PERTO DA PRAIA', 'Apartamento em Itapema perto da praia'], 'lindo apartamento em itapema': ['Lindo apartamento em Itapema', 'Lindo Apartamento em Itapema'], 'a poucos passos do mar': ['A poucos passos do Mar', 'A Poucos Passos do Mar', 'A poucos passos do mar'], 'casa de praia': ['casa de praia', 'Casa de praia'], 'apartamento 402': ['APARTAMENTO 402', 'Apartamento 402'], 'apartamento muito aconchegante': ['Apartamento muito aconchegante', 'Apartamento Muito Aconchegante'], 'casa a 2km da praia': ['Casa a 2km da Praia', 'Casa a 2km da praia'], 'meia praia itapema sc': ['Meia Praia Itapema Sc', 'Meia Praia Itapema SC'], 'apto frente mar em itapema': ['Apto Frente Mar em Itapema', 'Apto frente mar em Itapema'], 'lindo apto em itapema': ['Lindo apto em itapema', 'Lindo Apto em Itapema'], 'apartamento em meia praia.': ['Apartamento em Meia Praia.', 'Apartamento em meia praia.'], 'apartamento beira mar de itapema': ['Apartamento Beira Mar de Itapema', 'Apartamento beira mar de Itapema'], 'apartamento na quadra do mar em meia praia': ['Apartamento na quadra do mar em Meia Praia', 'Apartamento na QUADRA DO MAR em Meia Praia'], 'apartamento frente mar itapema': ['Apartamento Frente Mar Itapema', 'Apartamento frente mar Itapema', 'Apartamento Frente mar Itapema'], 'apartamento frente ao mar': ['Apartamento frente ao mar', 'Apartamento Frente ao Mar'], 'apartamento na quadra do mar': ['Apartamento na quadra do mar', 'Apartamento na Quadra do Mar'], 'casa próximo a praia': ['casa próximo a praia', 'Casa próximo a praia'], 'itapema sc a praia da família': ['Itapema SC A praia da família', 'Itapema sc A praia da família'], 'casa de veraneio': ['Casa de Veraneio', 'Casa de veraneio'], 'apartamento praia': ['apartamento praia', 'Apartamento Praia'], 'apartamento meia praia - itapema': ['Apartamento MEIA PRAIA - Itapema', 'Apartamento Meia Praia - Itapema'], 'férias na praia': ['Férias na praia', 'Férias na Praia'], 'apartamento próximo à praia': ['Apartamento Próximo à Praia', 'Apartamento próximo à praia'], 'apartamento à beira mar': ['Apartamento à Beira Mar', 'Apartamento à beira mar'], 'apto meia praia - quadra mar': ['Apto Meia Praia - Quadra Mar', 'Apto Meia Praia - Quadra mar']}`
- **`ad_description`**: 3982 categorias (non-null 4387)
  - Top: `Sua família vai estar perto de tudo ao ficar neste lugar bem-localizado`:68, `Relaxe com toda a família nesta acomodação tranquila`:58, `Leve toda a família a este ótimo lugar com muito espaço para se divertir`:37, `Conheça este maravilhoso apartamento no Edifício Manhattan Flats, no centro de Itapema! Este refúgio oferece todo o conforto: sala com TV, cozinha completa, ar-condicionado, Wi-Fi e academia no prédio. Relaxe na piscina do terraço com vista para o mar, e aproveite a sala de jogos, sauna e lavanderia. Reserve o boliche e as churrasqueiras, ambos com taxa de uso. Próximo a ótimos restaurantes e a apenas 280 metros da praia. Reserve já e viva momentos inesquecíveis!<br /><br />`:30, `Abrace a simplicidade neste lugar tranquilo e bem-localizado`:18
  - Inconsistentes: Nenhum problema encontrado
- **`space`**: 1853 categorias (non-null 1914)
  - Top: `<br />Para o conforto de nossos hóspedes, o imóvel possui:<br />- 1 Quarto com cama de casal queen size, cortinas blackout, guarda-roupa, cômoda, Smart TV de tela plana e ar-condicionado;<br />- Sala de estar com sofá-cama de casal, cortinas blackout, Smart TV de tela plana e ar-condicionado;<br />- Cozinha completa com geladeira, cooktop de indução, forno elétrico, micro-ondas, sanduicheira, cafeteira elétrica, chaleira elétrica, taças de vinho, panelas, louças e utensílios;<br />- Espaço para jantar com mesa e 4 cadeiras;<br />- Roupas de cama e banho de qualidade hoteleira (roupas de cama e toalhas extras são cobrados pela Seazone);<br />- Wi-fi disponível;<br />- Boliche: reserva via app com taxa de uso R$254,16/hora;<br />- Churrasqueiras (1 da piscina e 2 do 5º andar): reserva via app com taxa de uso R$197,68/turno;<br />- Lavanderia: sem reserva, com taxa de uso da OMO;<br />- Piscina, Academia, Sala de jogos, Sauna: sem reserva e sem taxa de uso;<br />- OBS: Há obras no entorno e pode haver barulho durante horário comercial;<br />- Vista mar.<br />* A limpeza inclusa no valor é realizada somente no check-out. Se o hóspede desejar uma limpeza extra durante a estadia, será cobrada uma nova taxa de limpeza.<br />* São disponibilizadas uma toalha de banho por hóspede e uma toalha de rosto por banheiro, além de lençóis para a quantidade de hóspedes indicada. Trocas de enxoval podem ser solicitadas pelo valor de meia taxa de limpeza.<br />Venha, relaxe, divirta-se e não se preocupe com mais nada.<br /><br />`:17, `<br />⛔️Não fornecemos roupas de cama, mesa e banho. Porém temos convênio com uma empresa de locação destes itens, caso precise, solicite um orçamento.<br /><br />Disponibilizamos 1 travesseiro por pessoa.<br /><br />`:6, `<br />* internet Wi-Fi<br />* 1 vaga de garagem <br />* 1 dormitório de casal com ar condicionado split e vent. teto<br />* sala de estar e jantar integradas com ventilador de teto e sofá-cama<br />* sacada com maquina lava roupas e churrasqueira<br />* cozinha completa com eletrodomésticos e utensílios<br />* banheiro com box blindex<br />* 2 cadeiras de praia + 1 guarda sol<br /><br />`:5, `<br />Ambiente rústico, bonito e aconchegante: A Pousada possui uma atmosfera rústica e encantadora. Os quartos são decorados com detalhes que refletem a essência do local, proporcionando um ambiente bonito e aconchegante, onde os hóspedes podem se sentir em casa.<br /><br />Piscina e churrasqueira: Para momentos de lazer e descontração, nossa pousada oferece uma piscina refrescante, perfeita para se refrescar e relaxar. Além disso, uma churrasqueira está disponível para os hóspedes desfrutarem de refeições ao ar livre, adicionando um toque especial à estadia.<br /><br />Integração com a natureza: Rodeada pela natureza exuberante, nossa pousada proporciona uma atmosfera serena e a oportunidade de estar em contato direto com o meio ambiente. Os hóspedes podem desfrutar de trilhas ecológicas, observação de pássaros e momentos de tranquilidade em meio à natureza.<br /><br />Estacionamento amplo: Sabemos que a comodidade de estacionar o veículo com segurança é essencial durante a viagem. Nossa pousada oferece um estacionamento amplo e seguro, proporcionando tranquilidade aos hóspedes que chegam de carro.<br /><br /> Exclusividade: Com 6 quartos, nossa espaço proporciona um ambiente intimista e exclusivo, um salão de festa para 100 pessoas sendo assim perfeito para confraternizações permitindo que os hóspedes desfrutem de uma estadia tranquila e relaxante, longe das aglomerações dos grandes hotéis`:5, `<br />Quarto até 4 hóspedes com ar<br /><br />1 quadra e meia da praia. Vocês vão estar perto de tudo ao ficar neste lugar bem localizado, no coração de Meia Praia. Próximo a supermercados, shopping, farmácia, restaurantes e muito mais…<br /><br />Além do dormitório privado e exclusivo a vocês, terão acesso à área compartilhada com 2 banheiros, sala, cozinha, lavanderia, churrasqueira, utensílios, eletroeletrônicos, equipamentos e decoração (microondas, geladeira, forno, fogão) e 5 vagas de garagem fechada.<br /><br />`:4
  - Inconsistentes: Nenhum problema encontrado
- **`house_rules`**: 587 categorias (non-null 4441)
  - Top: `["Máximo de 8 hóspedes"]`:181, `["Máximo de 6 hóspedes"]`:181, `["Máximo de 6 hóspedes", "Não é permitido animais de estimação", "Não são permitidas festas ou eventos", "Proibido fumar"]`:139, `["Máximo de 6 hóspedes", "Não é permitido animais de estimação", "Horário de silêncio", "Não são permitidas festas ou eventos", "Não é permitido fotografia comercial", "Proibido fumar"]`:106, `["Máximo de 4 hóspedes"]`:85
  - Inconsistentes: Nenhum problema encontrado
- **`amenities`**: 3878 categorias (non-null 4441)
  - Top: `["Máquina de Lavar", "TV", "Ar-condicionado", "Wi-Fi", "Cozinha", "Churrasqueira", "Estacionamento incluído"]`:77, `["Máquina de Lavar", "TV", "Ar-condicionado", "Wi-Fi", "Cozinha", "Estacionamento incluído"]`:42, `["Máquina de Lavar", "TV", "Ar-condicionado", "Wi-Fi", "Cozinha", "Acesso à praia (à beira-mar)", "Churrasqueira", "Estacionamento incluído"]`:22, `["Máquina de Lavar", "TV", "Ar-condicionado", "Câmeras de segurança na parte externa da propriedade", "Wi-Fi", "Cozinha", "Churrasqueira", "Estacionamento incluído"]`:18, `["Chuveiro externo", "Máquina de Lavar", "TV", "Ar-condicionado", "Wi-Fi", "Cozinha", "Churrasqueira", "Estacionamento incluído"]`:17
  - Inconsistentes: Nenhum problema encontrado
- **`safety_features`**: 67 categorias (non-null 4441)
  - Top: `["Alarme de monóxido de carbono não informado", "Detector de fumaça não informado"]`:2159, `["Câmeras de segurança na parte externa da propriedade", "Alarme de monóxido de carbono não informado", "Detector de fumaça não informado"]`:542, `["Não há alarme de monóxido de carbono", "Não há alarme de fumaça"]`:420, `["Alarme de monóxido de carbono não informado", "Detector de fumaça instalado"]`:241, `["Câmeras de segurança na parte externa da propriedade", "Alarme de monóxido de carbono não informado", "Detector de fumaça instalado"]`:113
  - Inconsistentes: Nenhum problema encontrado
- **`check_in`**: 108 categorias (non-null 4441)
  - Top: `Check-in após 15:00`:898, `Check-in após 14:00`:884, `<NA>`:446, `Check-in flexível`:215, `Check-in: 15:00 - 20:00`:205
  - Inconsistentes: Nenhum problema encontrado
- **`check_out`**: 20 categorias (non-null 4441)
  - Top: `Checkout antes das 10:00`:1493, `<NA>`:842, `Checkout antes das 11:00`:815, `Checkout antes das 12:00`:524, `Checkout antes das 09:00`:512
  - Inconsistentes: Nenhum problema encontrado
- **`listing_type`**: 4 categorias (non-null 4441)
  - Top: `apartamento`:3710, `casa`:443, `outros`:245, `hotel`:43
  - Inconsistentes: Nenhum problema encontrado
- **`can_instant_book`**: 3 categorias (non-null 4441)
  - Top: `false`:3127, `true`:959, `<NA>`:355
  - Inconsistentes: Nenhum problema encontrado
- **`is_professional`**: 2 categorias (non-null 4086)
  - Top: `false`:3697, `true`:389
  - Inconsistentes: Nenhum problema encontrado
- **`is_new_listing`**: 2 categorias (non-null 3567)
  - Top: `false`:2836, `true`:731
  - Inconsistentes: Nenhum problema encontrado
- **`is_guest_favorite`**: 2 categorias (non-null 4441)
  - Top: `false`:3567, `true`:874
  - Inconsistentes: Nenhum problema encontrado

### Valores suspeitos / impossíveis / fora do padrão
- latitude/longitude = 0 (Details sem geolocalização, usar Mesh): 4441 casos (100.0%)
- picture_count=0 mas is_guest_favorite=true: 81 casos (suspeito)
- number_of_bedrooms >=8: 9 casos (ex: 12,16)
- cleaning_fee=0: 939 casos (pode ser legitimo)
- is_professional vazio (nulo): 355

### Formatação para futuros JOINs (IDs)
- airbnb_listing_id: tamanhos variados {19: 2129, 18: 944, 8: 1342, 6: 1, 7: 25}
- owner_id: tamanhos variados {9: 3856, 8: 537, 7: 45, 6: 3}
- owner_id: 1384 duplicados (esperado - host com multiplos listings)

### Erro vs Legítimo
- `star_rating=0.0` com `number_of_reviews>0` = **erro/impossível**
- `star_rating=0.0` com `number_of_reviews=0` = **legítimo** (novo sem avaliação)
- `picture_count=0` + `is_guest_favorite=true` = **suspeito**
- `latitude/longitude=0.0` = **erro/suspeito**
- `is_professional=""` = **falta de info**
- `space=""` 56% vazio = **legítimo** (opcional)
- `encoding Mǭximo/nǜo` = **problema de charset**

---
## ARQUIVO: `Hosts_ids_Itapema.csv`

* **Linhas (dados, sem header, via csv):** 4440
* **Colunas:** 11
* **Colunas listadas:** `owner_id`, `owner`, `is_superhost`, `number_of_reviews_host`, `is_verified`, `star_rating_host`, `years_host`, `months_host`, `response_rate_shown`, `response_time_shown`, `host_snapshot_date`
* **Linhas 100% duplicadas:** 0

### Tipos inferidos
- `owner_id`: numérico (inteiro)
- `owner`: string/categórico
- `is_superhost`: booleano (string)
- `number_of_reviews_host`: numérico (inteiro)
- `is_verified`: booleano (string)
- `star_rating_host`: numérico (float)
- `years_host`: numérico (inteiro)
- `months_host`: numérico (inteiro)
- `response_rate_shown`: string (vazio/placeholder apenas)
- `response_time_shown`: string (vazio/placeholder apenas)
- `host_snapshot_date`: data/datetime (string)

### Nulos ("" ou espaços) e Placeholders (<NA>/não informado) por coluna

| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |
|---|---|---|---|---|---|---|---|---|
| `owner_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `owner` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `is_superhost` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `number_of_reviews_host` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 854 | 19.23% |
| `is_verified` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `star_rating_host` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 854 | 19.23% |
| `years_host` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 921 | 20.74% |
| `months_host` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 917 | 20.65% |
| `response_rate_shown` | 0 | 0.00% | 4440 | 100.00% | 0 | 0.00% | 0 | 0.00% |
| `response_time_shown` | 0 | 0.00% | 4440 | 100.00% | 0 | 0.00% | 0 | 0.00% |
| `host_snapshot_date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

_*Vazios = mesma definição de nulos._

### IDs
- **`owner_id`**: únicos `3057` / duplicados `1383` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{9: 3855, 8: 537, 7: 45, 6: 3}`
  - Exemplos: `['587657794', '446793136', '668234945']`

### Numéricas (min, max, mediana, média, qtd zero)

| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |
|---|---|---|---|---|---|---|---|
| `owner_id` | 4440 | 614119.0 | 669723189.0 | 268446727.5 | 302004039.98 | 0 | 0.0% |
| `number_of_reviews_host` | 4440 | 0.0 | 41299.0 | 7.0 | 1136.47 | 854 | 19.23% |
| `star_rating_host` | 4440 | 0.0 | 5.0 | 4.860000133514404 | 3.89 | 854 | 19.23% |
| `years_host` | 4440 | 0.0 | 13.0 | 3.0 | 3.31 | 921 | 20.74% |
| `months_host` | 4440 | 0.0 | 11.0 | 2.0 | 3.58 | 917 | 20.65% |

### Categóricas (qtd categorias, top, inconsistentes)
- **`owner`**: 1726 categorias (non-null 4440)
  - Top: `Seazone`:112, `Jarbas`:59, `Bruno`:39, `Vanessa`:38, `Casa Porto - Creci 27884`:34
  - Inconsistentes: Nenhum problema encontrado
- **`is_superhost`**: 2 categorias (non-null 4440)
  - Top: `false`:3549, `true`:891
  - Inconsistentes: Nenhum problema encontrado
- **`is_verified`**: 2 categorias (non-null 4440)
  - Top: `true`:4411, `false`:29
  - Inconsistentes: Nenhum problema encontrado
- **`response_rate_shown`**: 1 categorias (non-null 4440)
  - Top: `<NA>`:4440
  - Inconsistentes: Nenhum problema encontrado
- **`response_time_shown`**: 1 categorias (non-null 4440)
  - Top: `<NA>`:4440
  - Inconsistentes: Nenhum problema encontrado

### Valores suspeitos / impossíveis / fora do padrão
- response_rate_shown/response_time_shown com <NA>: 8880 placeholders
- years_host=0: 921 casos
- star_rating_host=0.0: 854

### Formatação para futuros JOINs (IDs)
- owner_id: tamanhos variados {9: 3855, 8: 537, 7: 45, 6: 3}
- owner_id: 1383 duplicados (esperado - mesmo host em multiplos listings; arquivo é por listing)

### Erro vs Legítimo
- `response_rate_shown=<NA>` = **legítimo/sentinela**
- `years_host=0` + `months_host>0` = **legítimo**

---
## ARQUIVO: `Mesh_Ids_Data_Itapema.csv`

* **Linhas (dados, sem header, via csv):** 4441
* **Colunas:** 8
* **Colunas listadas:** `airbnb_listing_id`, `latitude`, `longitude`, `suburb`, `country`, `state`, `city`, `aquisition_date`
* **Linhas 100% duplicadas:** 0

### Tipos inferidos
- `airbnb_listing_id`: numérico (inteiro)
- `latitude`: numérico (float)
- `longitude`: numérico (float)
- `suburb`: string/categórico
- `country`: string/categórico
- `state`: string/categórico
- `city`: string/categórico
- `aquisition_date`: data/datetime (string)

### Nulos ("" ou espaços) e Placeholders (<NA>/não informado) por coluna

| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |
|---|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `latitude` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `longitude` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `suburb` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `country` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `state` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `city` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `aquisition_date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

_*Vazios = mesma definição de nulos._

### IDs
- **`airbnb_listing_id`**: únicos `4441` / duplicados `0` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{19: 2129, 18: 944, 8: 1342, 7: 25, 6: 1}`
  - Exemplos: `['828307537051457546', '985445004274818605', '1048785577617228176']`

### Numéricas (min, max, mediana, média, qtd zero)

| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |
|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 4441 | 822704.0 | 1.3297872953081106e+18 | 9.8189445944595e+17 | 7.466437614346395e+17 | 0 | 0.0% |
| `latitude` | 4441 | -27.1490001678 | -27.055893951369278 | -27.12794359520252 | -27.12 | 0 | 0.0% |
| `longitude` | 4441 | -48.66191482543945 | -48.58594772482967 | -48.60499954223633 | -48.61 | 0 | 0.0% |

### Categóricas (qtd categorias, top, inconsistentes)
- **`suburb`**: 16 categorias (non-null 4441)
  - Top: `Meia Praia`:2860, `Centro`:657, `Morretes`:441, `Tabuleiro dos Oliveiras`:129, `Casa Branca`:88
  - Inconsistentes: Nenhum problema encontrado
- **`country`**: 1 categorias (non-null 4441)
  - Top: `Brasil`:4441
  - Inconsistentes: Nenhum problema encontrado
- **`state`**: 1 categorias (non-null 4441)
  - Top: `Santa Catarina`:4441
  - Inconsistentes: Nenhum problema encontrado
- **`city`**: 1 categorias (non-null 4441)
  - Top: `Itapema`:4441
  - Inconsistentes: Nenhum problema encontrado

### Valores suspeitos / impossíveis / fora do padrão
- suburb = none ou vazio: 5

### Formatação para futuros JOINs (IDs)
- airbnb_listing_id: tamanhos variados {19: 2129, 18: 944, 8: 1342, 7: 25, 6: 1}

### Erro vs Legítimo
- `suburb='none'`/vazio = **erro/falta**

---
## ARQUIVO: `Price_AV_Itapema.csv`

* **Linhas (dados, sem header, via csv):** 118839
* **Colunas:** 4
* **Colunas listadas:** `airbnb_listing_id`, `date`, `price`, `aquisition_date`
* **Linhas 100% duplicadas:** 0

### Tipos inferidos
- `airbnb_listing_id`: numérico (inteiro)
- `date`: data/datetime (string)
- `price`: numérico (float)
- `aquisition_date`: data/datetime (string)

### Nulos ("" ou espaços) e Placeholders (<NA>/não informado) por coluna

| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |
|---|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `price` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `aquisition_date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

_*Vazios = mesma definição de nulos._

### IDs
- **`airbnb_listing_id`**: únicos `1005` / duplicados `117834` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{19: 32742, 8: 57422, 18: 27532, 7: 1143}`
  - Exemplos: `['721635424816164605', '985445004274818605', '869504505210568410']`

### Numéricas (min, max, mediana, média, qtd zero)

| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |
|---|---|---|---|---|---|---|---|
| `airbnb_listing_id` | 118839 | 1977915.0 | 1.333504785474036e+18 | 5.775475025033966e+17 | 5.0916579844533414e+17 | 0 | 0.0% |
| `price` | 118839 | 63.0 | 29000.0 | 607.0 | 713.1 | 0 | 0.0% |

### Valores suspeitos / impossíveis / fora do padrão
- price max muito alto: 29000.0

### Formatação para futuros JOINs (IDs)
- airbnb_listing_id: tamanhos variados {19: 32742, 8: 57422, 18: 27532, 7: 1143}
- airbnb_listing_id: 117834 duplicados (esperado - historico)

### Erro vs Legítimo
- `price=0` = **erro/impossível**
- `airbnb_listing_id` duplicado = **legítimo** (histórico)

---
## ARQUIVO: `VivaReal_Itapema.csv`

* **Linhas (dados, sem header, via csv):** 8329
* **Colunas:** 22
* **Colunas listadas:** `listing_id`, `link_url`, `listing_title`, `business_types`, `listing_type`, `property_type`, `sale_price`, `rental_price`, `rental_period`, `yearly_iptu`, `monthly_condo_fee`, `amenities`, `usable_area`, `bathrooms`, `bedrooms`, `parking_spaces`, `state`, `city`, `suburb`, `advertiser_name`, `portal`, `aquisition_date`
* **Linhas 100% duplicadas:** 35

### Tipos inferidos
- `listing_id`: numérico (inteiro)
- `link_url`: string/categórico
- `listing_title`: string/categórico
- `business_types`: string/categórico
- `listing_type`: string/categórico
- `property_type`: string/categórico
- `sale_price`: numérico (inteiro)
- `rental_price`: numérico (inteiro)
- `rental_period`: string/categórico
- `yearly_iptu`: numérico (inteiro)
- `monthly_condo_fee`: numérico (inteiro)
- `amenities`: string/categórico
- `usable_area`: numérico (inteiro)
- `bathrooms`: numérico (inteiro)
- `bedrooms`: numérico (inteiro)
- `parking_spaces`: numérico (inteiro)
- `state`: string/categórico
- `city`: string/categórico
- `suburb`: string/categórico
- `advertiser_name`: string/categórico
- `portal`: string/categórico
- `aquisition_date`: data/datetime (string)

### Nulos ("" ou espaços) e Placeholders (<NA>/não informado) por coluna

| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |
|---|---|---|---|---|---|---|---|---|
| `listing_id` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `link_url` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `listing_title` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `business_types` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `listing_type` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `property_type` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `sale_price` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `rental_price` | 8327 | 99.98% | 0 | 0.00% | 8327 | 99.98% | 0 | 0.00% |
| `rental_period` | 0 | 0.00% | 8327 | 99.98% | 0 | 0.00% | 0 | 0.00% |
| `yearly_iptu` | 2714 | 32.58% | 0 | 0.00% | 2714 | 32.58% | 2231 | 26.79% |
| `monthly_condo_fee` | 2490 | 29.90% | 0 | 0.00% | 2490 | 29.90% | 2364 | 28.38% |
| `amenities` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `usable_area` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 11 | 0.13% |
| `bathrooms` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 172 | 2.07% |
| `bedrooms` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 230 | 2.76% |
| `parking_spaces` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 309 | 3.71% |
| `state` | 2 | 0.02% | 0 | 0.00% | 2 | 0.02% | 0 | 0.00% |
| `city` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `suburb` | 98 | 1.18% | 0 | 0.00% | 98 | 1.18% | 0 | 0.00% |
| `advertiser_name` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `portal` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |
| `aquisition_date` | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

_*Vazios = mesma definição de nulos._

### IDs
- **`listing_id`**: únicos `8293` / duplicados `36` / nulos `0` / placeholders `0` / com espaços pontas `0` / não numéricos `0`
  - Distribuição tamanhos: `{10: 8328, 8: 1}`
  - Exemplos: `['2764633839', '2753757926', '2764630659']`

### Numéricas (min, max, mediana, média, qtd zero)

| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |
|---|---|---|---|---|---|---|---|
| `listing_id` | 8329 | 94919065.0 | 2770391213.0 | 2743647361.0 | 2711137874.39 | 0 | 0.0% |
| `sale_price` | 8329 | 10000.0 | 44000000.0 | 1750000.0 | 2450770.28 | 0 | 0.0% |
| `rental_price` | 2 | 15000.0 | 15000.0 | 15000.0 | 15000.0 | 0 | 0.0% |
| `yearly_iptu` | 5615 | 0.0 | 2800000.0 | 150.0 | 2653.99 | 2231 | 39.73% |
| `monthly_condo_fee` | 5839 | 0.0 | 3150000.0 | 290.0 | 2372.78 | 2364 | 40.49% |
| `usable_area` | 8329 | 0.0 | 188000.0 | 128.0 | 196.69 | 11 | 0.13% |
| `bathrooms` | 8329 | 0.0 | 17.0 | 3.0 | 3.2 | 172 | 2.07% |
| `bedrooms` | 8329 | 0.0 | 11.0 | 3.0 | 2.94 | 230 | 2.76% |
| `parking_spaces` | 8329 | 0.0 | 30.0 | 2.0 | 2.08 | 309 | 3.71% |

### Categóricas (qtd categorias, top, inconsistentes)
- **`link_url`**: 8293 categorias (non-null 8329)
  - Top: `https://www.vivareal.com.br/imovel/apartamento-3-quartos-meia-praia-bairros-itapema-com-garagem-131m2-venda-RS1598122-id-2687011752/`:2, `https://www.vivareal.com.br/imovel/apartamento-3-quartos-castelo-branco-bairros-itapema-com-garagem-118m2-venda-RS1450000-id-2697432835/`:2, `https://www.vivareal.com.br/imovel/apartamento-3-quartos-meia-praia-bairros-itapema-com-garagem-125m2-venda-RS1500000-id-2612161501/`:2, `https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-70m2-venda-RS870000-id-2598271159/`:2, `https://www.vivareal.com.br/imovel/apartamento-3-quartos-meia-praia-bairros-itapema-com-garagem-130m2-venda-RS2150000-id-2691331590/`:2
  - Inconsistentes: Nenhum problema encontrado
- **`listing_title`**: 5874 categorias (non-null 8329)
  - Top: `APARTAMENTO - MEIA PRAIA - SC`:164, `Itapema - Apartamento Padrão - Meia Praia`:85, `apartamento a venda de 2 quartos em itapema - santa catarina`:66, `ITAPEMA - Apartamento Padrão - Meia Praia`:64, `Apartamento em Meia Praia - Itapema SC`:52
  - **Inconsistentes:** `{'itapema - apartamento padrão - meia praia': ['ITAPEMA - Apartamento Padrão - Meia Praia', 'Itapema - Apartamento Padrão - Meia Praia', 'ITAPEMA - Apartamento Padrão - Meia praia'], 'apartamento 4 dormitórios para venda em itapema, centro, 4 dormitórios, 4 suítes, 5 banheiros, 3 vag': ['Apartamento 4 dormitórios para Venda em Itapema, CENTRO, 4 dormitórios, 4 suítes, 5 banheiros, 3 vag', 'Apartamento 4 dormitórios para Venda em Itapema, Centro, 4 dormitórios, 4 suítes, 5 banheiros, 3 vag'], 'chateau unique 1402 - torre a': ['CHATEAU UNIQUE 1402 - TORRE A', 'Chateau Unique 1402 - Torre A'], 'apartamento 3 suítes, meia praia, itapema sc': ['Apartamento 3 suítes, Meia Praia, Itapema SC', 'APARTAMENTO 3 SUÍTES, MEIA PRAIA, ITAPEMA SC'], 'apartamento para venda em itapema, morretes, 2 dormitórios, 1 suíte, 2 banheiros, 1 vaga': ['Apartamento para Venda em Itapema, MORRETES, 2 dormitórios, 1 suíte, 2 banheiros, 1 vaga', 'Apartamento para Venda em Itapema, Morretes, 2 dormitórios, 1 suíte, 2 banheiros, 1 vaga'], 'itapema - apartamento padrão - centro': ['Itapema - Apartamento Padrão - Centro', 'ITAPEMA - Apartamento Padrão - Centro', 'ITAPEMA - Apartamento Padrão - CENTRO'], 'ótimo apartamento com 3 suítes à venda, meia praia - itapema/sc': ['Ótimo Apartamento com 3 Suítes à venda, Meia Praia - Itapema/SC', 'Ótimo Apartamento com 3 suítes à venda, Meia Praia - Itapema/SC'], 'apartamento para venda em itapema, meia praia, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas': ['Apartamento para Venda em Itapema, meia praia, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas', 'Apartamento para Venda em Itapema, Meia Praia, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas'], 'itapema - apartamento padrão - morretes': ['ITAPEMA - Apartamento Padrão - Morretes', 'Itapema - Apartamento Padrão - Morretes'], 'itapema - apartamento padrão - casa branca': ['ITAPEMA - Apartamento Padrão - Casa Branca', 'Itapema - Apartamento Padrão - Casa Branca'], 'apartamento centro de itapema': ['Apartamento Centro de Itapema', 'APARTAMENTO CENTRO DE ITAPEMA'], 'apartamento 3 dormitórios para venda em itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 3': ['Apartamento 3 dormitórios para Venda em Itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 3', 'Apartamento 3 dormitórios para Venda em Itapema, Meia Praia, 3 dormitórios, 3 suítes, 4 banheiros, 3'], 'apartamento frente av. nereu ramos': ['Apartamento frente Av. Nereu ramos', 'Apartamento frente av. nereu ramos'], 'itapema - terreno padrão - morretes': ['ITAPEMA - Terreno Padrão - Morretes', 'Itapema - Terreno Padrão - Morretes'], 'apartamento mobiliado pronto para morar': ['Apartamento mobiliado pronto para morar', 'APARTAMENTO MOBILIADO PRONTO PARA MORAR'], 'apartamento em itapema': ['APARTAMENTO EM ITAPEMA', 'Apartamento em Itapema'], 'apartamento para venda em itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas': ['Apartamento para Venda em Itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas', 'Apartamento para Venda em Itapema, Meia Praia, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas'], 'apartamento 3 dormitórios para venda em itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 2': ['Apartamento 3 dormitórios para Venda em Itapema, meia praia, 3 dormitórios, 3 suítes, 4 banheiros, 2', 'Apartamento 3 dormitórios para Venda em Itapema, Meia Praia, 3 dormitórios, 3 suítes, 4 banheiros, 2'], 'itapema - residencial - meia praia': ['Itapema - RESIDENCIAL - Meia Praia', 'ITAPEMA - RESIDENCIAL - Meia Praia'], 'apartamento em morretes': ['Apartamento em Morretes', 'APARTAMENTO EM MORRETES'], 'apartamento em meia praia - itapema': ['Apartamento em Meia Praia - Itapema', 'Apartamento em Meia praia - Itapema', 'Apartamento em meia praia - Itapema'], 'apartamento alto padrão em itapema': ['Apartamento alto padrão em Itapema', 'APARTAMENTO ALTO PADRÃO EM ITAPEMA'], 'apartamento semi mobiliado em itapema': ['Apartamento semi mobiliado em itapema', 'APARTAMENTO SEMI MOBILIADO EM ITAPEMA'], 'apartamento com vista mar e 4 suítes à venda, 156 m² em meia praia - itapema/sc': ['Apartamento com VISTA MAR e 4 suítes à venda, 156 m² em Meia Praia - Itapema/SC', 'Apartamento com vista mar e 4 Suítes à venda, 156 m² em Meia Praia - Itapema/SC'], 'apartamento novo 3 suítes, itapema sc': ['Apartamento novo 3 suítes, Itapema SC', 'APARTAMENTO NOVO 3 SUÍTES, ITAPEMA SC'], 'itapema - casa padrão - morretes': ['Itapema - Casa Padrão - Morretes', 'ITAPEMA - Casa Padrão - Morretes'], 'apartamento para venda em itapema, centro, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas': ['Apartamento para Venda em Itapema, Centro, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas', 'Apartamento para Venda em Itapema, CENTRO, 3 dormitórios, 3 suítes, 4 banheiros, 2 vagas'], 'apartamento 3 suítes, quadra mar, itapema sc': ['Apartamento 3 suítes, Quadra Mar, Itapema SC', 'Apartamento 3 suítes, quadra mar, Itapema SC'], 'itapema - apartamento padrão - canto da praia': ['ITAPEMA - Apartamento Padrão - Canto da Praia', 'Itapema - Apartamento Padrão - Canto Da Praia', 'ITAPEMA - Apartamento Padrão - CANTO DA PRAIA'], 'apartamento residencial em itapema - sc, meia praia': ['APARTAMENTO RESIDENCIAL em ITAPEMA - SC, MEIA PRAIA', 'APARTAMENTO RESIDENCIAL em Itapema - SC, Meia Praia', 'APARTAMENTO RESIDENCIAL em ITAPEMA - SC, Meia Praia'], 'apartamento residencial em itapema - sc, itapema': ['APARTAMENTO RESIDENCIAL em Itapema - SC, Itapema', 'APARTAMENTO RESIDENCIAL em ITAPEMA - SC, ITAPEMA'], 'sobrado mobiliado no morretes': ['Sobrado mobiliado no Morretes', 'SOBRADO MOBILIADO NO MORRETES'], 'apartamento à venda de 2 a 3 quartos em itapema sc': ['Apartamento à venda de 2 a 3 quartos em Itapema SC', 'Apartamento à venda de 2 A 3 quartos em Itapema SC'], 'apartamento à venda de 3 suítes em meia praia, itapema': ['Apartamento à Venda de 3 suítes em Meia Praia, Itapema', 'Apartamento à venda de 3 suítes em Meia Praia, Itapema'], 'apartamento à venda em meia praia, itapema': ['Apartamento à venda em Meia Praia, Itapema', 'Apartamento à Venda em Meia Praia, Itapema'], 'apartamento com vista mar e 3 suítes à venda, meia praia - itapema/sc': ['Apartamento com Vista Mar e 3 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 3 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com vista mar e 3 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 3 Suítes à venda, Meia Praia - Itapema/SC'], 'casas geminadas com 02 dorms, aceita financiamento!!! morretes itapema': ['Casas Geminadas com 02 dorms, Aceita Financiamento!!! Morretes Itapema', 'Casas Geminadas com 02 dorms, Aceita financiamento!!! Morretes Itapema'], 'apartamento em rua 323 - meia praia - itapema/sc': ['Apartamento em Rua 323 - Meia Praia - Itapema/SC', 'Apartamento em Rua 323 - Meia praia - Itapema/SC'], 'apartamento em segunda avenida - meia praia - itapema/sc': ['Apartamento em Segunda Avenida - Meia praia - Itapema/SC', 'Apartamento em Segunda Avenida - Meia Praia - Itapema/SC'], 'apartamento em rua 236 - meia praia - itapema/sc': ['Apartamento em Rua 236 - Meia praia - Itapema/SC', 'Apartamento em Rua 236 - Meia Praia - Itapema/SC'], 'apartamento em rua 207 - meia praia - itapema/sc': ['Apartamento em Rua 207 - Meia Praia - Itapema/SC', 'Apartamento em Rua 207 - Meia praia - Itapema/SC'], 'apartamento em rua 298 - meia praia - itapema/sc': ['Apartamento em Rua 298 - Meia praia - Itapema/SC', 'Apartamento em rua 298 - Meia praia - Itapema/SC', 'Apartamento em Rua 298 - Meia Praia - Itapema/SC'], 'apartamento em rua 317 - meia praia - itapema/sc': ['Apartamento em Rua 317 - Meia Praia - Itapema/SC', 'Apartamento em Rua 317 - Meia praia - Itapema/SC'], 'apartamento em rua 240 - meia praia - itapema/sc': ['Apartamento em Rua 240 - Meia praia - Itapema/SC', 'Apartamento em Rua 240 - Meia Praia - Itapema/SC'], 'apartamento em rua 238 - meia praia - itapema/sc': ['Apartamento em Rua 238 - Meia Praia - Itapema/SC', 'Apartamento em Rua 238 - Meia praia - Itapema/SC', 'Apartamento em rua 238 - Meia Praia - Itapema/SC'], 'apartamento em rua 129 c - centro - itapema/sc': ['Apartamento em RUA 129 C - Centro - Itapema/SC', 'Apartamento em Rua 129 C - Centro - Itapema/SC'], 'apartamento em rua 260 - meia praia - itapema/sc': ['Apartamento em Rua 260 - Meia praia - Itapema/SC', 'Apartamento em Rua 260 - Meia Praia - Itapema/SC'], 'apartamento em rua 241 - meia praia - itapema/sc': ['Apartamento em Rua 241 - Meia Praia - Itapema/SC', 'Apartamento em Rua 241 - Meia praia - Itapema/SC'], 'apartamento em rua 210 - meia praia - itapema/sc': ['Apartamento em Rua 210 - Meia praia - Itapema/SC', 'Apartamento em Rua 210 - Meia Praia - Itapema/SC'], 'apartamento em rua 305 - meia praia - itapema/sc': ['Apartamento em Rua 305 - Meia praia - Itapema/SC', 'Apartamento em Rua 305 - Meia Praia - Itapema/SC'], 'apartamento em rua 244 - meia praia - itapema/sc': ['Apartamento em Rua 244 - Meia praia - Itapema/SC', 'Apartamento em Rua 244 - Meia Praia - Itapema/SC'], 'apartamento em avenida nereu ramos - meia praia - itapema/sc': ['Apartamento em Avenida Nereu Ramos - Meia Praia - Itapema/SC', 'Apartamento em Avenida Nereu Ramos - Meia praia - Itapema/SC', 'Apartamento em AVENIDA NEREU RAMOS - Meia praia - Itapema/SC'], 'apartamento em rua 420 - morretes - itapema/sc': ['Apartamento em Rua 420 - Morretes - Itapema/SC', 'Apartamento em rua 420 - Morretes - Itapema/SC'], 'apartamento em 301 - meia praia - itapema/sc': ['Apartamento em 301 - Meia praia - Itapema/SC', 'Apartamento em 301 - Meia Praia - Itapema/SC'], 'apartamento em rua 262 - meia praia - itapema/sc': ['Apartamento em Rua 262 - Meia Praia - Itapema/SC', 'Apartamento em Rua 262 - Meia praia - Itapema/SC'], 'apartamento em rua 250 - meia praia - itapema/sc': ['Apartamento em Rua 250 - Meia praia - Itapema/SC', 'Apartamento em Rua 250 - Meia Praia - Itapema/SC'], 'apartamento em rua 216 - meia praia - itapema/sc': ['Apartamento em Rua 216 - Meia Praia - Itapema/SC', 'Apartamento em Rua 216 - Meia praia - Itapema/SC'], 'apartamento em rua 288 - meia praia - itapema/sc': ['Apartamento em Rua 288 - Meia praia - Itapema/SC', 'Apartamento em Rua 288 - Meia Praia - Itapema/SC'], 'apartamento em rua 306 - meia praia - itapema/sc': ['Apartamento em Rua 306 - Meia praia - Itapema/SC', 'Apartamento em Rua 306 - Meia Praia - Itapema/SC'], 'apartamento em rua 319 - meia praia - itapema/sc': ['Apartamento em Rua 319 - Meia praia - Itapema/SC', 'Apartamento em Rua 319 - Meia Praia - Itapema/SC'], 'apartamento em rua 315 - meia praia - itapema/sc': ['Apartamento em Rua 315 - Meia praia - Itapema/SC', 'Apartamento em Rua 315 - Meia Praia - Itapema/SC'], 'apartamento em av. nereu ramos - meia praia - itapema/sc': ['Apartamento em Av. Nereu Ramos - Meia Praia - Itapema/SC', 'Apartamento em Av. nereu ramos - Meia Praia - Itapema/SC', 'Apartamento em Av. Nereu Ramos - Meia praia - Itapema/SC'], 'apartamento em rua 226 - meia praia - itapema/sc': ['Apartamento em Rua 226 - Meia praia - Itapema/SC', 'Apartamento em Rua 226 - Meia Praia - Itapema/SC'], 'apartamento em rua 302 - meia praia - itapema/sc': ['Apartamento em Rua 302 - Meia praia - Itapema/SC', 'Apartamento em Rua 302 - Meia Praia - Itapema/SC'], 'apartamento em rua 242 - meia praia - itapema/sc': ['Apartamento em Rua 242 - Meia Praia - Itapema/SC', 'Apartamento em Rua 242 - Meia praia - Itapema/SC', 'Apartamento em rua 242 - Meia Praia - Itapema/SC'], 'apartamento em rua 294 - meia praia - itapema/sc': ['Apartamento em Rua 294 - Meia Praia - Itapema/SC', 'Apartamento em Rua 294 - Meia praia - Itapema/SC'], 'apartamento em rua 314 - meia praia - itapema/sc': ['Apartamento em Rua 314 - Meia Praia - Itapema/SC', 'Apartamento em Rua 314 - Meia praia - Itapema/SC'], 'apartamento em rua 310 - meia praia - itapema/sc': ['Apartamento em Rua 310 - Meia Praia - Itapema/SC', 'Apartamento em Rua 310 - Meia praia - Itapema/SC'], 'apartamento em rua 234 - meia praia - itapema/sc': ['Apartamento em Rua 234 - Meia praia - Itapema/SC', 'Apartamento em Rua 234 - Meia Praia - Itapema/SC'], 'apartamento em rua 313 b - meia praia - itapema/sc': ['Apartamento em Rua 313 B - Meia Praia - Itapema/SC', 'Apartamento em Rua 313 B - Meia praia - Itapema/SC'], 'apartamento em rua 232 - meia praia - itapema/sc': ['Apartamento em Rua 232 - Meia Praia - Itapema/SC', 'Apartamento em Rua 232 - Meia praia - Itapema/SC'], 'apartamento em rua 313 - meia praia - itapema/sc': ['Apartamento em Rua 313 - Meia praia - Itapema/SC', 'Apartamento em Rua 313 - Meia Praia - Itapema/SC'], 'apartamento em rua 274 - meia praia - itapema/sc': ['Apartamento em Rua 274 - Meia praia - Itapema/SC', 'Apartamento em Rua 274 - Meia Praia - Itapema/SC'], 'apartamento em rua 271 - meia praia - itapema/sc': ['Apartamento em Rua 271 - Meia Praia - Itapema/SC', 'Apartamento em Rua 271 - Meia praia - Itapema/SC'], 'apartamento em rua 280 - meia praia - itapema/sc': ['Apartamento em Rua 280 - Meia praia - Itapema/SC', 'Apartamento em Rua 280 - Meia Praia - Itapema/SC'], 'apartamento em rua 252 - meia praia - itapema/sc': ['Apartamento em Rua 252 - Meia praia - Itapema/SC', 'Apartamento em Rua 252 - Meia Praia - Itapema/SC'], 'apartamento em rua 607 - tabuleiro dos oliveiras - itapema/sc': ['Apartamento em Rua 607 - Tabuleiro dos Oliveiras - Itapema/SC', 'Apartamento em rUA 607 - Tabuleiro dos Oliveiras - Itapema/SC'], 'apartamento em rua 277 - meia praia - itapema/sc': ['Apartamento em Rua 277 - Meia Praia - Itapema/SC', 'Apartamento em Rua 277 - Meia praia - Itapema/SC'], 'apartamento em rua 284 - meia praia - itapema/sc': ['Apartamento em Rua 284 - Meia praia - Itapema/SC', 'Apartamento em Rua 284 - Meia Praia - Itapema/SC'], 'apartamento em rua 295 - meia praia - itapema/sc': ['Apartamento em Rua 295 - Meia praia - Itapema/SC', 'Apartamento em Rua 295 - Meia Praia - Itapema/SC'], 'apartamento em rua 278 - meia praia - itapema/sc': ['Apartamento em Rua 278 - Meia praia - Itapema/SC', 'Apartamento em Rua 278 - Meia Praia - Itapema/SC'], 'apartamento em rua 318 - meia praia - itapema/sc': ['Apartamento em Rua 318 - Meia Praia - Itapema/SC', 'Apartamento em Rua 318 - Meia praia - Itapema/SC'], 'apartamento em rua 248 - meia praia - itapema/sc': ['Apartamento em Rua 248 - Meia praia - Itapema/SC', 'Apartamento em Rua 248 - Meia Praia - Itapema/SC'], 'edifício everest': ['Edifício Everest', 'EDIFÍCIO EVEREST'], 'sala comercial em rua 256 - meia praia - itapema/sc': ['Sala comercial em Rua 256 - Meia praia - Itapema/SC', 'Sala comercial em Rua 256 - Meia Praia - Itapema/SC'], 'apartamento em rua 301 - meia praia - itapema/sc': ['Apartamento em Rua 301 - Meia praia - Itapema/SC', 'Apartamento em Rua 301 - Meia Praia - Itapema/SC'], 'apartamento vista mar em itapema': ['Apartamento Vista Mar em Itapema', 'Apartamento Vista mar em Itapema'], 'apartamento em rua 402 b - morretes - itapema/sc': ['Apartamento em RUA 402 B - Morretes - Itapema/SC', 'Apartamento em Rua 402 B - Morretes - Itapema/SC'], 'apartamento em av. beira mar - centro - itapema/sc': ['Apartamento em Av. Beira Mar - Centro - Itapema/SC', 'Apartamento em av. beira mar - Centro - Itapema/SC'], 'canvas residence': ['CANVAS RESIDENCE', 'Canvas Residence'], 'apartamento 4 dormitórios para venda em itapema, meia praia, 4 dormitórios, 4 suítes, 5 banheiros, 3': ['Apartamento 4 dormitórios para Venda em Itapema, meia praia, 4 dormitórios, 4 suítes, 5 banheiros, 3', 'Apartamento 4 dormitórios para Venda em Itapema, Meia Praia, 4 dormitórios, 4 suítes, 5 banheiros, 3'], 'edificio rosas de provence': ['EDIFICIO ROSAS DE PROVENCE', 'Edificio Rosas de Provence'], 'apartamento em rua 254 - meia praia - itapema/sc': ['Apartamento em Rua 254 - Meia Praia - Itapema/SC', 'Apartamento em Rua 254 - Meia praia - Itapema/SC'], 'apartamento quadra mar': ['Apartamento Quadra Mar', 'Apartamento quadra mar'], 'san martin': ['SAN MARTIN', 'San Martin'], 'apartamento 03 suítes sendo 01 master em meia praia, itapema.': ['Apartamento 03 Suítes sendo 01 Master em Meia Praia, Itapema.', 'Apartamento 03 suítes sendo 01 master em Meia Praia, Itapema.'], 'central tower - unidade 1001': ['CENTRAL TOWER - UNIDADE 1001', 'Central Tower - Unidade 1001'], 'apartamento 3 suítes, mobiliado, itapema sc': ['Apartamento 3 suítes, mobiliado, Itapema SC', 'APARTAMENTO 3 SUÍTES, MOBILIADO, ITAPEMA SC'], 'apartamento mobiliado com três quartos na meia praia itapema sc': ['Apartamento mobiliado com três quartos na Meia Praia Itapema SC', 'Apartamento mobiliado com três quartos na Meia praia Itapema SC'], 'apartamento em rua 303 - meia praia - itapema/sc': ['Apartamento em rua 303 - Meia praia - Itapema/SC', 'Apartamento em Rua 303 - Meia Praia - Itapema/SC', 'Apartamento em Rua 303 - Meia praia - Itapema/SC'], 'apartamento em rua 321 - meia praia - itapema/sc': ['Apartamento em Rua 321 - Meia praia - Itapema/SC', 'Apartamento em Rua 321 - Meia Praia - Itapema/SC'], 'imperial palace': ['IMPERIAL PALACE', 'Imperial Palace'], 'edifício palazzo del mare': ['EDIFÍCIO PALAZZO DEL MARE', 'Edifício Palazzo Del Mare'], 'apartamento em rua 286 - meia praia - itapema/sc': ['Apartamento em Rua 286 - Meia praia - Itapema/SC', 'Apartamento em Rua 286 - Meia Praia - Itapema/SC'], 'apartamento vista mar': ['Apartamento vista mar', 'APARTAMENTO VISTA MAR', 'Apartamento Vista Mar'], 'apartamento alto padrão meia praia': ['apartamento alto padrão Meia Praia', 'Apartamento alto padrão Meia Praia'], 'apartamento para venda em itapema, morretes, 2 dormitórios, 2 suítes, 3 banheiros, 1 vaga': ['Apartamento para Venda em Itapema, morretes, 2 dormitórios, 2 suítes, 3 banheiros, 1 vaga', 'Apartamento para Venda em Itapema, MORRETES, 2 dormitórios, 2 suítes, 3 banheiros, 1 vaga'], 'apartamento em rua 266 - meia praia - itapema/sc': ['Apartamento em Rua 266 - Meia Praia - Itapema/SC', 'Apartamento em Rua 266 - Meia praia - Itapema/SC'], 'brooklyn tower': ['BROOKLYN TOWER', 'Brooklyn Tower'], 'apartamento vista mar meia praia': ['Apartamento vista mar Meia Praia', 'Apartamento Vista Mar Meia Praia'], 'magnum cna home': ['MAGNUM CNA HOME', 'Magnum CNA Home'], 'apartamento em av nereu ramos - meia praia - itapema/sc': ['Apartamento em Av Nereu Ramos - Meia Praia - Itapema/SC', 'Apartamento em Av nereu ramos - Meia Praia - Itapema/SC'], 'apartamento em rua 265 - meia praia - itapema/sc': ['Apartamento em Rua 265 - Meia Praia - Itapema/SC', 'Apartamento em rua 265 - Meia praia - Itapema/SC'], 'arcos da lapa': ['Arcos da Lapa', 'ARCOS DA LAPA'], 'apartamento em rua 258 - meia praia - itapema/sc': ['Apartamento em Rua 258 - Meia praia - Itapema/SC', 'Apartamento em Rua 258 - Meia Praia - Itapema/SC'], 'apartamento diferenciado': ['APARTAMENTO DIFERENCIADO', 'Apartamento Diferenciado', 'Apartamento diferenciado'], 'apartamento 3 dormitórios para venda em itapema, centro, 3 dormitórios, 3 suítes, 4 banheiros, 2 vag': ['Apartamento 3 dormitórios para Venda em Itapema, CENTRO, 3 dormitórios, 3 suítes, 4 banheiros, 2 vag', 'Apartamento 3 dormitórios para Venda em Itapema, Centro, 3 dormitórios, 3 suítes, 4 banheiros, 2 vag'], 'apartamento em 236 - meia praia - itapema/sc': ['Apartamento em 236 - Meia Praia - Itapema/SC', 'Apartamento em 236 - Meia praia - Itapema/SC'], 'ed. murano': ['ED. MURANO', 'Ed. Murano'], 'apartamento 2 dormitórios para venda em itapema, morretes, 2 dormitórios, 1 suíte, 2 banheiros, 1 va': ['Apartamento 2 dormitórios para Venda em Itapema, MORRETES, 2 dormitórios, 1 suíte, 2 banheiros, 1 va', 'Apartamento 2 dormitórios para Venda em Itapema, Morretes, 2 dormitórios, 1 suíte, 2 banheiros, 1 va'], 'apartamento a venda, 3 quartos, morretes, itapema-sc.': ['Apartamento a venda, 3 quartos, morretes, Itapema-SC.', 'Apartamento a venda, 3 quartos, Morretes, Itapema-sc.'], 'apartamento 3 suítes em itapema': ['APARTAMENTO 3 SUÍTES EM ITAPEMA', 'Apartamento 3 suítes em Itapema'], 'apartamento 3 quartos , sendo 3 suítes': ['Apartamento 3 Quartos , sendo 3 Suítes', 'Apartamento 3 Quartos , sendo 3 suítes'], 'apartamento com vista mar e 3 suítes à venda, 114 m² em meia praia - itapema/sc': ['Apartamento com VISTA MAR e 3 Suítes à venda, 114 m² em Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 3 suítes à venda, 114 m² em Meia Praia - Itapema/SC'], 'apartamento à venda de 03 quartos em itapema sc': ['Apartamento à venda de 03 quartos em Itapema SC', 'APARTAMENTO À VENDA DE 03 QUARTOS EM ITAPEMA SC'], 'apartamento 03 dormitórios sendo 01 suíte em meia praia, itapema.': ['Apartamento 03 Dormitórios sendo 01 Suíte em Meia Praia, Itapema.', 'Apartamento 03 dormitórios sendo 01 suíte em Meia Praia, Itapema.'], 'apartamento finamente mobiliado 03 suítes em meia praia, itapema.': ['Apartamento finamente mobiliado 03 suítes em Meia Praia, Itapema.', 'Apartamento Finamente Mobiliado 03 Suítes em Meia Praia, Itapema.'], 'apartamento com vista mar e 4 suítes à venda, meia praia - itapema/sc': ['Apartamento com vista mar e 4 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 4 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 4 Suítes à venda, Meia Praia - Itapema/SC'], 'linder palace': ['LINDER PALACE', 'Linder Palace'], 'apartamento finamente mobiliado': ['Apartamento finamente mobiliado', 'Apartamento Finamente Mobiliado'], 'ed. província di vicenza': ['Ed. Província di Vicenza', 'ED. PROVÍNCIA DI VICENZA'], 'cobertura villa toscana': ['COBERTURA VILLA TOSCANA', 'Cobertura Villa Toscana'], 'le tre torri residenziale ap 803 bloco 1': ['Le Tre Torri Residenziale AP 803 Bloco 1', 'LE TRE TORRI RESIDENZIALE AP 803 BLOCO 1'], 'apartamento frente mar': ['Apartamento frente mar', 'Apartamento Frente Mar'], 'apartamento com 4 suítes à venda, meia praia - itapema/sc': ['Apartamento com 4 Suítes à venda, Meia Praia - Itapema/SC', 'Apartamento com 4 suítes à venda, Meia Praia - Itapema/SC'], 'edíficio saint antoine': ['Edíficio Saint Antoine', 'EDÍFICIO SAINT ANTOINE'], 'apartamento com vista mar e 3 suítes à venda, 123 m² em meia praia - itapema/sc': ['Apartamento com VISTA MAR e 3 Suítes à venda, 123 m² em Meia Praia - Itapema/SC', 'Apartamento com VISTA MAR e 3 suítes à venda, 123 m² em Meia Praia - Itapema/SC'], 'apartamento mobiliado com 4 suítes à venda, meia praia - itapema/sc': ['Apartamento mobiliado com 4 suítes à venda, Meia Praia - Itapema/SC', 'Apartamento Mobiliado com 4 suítes à venda, Meia Praia - Itapema/SC'], 'place vendome - unidade 1002': ['Place Vendome - Unidade 1002', 'PLACE VENDOME - UNIDADE 1002'], 'residencial magnum': ['RESIDENCIAL MAGNUM', 'Residencial Magnum'], 'apartamento mobiliado à venda em meia praia, itapema - sc': ['Apartamento Mobiliado à venda em Meia Praia, Itapema - SC', 'Apartamento mobiliado à venda em Meia Praia, Itapema - SC'], 'mar das arábias': ['Mar das Arábias', 'MAR DAS ARÁBIAS'], 'apartamento 3 suítes, quadra mar , itapema sc': ['Apartamento 3 suítes, quadra mar , Itapema SC', 'Apartamento 3 suítes, Quadra mar , Itapema SC'], 'apartamento 3 suítes 2 vagas em itapema!': ['Apartamento 3 Suítes 2 vagas em Itapema!', 'Apartamento 3 Suítes 2 Vagas em Itapema!'], 'apartamento para venda em itapema, centro, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas': ['Apartamento para Venda em Itapema, Centro, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas', 'Apartamento para Venda em Itapema, CENTRO, 4 dormitórios, 4 suítes, 5 banheiros, 3 vagas'], 'apartamento 4 suítes, vista mar, itapema sc': ['Apartamento 4 Suítes, vista mar, Itapema SC', 'Apartamento 4 suítes, vista mar, Itapema SC'], 'apartamento 3 suítes mobiliado e decorado à venda em meia praia, itapema/sc': ['Apartamento 3 suítes MOBILIADO e DECORADO à venda em Meia Praia, Itapema/SC', 'Apartamento 3 suítes MOBILIADO E DECORADO à venda em Meia Praia, Itapema/SC'], 'itapema - apartamento padrão - jardim praia mar': ['ITAPEMA - Apartamento Padrão - Jardim Praia Mar', 'Itapema - Apartamento Padrão - Jardim Praia Mar'], 'itapema - apartamento padrão - várzea': ['Itapema - Apartamento Padrão - Várzea', 'ITAPEMA - Apartamento Padrão - Várzea'], 'lá lumiere': ['LÁ LUMIERE', 'Lá Lumiere'], 'itapema - apartamento padrão - tabuleiro dos oliveiras': ['Itapema - Apartamento Padrão - Tabuleiro dos Oliveiras', 'ITAPEMA - Apartamento Padrão - Tabuleiro dos Oliveiras'], 'lindo apartamento com 4 suítes à venda, meia praia - itapema/sc': ['Lindo Apartamento com 4 Suítes à venda, Meia Praia - Itapema/SC', 'Lindo Apartamento com 4 suítes à venda, Meia Praia - Itapema/SC']}`
- **`business_types`**: 2 categorias (non-null 8329)
  - Top: `Venda`:8327, `Ambos`:2
  - Inconsistentes: Nenhum problema encontrado
- **`listing_type`**: 5 categorias (non-null 8329)
  - Top: `apartamento`:7529, `casa`:547, `terreno`:164, `comercial`:79, `outros`:10
  - Inconsistentes: Nenhum problema encontrado
- **`property_type`**: 1 categorias (non-null 8329)
  - Top: `UNIT`:8329
  - Inconsistentes: Nenhum problema encontrado
- **`rental_period`**: 2 categorias (non-null 8329)
  - Top: `<NA>`:8327, `MONTHLY`:2
  - Inconsistentes: Nenhum problema encontrado
- **`amenities`**: 5037 categorias (non-null 8329)
  - Top: `[]`:420, `["KITCHEN"]`:231, `["GARAGE"]`:216, `["POOL", "BARBECUE_GRILL", "ELEVATOR", "GYM", "PETS_ALLOWED", "GOURMET_SPACE", "PLAYGROUND", "PARTY_HALL", "DEPOSIT", "ADULT_GAME_ROOM"]`:78, `["BARBECUE_GRILL", "BALCONY", "PETS_ALLOWED", "AIR_CONDITIONING", "SERVICE_AREA", "BICYCLES_PLACE", "DISABLED_ACCESS", "ELECTRONIC_GATE"]`:70
  - Inconsistentes: Nenhum problema encontrado
- **`state`**: 1 categorias (non-null 8327)
  - Top: `SC`:8327
  - Inconsistentes: Nenhum problema encontrado
- **`city`**: 1 categorias (non-null 8329)
  - Top: `Itapema`:8329
  - Inconsistentes: Nenhum problema encontrado
- **`suburb`**: 25 categorias (non-null 8231)
  - Top: `Meia Praia`:3452, `Morretes`:1777, `Centro`:1009, `Andorinha`:782, `Castelo Branco`:510
  - **Inconsistentes:** `{'meia praia': ['Meia Praia', 'Meia praia', 'MEIA PRAIA', 'meia praia'], 'centro': ['Centro', 'CENTRO'], 'sertão do trombudo': ['Sertão do Trombudo', 'Sertão Do Trombudo']}`
- **`advertiser_name`**: 471 categorias (non-null 8329)
  - Top: `USUÁRIO NEWCORE`:625, `Nei Costa`:555, `Imobille Negócios Imobiliários`:493, `Eraci Eponina Jaques de Oliveira`:399, `Airton Investimentos Imobiliários Itapema`:396
  - Inconsistentes: Nenhum problema encontrado
- **`portal`**: 1 categorias (non-null 8329)
  - Top: `GRUPOZAP`:8329
  - Inconsistentes: Nenhum problema encontrado

### Valores suspeitos / impossíveis / fora do padrão
- usable_area=0: 11
- amenities=[]: 420
- monthly_condo_fee vazio: 2490
- yearly_iptu vazio: 2714
- suburb none/vazio em VivaReal: 98

### Formatação para futuros JOINs (IDs)
- listing_id: tamanhos variados {10: 8328, 8: 1}
- listing_id: 36 duplicados (esperado - historico)

### Erro vs Legítimo
- `amenities=[]` = **legítimo**
- `monthly_condo_fee` vazio = **legítimo**
- `sale_price=0` / `usable_area=0` = **erro/impossível**

---
## Chaves de Relacionamento (sem JOIN, recomputado)
- **Details vs Mesh** | chave `airbnb_listing_id` | {'chave': 'airbnb_listing_id', 'par': 'Details vs Mesh', 'details_total': 4441, 'mesh_total': 4441, 'intersecao': 4441, 'so_details': 0, 'so_mesh': 0, 'compativel': True, 'obs': '100% compatível'}
- **Details vs Price** | chave `airbnb_listing_id` | {'chave': 'airbnb_listing_id', 'par': 'Details vs Price', 'details_total': 4441, 'price_total_distinct': 1005, 'intersecao': 999, 'so_details': 3442, 'so_price': 6, 'compativel': False, 'obs': 'Cobertura parcial: 999/4441 (22.5%) de Details têm preço; 6 ids em Price não existem em Details'}
- **Mesh vs Price** | chave `airbnb_listing_id` | {'chave': 'airbnb_listing_id', 'par': 'Mesh vs Price', 'mesh_total': 4441, 'price_total_distinct': 1005, 'intersecao': 999, 'so_mesh': 3442, 'so_price': 6, 'compativel': True, 'obs': '999 em comum; 6 em Price sem Mesh'}
- **Details vs Hosts** | chave `owner_id` | {'chave': 'owner_id', 'par': 'Details vs Hosts', 'details_total_distinct': 3057, 'hosts_total_distinct': 3057, 'intersecao': 3057, 'so_details': 0, 'so_hosts': 0, 'compativel': True, 'obs': 'Verificar 1 a 1'}
- **Details_Itapema.csv** | chave `airbnb_listing_id formato` | {'chave': 'airbnb_listing_id formato', 'par': 'Details_Itapema.csv', 'distribuicao_tamanhos': {18: 944, 19: 2129, 7: 25, 8: 1342, 6: 1}, 'exemplo': ['828307537051457546', '985445004274818605'], 'obs': 'Tamanhos consistentes ~19 dígitos se 1 tamanho'}
- **Mesh_Ids_Data_Itapema.csv** | chave `airbnb_listing_id formato` | {'chave': 'airbnb_listing_id formato', 'par': 'Mesh_Ids_Data_Itapema.csv', 'distribuicao_tamanhos': {18: 944, 19: 2129, 7: 25, 8: 1342, 6: 1}, 'exemplo': ['828307537051457546', '985445004274818605'], 'obs': 'Tamanhos consistentes ~19 dígitos se 1 tamanho'}
- **Price_AV_Itapema.csv** | chave `airbnb_listing_id formato` | {'chave': 'airbnb_listing_id formato', 'par': 'Price_AV_Itapema.csv', 'distribuicao_tamanhos': {18: 243, 8: 520, 7: 12, 19: 230}, 'exemplo': ['721635424816164605', '985445004274818605'], 'obs': 'Tamanhos consistentes ~19 dígitos se 1 tamanho'}

---
## Resumo por Arquivo (formato solicitado)
### Details_Itapema.csv
* **Linhas:** 4441
* **Colunas:** 35
* **Principais problemas:** `space` 2527 nulos (56.9%); `safety_features` 3137 placeholders (70.6%); `check_in` 446 placeholders (10.0%); `check_out` 842 placeholders (19.0%); `is_new_listing` 874 nulos (19.7%); 5 tipos de valores suspeitos
* **Problemas que precisam de limpeza:** Normalizar encoding; Tratar lat/lon 0 como NULL+flag; Tratar star 0 sem reviews como NULL lógico; Strip IDs antes de JOIN
* **Problemas que podem ser mantidos:** space vazio 56% (opcional); is_professional vazio (flag unknown); cleaning_fee 0; check_in/out <NA> como placeholder
* **Observações importantes para a análise:** Cobertura Price 22.5% limita receita; Mesh 100% para localização

### Hosts_ids_Itapema.csv
* **Linhas:** 4440
* **Colunas:** 11
* **Principais problemas:** `response_rate_shown` 4440 placeholders (100.0%); `response_time_shown` 4440 placeholders (100.0%); 3 tipos de valores suspeitos
* **Problemas que precisam de limpeza:** Strip IDs; Tratar <NA> como sentinela
* **Problemas que podem ser mantidos:** years_host 0 com months>0; response_* <NA> como sentinela
* **Observações importantes para a análise:** OK

### Mesh_Ids_Data_Itapema.csv
* **Linhas:** 4441
* **Colunas:** 8
* **Principais problemas:** 1 tipos de valores suspeitos
* **Problemas que precisam de limpeza:** Tratar suburb none/vazio como SEM_BAIRRO+flag; Strip IDs
* **Problemas que podem ser mantidos:** country/state/city constantes
* **Observações importantes para a análise:** OK

### Price_AV_Itapema.csv
* **Linhas:** 118839
* **Colunas:** 4
* **Principais problemas:** 1 tipos de valores suspeitos
* **Problemas que precisam de limpeza:** Verificar price 0/outliers; Strip IDs
* **Problemas que podem ser mantidos:** airbnb_listing_id duplicado (histórico)
* **Observações importantes para a análise:** OK

### VivaReal_Itapema.csv
* **Linhas:** 8329
* **Colunas:** 22
* **Principais problemas:** 35 linhas 100% duplicadas; `rental_price` 8327 nulos (100.0%); `rental_period` 8327 placeholders (100.0%); `yearly_iptu` 2714 nulos (32.6%); `monthly_condo_fee` 2490 nulos (29.9%); 5 tipos de valores suspeitos
* **Problemas que precisam de limpeza:** Tratar suburb none/vazio; Strip IDs; Verificar sale_price/area 0
* **Problemas que podem ser mantidos:** amenities []; condo_fee/iptu vazio; rental_price vazio (venda)
* **Observações importantes para a análise:** OK

---
## Tabela Final de Problemas

| Arquivo | Problema | Quantidade | Gravidade (baixa/média/alta) | Precisa tratar? | Tratamento recomendado |
|---|---|---|---|---|---|
| `Details_Itapema.csv` | `space` nulos | 2527 (56.9%) | média | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `Details_Itapema.csv` | `safety_features` placeholders | 3137 (70.6%) | média | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Details_Itapema.csv` | `check_in` placeholders | 446 (10.0%) | baixa | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Details_Itapema.csv` | `check_out` placeholders | 842 (19.0%) | baixa | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Details_Itapema.csv` | `can_instant_book` placeholders | 355 (8.0%) | baixa | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Details_Itapema.csv` | `is_professional` nulos | 355 (8.0%) | baixa | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `Details_Itapema.csv` | `is_new_listing` nulos | 874 (19.7%) | baixa | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `Details_Itapema.csv` | latitude/longitude = 0 (Details sem geolocalização, usar Mesh): 4441 casos (100. | 0 | alta | Sim | Ver seção suspeitos |
| `Details_Itapema.csv` | picture_count=0 mas is_guest_favorite=true: 81 casos (suspeito) | 0 | média | Sinalizar | Ver seção suspeitos |
| `Details_Itapema.csv` | number_of_bedrooms >=8: 9 casos (ex: 12,16) | 8 | baixa | Sinalizar | Ver seção suspeitos |
| `Details_Itapema.csv` | cleaning_fee=0: 939 casos (pode ser legitimo) | 0 | baixa | Sinalizar | Ver seção suspeitos |
| `Details_Itapema.csv` | is_professional vazio (nulo): 355 | 355 | baixa | Sinalizar | Ver seção suspeitos |
| `Details_Itapema.csv` | Formato JOIN: airbnb_listing_id: tamanhos variados {19: 2129, 18: 944, 8: 1342, 6: 1 | 19 | média | Sim | Aplicar strip() nos IDs |
| `Details_Itapema.csv` | Formato JOIN: owner_id: tamanhos variados {9: 3856, 8: 537, 7: 45, 6: 3} | 9 | média | Sim | Aplicar strip() nos IDs |
| `Details_Itapema.csv` | Formato JOIN: owner_id: 1384 duplicados (esperado - host com multiplos listings) | 1384 | média | Sim | Aplicar strip() nos IDs |
| `Details_Itapema.csv` | Linhas 100% duplicadas | 0 | baixa | Não | Nenhum problema encontrado |
| `Details_Itapema.csv` | `owner_id` duplicados | 1384 | baixa | Não (esperado) | Manter - host com multiplos listings; usar distinct para contar hosts |
| `Hosts_ids_Itapema.csv` | `response_rate_shown` placeholders | 4440 (100.0%) | média | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Hosts_ids_Itapema.csv` | `response_time_shown` placeholders | 4440 (100.0%) | média | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `Hosts_ids_Itapema.csv` | response_rate_shown/response_time_shown com <NA>: 8880 placeholders | 8880 | baixa | Sinalizar | Ver seção suspeitos |
| `Hosts_ids_Itapema.csv` | years_host=0: 921 casos | 0 | baixa | Sinalizar | Ver seção suspeitos |
| `Hosts_ids_Itapema.csv` | star_rating_host=0.0: 854 | 0 | baixa | Sinalizar | Ver seção suspeitos |
| `Hosts_ids_Itapema.csv` | Formato JOIN: owner_id: tamanhos variados {9: 3855, 8: 537, 7: 45, 6: 3} | 9 | média | Sim | Aplicar strip() nos IDs |
| `Hosts_ids_Itapema.csv` | Formato JOIN: owner_id: 1383 duplicados (esperado - mesmo host em multiplos listings | 1383 | média | Sim | Aplicar strip() nos IDs |
| `Hosts_ids_Itapema.csv` | Linhas 100% duplicadas | 0 | baixa | Não | Nenhum problema encontrado |
| `Hosts_ids_Itapema.csv` | `owner_id` duplicados | 1383 | baixa | Não (esperado) | Manter - host com multiplos listings; usar distinct para contar hosts |
| `Mesh_Ids_Data_Itapema.csv` | suburb = none ou vazio: 5 | 5 | baixa | Sinalizar | Ver seção suspeitos |
| `Mesh_Ids_Data_Itapema.csv` | Formato JOIN: airbnb_listing_id: tamanhos variados {19: 2129, 18: 944, 8: 1342, 7: 2 | 19 | média | Sim | Aplicar strip() nos IDs |
| `Mesh_Ids_Data_Itapema.csv` | Linhas 100% duplicadas | 0 | baixa | Não | Nenhum problema encontrado |
| `Price_AV_Itapema.csv` | price max muito alto: 29000.0 | 29000 | baixa | Sinalizar | Ver seção suspeitos |
| `Price_AV_Itapema.csv` | Formato JOIN: airbnb_listing_id: tamanhos variados {19: 32742, 8: 57422, 18: 27532,  | 19 | média | Sim | Aplicar strip() nos IDs |
| `Price_AV_Itapema.csv` | Formato JOIN: airbnb_listing_id: 117834 duplicados (esperado - historico) | 117834 | média | Sim | Aplicar strip() nos IDs |
| `Price_AV_Itapema.csv` | Linhas 100% duplicadas | 0 | baixa | Não | Nenhum problema encontrado |
| `Price_AV_Itapema.csv` | `airbnb_listing_id` duplicados | 117834 | baixa | Não (esperado) | Manter - histórico temporal |
| `VivaReal_Itapema.csv` | `rental_price` nulos | 8327 (100.0%) | média | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `VivaReal_Itapema.csv` | `rental_period` placeholders | 8327 (100.0%) | média | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |
| `VivaReal_Itapema.csv` | `yearly_iptu` nulos | 2714 (32.6%) | média | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `VivaReal_Itapema.csv` | `monthly_condo_fee` nulos | 2490 (29.9%) | média | Não (sinalizar) | Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico |
| `VivaReal_Itapema.csv` | usable_area=0: 11 | 0 | baixa | Sinalizar | Ver seção suspeitos |
| `VivaReal_Itapema.csv` | amenities=[]: 420 | 420 | baixa | Sinalizar | Ver seção suspeitos |
| `VivaReal_Itapema.csv` | monthly_condo_fee vazio: 2490 | 2490 | baixa | Sinalizar | Ver seção suspeitos |
| `VivaReal_Itapema.csv` | yearly_iptu vazio: 2714 | 2714 | baixa | Sinalizar | Ver seção suspeitos |
| `VivaReal_Itapema.csv` | suburb none/vazio em VivaReal: 98 | 98 | baixa | Sinalizar | Ver seção suspeitos |
| `VivaReal_Itapema.csv` | Formato JOIN: listing_id: tamanhos variados {10: 8328, 8: 1} | 10 | média | Sim | Aplicar strip() nos IDs |
| `VivaReal_Itapema.csv` | Formato JOIN: listing_id: 36 duplicados (esperado - historico) | 36 | média | Sim | Aplicar strip() nos IDs |
| `VivaReal_Itapema.csv` | Linhas 100% duplicadas | 35 | média | Sim (deduplicar) | Remover duplicatas mantendo 1, flag is_duplicate |
| `VivaReal_Itapema.csv` | `listing_id` duplicados | 36 | baixa | Não (esperado) | Manter - histórico temporal |
| `CHAVES` | Chave airbnb_listing_id Details vs Mesh cobertura | interseção 4441 | média | Sim (documentar) | 100% compatível |
| `CHAVES` | Chave airbnb_listing_id Details vs Price cobertura | interseção 999 | alta | Sim (documentar) | Cobertura parcial: 999/4441 (22.5%) de Details têm preço; 6 ids em Price não existem em Details |
| `CHAVES` | Chave airbnb_listing_id Mesh vs Price cobertura | interseção 999 | média | Sim (documentar) | 999 em comum; 6 em Price sem Mesh |
| `CHAVES` | Chave owner_id Details vs Hosts cobertura | interseção 3057 | média | Sim (documentar) | Verificar 1 a 1 |

_Se não encontrar um problema em alguma categoria, consta como 'Nenhum problema encontrado' nas seções acima._

## Observações Finais
- **READ-ONLY confirmado:** nenhum `data/*.csv` foi alterado, nenhuma linha excluída, nenhum valor substituído, nenhum JOIN executado.
- **Placeholders `<NA>`/`não informado` foram contados separadamente de nulos.**
- **Zeros mantidos:** `0`/`0.0` não convertidos para nulo; sinalizados apenas quando suspeitos (ex: lat/lon 0).
- **Reprodutível:** `python analysis/audit.py` gera este `relatorio_auditoria.md` a partir de leitura `csv` com `utf-8 errors=replace`.
