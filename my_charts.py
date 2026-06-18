import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_charts(df):
    charts = {}
    
    # Saját sötét téma a hibás gyári "plotly_dark" helyett
    def apply_dark_theme(fig, title):
        fig.update_layout(
            title=title,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E0E0E0"),
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode="x unified"
        )
        fig.update_xaxes(showgrid=True, gridcolor="#2A2E35", zerolinecolor="#2A2E35")
        fig.update_yaxes(showgrid=True, gridcolor="#2A2E35", zerolinecolor="#2A2E35")
        return fig

    # 1. Diagram: Brent olajár alakulása
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['Dátum'], y=df['Brent_Olaj_USD'], mode='lines', name='Brent (USD)', line=dict(color='#00D2FF', width=3)))
    charts['brent'] = apply_dark_theme(fig1, "1. A Brent nyersolaj világpiaci ára (USD / hordó)")

    # 2. Diagram: USD/RON és EUR/RON árfolyamok
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['Dátum'], y=df['USD_RON'], mode='lines', name='USD/RON', line=dict(color='#FF007F', width=2)))
    fig2.add_trace(go.Scatter(x=df['Dátum'], y=df['EUR_RON'], mode='lines', name='EUR/RON', line=dict(color='#FFD700', width=2)))
    charts['fx'] = apply_dark_theme(fig2, "2. A valutaárfolyamok alakulása (RON)")

    # 3. Diagram: Üzemanyagárak Romániában (RON)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df['Dátum'], y=df['Benzin_RON'], mode='lines', name='Benzin', line=dict(color='#00FF66', width=2.5)))
    fig3.add_trace(go.Scatter(x=df['Dátum'], y=df['Motorina_RON'], mode='lines', name='Motorina (Gázolaj)', line=dict(color='#FFA500', width=2.5)))
    charts['fuel'] = apply_dark_theme(fig3, "3. Hazai üzemanyagárak alakulása a kutakon (RON / liter)")

    # 4. Diagram: Romániai Infláció (%)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=df['Dátum'], y=df['Inflacio_Szazalek'], name='Infláció', marker_color='#FF4136'))
    charts['inflation'] = apply_dark_theme(fig4, "4. Romániai éves inflációs ráta (%)")

    # 5. Diagram: Olajár vs Üzemanyagár korreláció
    fig5 = px.scatter(df, x='Brent_Olaj_USD', y='Benzin_RON', trendline="ols", 
                     labels={'Brent_Olaj_USD': 'Brent Olaj (USD)', 'Benzin_RON': 'Benzin ár (RON)'})
    fig5.update_traces(marker=dict(size=10, color='#00D2FF', line=dict(width=1, color='#FFFFFF')))
    charts['correlation'] = apply_dark_theme(fig5, "5. Korreláció: Világpiaci olajár vs. Hazai benzinár")

    # 6. Diagram: Nettó átlagbér vs Vásárlóerő
    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig6.add_trace(
        go.Scatter(x=df['Dátum'], y=df['Netto_Atlagber_RON'], mode='lines', name='Nettó bér (RON)', line=dict(color='#11FF00')),
        secondary_y=False,
    )
    fig6.add_trace(
        go.Scatter(x=df['Dátum'], y=df['Vasarloero_Index'], mode='lines', name='Vásárlóerő index', line=dict(color='#B10DC9', dash='dash')),
        secondary_y=True,
    )

    apply_dark_theme(fig6, "6. Nettó átlagbér növekedése vs. Reál vásárlóerő")
    
    fig6.update_yaxes(title_text="Nettó bér (RON)", secondary_y=False)
    fig6.update_yaxes(title_text="Vásárlóerő", secondary_y=True)
    
    charts['salary'] = fig6

    return charts