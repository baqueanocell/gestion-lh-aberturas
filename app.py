import streamlit as st

st.set_page_config(page_title="LH Gremio - Visual Test", page_icon="🦁")

# --- CONFIGURACIÓN ---
NUMERO_WHATSAPP = "54911XXXXXXXX" # Tu número aquí

if 'precio_kilo' not in st.session_state:
    st.session_state['precio_kilo'] = 11500.0

# --- INTERFAZ ---
st.title("🦁 LH Aberturas - Gremio")
st.sidebar.header("Configuración Admin")
st.session_state['precio_kilo'] = st.sidebar.number_input("Precio Kilo Aluminio ($)", value=st.session_state['precio_kilo'])

st.write(f"### Valor actual: **${st.session_state['precio_kilo']:,.0f} / kg**")

# Contenedor de pedidos
with st.expander("📝 Cargar nuevas medidas", expanded=True):
    cant = st.number_input("¿Cuántas aberturas?", min_value=1, max_value=20, value=1)
    
    pedidos = []
    for i in range(int(cant)):
        col1, col2, col3 = st.columns([2, 1, 1])
        linea = col1.selectbox(f"Línea {i+1}", ["Modena", "Herrero"], key=f"l{i}")
        ancho = col2.number_input(f"Ancho cm", key=f"an{i}", format="%.1f")
        alto = col3.number_input(f"Alto cm", key=f"al{i}", format="%.1f")
        pedidos.append({"linea": linea, "ancho": ancho, "alto": alto})

if st.button("CALCULAR Y GENERAR PEDIDO"):
    peso_total = 0
    detalle_texto = ""
    
    for i, p in enumerate(pedidos):
        # Constante de peso promedio para la visualización
        factor = 0.85 if p['linea'] == "Modena" else 0.55
        peso = ((p['ancho'] * 2 + p['alto'] * 2) / 100) * factor
        peso_total += peso
        detalle_texto += f"- {p['linea']}: {p['ancho']}x{p['alto']} cm%0A"

    costo = peso_total * st.session_state['precio_kilo']
    
    st.metric("Peso Total", f"{peso_total:.2f} kg")
    st.metric("Total Gremio", f"${costo:,.0f}")
    
    # Botón de WhatsApp con el mensaje estructurado
    mensaje = f"Hola LH Aberturas!%0AQuiero encargar {int(cant)} ventanas:%0A{detalle_texto}%0APeso total: {peso_total:.2f}kg.%0APresupuesto: ${costo:,.0f}"
    url_wa = f"https://wa.me/{+541122513169}?text={mensaje}"
    
    st.markdown(f'''
        <a href="{url_wa}" target="_blank">
            <button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
                ✅ ENVIAR PEDIDO A PRODUCCIÓN POR WHATSAPP
            </button>
        </a>
    ''', unsafe_allow_html=True)
