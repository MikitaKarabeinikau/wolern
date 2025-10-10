from .fetchers import get_cefr_level, get_frequency # Absolute import

if __name__ == "__main__":
    test = get_cefr_level('example')

    print(f'Test fetcher result for "example": {test}')
    freq = get_frequency('example')
    print(f'Frequency for "example": {freq}')

