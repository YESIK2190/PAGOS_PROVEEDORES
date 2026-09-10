# Tablero Interactivo de Operaciones

## Descripción
Aplicación Streamlit para visualizar:
- Cantidad de operaciones por proveedor.
- Cantidad de operaciones por fecha de grabación de pago.
- Cantidad de operaciones por negocio.
- Cantidad de operaciones por gestor.

## Estructura esperada
Columnas requeridas:
- Fecha Grabacion Pago
- Proveedor
- Negocio
- Gestor

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
streamlit run app.py
```

## Funcionalidades
- Filtros por proveedor, negocio y gestor.
- Indicadores KPI.
- Gráfico de línea por fecha.
- Gráfico de barras por proveedor y gestor.
- Gráfico circular por negocio.
