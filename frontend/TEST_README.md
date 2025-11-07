# Frontend Testing

This directory contains the React frontend application with comprehensive test coverage using Vitest and React Testing Library.

## Test Infrastructure

- **Test Runner**: Vitest
- **Testing Library**: React Testing Library
- **Assertion Library**: @testing-library/jest-dom
- **DOM Environment**: jsdom

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm run test
```

### Run tests with UI
```bash
npm run test:ui
```

### Run tests with coverage
```bash
npm run test:coverage
```

## Test Files

Tests are located alongside their corresponding components with the `.test.jsx` extension:

- `src/quiz/Row.test.jsx` - Tests for the Row component
- `src/quiz/QuizWord.test.jsx` - Tests for the QuizWord component with collapsible sections
- `src/quiz/QuizAnswerUnit.test.jsx` - Tests for the QuizAnswerUnit collapsible component
- `src/home/HomePanel.test.jsx` - Tests for the HomePanel component
- `src/vocabularies/UnitCell.test.jsx` - Tests for the interactive UnitCell component
- `src/exerciese/Exercise.test.jsx` - Tests for the Exercise component

## Test Setup

The test setup is configured in `src/test/setup.js` which:
- Extends Vitest's expect with React Testing Library matchers
- Configures automatic cleanup after each test

## Writing Tests

Example test structure:

```javascript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

For components with user interactions:

```javascript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('handles click events', async () => {
    const user = userEvent.setup();
    render(<MyComponent />);
    
    await user.click(screen.getByRole('button'));
    expect(screen.getByText('Clicked')).toBeInTheDocument();
  });
});
```

## Current Test Coverage

- 6 test suites
- 26 passing tests
- Components tested:
  - Simple presentational components (Row, HomePanel, Exercise)
  - Interactive components with state (UnitCell, QuizAnswerUnit)
  - Complex components with data transformation (QuizWord)

## Notes

- Some tests may show `act()` warnings - these are informational and don't indicate test failures
- The tests are designed to test component behavior from a user's perspective
- Mock functions are used to test callbacks and interactions
