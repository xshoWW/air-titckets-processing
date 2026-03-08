import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)

def wait_for_enter():
    input("\n⏎ Нажмите Enter...")

def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"❌ Минимум {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ Максимум {max_val}")
                continue
            return value
        except ValueError:
            print("❌ Введите число")

def input_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['д', 'да', 'y', 'yes', '1']:
            return True
        if answer in ['н', 'нет', 'n', 'no', '0']:
            return False
        print("❌ Введите да/нет")