def crop(word, allowed_length):
    if len(word) > allowed_length:
        return word[:allowed_length - 4] + "..."
    return word

def draw_text_bar(allowed_rows, col_start, col_end, stdscr, pointer, words):
    center_row = int(allowed_rows / 2)
    bar_ptr = pointer
    min_ptr = pointer - center_row
    if min_ptr < 0:
        min_ptr = 0
    max_ptr = pointer + center_row
    if max_ptr >= len(words):
        max_ptr = len(words) - 1
    num_cols = col_end - col_start + 1
    stdscr.addstr(center_row, col_start, crop("> " + words[pointer], num_cols))
    current_row = center_row - 1
    while current_row >= 0:
        bar_ptr -= 1
        if bar_ptr < min_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(words[bar_ptr], num_cols))
        current_row -= 1
    current_row = center_row + 1
    bar_ptr = pointer
    while current_row < allowed_rows - 1:
        bar_ptr += 1
        if bar_ptr > max_ptr:
            break
        stdscr.addstr(current_row, col_start, crop(words[bar_ptr], num_cols))
        current_row += 1