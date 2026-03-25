import pyCandle
import sys

def scan():
    try:
        # 1. Inicjalizacja adaptera
        # UWAGA: Jeśli w candletool bitrate był inny niż 1M, zmień to tutaj!
        candle = pyCandle.attachCandle(pyCandle.CAN_DATARATE_1M, pyCandle.USB)
        print("--- Adapter USB-CAN podłączony ---")
    except Exception as e:
        print(f"Błąd: Nie można połączyć się z adapterem USB: {e}")
        return

    print("Skanowanie ID od 1 do 500... (to potrwa chwilę)")
    found_any = False
    
    for can_id in range(1, 501):
        md = pyCandle.MD(can_id, candle)
        # Próbujemy zainicjować sterownik
        if md.init() == pyCandle.OK:
            print(f">>> ZNALEZIONO STEROWNIK: ID = {can_id}")
            found_any = True
    
    if not found_any:
        print("Nie znaleziono żadnego sterownika. Sprawdź Bitrate.")

if __name__ == "__main__":
    scan()
