from PIL import Image

# Открываем GIF-файл
with Image.open("g8.gif") as gif:
    # Проверяем, что файл - анимация
    if gif.is_animated:
        # Получаем длительность одного кадра в миллисекундах
        duration = gif.info['duration']
        
        # Рассчитываем FPS (частоту кадров)
        fps = 1000 / duration
        print(f"Частота кадров (FPS): {fps}")
    else:
        print("Этот GIF не является анимацией.")