/**
 * KayfMess - написан в 3 часа ночи под энергетиком
 * Главный JavaScript файл
 */

// Переменная, показывающая уровень "бодрствования" программиста
let awakenessLevel = 100;

// Функция, которая постепенно уменьшает бодрствование
function decreaseAwakeness() {
    awakenessLevel -= Math.random() * 5;
    
    // Если бодрствование слишком низкое, добавляем случайные баги
    if (awakenessLevel < 30) {
        applyRandomGlitches();
        // Выпьем энергетик и восстановим бодрствование
        awakenessLevel = 100;
        console.log("Программист выпил энергетик в " + new Date().toLocaleTimeString());
    }
    
    // Запланируем следующее уменьшение бодрствования
    setTimeout(decreaseAwakeness, Math.random() * 30000 + 15000);  // От 15 до 45 секунд
}

// Функция для применения случайных визуальных глюков
function applyRandomGlitches() {
    // Выбираем случайный элемент DOM
    const allElements = document.querySelectorAll('div, p, span, h1, h2, h3, h4, h5, button, a');
    if (allElements.length === 0) return;
    
    const randomElement = allElements[Math.floor(Math.random() * allElements.length)];
    
    // Применяем случайный эффект
    const effect = Math.floor(Math.random() * 5);
    
    switch (effect) {
        case 0:
            // Эффект дрожания
            randomElement.classList.add('drunk');
            setTimeout(() => {
                randomElement.classList.remove('drunk');
            }, 5000);
            break;
        
        case 1:
            // Эффект глитча
            randomElement.classList.add('glitch');
            setTimeout(() => {
                randomElement.classList.remove('glitch');
            }, 3000);
            break;
            
        case 2:
            // Временное изменение цвета
            const originalColor = randomElement.style.color;
            randomElement.style.color = '#00FF00';
            setTimeout(() => {
                randomElement.style.color = originalColor;
            }, 2000);
            break;
            
        case 3:
            // Случайное сообщение о "баге"
            if (document.querySelector('.flash-messages')) {
                const messages = [
                    "Энергетик закончился!",
                    "Программист заснул на клавиатуре!",
                    "Кофеин перестал действовать!",
                    "Ошибка: zzZZzzZ (сон программиста)",
                    "Слишком мало кода, нужно больше энергетика!"
                ];
                
                const flashMsg = document.createElement('div');
                flashMsg.className = 'alert alert-warning alert-dismissible fade show';
                flashMsg.innerHTML = `
                    <i class="fas fa-exclamation-triangle"></i> ${messages[Math.floor(Math.random() * messages.length)]}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                
                document.querySelector('.flash-messages').appendChild(flashMsg);
                
                // Автоматически удаляем через 5 секунд
                setTimeout(() => {
                    flashMsg.classList.remove('show');
                    setTimeout(() => {
                        if (flashMsg.parentNode) {
                            flashMsg.parentNode.removeChild(flashMsg);
                        }
                    }, 1000);
                }, 5000);
            }
            break;
            
        case 4:
            // Имитация задержек
            document.body.style.opacity = '0.8';
            document.body.style.transition = 'opacity 0.5s';
            
            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 500);
            break;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log("KayfMess загружен в " + new Date().toLocaleTimeString());
    console.log("Уровень энергетика программиста: " + awakenessLevel + "%");
    
    // Начинаем отслеживать уровень бодрствования
    decreaseAwakeness();
    
    // Случайные баги на странице с определенным шансом
    if (Math.random() < 0.2) { // 20% шанс
        setTimeout(applyRandomGlitches, Math.random() * 5000);
    }
    
    // Отслеживаем клики для эффекта "энергетика"
    document.addEventListener('click', function(e) {
        if (Math.random() < 0.05) { // 5% шанс
            // Создаем эффект "всплеска энергетика"
            const splash = document.createElement('div');
            splash.style.position = 'fixed';
            splash.style.width = '10px';
            splash.style.height = '10px';
            splash.style.borderRadius = '50%';
            splash.style.backgroundColor = '#00FFFF';
            splash.style.left = e.clientX + 'px';
            splash.style.top = e.clientY + 'px';
            splash.style.pointerEvents = 'none';
            splash.style.zIndex = '9999';
            splash.style.transition = 'all 0.5s';
            
            document.body.appendChild(splash);
            
            setTimeout(() => {
                splash.style.width = '50px';
                splash.style.height = '50px';
                splash.style.opacity = '0';
                
                setTimeout(() => {
                    if (splash.parentNode) {
                        splash.parentNode.removeChild(splash);
                    }
                }, 500);
            }, 10);
        }
    });
});

// Имитация утечки памяти в 3 часа ночи
let memoryLeakArray = [];

function simulateMemoryLeak() {
    // Добавляем небольшой объект в массив каждую минуту
    if (Math.random() < 0.1) { // 10% шанс на утечку
        memoryLeakArray.push({
            time: new Date().toISOString(),
            randomData: 'Энергетик был здесь ' + Math.random().toString(36).substring(2)
        });
        
        // "Исправляем" утечку через 5 минут
        setTimeout(() => {
            if (Math.random() < 0.8) { // 80% шанс исправить утечку
                memoryLeakArray = [];
                console.log("Программист заметил утечку памяти и исправил её!");
            }
        }, 300000); // 5 минут
    }
    
    setTimeout(simulateMemoryLeak, 60000); // Повторяем каждую минуту
}

// Запускаем только в 10% случаев
if (Math.random() < 0.1) {
    console.log("Опасно! Программист может случайно создать утечку памяти в 3 часа ночи...");
    simulateMemoryLeak();
} 