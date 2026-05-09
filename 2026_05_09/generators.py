def doctor_reception(patients_queue):
    print("👨‍⚕️ Доктор: Начинаю смену. Открываю дверь кабинета.")

    for patient in patients_queue:
        print(f"\n👨‍⚕️ Доктор: Следующий! Заходите, {patient}.")

        # yield ставит функцию НА ПАУЗУ. Доктор лечит пациента и ждет.
        yield f"🩺 Идет осмотр пациента: {patient}"

        # Этот код выполнится только когда вызовут next() в следующий раз
        print(f"👨‍⚕️ Доктор: До свидания, {patient}. Заполняю карточку...")

    print("\n👨‍⚕️ Доктор: Очередь закончилась. Смена окончена, иду домой!")


# Наша очередь в коридоре
waiting_room = ["Иванов", "Петров", "Сидорова"]

# Доктор садится за стол (создаем объект генератора)
# В этот момент прием еще НЕ начался!
reception = doctor_reception(waiting_room)

print("--- Время: 09:00 ---")
# Вызываем первого пациента
current_patient = next(reception)
print(current_patient)

print("\n--- Время: 09:30 (прошло полчаса) ---")
# Вызываем второго
current_patient = next(reception)
print(current_patient)

print("\n--- Время: 10:00 ---")
# Вызываем третьего
current_patient = next(reception)
print(current_patient)
