import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Row from './Row';

describe('Row Component', () => {
  it('renders the data prop correctly', () => {
    const testData = 'Test row content';
    render(<Row data={testData} />);
    
    const rowElement = screen.getByText(testData);
    expect(rowElement).toBeInTheDocument();
    expect(rowElement).toHaveClass('row');
  });

  it('renders empty string when data is empty', () => {
    render(<Row data="" />);
    
    const rowElement = document.querySelector('.row');
    expect(rowElement).toBeInTheDocument();
    expect(rowElement).toHaveTextContent('');
  });

  it('renders with different data values', () => {
    const { rerender } = render(<Row data="First value" />);
    expect(screen.getByText('First value')).toBeInTheDocument();
    
    rerender(<Row data="Second value" />);
    expect(screen.getByText('Second value')).toBeInTheDocument();
  });
});
