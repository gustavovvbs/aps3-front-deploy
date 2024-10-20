import streamlit as st
import requests

API_URL = 'https://aps3-deploy.onrender.com/'  

st.title('Sistema de Empréstimo de Bicicletas')

menu = ['Usuários', 'Bikes', 'Empréstimos']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Usuários':
    st.header('Usuários')
    action = st.radio('Ação', ['Visualizar', 'Adicionar', 'Editar', 'Deletar'], horizontal=True)

    if action == 'Visualizar':
        response = requests.get(f'{API_URL}/usuarios/')
        if response.status_code == 200:
            users = response.json()['usuarios']

            st.subheader('Visualizar Usuários')

            user_options = {user['nome']: user['_id'] for user in users}
            
            selected_user = st.selectbox('Selecione um usuário (opcional)', ['Todos'] + list(user_options.keys()))

            emprestimo_response = requests.get(f'{API_URL}/emprestimos/')
            emprestimo = []
            if selected_user == 'Todos':
                filtered_users = users
            else:
                filtered_users = [user for user in users if user['nome'] == selected_user]
                emprestimos = emprestimo_response.json().get('emprestimos', [])
                for e in emprestimos:
                    if e['id_usuario'] == user_options[selected_user]:
                        emprestimo = [e]
            if filtered_users:
                st.subheader('Lista de Usuários')
                st.table(filtered_users)
                if emprestimo != []:
                    st.subheader('Lista de Empréstimos do Usuário')
                    st.table(emprestimo)
                else:
                    pass
            else:
                st.info('Nenhum usuário encontrado.')
        else:
            st.error('Erro ao obter usuários')

    elif action == 'Adicionar':
        st.subheader('Adicionar Usuário')
        nome = st.text_input('Nome')
        data_nascimento = st.text_input('Data de Nascimento (dd/mm/aaaa)')
        cpf = st.text_input('CPF')
        if st.button('Adicionar'):
            data = {'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf}
            response = requests.post(f'{API_URL}/usuarios/', json=data)
            if response.status_code == 201:
                st.success('Usuário adicionado com sucesso')
            else:
                st.error(f"Erro ao adicionar usuário: {response.json().get('erro')}")

    elif action == 'Editar':
        st.subheader('Editar Usuário')
        response = requests.get(f'{API_URL}/usuarios/')
        if response.status_code == 200:
            users = response.json()['usuarios']
            if users:
                user_options = {f"{user['nome']} (CPF: {user['cpf']})": user for user in users}
                selected_user = st.selectbox('Selecione um usuário', list(user_options.keys()))
                user_data = user_options[selected_user]
                nome = st.text_input('Nome', value=user_data['nome'])
                data_nascimento = st.text_input('Data de Nascimento', value=user_data['data_nascimento'])
                cpf = st.text_input('CPF', value=user_data['cpf'])
                if st.button('Atualizar'):
                    data = {'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf}
                    id_usuario = user_data['_id']
                    response = requests.put(f'{API_URL}/usuarios/{id_usuario}', json=data)
                    if response.status_code == 200:
                        st.success('Usuário atualizado com sucesso')
                    else:
                        st.error(f"Erro ao atualizar usuário: {response.json().get('erro')}")
            else:
                st.info('Nenhum usuário encontrado para editar.')
        else:
            st.error('Erro ao obter usuários')

    elif action == 'Deletar':
        st.subheader('Deletar Usuário')
        response = requests.get(f'{API_URL}/usuarios/')
        if response.status_code == 200:
            users = response.json()['usuarios']
            if users:
                user_options = {f"{user['nome']} (CPF: {user['cpf']})": user for user in users}
                selected_user = st.selectbox('Selecione um usuário para deletar', list(user_options.keys()))
                user_data = user_options[selected_user]
                if st.button('Deletar'):
                    id_usuario = user_data['_id']
                    response = requests.delete(f'{API_URL}/usuarios/{id_usuario}')
                    if response.status_code == 200:
                        st.success('Usuário deletado com sucesso')
                    else:
                        st.error(f"Erro ao deletar usuário: {response.json().get('erro')}")
            else:
                st.info('Nenhum usuário encontrado para deletar.')
        else:
            st.error('Erro ao obter usuários')

elif choice == 'Bikes':
    st.header('Bikes')
    action = st.radio('Ação', ['Visualizar', 'Adicionar', 'Editar', 'Deletar'], horizontal=True)

    if action == 'Visualizar':
        response = requests.get(f'{API_URL}/bikes/')
        if response.status_code == 200:
            bikes = response.json()['bikes']

            st.subheader('Visualizar Bikes')

            bike_options = {bike['_id']: bike['_id'] for bike in bikes}
            
            selected_bike = st.selectbox('Selecione um usuário (opcional)', ['Todos'] + list(bike_options.keys()))

            emprestimo_response = requests.get(f'{API_URL}/emprestimos/')
            emprestimo = []
            if selected_bike == 'Todos':
                filtered_bikes = bikes
            else:
                filtered_bikes = [bike for bike in bikes if bike['_id'] == selected_bike]
                emprestimos = emprestimo_response.json().get('emprestimos', [])
                for e in emprestimos:
                    print(e)
                    if e['id_bike'] == bike_options[selected_bike]:
                        emprestimo = [e]
            if filtered_bikes:
                st.subheader('Lista de Bikes')
                st.table(filtered_bikes)
                if emprestimo != []:
                    st.subheader('Lista de Empréstimo da Bike')
                    st.table(emprestimo)
                else:
                    pass
            else:
                st.info('Nenhuma bike encontrada.')
        else:
            st.error('Erro ao obter bikes')

    elif action == 'Adicionar':
        st.subheader('Adicionar Bike')
        marca = st.text_input('Marca')
        modelo = st.text_input('Modelo')
        cidadeAlocada = st.text_input('Cidade Alocada')
        if st.button('Adicionar'):
            data = {'marca': marca, 'modelo': modelo, 'cidadeAlocada': cidadeAlocada}
            response = requests.post(f'{API_URL}/bikes/', json=data)
            if response.status_code == 201:
                st.success('Bike adicionada com sucesso')
            else:
                st.error(f"Erro ao adicionar bike: {response.json().get('erro')}")

    elif action == 'Editar':
        st.subheader('Editar Bike')
        response = requests.get(f'{API_URL}/bikes/')
        if response.status_code == 200:
            bikes = response.json()['bikes']
            if bikes:
                bike_options = {f"{bike['marca']} {bike['modelo']}": bike for bike in bikes}
                selected_bike = st.selectbox('Selecione uma bike', list(bike_options.keys()))
                bike_data = bike_options[selected_bike]
                print(bike_options)
                print(bike_data)
                marca = st.text_input('Marca', value=bike_data['marca'])
                modelo = st.text_input('Modelo', value=bike_data['modelo'])
                cidadeAlocada = st.text_input('Cidade Alocada', value=bike_data['cidadeAlocada'])
                status = st.selectbox('Status', ['Disponível', 'Ocupado'], index=0 if bike_data['status'] == 'Disponível' else 1)
                if st.button('Atualizar'):
                    data = {'marca': marca, 'modelo': modelo, 'cidadeAlocada': cidadeAlocada, 'status': status}
                    id_bike = bike_data['_id']
                    response = requests.put(f'{API_URL}/bikes/{id_bike}', json=data)
                    if response.status_code == 200:
                        st.success('Bike atualizada com sucesso')
                    else:
                        st.error(f"Erro ao atualizar bike: {response.json().get('erro')}")
            else:
                st.info('Nenhuma bike encontrada para editar.')
        else:
            st.error('Erro ao obter bikes')

    elif action == 'Deletar':
        st.subheader('Deletar Bike')
        response = requests.get(f'{API_URL}/bikes/')
        if response.status_code == 200:
            bikes = response.json()['bikes']
            if bikes:
                bike_options = {f"{bike['marca']} {bike['modelo']}": bike for bike in bikes}
                selected_bike = st.selectbox('Selecione uma bike para deletar', list(bike_options.keys()))
                bike_data = bike_options[selected_bike]
                if st.button('Deletar'):
                    id_bike = bike_data['_id']
                    response = requests.delete(f'{API_URL}/bikes/{id_bike}')
                    if response.status_code == 200:
                        st.success('Bike deletada com sucesso')
                    else:
                        st.error(f"Erro ao deletar bike: {response.json().get('erro')}")
            else:
                st.info('Nenhuma bike encontrada para deletar.')
        else:
            st.error('Erro ao obter bikes')

if choice == 'Empréstimos':
    st.header('Empréstimos')
    action = st.radio('Ação', ['Visualizar', 'Criar', 'Deletar'], horizontal=True)

    if action == 'Visualizar':
        st.subheader('Visualizar Empréstimos')

        user_response = requests.get(f'{API_URL}/usuarios/')
        bike_response = requests.get(f'{API_URL}/bikes/')

        if user_response.status_code == 200 and bike_response.status_code == 200:
            users = user_response.json().get('usuarios', [])
            bikes = bike_response.json().get('bikes', [])

            user_options = {user['nome']: user['_id'] for user in users}
            bike_options = {f"{bike['marca']} {bike['modelo']}": bike['_id'] for bike in bikes}

            selected_user = st.selectbox('Selecione um usuário (opcional)', ['Todos'] + list(user_options.keys()))
            selected_bike = st.selectbox('Selecione uma bike (opcional)', ['Todas'] + list(bike_options.keys()))

            response = requests.get(f'{API_URL}/emprestimos/')
            if response.status_code == 200:
                emprestimos = response.json().get('emprestimos', [])

                if selected_user != 'Todos' and selected_bike != 'Todas':
                    emprestimos = [e for e in emprestimos if e['id_usuario'] == user_options[selected_user] and e['id_bike'] == bike_options[selected_bike]]
                elif selected_user != 'Todos':
                    emprestimos = [e for e in emprestimos if e['id_usuario'] == user_options[selected_user]]
                elif selected_bike != 'Todas':
                    emprestimos = [e for e in emprestimos if e['id_bike'] == bike_options[selected_bike]]

                if emprestimos:
                    user_dict = {user['_id']: user['nome'] for user in users}
                    bike_dict = {bike['_id']: f"{bike['marca']} {bike['modelo']}" for bike in bikes}

                    emprestimos_data = []
                    for emprestimo in emprestimos:
                        usuario_nome = user_dict.get(emprestimo['id_usuario'], "Usuário não encontrado")
                        bike_desc = bike_dict.get(emprestimo['id_bike'], "Bike não encontrada")
                        emprestimos_data.append({
                            "ID": emprestimo['_id'],
                            "Usuário": usuario_nome,
                            "Bike": bike_desc,
                            "Data de Empréstimo": emprestimo['data_emprestimo'],
                            "Data de Devolução": emprestimo['data_devolucao']
                        })

                    st.subheader('Lista de Empréstimos')
                    st.table(emprestimos_data)
                else:
                    st.info('Nenhum empréstimo encontrado com os filtros aplicados.')
            else:
                st.error('Erro ao obter empréstimos.')
        else:
            st.error('Erro ao obter usuários ou bikes.')



    elif action == 'Criar':
        st.subheader('Criar Empréstimo')
        user_response = requests.get(f'{API_URL}/usuarios/')
        bike_response = requests.get(f'{API_URL}/bikes/')
        
        if user_response.status_code == 200 and bike_response.status_code == 200:
            users = user_response.json().get('usuarios', [])
            bikes = bike_response.json().get('bikes', [])

            if users and bikes:
                user_options = {}
                for user in users:
                        user_options[f"{user['nome']} (CPF: {user['cpf']})"] = user['_id']
                
                selected_user = st.selectbox('Selecione um usuário', list(user_options.keys()))
                id_usuario = user_options[selected_user]

                available_bikes = [bike for bike in bikes if bike.get('status') == 'Disponível']
                if available_bikes:
                    bike_options = {f"{bike['marca']} {bike['modelo']}": bike['_id'] for bike in available_bikes}
                    selected_bike = st.selectbox('Selecione uma bike disponível', list(bike_options.keys()))
                    id_bike = bike_options[selected_bike]

                    if st.button('Criar Empréstimo'):
                        url = f'{API_URL}/emprestimos/usuarios/{id_usuario}/bikes/{id_bike}'
                        response = requests.post(url)
                        if response.status_code == 201:
                            st.success('Empréstimo criado com sucesso')
                        else:
                            st.error(f"Erro ao criar empréstimo: {response.json().get('erro')}")
                else:
                    st.info('Nenhuma bike disponível para empréstimo.')
            else:
                st.info('Usuários ou bikes não encontrados.')
        else:
            st.error('Erro ao obter usuários ou bikes')


    elif action == 'Deletar':
        st.subheader('Deletar Empréstimo')
        response = requests.get(f'{API_URL}/emprestimos/')
        if response.status_code == 200:
            emprestimos = response.json().get('emprestimos', [])
            if emprestimos:
                emprestimo_options = {}
                for emprestimo in emprestimos:
                    print(emprestimo)
                    id_usuario = emprestimo.get('id_usuario')
                    id_bike = emprestimo.get('id_bike')
                    
                    if id_usuario and id_bike:
                        usuario_resp = requests.get(f'{API_URL}/usuarios/{id_usuario}')
                        bike_resp = requests.get(f'{API_URL}/bikes/{id_bike}')
                        if usuario_resp.status_code == 200 and bike_resp.status_code == 200:
                            usuario_nome = usuario_resp.json()['usuario'].get('nome', 'Desconhecido')
                            bike_info = bike_resp.json()['Bike']
                            bike_desc = f"{bike_info['marca']} {bike_info['modelo']}"
                            key = f"Usuário: {usuario_nome} - Bike: {bike_desc}"
                            emprestimo_options[key] = emprestimo['_id']
                        else:
                            continue
                
                if emprestimo_options:
                    selected_emprestimo = st.selectbox('Selecione um empréstimo para deletar', list(emprestimo_options.keys()))
                    id_emprestimo = emprestimo_options[selected_emprestimo]
                    if st.button('Deletar'):
                        response = requests.delete(f'{API_URL}/emprestimos/{id_emprestimo}')
                        if response.status_code == 200:
                            st.success('Empréstimo deletado com sucesso')
                        else:
                            st.error(f"Erro ao deletar empréstimo: {response.json().get('erro')}")
                else:
                    st.info('Nenhum empréstimo encontrado para deletar.')
            else:
                st.info('Nenhum empréstimo encontrado.')
        else:
            st.error('Erro ao obter empréstimos')
