import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tablero de Operaciones", layout="wide")
st.title("📊 Tablero Interactivo de Operaciones")

archivo = st.file_uploader("Cargue archivo Excel o CSV", type=["xlsx","csv"])

if archivo:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    st.sidebar.header("Filtros")

    fecha_col = "Fecha Grabacion Pago"
    proveedor_col = "Proveedor"
    negocio_col = "Negocio"
    gestor_col = "Gestor"

    if fecha_col in df.columns:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")

    proveedores = st.sidebar.multiselect(
        "Proveedor",
        options=sorted(df[proveedor_col].dropna().unique()) if proveedor_col in df.columns else []
    )

    negocios = st.sidebar.multiselect(
        "Negocio",
        options=sorted(df[negocio_col].dropna().unique()) if negocio_col in df.columns else []
    )

    gestores = st.sidebar.multiselect(
        "Gestor",
        options=sorted(df[gestor_col].dropna().unique()) if gestor_col in df.columns else []
    )

    filtro = df.copy()

    if proveedores:
        filtro = filtro[filtro[proveedor_col].isin(proveedores)]

    if negocios:
        filtro = filtro[filtro[negocio_col].isin(negocios)]

    if gestores:
        filtro = filtro[filtro[gestor_col].isin(gestores)]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Operaciones", len(filtro))
    col2.metric("Total Proveedores", filtro[proveedor_col].nunique() if proveedor_col in filtro.columns else 0)
    col3.metric("Total Gestores", filtro[gestor_col].nunique() if gestor_col in filtro.columns else 0)

    if fecha_col in filtro.columns:
        ops_fecha = filtro.groupby(fecha_col).size().reset_index(name='Operaciones')
        fig_fecha = px.line(ops_fecha, x=fecha_col, y='Operaciones', title='Operaciones por Fecha de Grabación Pago')
        st.plotly_chart(fig_fecha, use_container_width=True)

    c1, c2 = st.columns(2)

    if proveedor_col in filtro.columns:
        ops_proveedor = filtro.groupby(proveedor_col).size().reset_index(name='Operaciones')
        fig_proveedor = px.bar(ops_proveedor, x=proveedor_col, y='Operaciones', title='Operaciones por Proveedor')
        c1.plotly_chart(fig_proveedor, use_container_width=True)

    if gestor_col in filtro.columns:
        ops_gestor = filtro.groupby(gestor_col).size().reset_index(name='Operaciones')
        fig_gestor = px.bar(ops_gestor, x=gestor_col, y='Operaciones', title='Operaciones por Gestor')
        c2.plotly_chart(fig_gestor, use_container_width=True)

    if negocio_col in filtro.columns:
        ops_negocio = filtro.groupby(negocio_col).size().reset_index(name='Operaciones')
        fig_negocio = px.pie(ops_negocio, names=negocio_col, values='Operaciones', title='Operaciones por Negocio')
        st.plotly_chart(fig_negocio, use_container_width=True)

    st.subheader('Datos filtrados')
    st.dataframe(filtro)
else:
    st.info('Cargue un archivo para visualizar el tablero.')
