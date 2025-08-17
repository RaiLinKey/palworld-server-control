import streamlit as st
import subprocess
import os

# Пути к конфигам
LOCAL_CONFIG = "./currentConfig.ini"
GAME_CONFIG = "/home/steam/.steam/steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini"

# Функция для выполнения bash-команд
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)

# Функция обновления статуса
def get_status():
    return run_command("systemctl status palworld.service")

# Функции для работы с конфигом
def load_config():
    if os.path.exists(LOCAL_CONFIG):
        with open(LOCAL_CONFIG, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_config(content):
    try:
        # Сохраняем в локальный конфиг
        with open(LOCAL_CONFIG, "w", encoding="utf-8") as f:
            f.write(content)

        # Сохраняем в рабочий конфиг Palworld
        os.makedirs(os.path.dirname(GAME_CONFIG), exist_ok=True)
        with open(GAME_CONFIG, "w", encoding="utf-8") as f:
            f.write(content)

        return True, "Конфиг успешно сохранён"
    except Exception as e:
        return False, f"Ошибка при сохранении: {e}"

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Palworld Server Control", layout="wide")
st.title("Управление Palworld сервером")

# При открытии страницы показать статус
st.subheader("Текущий статус сервера")
status_output = get_status()
st.text_area("Вывод systemctl status", status_output, height=400)

# Кнопки управления сервером
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Запустить сервер"):
        run_command("systemctl start palworld.service")
        st.success("Сервер запущен")
        st.text_area("Актуальный статус", get_status(), height=400)

with col2:
    if st.button("Перезапустить сервер"):
        run_command("systemctl restart palworld.service")
        st.success("Сервер перезапущен")
        st.text_area("Актуальный статус", get_status(), height=400)

with col3:
    if st.button("Остановить сервер"):
        run_command("systemctl stop palworld.service")
        st.warning("Сервер остановлен")
        st.text_area("Актуальный статус", get_status(), height=400)

with col4:
    if st.button("Статус сервера"):
        st.text_area("Актуальный статус", get_status(), height=400)

# ---------------- Редактор конфига ----------------
st.subheader("Редактор конфигурации Palworld")

config_content = st.text_area("Файл конфигурации", load_config(), height=400, key="config_editor")

if st.button("Сохранить конфиг"):
    success, msg = save_config(config_content)
    if success:
        st.success(msg)
    else:
        st.error(msg)
