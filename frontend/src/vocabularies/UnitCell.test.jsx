import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UnitCell from './UnitCell';

describe('UnitCell Component', () => {
  const mockItem = {
    id: 1,
    text: 'Test item text'
  };

  let mockOnUpdate;
  let mockOnDelete;

  beforeEach(() => {
    mockOnUpdate = vi.fn();
    mockOnDelete = vi.fn();
  });

  it('renders the item text in display mode', () => {
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    expect(screen.getByText('Test item text')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument();
  });

  it('calls onDelete when delete button is clicked', () => {
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);
    
    expect(mockOnDelete).toHaveBeenCalledWith(mockItem.id);
  });

  it('switches to edit mode when edit button is clicked', () => {
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);
    
    // In edit mode, we should see a textarea with the text
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toHaveValue('Test item text');
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });

  it('updates text and calls onUpdate when save is clicked', async () => {
    const user = userEvent.setup();
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    // Enter edit mode
    const editButton = screen.getByRole('button', { name: /edit/i });
    await user.click(editButton);
    
    // Change the text
    const textarea = screen.getByRole('textbox');
    await user.clear(textarea);
    await user.type(textarea, 'Updated text');
    
    // Save the changes
    const saveButton = screen.getByRole('button', { name: /save/i });
    await user.click(saveButton);
    
    expect(mockOnUpdate).toHaveBeenCalledWith(mockItem.id, 'Updated text');
  });

  it('cancels editing and reverts to display mode when cancel is clicked', async () => {
    const user = userEvent.setup();
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    // Enter edit mode
    const editButton = screen.getByRole('button', { name: /edit/i });
    await user.click(editButton);
    
    // Change the text
    const textarea = screen.getByRole('textbox');
    await user.clear(textarea);
    await user.type(textarea, 'Changed text');
    
    // Cancel the changes
    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    await user.click(cancelButton);
    
    // Should be back in display mode with original text
    expect(screen.getByText('Test item text')).toBeInTheDocument();
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    expect(mockOnUpdate).not.toHaveBeenCalled();
  });

  it('preserves original text in display mode during editing', () => {
    render(<UnitCell item={mockItem} onUpdate={mockOnUpdate} onDelete={mockOnDelete} />);
    
    // Enter edit mode
    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);
    
    // Original text should still be visible in edit mode
    const displayTexts = screen.getAllByText('Test item text');
    expect(displayTexts.length).toBeGreaterThan(0);
  });
});
