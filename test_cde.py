import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from apps.eventos.models import Evento, TipoTicket
from apps.reservas.models import Reserva, Ticket
from apps.pagos.models import Pago

BASE_URL = 'http://localhost:8000'

def get_csrf_token(client, url):
    r = client.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    return s.find('input', {'name': 'csrfmiddlewaretoken'})['value']

def run_tests():
    client_a = requests.Session()
    client_b = requests.Session()
    
    User.objects.get_or_create(username='user_b', defaults={'email':'b@b.com', 'password':'pbkdf2_sha256$600000$xxx'})
    u = User.objects.get(username='user_b')
    u.set_password('user_b')
    u.save()
    
    print('--- LOGIN ---')
    csrf_a = get_csrf_token(client_a, f'{BASE_URL}/accounts/login/')
    client_a.post(f'{BASE_URL}/accounts/login/', data={'username': 'cliente_demo', 'password': 'cliente_demo', 'csrfmiddlewaretoken': csrf_a})
    csrf_b = get_csrf_token(client_b, f'{BASE_URL}/accounts/login/')
    client_b.post(f'{BASE_URL}/accounts/login/', data={'username': 'user_b', 'password': 'user_b', 'csrfmiddlewaretoken': csrf_b})
    
    print('--- TEST C1 & C2: Crear reserva ---')
    tt = TipoTicket.objects.filter(nombre='General').first()
    ev_id = tt.evento.id
    i_qty = tt.cantidad_disponible
    
    url_res = f'{BASE_URL}/reservas/crear/{ev_id}/'
    csrf_res = get_csrf_token(client_a, url_res)
    r_c1 = client_a.post(url_res, data={'tipo_ticket': tt.id, 'cantidad': 2, 'csrfmiddlewaretoken': csrf_res})
    tt.refresh_from_db()
    print(f'C1 Status: {r_c1.status_code == 200 and "mis_reservas" in r_c1.url or r_c1.status_code == 200}')
    print(f'C2 Disponibilidad (baja 2 tickets): {i_qty - 2 == tt.cantidad_disponible}')
    
    res_id = Reserva.objects.filter(usuario__username='cliente_demo').last().id
    
    print('--- TEST C3: Exceder cantidad ---')
    r_c3 = client_a.post(url_res, data={'tipo_ticket': tt.id, 'cantidad': 9999, 'csrfmiddlewaretoken': csrf_res})
    print(f'C3 Validation Error: {"Solo hay" in r_c3.text}')
    
    print('--- TEST C4: Preselección ---')
    r_c4 = client_a.get(f'{url_res}?tipo={tt.id}')
    s_c4 = BeautifulSoup(r_c4.text, 'html.parser')
    opt = s_c4.find('select', {'name': 'tipo_ticket'}).find('option', selected=True)
    print(f'C4 Preselected: {opt and int(opt["value"]) == tt.id}')
    
    print('--- TEST C6: Cancelación ajena ---')
    url_cancel = f'{BASE_URL}/reservas/cancelar/{res_id}/'
    r_c6 = client_b.get(url_cancel)
    print(f'C6 Forbidden/404 for User B: {r_c6.status_code == 404}')
    
    print('--- TEST D1: Crear pago ---')
    url_pago = f'{BASE_URL}/pagos/crear/{res_id}/'
    csrf_pago = get_csrf_token(client_a, url_pago)
    r_d1 = client_a.post(url_pago, data={'metodo': 'tarjeta', 'csrfmiddlewaretoken': csrf_pago})
    pago = Pago.objects.last()
    res_obj = Reserva.objects.get(id=res_id)
    print(f'D1 Pago aprobado: {pago.estado == "aprobado"}')
    print(f'D1 Reserva pendiente (Hallazgo): {res_obj.estado == "pendiente"}')
    
    print('--- TEST D3: No duplicar pago ---')
    r_d3 = client_a.get(url_pago)
    print(f'D3 Already paid msg: {"ya fue pagada" in r_d3.text or r_d3.url != url_pago}')
    
    print('--- TEST C5: Cancelar reserva ---')
    client_a.post(url_res, data={'tipo_ticket': tt.id, 'cantidad': 1, 'csrfmiddlewaretoken': csrf_res})
    res_cn = Reserva.objects.filter(usuario__username='cliente_demo', estado='pendiente').last()
    tt.refresh_from_db()
    q_bc = tt.cantidad_disponible
    client_a.post(f'{BASE_URL}/reservas/cancelar/{res_cn.id}/', data={'csrfmiddlewaretoken': csrf_res})
    tt.refresh_from_db()
    res_cn.refresh_from_db()
    print(f'C5 Cancelada: {res_cn.estado == "cancelada"}')
    print(f'C5 restored: {tt.cantidad_disponible == q_bc + 1}')
    
    print('--- TEST D2: No pagar cancelada ---')
    url_pg_cn = f'{BASE_URL}/pagos/crear/{res_cn.id}/'
    r_d2 = client_a.get(url_pg_cn)
    print(f'D2 Blocked: {"no puede ser pagada" in r_d2.text or r_d2.url != url_pg_cn}')
    
    print('--- TEST E1 / E2: Descarga PDF ---')
    ticket = Ticket.objects.create(reserva=res_obj, codigo='TCK-1234', precio_final=0)
    url_tk = f'{BASE_URL}/pagos/ticket/{ticket.id}/pdf/'
    r_e1 = client_a.get(url_tk)
    print(f'E1 Returns PDF: {r_e1.headers.get("Content-Type") == "application/pdf"}')
    r_e2 = client_b.get(url_tk)
    print(f'E2 Blocked for user B: {r_e2.status_code == 404}')

if __name__ == "__main__":
    run_tests()
