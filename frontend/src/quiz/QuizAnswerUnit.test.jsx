import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QuizAnswerUnit from './QuizAnswerUnit';

describe('QuizAnswerUnit Component', () => {
  it('renders hint type header', () => {
    render(
      <QuizAnswerUnit 
        hintType="Translation" 
        hintInfo={<p>Test info</p>}
        isFirst={false}
      />
    );
    
    expect(screen.getByText('Translation')).toBeInTheDocument();
  });

  it('is collapsed by default when isFirst is false', () => {
    render(
      <QuizAnswerUnit 
        hintType="Translation" 
        hintInfo={<p>Test info</p>}
        isFirst={false}
      />
    );
    
    // Content should not be visible
    expect(screen.queryByText('Test info')).not.toBeInTheDocument();
  });

  it('is expanded by default when isFirst is true', () => {
    render(
      <QuizAnswerUnit 
        hintType="Definition" 
        hintInfo={<p>Test definition</p>}
        isFirst={true}
      />
    );
    
    // Content should be visible
    expect(screen.getByText('Test definition')).toBeInTheDocument();
  });

  it('toggles collapse state when clicked', async () => {
    const user = userEvent.setup();
    
    render(
      <QuizAnswerUnit 
        hintType="Synonyms" 
        hintInfo={<p>Synonym list</p>}
        isFirst={false}
      />
    );
    
    // Initially collapsed
    expect(screen.queryByText('Synonym list')).not.toBeInTheDocument();
    
    // Click to expand
    const header = screen.getByText('Synonyms');
    await user.click(header);
    
    // Now should be visible
    expect(screen.getByText('Synonym list')).toBeInTheDocument();
    
    // Click again to collapse
    await user.click(header);
    
    // Should be hidden again
    expect(screen.queryByText('Synonym list')).not.toBeInTheDocument();
  });

  it('applies correct CSS classes', () => {
    const { container } = render(
      <QuizAnswerUnit 
        hintType="Examples" 
        hintInfo={<p>Example sentences</p>}
        isFirst={true}
      />
    );
    
    const answerUnit = container.querySelector('.answer-unit-container');
    expect(answerUnit).toBeInTheDocument();
    expect(answerUnit).toHaveClass('first-child');
    expect(answerUnit).not.toHaveClass('collapsed');
  });

  it('applies collapsed class when initially collapsed', () => {
    const { container } = render(
      <QuizAnswerUnit 
        hintType="Examples" 
        hintInfo={<p>Example sentences</p>}
        isFirst={false}
      />
    );
    
    const answerUnit = container.querySelector('.answer-unit-container');
    expect(answerUnit).toHaveClass('collapsed');
  });
});
