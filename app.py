import streamlit as str_app
from database import get_dashboard_data
from my_charts import create_charts

# Oldal konfiguráció
str_app.set_page_config(page_title="Románia Energia & Infláció Dashboard", layout="wide")

# Letisztult CSS, a modern navigációs gombokkal
str_app.markdown("""
    <style>
    h1, h2, h3 { font-family: 'Helvetica Neue', Arial, sans-serif; }
    
    .story-text { 
        font-size: 1.15rem; 
        line-height: 1.7; 
        margin-bottom: 20px; 
        border-left: 4px solid #FF007F; 
        padding-left: 15px;
        font-style: italic;
    }
    
    /* Egyedi, gomb-szerű Tartalomjegyzék stílus */
    .toc-menu a {
        display: block;
        color: #E0E0E0 !important;
        text-decoration: none !important;
        background-color: #1F242E;
        padding: 12px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: 500;
        border-left: 4px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Hover effektus: ha ráviszi az egeret a tanár */
    .toc-menu a:hover {
        background-color: #2A2E35;
        border-left: 4px solid #00D2FF;
        color: #00D2FF !important;
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- OLDALSÁV ÉS TARTALOMJEGYZÉK ---
str_app.sidebar.header("Tartalomjegyzék")

# Itt cseréltük le a sima linkeket az új formátumra
str_app.sidebar.markdown("""
<div class="toc-menu">
    <a href="#projekt-dokumentacio">📋 Projekt Dokumentáció</a>
    <a href="#fejezet-1">🌍 I. Felvonás: Világpiac</a>
    <a href="#fejezet-2">🇷🇴 II. Felvonás: Hazai Gazdaság</a>
    <a href="#fejezet-3">🛒 III. Felvonás: Vásárlóerő</a>
</div>
<br>
""", unsafe_allow_html=True)

str_app.sidebar.header("Szűrők és Beállítások")
df = get_dashboard_data()
start_date = str_app.sidebar.date_input("Kezdő dátum", df['Dátum'].min().date())
end_date = str_app.sidebar.date_input("Záró dátum", df['Dátum'].max().date())

# Adatok szűrése
filtered_df = df[(df['Dátum'].dt.date >= start_date) & (df['Dátum'].dt.date <= end_date)]
charts = create_charts(filtered_df)

# --- FŐOLDAL FEJLÉC ---
str_app.title("Makrogazdasági Elemzés: Az olajtól a bevásárlókosárig")
str_app.markdown("*Hogyan gyűrűzik be a világpiaci válság a romániai mindennapokba (2021–2026)?*")
str_app.markdown("---")

# --- 1. SZEKCIÓ: DOKUMENTÁCIÓ ---
str_app.markdown("<a id='projekt-dokumentacio'></a>", unsafe_allow_html=True)
with str_app.expander("KATTINTS IDE: Projekt Dokumentáció & Elméleti Útmutató"):
    
    tab1, tab2, tab3 = str_app.tabs(["Koncepció & Adatok", "Célközönség", "Skálázhatóság & Jövő"])
    
    with tab1:
        str_app.info("**Miről szól a projekt?**\n\nEz az összefüggő portfólió azt mutatja be, hogyan gyűrűzik be a világpiaci nyersolaj (Brent) árváltozása és a valutaárfolyamok mozgása a romániai gazdaságba, közvetlenül befolyásolva a lakossági üzemanyagárakat, a nemzeti inflációt (CPI) és a lakosság valós vásárlóerejét.")
        str_app.info("**Milyen adatokat használsz és miért érdekesek?**\n\nA projekt **élő, API-alapú piaci adatokat** használ (a Yahoo Finance rendszeréből lekérve a Brent olaj és a devizaárfolyamok esetében), melyeket a hivatalos román statisztikai trendekkel (INSSE) kombinálunk a makrogazdasági mutatókhoz. Az adatok azért érdekesek, mert számszerűsítik, hogy a globális geopolitikai sokkok hogyan válnak azonnal kézzelfogható drágulássá a romániai kutakon és a boltokban.")
        
    with tab2:
        str_app.success("**Ki a cél-felhasználó és mit tanul ebből?**\n\nA cél-felhasználók gazdasági/marketing szakos egyetemi hallgatók, illetve pénzügyi elemzők. A felhasználó megérti a korrelációt a globális nyersanyagárak és a lokális infláció között.")
        
    with tab3:
        str_app.warning("**Mennyire skálázható a megoldás?**\n\nA megoldás rendkívül skálázható. A moduláris architektúra lehetővé teszi újabb országok vagy egyéb nyersanyagok (földgáz, áram) integrálását a struktúra átépítése nélkül.")
        str_app.warning("**Mennyire automatizálható a megoldás?**\n\nA megoldás már jelenleg is **magas fokon automatizált**. A tőzsdei adatok frissítése élő API-lekéréseken keresztül történik, így a dashboard minden megnyitáskor automatikusan a legfrissebb elérhető piaci adatokat húzza be. Az architektúra fel van készítve arra is, hogy a jövőben a statisztikai adatok (Eurostat) is közvetlen API-kapcsolaton keresztül frissüljenek.")
        str_app.error("**Mivel lenne még hasznos bővíteni?**\n\nHasznos lenne kiegészíteni a fogyasztói kosár részletesebb bontásával (élelmiszerek és szolgáltatások egyedi inflációja), valamint egy prediktív gépi tanulási (Machine Learning - ARIMA) modellel, ami előrejelzi a következő hónapok várható üzemanyagárait.")

str_app.markdown("<br>", unsafe_allow_html=True)

# --- SZTORI 1. FEJEZET ---
str_app.markdown("<a id='fejezet-1'></a>", unsafe_allow_html=True)
str_app.header("I. Felvonás: A Vihar a Világpiacon")
str_app.markdown("""
<div class="story-text">
Minden gazdasági folyamat az országhatárokon kívül kezdődik. Az elmúlt évek geopolitikai feszültségei és ellátási lánc problémái drasztikusan mozgatták a <b>Brent nyersolaj</b> világpiaci árát. Ezzel párhuzamosan a román lej (RON) árfolyama is folyamatos nyomás alatt állt az euróval és a dollárral szemben. Mivel Románia is importál energiahordozókat, a gyengülő lej és a drága olaj kombinációja tökéletes vihart teremtett az importköltségekben.
</div>
""", unsafe_allow_html=True)

row1_col1, row1_col2 = str_app.columns(2)
with row1_col1:
    str_app.plotly_chart(charts['brent'], use_container_width=True)
with row1_col2:
    str_app.plotly_chart(charts['fx'], use_container_width=True)

str_app.markdown("---")

# --- SZTORI 2. FEJEZET ---
str_app.markdown("<a id='fejezet-2'></a>", unsafe_allow_html=True)
str_app.header("II. Felvonás: Begyűrűzés a Hazai Gazdaságba")
str_app.markdown("""
<div class="story-text">
A globális drágulás nem áll meg a határon: szinte azonnal megjelenik a hazai benzinkutak totemoszlopain. A megnövekedett üzemanyagárak drágítják a logisztikát és a szállítást, ami dominóeffektusként hajtja fel az összes fogyasztási cikk – különösen az élelmiszerek – árát. Jól látható, hogyan követte a romániai kutak árazása az olajár-sokkokat, és hogyan robbant be az infláció az országban.
</div>
""", unsafe_allow_html=True)

row2_col1, row2_col2 = str_app.columns(2)
with row2_col1:
    str_app.plotly_chart(charts['fuel'], use_container_width=True)
with row2_col2:
    str_app.plotly_chart(charts['inflation'], use_container_width=True)

str_app.markdown("---")

# --- SZTORI 3. FEJEZET ---
str_app.markdown("<a id='fejezet-3'></a>", unsafe_allow_html=True)
str_app.header("III. Felvonás: A Valóság a Pénztárcákban")
str_app.markdown("""
<div class="story-text">
De mit jelent ez az átlagember és a vállalatok számára? A bal oldali regressziós modell egyértelmű matematikai korrelációt bizonyít a világpiaci olajár és a hazai benzinár között. A legfájdalmasabb igazság azonban a jobb oldali grafikonon látszik: hiába nőttek a nominális nettó átlagbérek Romániában az elmúlt években, az elszabadult infláció miatt a reálbér és a vásárlóerő drasztikusan lecsökkent. Több pénzt viszünk haza, de kevesebbet ér.
</div>
""", unsafe_allow_html=True)

row3_col1, row3_col2 = str_app.columns(2)
with row3_col1:
    str_app.plotly_chart(charts['correlation'], use_container_width=True)
with row3_col2:
    str_app.plotly_chart(charts['salary'], use_container_width=True)

str_app.markdown("---")
str_app.caption("Készítette: Varga Norbert és Kovács Ákos, a Babeș-Bolyai Tudományegyetem hallgatói - 2026")
