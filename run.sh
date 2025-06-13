#!/bin/bash

# Скрипт написан в 3 часа ночи под энергетиком
# KayfMess - Запуск и управление

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

function print_banner() {
    echo -e "${PURPLE}"
    echo "  _  __              __   __  __                "
    echo " | |/ /__ _ _   _ __/ _| |  \/  | ___  ___ ___ "
    echo " | ' // _\` | | | / _\` | | |\/| |/ _ \/ __/ __|"
    echo " | . \ (_| | |_| | (_| | | |  | |  __/\__ \__ \\"
    echo " |_|\_\__,_|\__, |\__,_| |_|  |_|\___||___/___/"
    echo "            |___/                              "
    echo -e "${NC}"
    echo -e "${YELLOW}Написан в 3 часа ночи под энергетиком${NC}"
    echo -e "${BLUE}=======================================================${NC}"
}

function check_deps() {
    echo -e "${BLUE}[*] Проверяем зависимости...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[!] Docker не установлен!${NC}"
        return 1
    fi
    
    # Проверяем новую версию Docker Compose (как плагин Docker)
    if docker compose version &> /dev/null; then
        echo -e "${GREEN}[+] Docker Compose (плагин) установлен!${NC}"
        export DOCKER_COMPOSE="docker compose"
        return 0
    fi
    
    # Если новая версия не найдена, проверяем старую
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}[+] Docker Compose (standalone) установлен!${NC}"
        export DOCKER_COMPOSE="docker-compose"
        return 0
    fi
    
    echo -e "${RED}[!] Docker Compose не установлен!${NC}"
    return 1
}

function setup_dirs() {
    echo -e "${BLUE}[*] Создаем необходимые директории...${NC}"
    mkdir -p nginx/webroot nginx/letsencrypt logs static/{css,js,img}
    echo -e "${GREEN}[+] Директории созданы!${NC}"
}

function start_app() {
    echo -e "${BLUE}[*] Запускаем KayfMess...${NC}"
    echo -e "${YELLOW}[?] Кажется, я немного устал... Сколько сейчас времени?${NC}"
    current_time=$(date +"%H:%M")
    echo -e "${PURPLE}[!] Сейчас $current_time${NC}"
    
    if $DOCKER_COMPOSE up -d; then
        echo -e "${GREEN}[+] KayfMess запущен успешно!${NC}"
        echo -e "${YELLOW}[i] Адрес: https://kayfmess.qndk.fun${NC}"
        return 0
    else
        echo -e "${RED}[!] Ошибка при запуске KayfMess!${NC}"
        echo -e "${RED}[!] Возможно, это из-за того, что я писал это в 3 часа ночи...${NC}"
        return 1
    fi
}

function stop_app() {
    echo -e "${BLUE}[*] Останавливаем KayfMess...${NC}"
    echo -e "${YELLOW}[?] Рано пить энергетик?${NC}"
    
    if $DOCKER_COMPOSE down; then
        echo -e "${GREEN}[+] KayfMess остановлен успешно!${NC}"
        return 0
    else
        echo -e "${RED}[!] Ошибка при остановке KayfMess!${NC}"
        return 1
    fi
}

function setup_ssl() {
    echo -e "${BLUE}[*] Настраиваем SSL для kayfmess.qndk.fun...${NC}"
    echo -e "${YELLOW}[?] Let's Encrypt нужен энергетик, чтобы работать ночью...${NC}"
    
    if $DOCKER_COMPOSE --profile certbot run --rm certbot; then
        echo -e "${GREEN}[+] SSL сертификаты получены успешно!${NC}"
        
        echo -e "${BLUE}[*] Перезапускаем Nginx для применения сертификатов...${NC}"
        if $DOCKER_COMPOSE restart nginx; then
            echo -e "${GREEN}[+] Nginx перезапущен успешно!${NC}"
            return 0
        else
            echo -e "${RED}[!] Ошибка при перезапуске Nginx!${NC}"
            return 1
        fi
    else
        echo -e "${RED}[!] Ошибка при получении SSL сертификатов!${NC}"
        return 1
    fi
}

function show_logs() {
    echo -e "${BLUE}[*] Просмотр логов KayfMess...${NC}"
    echo -e "${YELLOW}[?] Что же происходило, пока я спал?${NC}"
    
    $DOCKER_COMPOSE logs -f
}

function show_help() {
    echo -e "${BLUE}Использование:${NC}"
    echo -e "  ${GREEN}./run.sh${NC} ${YELLOW}[команда]${NC}"
    echo -e ""
    echo -e "${BLUE}Команды:${NC}"
    echo -e "  ${GREEN}start${NC}     - Запустить KayfMess"
    echo -e "  ${GREEN}stop${NC}      - Остановить KayfMess"
    echo -e "  ${GREEN}setup${NC}     - Настроить директории и SSL"
    echo -e "  ${GREEN}logs${NC}      - Просмотреть логи"
    echo -e "  ${GREEN}help${NC}      - Показать эту справку"
    echo -e ""
    echo -e "${YELLOW}Пример:${NC}"
    echo -e "  ${GREEN}./run.sh start${NC}"
}

# Главный код
print_banner

# По умолчанию используем новый вариант Docker Compose
export DOCKER_COMPOSE="docker compose"

if ! check_deps; then
    exit 1
fi

case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    setup)
        setup_dirs
        setup_ssl
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${YELLOW}[?] Команда не указана или неизвестна.${NC}"
        show_help
        ;;
esac

echo -e "${BLUE}=======================================================${NC}"
echo -e "${PURPLE}KayfMess - Весь кайф в 3 часа ночи!${NC}"
echo -e "${BLUE}=======================================================${NC}" 