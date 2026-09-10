import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Tablero de Operaciones", layout="wide")
st.title("Tablero Interactivo de Operaciones")

archivo = st.file_uploader("Cargue archivo Excel o CSV", type=["xlsx", "csv"])

if archivo is not None:
    if archivo.name.lower().endswith('.csv'):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    fecha_col = 'Fecha Grabacion Pago'
    proveedor_col = 'Proveedor'
    negocio_col = 'Negocio'
    gestor_col = 'Gestor'

    if fecha_col in df.columns:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')

    st.sidebar.header('Filtros')

    filtrado = df.copy()

    if proveedor_col in df.columns:
        sel = st.sidebar.multiselect('Proveedor', sorted(df[proveedor_col].dropna().unique()))
        if sel:
            filtrado = filtrado[filtrado[proveedor_col].isin(sel)]

    if negocio_col in df.columns:
        sel = st.sidebar.multiselect('Negocio', sorted(df[negocio_col].dropna().unique()))
        if sel:
            filtrado = filtrado[filtrado[negocio_col].isin(sel)]

    if gestor_col in df.columns:
        sel = st.sidebar.multiselect('Gestor', sorted(df[gestor_col].dropna().unique()))
        if sel:
            filtrado = filtrado[filtrado[gestor_col].isin(sel)]

    c1,c2,c3 = st.columns(3)
    c1.metric('Total Operaciones', len(filtrado))
    c2.metric('Proveedores', filtrado[proveedor_col].nunique() if proveedor_col in filtrado.columns else 0)
    c3.metric('Gestores', filtrado[gestor_col].nunique() if gestor_col in filtrado.columns else 0)

    if fecha_col in filtrado.columns:
        data = filtrado.groupby(fecha_col).size().reset_index(name='Operaciones')
        chart = alt.Chart(data).mark_line(point=True).encode(x=fecha_col,y='Operaciones')
        st.altair_chart(chart, use_container_width=True)

    col1,col2 = st.columns(2)

    if proveedor_col in filtrado.columns:
        data = filtrado.groupby(proveedor_col).size().reset_index(name='Operaciones')
        chart = alt.Chart(data).mark_bar().encode(x=proveedor_col,y='Operaciones')
        col1.altair_chart(chart, use_container_width=True)

    if gestor_col in filtrado.columns:
        data = filtrado.groupby(gestor_col).size().reset_index(name='Operaciones')
        chart = alt.Chart(data).mark_bar().encode(x=gestor_col,y='Operaciones')
        col2.altair_chart(chart, use_container_width=True)

    if negocio_col in filtrado.columns:
        st.subheader('Operaciones por Negocio')
        st.dataframe(filtrado.groupby(negocio_col).size().reset_index(name='Operaciones'))

    st.subheader('Datos Filtrados')
    st.dataframe(filtrado)
else:
    st.info('Cargue un archivo Excel o CSV.')
