def _build_bad_char_table(pattern):
    bad_char = {}
    length = len(pattern)
    for i in range(length - 1):
        bad_char[pattern[i]] = length - 1 - i
    return bad_char

def boyer_moore_search(text, pattern):
    """
    Поиск подстроки pattern в строке text.
    Возвращает индекс первого вхождения или -1. 
    Регистронезависимый.
    """
    text = str(text).lower()
    pattern = str(pattern).lower()
    
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return 0
    if m > n:
        return -1
        
    bad_char = _build_bad_char_table(pattern)
    shift = 0
    
    while shift <= (n - m):
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
            
        if j < 0:
            return shift  # Совпадение найдено
        else:
            char_shift = bad_char.get(text[shift + j], m)
            shift += max(1, char_shift)
            
    return -1