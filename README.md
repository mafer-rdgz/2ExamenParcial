# 📊 Análisis de Empresas con Python y Streamlit

Esta es una aplicación interactiva desarrollada con **Python**, **Streamlit** y **YFinance** que permite consultar información clave sobre empresas que cotizan en bolsa utilizando su *ticker* (símbolo bursátil). También calcula métricas financieras como **CAGR** y **Volatilidad Anualizada**, integrando herramientas de visualización y traducción automática con IA.

---

## 🚀 Características Principales

- 📌 **Descripción de la empresa** (traducida al español con Gemini AI)
- 📈 **Gráfico del precio de cierre histórico** (últimos 5 años)
- 📊 **Cálculo del CAGR** (1, 3 y 5 años)
- 📉 **Cálculo de la Volatilidad Anualizada**
- 💰 **Simulador de inversión interactivo**
- 🎨 Interfaz visual con Plotly y estilo personalizado

---

## 🧰 Tecnologías Utilizadas

- `Python 3.x`
- `Streamlit`
- `yfinance`
- `plotly`
- `pandas`
- `numpy`
- `Google Gemini API` (traducción automática)

---

## 📂 Desglose de Funcionalidades

### 📌 1. Descripción de la Empresa

- Consulta y muestra información general del ticker ingresado, como nombre completo, sector y resumen de negocio.
- La descripción se traduce y resume automáticamente al español usando Gemini.
- Se visualiza también el logo de la empresa si está disponible.

### 📈 2. Precio Histórico de Cierre

- Se obtiene el precio de cierre ajustado de los últimos 5 años.
- Se presenta una gráfica interactiva con Plotly que permite explorar visualmente el comportamiento de la acción a lo largo del tiempo.

### 📊 3. Rendimiento Compuesto Anual (CAGR)

- Se calcula el **CAGR** para 1, 3 y 5 años usando la fórmula:
  
 Fórmula CAGR = ((Valor Final/Valor Inicial)^(1/número de periodos)) - 1

- Se muestra una tabla con los rendimientos porcentuales anuales para distintos periodos.

---

### 📉 4. Volatilidad Anualizada (Riesgo)

- Calcula la **volatilidad histórica anualizada** de la acción, a partir de la desviación estándar de los retornos diarios.
- Muestra una **tabla con los niveles de volatilidad anualizada** para 1, 3 y 5 años.
- Se clasifica el riesgo con un sistema de colores:
  - 🟢 Menor al 20%: Riesgo bajo
  - 🟡 Entre 20% y 40%: Riesgo medio
  - 🔴 Mayor al 40%: Riesgo alto
- También se incluye una **tabla interpretativa** que ayuda al usuario a entender mejor estos valores.
- La fórmula utilizada es:

Volatilidad: desviación estándar rendimientos diarios * √ 252

> _Nota: `σ` representa la desviación estándar de los rendimientos diarios._

---

### 💰 5. Simulador de Inversión

- El usuario puede **ingresar una cantidad de dinero (en USD)** e imaginar cuánto tendría hoy si hubiera invertido hace 1, 3 o 5 años en la acción seleccionada.
- Se calcula el valor de la inversión usando precios históricos normalizados.
- Muestra:
  - Una **frase de resultado** con el valor final estimado.
  - Una **gráfica interactiva** que ilustra cómo habría evolucionado la inversión a lo largo del tiempo.
- Ideal para comprender el efecto del crecimiento compuesto y visualizar escenarios hipotéticos de rentabilidad.


---

## 🧠 Créditos

Desarrollado por:  
**María Fernanda Rodríguez Calderón**  
Estudiante de Ingeniería Financiera – ID 0242636  
💡 Proyecto educativo con enfoque en análisis de inversiones.

---
