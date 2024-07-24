from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# TOKEN / ID ===================================
PIPEFY_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MDQyMDIzOTMsImp0aSI6IjAyZmI0MGFmLWYwNGQtNGNjMi05Yjc4LWJkZmQ5YzhhZWM4NCIsInN1YiI6MzA0MTY1MTY2LCJ1c2VyIjp7ImlkIjozMDQxNjUxNjYsImVtYWlsIjoiZGVzYWZpb2ludGVncmFjYW9AcHJvZmVjdHVtLmNvbS5iciIsImFwcGxpY2F0aW9uIjozMDAzMDU3MDEsInNjb3BlcyI6W119LCJpbnRlcmZhY2VfdXVpZCI6bnVsbH0.NDCy-EvEyaQpct5lEeaXRdCCWCuU4K-DRggf2wdZIsVMo8tIwk0kY7bPVPnngajjULE_hF-O0rqqydkyzJiNBA'
PIPE_ID = '303843596'

# HEADER =======================================
HEADERS = {
    'Authorization': f'Bearer {PIPEFY_TOKEN}',
    'Content-Type': 'application/json'
}
BASE_URL = 'https://api.pipefy.com/graphql' 

#PHASES ========================================
@app.route('/pipefy', methods=['GET'])
def pipefy():
    query = '''
    query {
        pipe(id: "%s") {
            id
            name
            phases {
                id
                name
            }
        }
    }
    ''' % PIPE_ID
    
    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    data = response.json()
    return jsonify(data)
    if response.status_code == 200:
        return jsonify({'Message': 'Successful Operation', 'cards': data})
    else:
        return jsonify({'error': 'Failed to fetch cards', 'details': data}), response.status_code

# VISUALIZAR TODOS OS CARDS ========================================
@app.route('/allcards', methods=['GET'])
def all_cards():
    query = '''
    query {
      allCards(pipeId: "%s") {
        edges {
          node {
            id
            title
            current_phase {
              name
            }
          }
        }
      }
    }
    ''' % PIPE_ID

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    data = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Successful Operation', 'cards': data})
    else:
        return jsonify({'error': 'Failed to fetch cards', 'details': data}), response.status_code
    
# VISUALIZAR CARD ==========================================
@app.route('/viewcard', methods=['GET'])
def view_card():
    data = request.json
    card_id = data.get('card_id')
    query = '''
    query {
        card(id: %s){
            title
            id
            created_at
            fields {
                name
                value
                updated_at
            }
        }
    }
    ''' % card_id

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    data = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Successful Operation', 'cards': data})
    else:
        return jsonify({'error': 'Failed to fetch cards', 'details': data}), response.status_code

#CRIAR CARD =======================================
@app.route('/createcard', methods=['POST'])
def create_card():
    data = request.json
    title = data.get('title')
    name = data.get('name')
    birthdate = data.get('birthdate')
    cpf = data.get('cpf')
    phone = data.get('phone')
    hobbie = data.get('hobbie')
    city = data.get('city')
    
    mutation = '''
    mutation {
        createCard(input: {
            pipe_id: %s,
            title: "%s",
            fields_attributes: [
                {field_id: "nome", field_value: "%s"},
                {field_id: "data_de_nascimento", field_value: "%s"},
                {field_id: "cpf", field_value: "%s"},
                {field_id: "telefone", field_value: "%s"},
                {field_id: "hobbies", field_value: "%s"},
                {field_id: "cidade", field_value: "%s"}
            ]
        }) {
            card {
                title
                id
                fields{
                    name
                    value
                }
            }
        }
    }
    ''' % (PIPE_ID, title, name, birthdate, cpf, phone, hobbie, city)
    
    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    card = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Card Created Successfully !!!', 'card': card})
    else:
        return jsonify({'error': 'Failed to create card ... :(', 'details': card}), response.status_code

#DELETAR CARD ====================================================================
@app.route('/deletecard', methods=['DELETE'])
def delete_card():
    data = request.json
    CARD_ID = data.get('id')
    
    mutation = '''
    mutation {
        deleteCard(input: {id: %s}) {
        success
        }
    }
    ''' % CARD_ID
    
    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    card = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Card Deleted Successfully !!!', 'card': card})
    else:
        return jsonify({'error': 'Failed to delete card ... :(', 'details': card}), response.status_code

#MOVE FASE DO CARD ============================================
@app.route('/movephase', methods=['POST'])
def move_phase():
    data = request.json
    card_id = data.get('card_id')
    phase_id = data.get('phase_id')
    
    mutation = '''
    mutation {
        moveCardToPhase(input: {
            card_id: "%s",
            destination_phase_id: "%s"
        }) {
            card {
                id
                title
                current_phase {
                    id
                    name
                }
            }
        }
    }
    ''' % (card_id, phase_id)
    
    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    move_result = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Card moved successfully !!!', 'result': move_result})
    else:
        return jsonify({'error': 'Failed to move card', 'details': move_result}), response.status_code


#FIND TABLES (PRA ACHAR A CIDADE) =====================================
@app.route('/findtables', methods=['GET'])
def find_tables():
    data = request.json
    org_id = data.get('org_id')
    query = '''
    query {
        organization(id: "%s") {
            id
            tables {
                edges {
                    node {
                        name
                        internal_id
                    }
                }
            }
        }
    }
    ''' % org_id

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    move_result = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Tables Found !!!', 'result': move_result})
    else:
        return jsonify({'error': 'Failed to find tables', 'details': move_result}), response.status_code
    
#CHECAR ID CIDADES ===========================================================================================
@app.route('/cities', methods=['GET'])
def cities():
    data = request.json
    table_id = data.get('table_id')

    query = '''
    query {
        table_records(table_id: "%s") {
            edges {
                node {
                    id
                    title
                }
            }
        }
    }
    ''' % table_id

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    move_result = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Cities ID found !!!', 'result': move_result})
    else:
        return jsonify({'error': 'Failed to find ids', 'details': move_result}), response.status_code

#UPDATE FIELD DO CARD ============================================
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    card_id = data.get('card_id')
    field_id = data.get('field_id')
    new_value = data.get('new_value')
    
    mutation = '''
    mutation {
        updateCardField(input: {card_id: "%s", field_id: "%s", new_value: "%s"}) {
            card {
                title
                id
                fields {
                    name
                    value
                    updated_at
                }
            }
        }
    }
    ''' % (card_id, field_id, new_value)

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    move_result = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Card updated successfully !!!', 'result': move_result})
    else:
        return jsonify({'error': 'Failed to update card', 'details': move_result}), response.status_code
    
#VER FIELD ID ===============================================================
@app.route('/fieldID', methods=['GET'])
def field_id():
    
    query = '''
    query{
        pipe(id: %s) {
            start_form_fields {
            id
            label
            }
        }
    }
    ''' % PIPE_ID

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': query})
    move_result = response.json()
    if response.status_code == 200:
        return jsonify({'Message': 'Card showed successfully !!!', 'result': move_result})
    else:
        return jsonify({'error': 'Failed to show card', 'details': move_result}), response.status_code

# =====================================================================================================

if __name__ == '__main__':
    app.run(debug=True)