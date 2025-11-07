import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Exercise from './Exercise';

describe('Exercise Component', () => {
  it('renders the exercise title', () => {
    render(<Exercise data={{}} />);
    
    const title = screen.getByRole('heading', { name: /exercise title/i });
    expect(title).toBeInTheDocument();
    expect(title.tagName).toBe('H1');
  });

  it('renders with data prop', () => {
    const mockData = { id: 1, name: 'Test Exercise' };
    const { container } = render(<Exercise data={mockData} />);
    
    expect(container).toBeInTheDocument();
  });

  it('renders without data prop', () => {
    const { container } = render(<Exercise />);
    
    expect(container).toBeInTheDocument();
    expect(screen.getByText(/exercise title/i)).toBeInTheDocument();
  });
});
