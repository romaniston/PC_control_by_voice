import os
import ctypes


# -------------------------
# СОН ПК
# -------------------------

def sleep_pc():
    os.system(
        "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    )


# -------------------------
# ВЫКЛЮЧЕНИЕ ПК
# -------------------------

def shutdown_pc():
    os.system(
        "shutdown /s /t 0"
    )


# -------------------------
# ГРОМКОСТЬ (WinAPI)
# -------------------------
# уровень: 0–10
# реализовано через системные клавиши
# максимально стабильный способ


VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF


def set_volume(level: int):

    level = max(0, min(level, 10))

    # Сначала сбрасываем вниз почти до нуля
    for _ in range(50):
        ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)

    # Поднимаем до нужного уровня
    for _ in range(level):
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)

    print(f"Громкость: {level * 10}%")