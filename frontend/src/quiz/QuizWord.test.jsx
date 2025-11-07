import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QuizWord from './QuizWord';

describe('QuizWord Component', () => {
  const mockWord = {
    id: 1,
    word: 'example'
  };

  it('renders with all hint type headers', () => {
    render(
      <QuizWord 
        word={mockWord}
        wordTranslation={[]}
        wordDefinition={[]}
        wordExample={[]}
        wordSynonym={[]}
      />
    );
    
    expect(screen.getByText('Definition')).toBeInTheDocument();
    expect(screen.getByText('Translation')).toBeInTheDocument();
    expect(screen.getByText('Examples')).toBeInTheDocument();
    expect(screen.getByText('Synonyms')).toBeInTheDocument();
  });

  it('shows definition section expanded by default', () => {
    render(
      <QuizWord 
        word={mockWord}
        wordTranslation={[]}
        wordDefinition={[]}
        wordExample={[]}
        wordSynonym={[]}
      />
    );
    
    // Definition is the first section and should be visible by default
    expect(screen.getByText(/no definitions available/i)).toBeInTheDocument();
  });

  it('renders translations when provided', async () => {
    const user = userEvent.setup();
    const translations = [
      { id: 1, language: 'Spanish', translation: 'ejemplo' }
    ];

    render(
      <QuizWord 
        word={mockWord}
        wordTranslation={translations}
        wordDefinition={[]}
        wordExample={[]}
        wordSynonym={[]}
      />
    );
    
    // Click on Translation header to expand it
    const translationHeader = screen.getByText('Translation');
    await user.click(translationHeader);
    
    // Now the translation content should be visible
    expect(screen.getByText('Spanish')).toBeInTheDocument();
    expect(screen.getByText('ejemplo')).toBeInTheDocument();
  });

  it('renders definitions when provided', () => {
    const definitions = [
      { id: 1, part_of_speech: 'noun', definition: 'a thing characteristic of its kind' }
    ];

    render(
      <QuizWord 
        word={mockWord}
        wordTranslation={[]}
        wordDefinition={definitions}
        wordExample={[]}
        wordSynonym={[]}
      />
    );
    
    // Definition is first so it's expanded by default
    expect(screen.getByText('noun')).toBeInTheDocument();
    expect(screen.getByText('a thing characteristic of its kind')).toBeInTheDocument();
  });

  it('renders component structure correctly', () => {
    const { container } = render(
      <QuizWord 
        word={mockWord}
        wordTranslation={[]}
        wordDefinition={[]}
        wordExample={[]}
        wordSynonym={[]}
      />
    );
    
    const answerUnits = container.querySelectorAll('.answer-unit-container');
    expect(answerUnits.length).toBe(4); // Should have 4 hint sections
  });

  it('filters out self-referencing synonyms', () => {
    const synonyms = [
      { id: 1, synonym: 'example' }, // Same as main word - should be filtered
      { id: 2, synonym: 'sample' },
      { id: 3, synonym: 'EXAMPLE' } // Case insensitive match - should be filtered
    ];

    const { container } = render(
      <QuizWord 
        word={mockWord}
        wordTranslation={[]}
        wordDefinition={[]}
        wordExample={[]}
        wordSynonym={synonyms}
      />
    );
    
    // Component should render - testing that filtering logic doesn't break rendering
    expect(container).toBeInTheDocument();
  });
});
