import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { HomePanel } from './HomePanel';

describe('HomePanel Component', () => {
  it('renders the home panel heading', () => {
    render(<HomePanel />);
    
    const heading = screen.getByRole('heading', { name: /home panel/i });
    expect(heading).toBeInTheDocument();
    expect(heading.tagName).toBe('H1');
  });

  it('renders a div container', () => {
    const { container } = render(<HomePanel />);
    
    const div = container.querySelector('div');
    expect(div).toBeInTheDocument();
  });
});
