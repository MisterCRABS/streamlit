import streamlit as st 
import pandas as pd 
import yfinance as yf 
import matplotlib.pyplot as plt
import seaborn as sns 

# Настройки страницы
st.set_page_config(
    page_title="Анализ акций Apple",
    layout="wide"
)

# Заголовок приложения
st.title(" Анализ котировок Apple")

# Описание приложения
st.write("""
Это приложение показывает исторические данные о котировках акций компании Apple.
Используйте настройки ниже для выбора периода анализа.
""")

# Боковая панель с настройками
with st.sidebar:
    st.header("⚙️ Настройки")
    start_date = st.date_input("Начальная дата", pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Конечная дата", pd.to_datetime("today"))
    period = st.selectbox("Период", ["1d", "1wk", "1mo"], index=2)

# Загрузка данных
@st.cache_data  # Кэшируем данные, чтобы не загружать их каждый раз
def load_data():
    ticker = "AAPL"
    data = yf.download(ticker, start=start_date, end=end_date, interval=period)
    return data

try:
    data = load_data()
    
    if data.empty:
        st.warning("Не удалось загрузить данные. Попробуйте изменить параметры.")
    else:
        # Показываем последние 5 записей
        st.subheader("Последние данные")
        st.dataframe(data.tail().style.format("{:.2f}"), use_container_width=True)
        
        # График цен закрытия
        st.subheader("График цен закрытия")
        fig, ax = plt.subplots(figsize=(10, 5))
        data['Close'].plot(ax=ax, title='Цена закрытия AAPL', grid=True)
        st.pyplot(fig)
        
        # Основные статистики
        st.subheader("Основные статистики")
        st.table(data.describe().style.format("{:.2f}"))
        
        # Информация о компании
        st.subheader("Информация о компании")
        info = yf.Ticker("AAPL").info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Текущая цена", f"${info.get('currentPrice', 'N/A')}")
            st.metric("Рыночная капитализация", f"${info.get('marketCap', 'N/A'):,}")
        with col2:
            st.metric("P/E (Коэф. P/E)", info.get('trailingPE', 'N/A'))
            st.metric("Дивидендная доходность", f"{info.get('dividendYield', 'N/A')*100:.2f}%" if info.get('dividendYield') else 'N/A')

except Exception as e:
    st.error(f"Произошла ошибка: {str(e)}")