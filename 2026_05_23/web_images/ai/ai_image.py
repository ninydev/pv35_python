import argparse
import json
import random
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="AI Water Meters Recognition - Mock Demo")
    parser.add_argument(
        "-i", "--image",
        type=str,
        required=True,
        help="Шлях до тестового фото лічильника"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        help="Шлях до файлу навченої моделі",
        default="demo/demo_2026_05/nn_models/nn640x640/640x640.pt"
    )
    parser.add_argument(
        "--show-gui",
        action="store_true",
        help="Показати вікно (Симуляція)"
    )
    parser.add_argument(
        "--show-details",
        action="store_true",
        help="Включити в JSON-відповідь детальний список усіх знайдених об'єктів"
    )

    args = parser.parse_args()

    # Симуляция проверки файлов (убрали жесткий return, чтобы можно было тестить без реальных файлов)
    if not Path(args.model).exists():
        pass  # В реальном скрипте тут ошибка, в моке просто идем дальше

    # Имитация задержки обработки нейросетью (например, от 0.5 до 1.5 секунд)
    time.sleep(random.uniform(0.5, 1.5))

    # С вероятностью 20% возвращаем ошибку, с вероятностью 80% — успех
    is_success = random.choices([True, False], weights=[80, 20])[0]

    if not is_success:
        error_reasons = [
            "Зображення занадто розмите для розпізнавання.",
            "Лічильник не знайдено в кадрі.",
            "Відблиск на склі лічильника заважає зчитуванню."
        ]
        print(json.dumps({
            "status": "error",
            "message": random.choice(error_reasons)
        }, ensure_ascii=False, indent=4))
        return

    # --- Генерация успешного результата ---

    # Генерируем случайное 5-значное показание счетчика
    reading_str = "".join([str(random.randint(0, 9)) for _ in range(5)])

    result_json_dict = {
        "status": "success",
        "reading": reading_str,
        "confidence": round(random.uniform(0.70, 0.99), 2),
        "message": "Показання успішно розпізнано"
    }

    # Если попросили детали, генерируем рамки (Bounding Boxes) для каждой цифры
    if args.show_details:
        details = []
        for i, digit in enumerate(reading_str):
            details.append({
                "class": "digit",
                "value": digit,
                "bbox": [100 + i * 40, 200, 140 + i * 40, 260],  # Имитация [x1, y1, x2, y2]
                "confidence": round(random.uniform(0.85, 0.99), 2)
            })
        result_json_dict["details"] = details

    # Виводимо форматований JSON в консоль
    print(json.dumps(result_json_dict, indent=4, ensure_ascii=False))

    # Симуляция GUI
    if args.show_gui:
        print(f"\n[GUI SIMULATION] Відкрито вікно з зображенням: {args.image}")
        print("[GUI SIMULATION] Натисніть 'q' для закриття (завершуємо автоматично у мок-версії).")


if __name__ == "__main__":
    main()