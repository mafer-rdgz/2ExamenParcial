import streamlit as st
import yfinance as yf
import pandas as pd
from google import genai
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

tokenGenAI = st.secrets["API_KEY_GENAI"]
# Configuración API Gemini

client = genai.Client(api_key=tokenGenAI)

# Configuración general
st.set_page_config(page_title="Análisis de Empresas", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #f8f9fa, #e0f7fa);
            font-family: 'Segoe UI', sans-serif;
        }
        .section-header {
            color: #007B9E;
            font-size: 26px;
            padding-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar con parámetros
with st.sidebar:
    st.title(" TickerLens 📊🔎")
    st.markdown("TickerLens es una app que sirve para saber información general de la empresa que desees, al igual que te brinda datos relevantes que serviran para analizar más a profundidad la empresa. \
    \n\n" \
    "A continuación, ingresa el ticker de la empresa que desees saber más información de ella:")
    symbol = st.text_input("Símbolo de la acción", value="AAPL", help="Ejemplo: AAPL, TSLA, MSFT")
    st.markdown("---")
    st.markdown("Hecho por👩‍💻: María Fernanda Rodríguez Calderón\n\nID 0242636")

# Si se ingresó un símbolo válido
if symbol:
    try:
        company = yf.Ticker(symbol)
        info = company.info

        if not info or 'longBusinessSummary' not in info:
            st.warning("⚠️ No se encontró información para el símbolo ingresado.")
        else:
            company_name = info.get("longName", "Nombre no disponible").upper()
            sector = info.get("sector", "Sector no disponible")
            description = info.get("longBusinessSummary", "Descripción no disponible")
            logo_url = info.get("logo_url", "")

            # === SECCIÓN 1: Información de la empresa ===
            st.markdown(f"<div class='section-header'>📌 Descripción de la Empresa</div>", unsafe_allow_html=True)
            st.subheader(company_name)
            st.markdown(f"<p style='color: #2ca02c; font-size: 16px;'><strong>Sector:</strong> {sector}</p>", unsafe_allow_html=True)

            # Traducir descripción
            prompt = "Traduce el siguiente texto al español dando la información más relevante resumido: " + description
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            translated = response.text

            st.markdown(f"""
                <div style='text-align: justify; background-color: #f4f4f4; padding: 10px; border-radius: 10px;'>
                    {translated}
                
            """, unsafe_allow_html=True)

            if logo_url:
                st.image(logo_url, width=150)

            # === Cargar precios históricos ===
            end_date = datetime.today()
            start_date = end_date - timedelta(days=5*365)
            hist = company.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

            if not hist.empty:
                # === SECCIÓN 2: Gráfica ===
                st.markdown(f"<div class='section-header'>📈 Precio Histórico de Cierre (2020–2025)</div>", unsafe_allow_html=True)
                
                st.markdown(f"La siguiente gráfica muestra el precio histórico de cierre de los últimos 5 años (2020-2025) de **{symbol.upper()}**:")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Precio de cierre"))
                fig.update_layout(
                    title=f"Precio histórico de cierre – {symbol.upper()}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio (USD)",
                    template="plotly_white",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)

        

                # === SECCIÓN 3: CAGR ===
                st.markdown(f"<div class='section-header'>📊 Rendimiento Compuesto Anual (CAGR)</div>", unsafe_allow_html=True)

                st.markdown("""
                    <div style='text-align: justify; font-size: 16px;'>
                        El <strong>rendimiento compuesto anual (CAGR)</strong> muestra el crecimiento medio anual de la acción,
                        considerando reinversión de ganancias. Es útil para analizar el comportamiento a largo plazo de una empresa. \n\n 
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f" \n El cálculo de los rendimientos considera el precio al inicio y al final del periodo de  {symbol.upper()} para determinar el rendimiento anualizado.  \n\n A continuación se muestra una tabla con los rendimientos compuestos anuales de {symbol.upper()}:" )

                def calculate_cagr(start_value, end_value, years):
                    return (end_value / start_value) ** (1 / years) - 1

                cagr_results = {}
                today = hist.index[-1]
                periods = {
                    "1 año": 252,
                    "3 años": 252 * 3,
                    "5 años": 252 * 5,
                }

                for label, days in periods.items():
                    try:
                        start_date = today - pd.tseries.offsets.BDay(days)
                        if start_date < hist.index[0]:
                            cagr_results[label] = "No disponible"
                            continue
                        start_price = hist.loc[hist.index >= start_date][0:1]["Close"].values[0]
                        end_price = hist["Close"].iloc[-1]
                        years = days / 252
                        cagr = calculate_cagr(start_price, end_price, years)
                        cagr_results[label] = f"{cagr*100:.2f}%"
                    except Exception:
                        cagr_results[label] = "Error"

                st.table(pd.DataFrame.from_dict(cagr_results, orient="index", columns=["CAGR"]))
                

        

                st.markdown("El rendimiento anualizado se calculó usando la fórmula de CAGR.")

                st.latex(r"""
                    \text{CAGR} = \left( \frac{\text{Valor Final}}{\text{Valor Inicial}} \right)^{\frac{1}{\text{número de periodos}}} - 1
                    """)
                
                

                # === SECCIÓN 4: Volatilidad Anualizada ===
                st.markdown(f"<div class='section-header'>📉 Volatilidad Anualizada (Riesgo)</div>", unsafe_allow_html=True)

                st.markdown("La **volatilidad** es la medida de la desviación de los rendimientos con respecto a la media. Se utiliza para cuantificar el riesgo de una inversión o una cartera al indicar cuánto es probable que fluctúe el valor de la inversión durante un periodo determinado.")

                st.markdown("""
                    <div style='text-align: justify; font-size: 16px;'>
                        Este valor representa la <strong>volatilidad anual histórica</strong> del activo,
                        medida por la <strong>desviación estándar de los rendimientos diarios</strong>.
                        Una mayor volatilidad implica mayor riesgo e incertidumbre sobre los posibles movimientos del precio. Mientras que una menor implica que los movimientos del precio son más estables y con menor riesgo. \n\n 
                    </div>
                """, unsafe_allow_html=True)

            

                daily_returns = hist["Close"].pct_change().dropna()
                daily_std = np.std(daily_returns)
                annualized_volatility = daily_std * np.sqrt(252)


        
                

                # Tabla de volatilidad anualizada para 1, 3 y 5 años
                vol_results = {}
                for label, days in periods.items():
                    try:
                        start_date = today - pd.tseries.offsets.BDay(days)
                        if start_date < hist.index[0]:
                            vol_results[label] = "No disponible"
                            continue
                        data_range = hist.loc[hist.index >= start_date]["Close"].pct_change().dropna()
                        daily_std = np.std(data_range)
                        annualized_vol = daily_std * np.sqrt(252)
                       
                        # Colorear según el nivel de riesgo
                        color = "🟢" if annualized_vol < 0.20 else "🟡" if annualized_vol < 0.40 else "🔴"
                        vol_results[label] = f"{color} {annualized_vol*100:.2f}%"
                    except Exception:
                        vol_results[label] = "Error"


                st.markdown(f"A continuación, se muestra la tabla de volatilidad anualizada para {symbol.upper()} en distintos periodos:")


                st.table(pd.DataFrame.from_dict(vol_results, orient="index", columns=["Volatilidad Anualizada"]))


                vol_color = "green" if annualized_volatility < 0.20 else \
                            "orange" if annualized_volatility < 0.40 else "red"

                

                # Tabla de interpretación de la volatilidad
                st.markdown(f"Para que tengas una noción del grado de volatilidad de {symbol.upper()}, la siguiente tabla te ayudará:")

                st.markdown("""
                <table style='width:100%; border-collapse: collapse; font-size: 16px;'>
                  <thead>
                    <tr style='background-color: #f0f0f0;'>
                      <th style='padding: 10px; border-bottom: 1px solid #ccc;'>Volatilidad anualizada</th>
                      <th style='padding: 10px; border-bottom: 1px solid #ccc;'>Color</th>
                      <th style='padding: 10px; border-bottom: 1px solid #ccc;'>Interpretación</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style='padding: 8px;'>&lt; 20%</td>
                      <td style='padding: 8px;'>🟢 Verde</td>
                      <td style='padding: 8px;'>Baja volatilidad (riesgo bajo)</td>
                    </tr>
                    <tr>
                      <td style='padding: 8px;'>20% – 40%</td>
                      <td style='padding: 8px;'>🟡 Naranja</td>
                      <td style='padding: 8px;'>Volatilidad moderada</td>
                    </tr>
                    <tr>
                      <td style='padding: 8px;'>&gt; 40%</td>
                      <td style='padding: 8px;'>🔴 Rojo</td>
                      <td style='padding: 8px;'>Alta volatilidad (riesgo alto)</td>
                    </tr>
                  </tbody>
                </table>
                """, unsafe_allow_html=True)

            
                st.latex(r"""
                \text{Volatilidad Anualizada} = \sigma_{\text{diaria}} \times \sqrt{252}
                """)

                st.markdown(
                "_Nota: $\sigma$ representa la desviación estándar de los rendimientos diarios._",
                unsafe_allow_html=True
)

                # === SECCIÓN 5: Simulador de Inversión ===
                st.markdown(f"<div class='section-header'>💰 Simulador de Inversión</div>", unsafe_allow_html=True)

                st.markdown("""
                Imagina que hubieras invertido en esta acción hace un tiempo. ¿Cuánto tendrías hoy? Usa este simulador para descubrirlo.
                """)

                # Periodos disponibles
                period_options = {
                    "1 año": 252,
                    "3 años": 252 * 3,
                    "5 años": 252 * 5
                }

                # Entrada del usuario
                inversion_inicial = st.number_input("Monto de inversión inicial (USD)", min_value=100.0, value=1000.0, step=100.0)
                periodo_seleccionado = st.selectbox("Selecciona el período de inversión", list(period_options.keys()))

                # Cálculo del valor de la inversión
                dias = period_options[periodo_seleccionado]
                fecha_inicio = today - pd.tseries.offsets.BDay(dias)
                hist_periodo = hist.loc[hist.index >= fecha_inicio]

                if not hist_periodo.empty:
                    precios_normalizados = hist_periodo["Close"] / hist_periodo["Close"].iloc[0]
                    valor_inversion = precios_normalizados * inversion_inicial
                    valor_futuro = valor_inversion.iloc[-1]

                    # Resultado en texto
                    st.markdown(f"""
                    <div style='background-color:#d4edda; padding: 15px; border-radius: 10px; font-size: 18px; color: #155724;'>
                    💸 Si hubieras invertido <strong>${inversion_inicial:,.2f}</strong> dólares hace <strong>{periodo_seleccionado}</strong>, hoy tendrías aproximadamente <strong>${valor_futuro:,.2f}</strong> dólares.
                    </div>
                    """, unsafe_allow_html=True)

                    # Gráfica del crecimiento
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=valor_inversion.index, y=valor_inversion, mode='lines', name='Valor de la inversión'))
                    fig.update_layout(
                        title="📈 Crecimiento de la inversión a lo largo del tiempo",
                        xaxis_title="Fecha",
                        yaxis_title="Valor de inversión (USD)",
                        template="plotly_white",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Comentario educativo
                    st.markdown("""
                    > **Nota:** Esta gráfica muestra cómo habría evolucionado tu inversión, considerando solo el precio de cierre de la acción.
                    """)
                else:
                    st.warning("No se encontraron suficientes datos históricos para ese periodo.")





            else:
                st.warning("No se encontraron datos históricos para graficar.")

    except Exception as e:
        st.error("No se pudo obtener información. Verifica el símbolo e intenta nuevamente.")
