# Estate Chatbot - Frontend

Multilingual real estate chatbot frontend built with React, TypeScript, and Vite.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Query** - Server state management
- **Zustand** - Client state management
- **i18next** - Internationalization (ja, en, vi)
- **Vitest** - Unit testing
- **Playwright** - E2E testing
- **React Router** - Routing

## Getting Started

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

### Environment Variables

Copy `.env.example` to `.env.development` and configure:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_DEFAULT_LANGUAGE=ja
```

## Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run test         # Run unit tests
npm run test:ui      # Run tests with UI
npm run test:e2e     # Run E2E tests
npm run lint         # Lint code
npm run format       # Format code with Prettier
npm run type-check   # Check TypeScript types
```

## Project Structure

```
src/
├── app/              # Application initialization
│   ├── providers/    # Context providers
│   ├── routes/       # Route configuration
│   └── styles/       # Global styles
├── pages/            # Page components
├── widgets/          # Complex feature blocks
├── features/         # User interactions
├── entities/         # Business entities
└── shared/           # Shared code
    ├── api/          # API client
    ├── ui/           # UI components
    ├── lib/          # Utilities
    ├── hooks/        # Custom hooks
    └── types/        # TypeScript types
```

## Features

- ✅ Multilingual support (Japanese, English, Vietnamese)
- ✅ Real-time chat interface
- ✅ Property brief management
- ✅ Glossary search
- ✅ Responsive design (mobile-first)
- ✅ Type-safe with TypeScript
- ✅ 90%+ test coverage target

## Development Guidelines

### Code Style

- Use TypeScript strict mode
- Follow ESLint and Prettier configurations
- Use functional components with hooks
- Prefer named exports

### Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm run test:coverage
```

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Implementation Status

- ✅ **Phase 0: Setup & Foundation** - COMPLETE
  - Project initialization
  - Configuration files
  - Folder structure
  - i18n setup
  - Basic routing

- 🚧 **Phase 1: Core Infrastructure** - IN PROGRESS
- ⏳ **Phase 2: Chat Interface** - PENDING
- ⏳ **Phase 3: Brief Management** - PENDING
- ⏳ **Phase 4: Glossary Feature** - PENDING
- ⏳ **Phase 5: Advanced Features** - PENDING
- ⏳ **Phase 6: Testing & Documentation** - PENDING
- ⏳ **Phase 7: Production Ready** - PENDING

## License

Proprietary - Estate Chatbot Team
