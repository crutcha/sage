def find_and_clean_element(elem, value):
    # We may or may not have the text element so always check for attribute
    result_elem = elem.find(value)
    result_text = getattr(result_elem, 'text', None)

    if result_text:
        # Re-assign with returned value
        result_text = result_text.replace('\n', '')

    return result_text