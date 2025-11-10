# Frontend Implementation Plan - Estate Chatbot

## 📋 Executive Summary

This document outlines the comprehensive frontend implementation plan for the Estate Chatbot system. The frontend will be a modern, responsive, multilingual (Japanese, English, Vietnamese) chat interface that integrates seamlessly with the FastAPI backend.

**Project Goals:**
- Intuitive chat interface for property search
- Multilingual support (ja, en, vi)
- Real-time conversation with AI agent
- Brief management and submission
- Glossary term lookup
- Responsive design (mobile-first)
- High performance and accessibility
- 90%+ test coverage

---

## 🛠 Technology Stack

### Core Framework
- **React 18.2+** with TypeScript
  - Modern hooks-based architecture
  - Strong type safety
  - Excellent ecosystem

### Build Tools
- **Vite 5.0+**
  - Lightning-fast HMR
  - Optimized production builds
  - Native ESM support

### State Management
- **Zustand** (lightweight alternative to Redux)
  - Simple API
  - TypeScript-first
  - Minimal boilerplate
  - Excellent DevTools

### API Communication
- **TanStack Query (React Query) v5**
  - Server state management
  - Automatic caching and revalidation
  - Optimistic updates
  - Request deduplication

### Styling
- **Tailwind CSS 3.4+**
  - Utility-first approach
  - Highly customizable
  - Excellent mobile support
- **shadcn/ui** components
  - Beautiful, accessible components
  - Radix UI primitives
  - Customizable with Tailwind

### Internationalization
- **i18next + react-i18next**
  - Industry standard
  - Robust pluralization
  - Namespace support
  - Language detection

### Form Management
- **React Hook Form**
  - Performant validation
  - TypeScript support
  - Minimal re-renders

### Testing
- **Vitest** (unit/integration tests)
- **Testing Library** (React Testing Library)
- **Playwright** (E2E tests)
- **MSW** (Mock Service Worker) for API mocking

### Code Quality
- **ESLint** + **Prettier**
- **TypeScript strict mode**
- **Husky** for git hooks
- **Commitlint** for conventional commits

---

## 🏗 Architecture Overview

### Architecture Pattern
**Feature-Sliced Design (FSD)**

```
frontend/
├── src/
│   ├── app/                 # Application initialization
│   │   ├── providers/       # Context providers
│   │   ├── routes/          # Route configuration
│   │   └── styles/          # Global styles
│   │
│   ├── pages/               # Page components
│   │   ├── ChatPage/        # Main chat interface
│   │   ├── BriefPage/       # Brief summary/edit
│   │   └── GlossaryPage/    # Glossary browser
│   │
│   ├── widgets/             # Complex feature blocks
│   │   ├── ChatWidget/      # Chat container
│   │   ├── BriefWidget/     # Brief display
│   │   └── HeaderWidget/    # App header
│   │
│   ├── features/            # User interactions
│   │   ├── send-message/    # Message sending
│   │   ├── create-session/  # Session creation
│   │   ├── submit-brief/    # Brief submission
│   │   └── search-glossary/ # Glossary search
│   │
│   ├── entities/            # Business entities
│   │   ├── session/         # Session entity
│   │   ├── message/         # Message entity
│   │   ├── brief/           # Brief entity
│   │   └── glossary/        # Glossary entity
│   │
│   ├── shared/              # Shared code
│   │   ├── api/             # API client
│   │   ├── ui/              # UI components
│   │   ├── lib/             # Utilities
│   │   ├── hooks/           # Custom hooks
│   │   └── types/           # TypeScript types
│   │
│   └── main.tsx             # Entry point
```

### Core Principles
1. **Separation of Concerns** - Clear boundaries between layers
2. **Unidirectional Data Flow** - Predictable state updates
3. **Type Safety** - TypeScript everywhere
4. **Testability** - Easy to mock and test
5. **Performance** - Code splitting and lazy loading

---

## 🧩 Component Hierarchy

### Page Components

#### 1. ChatPage (Main Page)
```
ChatPage
├── HeaderWidget
│   ├── LanguageSelector
│   ├── SessionInfo
│   └── HelpButton
├── ChatWidget
│   ├── MessageList
│   │   ├── MessageItem (user)
│   │   ├── MessageItem (assistant)
│   │   ├── TypingIndicator
│   │   └── ScrollToBottom
│   ├── MessageInput
│   │   ├── TextArea
│   │   ├── SendButton
│   │   ├── AttachButton (future)
│   │   └── EmojiPicker (future)
│   └── QuickActions
│       ├── BuyButton
│       ├── RentButton
│       └── SellButton
├── BriefSidePanel (collapsible)
│   ├── BriefSummary
│   ├── BriefProgress
│   └── SubmitButton
└── GlossaryPanel (modal/drawer)
    ├── SearchInput
    └── TermList
```

#### 2. BriefPage
```
BriefPage
├── BriefHeader
├── BriefForm
│   ├── PropertyTypeSelector
│   ├── LocationInput
│   ├── BudgetRangeInput
│   ├── RoomsSelector
│   └── AdditionalFields
├── BriefPreview
└── SubmitSection
    ├── ValidationErrors
    └── SubmitButton
```

#### 3. GlossaryPage
```
GlossaryPage
├── GlossaryHeader
├── SearchBar
├── CategoryFilter
├── TermGrid/List
│   └── TermCard
│       ├── TermTitle
│       ├── Translation
│       ├── Explanation
│       └── Examples
└── Pagination
```

---

## 📦 State Management Strategy

### State Types

#### 1. Server State (React Query)
- Session data
- Messages history
- Brief data
- Glossary terms
- **Why:** Auto-caching, revalidation, sync

#### 2. Client State (Zustand)
- UI state (sidebars, modals)
- Current language
- Theme preferences
- Temporary form data

#### 3. URL State (React Router)
- Current page
- Session ID
- Query parameters

### Zustand Stores

```typescript
// stores/uiStore.ts
interface UIStore {
  isBriefPanelOpen: boolean;
  isGlossaryOpen: boolean;
  toggleBriefPanel: () => void;
  toggleGlossary: () => void;
}

// stores/sessionStore.ts
interface SessionStore {
  currentSessionId: string | null;
  setCurrentSessionId: (id: string) => void;
  clearSession: () => void;
}

// stores/languageStore.ts
interface LanguageStore {
  language: 'ja' | 'en' | 'vi';
  setLanguage: (lang: 'ja' | 'en' | 'vi') => void;
}
```

### React Query Hooks

```typescript
// hooks/useSession.ts
const useSession = (sessionId: string) => {
  return useQuery({
    queryKey: ['session', sessionId],
    queryFn: () => api.getSession(sessionId),
  });
};

// hooks/useMessages.ts
const useMessages = (sessionId: string) => {
  return useQuery({
    queryKey: ['messages', sessionId],
    queryFn: () => api.getMessages(sessionId),
  });
};

// hooks/useSendMessage.ts
const useSendMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.sendMessage,
    onSuccess: (data, variables) => {
      // Optimistic update
      queryClient.invalidateQueries(['messages', variables.sessionId]);
    },
  });
};
```

---

## 🎨 UI/UX Design Specifications

### Design Principles
1. **Minimalist** - Clean, uncluttered interface
2. **Conversational** - Chat-first experience
3. **Accessible** - WCAG 2.1 AA compliance
4. **Responsive** - Mobile-first approach
5. **Performant** - <100ms interactions

### Color Palette

```typescript
// Theme configuration
const colors = {
  // Primary (Real estate blue)
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
  },

  // Neutral
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    500: '#6b7280',
    700: '#374151',
    900: '#111827',
  },

  // Success (for positive actions)
  success: '#10b981',

  // Warning (for important info)
  warning: '#f59e0b',

  // Error
  error: '#ef4444',
};
```

### Typography

```typescript
const typography = {
  fontFamily: {
    sans: ['Inter', 'Noto Sans JP', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },

  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
  },
};
```

### Component Specifications

#### Message Bubble
- **User messages:** Right-aligned, blue background
- **Assistant messages:** Left-aligned, gray background
- **Max width:** 70% on desktop, 85% on mobile
- **Border radius:** 16px
- **Padding:** 12px 16px
- **Shadow:** subtle drop shadow
- **Animation:** Fade in + slide up (200ms)

#### Input Area
- **Position:** Fixed bottom (mobile) / Sticky (desktop)
- **Height:** Auto-expand (max 5 lines)
- **Border:** 2px solid on focus
- **Send button:** Disabled when empty
- **Loading state:** Pulsing animation

#### Brief Panel
- **Width:** 320px (desktop) / Full width (mobile)
- **Position:** Right sidebar (desktop) / Bottom sheet (mobile)
- **Animation:** Slide from right
- **Progress indicator:** Circular progress (0-100%)

---

## 🌍 Internationalization Strategy

### Language Support
1. **Japanese (ja)** - Primary
2. **English (en)** - Secondary
3. **Vietnamese (vi)** - Tertiary

### i18n Structure

```typescript
// locales/ja/translation.json
{
  "chat": {
    "title": "不動産チャット",
    "placeholder": "メッセージを入力...",
    "send": "送信",
    "typing": "入力中..."
  },
  "propertyTypes": {
    "buy": "購入",
    "rent": "賃貸",
    "sell": "売却"
  },
  "brief": {
    "title": "物件情報",
    "submit": "送信",
    "completeness": "完了度"
  }
}

// locales/en/translation.json
{
  "chat": {
    "title": "Real Estate Chat",
    "placeholder": "Type a message...",
    "send": "Send",
    "typing": "Typing..."
  },
  // ... etc
}
```

### Language Detection
1. **URL parameter:** `?lang=ja`
2. **Browser language:** `navigator.language`
3. **Local storage:** Persistent preference
4. **Default:** Japanese

---

## 🧪 Testing Strategy

### Test Pyramid

```
        E2E Tests (10%)
      ─────────────────
     Integration Tests (20%)
   ─────────────────────────
  Unit Tests (70%)
─────────────────────────────
```

### Unit Tests (Vitest)
- **Target:** 90% coverage
- **Focus:**
  - Component logic
  - Utility functions
  - Hooks
  - State management

```typescript
// Example: MessageItem.test.tsx
describe('MessageItem', () => {
  it('renders user message correctly', () => {
    render(<MessageItem role="user" content="Hello" />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('applies correct styling for assistant', () => {
    render(<MessageItem role="assistant" content="Hi" />);
    const bubble = screen.getByTestId('message-bubble');
    expect(bubble).toHaveClass('bg-gray-100');
  });
});
```

### Integration Tests (Testing Library)
- **Focus:**
  - Feature workflows
  - API integration
  - State synchronization

```typescript
// Example: ChatWidget.integration.test.tsx
describe('ChatWidget Integration', () => {
  it('sends message and displays response', async () => {
    render(<ChatWidget sessionId="test-123" />);

    const input = screen.getByPlaceholderText('Type a message...');
    await userEvent.type(input, 'Hello');
    await userEvent.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument();
    });
  });
});
```

### E2E Tests (Playwright)
- **Focus:**
  - Critical user journeys
  - Cross-browser testing
  - Performance monitoring

```typescript
// Example: buy-flow.e2e.ts
test('complete buy property flow', async ({ page }) => {
  await page.goto('/');

  // Select language
  await page.click('[data-testid="language-selector"]');
  await page.click('[data-testid="lang-ja"]');

  // Start conversation
  await page.fill('[data-testid="message-input"]', 'マンションを買いたい');
  await page.click('[data-testid="send-button"]');

  // Wait for response
  await expect(page.locator('[data-testid="assistant-message"]').first())
    .toBeVisible();

  // Continue flow...
});
```

### API Mocking (MSW)

```typescript
// mocks/handlers.ts
export const handlers = [
  rest.post('/api/v1/sessions', (req, res, ctx) => {
    return res(
      ctx.json({
        session_id: 'mock-session-123',
        status: 'active',
        created_at: new Date().toISOString(),
      })
    );
  }),

  rest.post('/api/v1/sessions/:id/messages', (req, res, ctx) => {
    return res(
      ctx.json({
        message_id: 'mock-msg-123',
        response: 'こんにちは！',
        intent: 'greeting',
      })
    );
  }),
];
```

---

## 📁 Detailed File Structure

```
frontend/
├── public/
│   ├── locales/              # i18n translation files
│   │   ├── ja/
│   │   │   └── translation.json
│   │   ├── en/
│   │   │   └── translation.json
│   │   └── vi/
│   │       └── translation.json
│   └── favicon.ico
│
├── src/
│   ├── app/
│   │   ├── providers/
│   │   │   ├── AppProviders.tsx    # All providers wrapper
│   │   │   ├── QueryProvider.tsx   # React Query
│   │   │   └── I18nProvider.tsx    # i18next
│   │   ├── routes/
│   │   │   ├── index.tsx           # Route definitions
│   │   │   └── ProtectedRoute.tsx
│   │   ├── styles/
│   │   │   ├── globals.css         # Global styles
│   │   │   └── tailwind.css
│   │   └── App.tsx
│   │
│   ├── pages/
│   │   ├── ChatPage/
│   │   │   ├── index.tsx
│   │   │   └── ChatPage.test.tsx
│   │   ├── BriefPage/
│   │   │   ├── index.tsx
│   │   │   └── BriefPage.test.tsx
│   │   ├── GlossaryPage/
│   │   │   ├── index.tsx
│   │   │   └── GlossaryPage.test.tsx
│   │   └── NotFoundPage/
│   │       └── index.tsx
│   │
│   ├── widgets/
│   │   ├── ChatWidget/
│   │   │   ├── index.tsx
│   │   │   ├── ChatWidget.test.tsx
│   │   │   └── styles.module.css
│   │   ├── HeaderWidget/
│   │   │   ├── index.tsx
│   │   │   └── HeaderWidget.test.tsx
│   │   └── BriefWidget/
│   │       ├── index.tsx
│   │       └── BriefWidget.test.tsx
│   │
│   ├── features/
│   │   ├── send-message/
│   │   │   ├── ui/
│   │   │   │   ├── MessageInput.tsx
│   │   │   │   └── SendButton.tsx
│   │   │   ├── model/
│   │   │   │   └── useSendMessage.ts
│   │   │   └── index.ts
│   │   ├── create-session/
│   │   │   ├── ui/
│   │   │   │   └── CreateSessionButton.tsx
│   │   │   ├── model/
│   │   │   │   └── useCreateSession.ts
│   │   │   └── index.ts
│   │   ├── submit-brief/
│   │   │   ├── ui/
│   │   │   │   └── SubmitButton.tsx
│   │   │   ├── model/
│   │   │   │   └── useSubmitBrief.ts
│   │   │   └── index.ts
│   │   └── search-glossary/
│   │       ├── ui/
│   │       │   └── SearchBar.tsx
│   │       ├── model/
│   │       │   └── useSearchGlossary.ts
│   │       └── index.ts
│   │
│   ├── entities/
│   │   ├── session/
│   │   │   ├── model/
│   │   │   │   ├── types.ts
│   │   │   │   ├── store.ts
│   │   │   │   └── hooks.ts
│   │   │   ├── api/
│   │   │   │   └── sessionApi.ts
│   │   │   └── index.ts
│   │   ├── message/
│   │   │   ├── model/
│   │   │   │   ├── types.ts
│   │   │   │   └── hooks.ts
│   │   │   ├── api/
│   │   │   │   └── messageApi.ts
│   │   │   ├── ui/
│   │   │   │   └── MessageItem.tsx
│   │   │   └── index.ts
│   │   ├── brief/
│   │   │   ├── model/
│   │   │   │   ├── types.ts
│   │   │   │   └── hooks.ts
│   │   │   ├── api/
│   │   │   │   └── briefApi.ts
│   │   │   └── index.ts
│   │   └── glossary/
│   │       ├── model/
│   │       │   ├── types.ts
│   │       │   └── hooks.ts
│   │       ├── api/
│   │       │   └── glossaryApi.ts
│   │       ├── ui/
│   │       │   └── TermCard.tsx
│   │       └── index.ts
│   │
│   ├── shared/
│   │   ├── api/
│   │   │   ├── client.ts           # Axios instance
│   │   │   ├── types.ts            # API types
│   │   │   └── errors.ts           # Error handling
│   │   ├── ui/
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   └── Button.test.tsx
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   ├── Spinner/
│   │   │   ├── Avatar/
│   │   │   └── index.ts
│   │   ├── lib/
│   │   │   ├── utils.ts            # Helper functions
│   │   │   ├── date.ts
│   │   │   ├── format.ts
│   │   │   └── validation.ts
│   │   ├── hooks/
│   │   │   ├── useDebounce.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── useMediaQuery.ts
│   │   │   └── useClickOutside.ts
│   │   ├── types/
│   │   │   ├── common.ts
│   │   │   └── api.ts
│   │   └── constants/
│   │       ├── routes.ts
│   │       └── config.ts
│   │
│   ├── main.tsx                    # Entry point
│   └── vite-env.d.ts
│
├── tests/
│   ├── e2e/
│   │   ├── buy-flow.spec.ts
│   │   ├── rent-flow.spec.ts
│   │   └── sell-flow.spec.ts
│   ├── mocks/
│   │   ├── handlers.ts
│   │   └── server.ts
│   └── setup.ts
│
├── .env.example
├── .env.development
├── .env.production
├── .eslintrc.json
├── .prettierrc
├── index.html
├── package.json
├── playwright.config.ts
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── vite.config.ts
└── vitest.config.ts
```

---

## 🚀 Implementation Phases

### Phase 0: Setup & Foundation (Week 1)
**Goal:** Initialize project with proper tooling

**Tasks:**
- [ ] Initialize Vite + React + TypeScript project
- [ ] Configure Tailwind CSS + shadcn/ui
- [ ] Set up ESLint, Prettier, Husky
- [ ] Configure testing environment (Vitest, Testing Library, Playwright)
- [ ] Set up i18next with Japanese, English, Vietnamese
- [ ] Create base folder structure (FSD)
- [ ] Configure environment variables
- [ ] Set up CI/CD pipeline (GitHub Actions)

**Deliverables:**
- Empty project with all tooling configured
- README with setup instructions
- CI pipeline running linting + tests

---

### Phase 1: Core Infrastructure (Week 2)
**Goal:** Build foundational layers

**Tasks:**
- [ ] Create API client with axios/fetch
- [ ] Set up React Query configuration
- [ ] Create Zustand stores (UI, session, language)
- [ ] Build shared UI components (Button, Input, Modal, Spinner)
- [ ] Create custom hooks (useDebounce, useLocalStorage, useMediaQuery)
- [ ] Set up routing with React Router
- [ ] Create AppProviders wrapper
- [ ] Implement error boundary
- [ ] Create loading states
- [ ] Set up MSW for API mocking

**Deliverables:**
- Reusable UI component library
- API client with error handling
- State management scaffolding
- 80%+ test coverage

---

### Phase 2: Chat Interface (Week 3-4)
**Goal:** Build core chat functionality

**Tasks:**
- [ ] Create session entity (types, hooks, API)
- [ ] Create message entity (types, hooks, API, UI)
- [ ] Build MessageItem component
- [ ] Build MessageList component
- [ ] Build MessageInput component
- [ ] Implement send-message feature
- [ ] Implement create-session feature
- [ ] Build ChatWidget
- [ ] Build ChatPage
- [ ] Add typing indicator
- [ ] Add scroll-to-bottom functionality
- [ ] Add message timestamps
- [ ] Implement optimistic updates
- [ ] Add error handling and retry logic
- [ ] Mobile responsive design

**Deliverables:**
- Fully functional chat interface
- Real-time message exchange
- Responsive design (mobile + desktop)
- 85%+ test coverage
- E2E test for basic chat flow

---

### Phase 3: Brief Management (Week 5)
**Goal:** Implement brief creation and submission

**Tasks:**
- [ ] Create brief entity (types, hooks, API)
- [ ] Build BriefSummary component
- [ ] Build BriefProgress component
- [ ] Build BriefWidget
- [ ] Implement submit-brief feature
- [ ] Build BriefPage (full brief editor)
- [ ] Add brief validation
- [ ] Add completeness calculation
- [ ] Integrate with chat (auto-populate from conversation)
- [ ] Add brief submission confirmation
- [ ] Mobile responsive design

**Deliverables:**
- Brief side panel in chat
- Full brief editing page
- Brief submission workflow
- 85%+ test coverage
- E2E test for brief submission

---

### Phase 4: Glossary Feature (Week 6)
**Goal:** Implement glossary search and display

**Tasks:**
- [ ] Create glossary entity (types, hooks, API, UI)
- [ ] Build TermCard component
- [ ] Build SearchBar component
- [ ] Implement search-glossary feature
- [ ] Build GlossaryPanel (modal/drawer)
- [ ] Build GlossaryPage
- [ ] Add category filtering
- [ ] Add term highlighting in messages
- [ ] Add quick glossary access from chat
- [ ] Mobile responsive design

**Deliverables:**
- Glossary search functionality
- Glossary browser page
- Term highlighting in chat
- 85%+ test coverage
- E2E test for glossary search

---

### Phase 5: Advanced Features (Week 7)
**Goal:** Add polish and advanced functionality

**Tasks:**
- [ ] Add quick action buttons (Buy, Rent, Sell)
- [ ] Implement language switcher
- [ ] Add session management (history, delete)
- [ ] Add conversation export
- [ ] Implement dark mode
- [ ] Add accessibility improvements (ARIA labels, keyboard nav)
- [ ] Add loading skeletons
- [ ] Add empty states
- [ ] Add error states
- [ ] Optimize performance (code splitting, lazy loading)
- [ ] Add analytics tracking

**Deliverables:**
- Polished user experience
- Accessibility compliance
- Performance optimizations
- Analytics integration

---

### Phase 6: Testing & Documentation (Week 8)
**Goal:** Comprehensive testing and documentation

**Tasks:**
- [ ] Reach 90%+ unit test coverage
- [ ] Create E2E tests for all critical flows
- [ ] Performance testing (Lighthouse)
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] Accessibility audit (WAVE, axe)
- [ ] Create user documentation
- [ ] Create developer documentation
- [ ] Create Storybook for components
- [ ] Load testing
- [ ] Security audit

**Deliverables:**
- 90%+ test coverage
- E2E test suite
- Performance report
- Accessibility report
- Complete documentation
- Storybook component library

---

### Phase 7: Production Ready (Week 9)
**Goal:** Deploy to production

**Tasks:**
- [ ] Configure production environment
- [ ] Set up CDN for static assets
- [ ] Implement monitoring (Sentry, LogRocket)
- [ ] Set up error tracking
- [ ] Configure analytics (Google Analytics / Plausible)
- [ ] Create deployment pipeline
- [ ] Perform security hardening
- [ ] Create runbook for operations
- [ ] Conduct final QA
- [ ] Deploy to staging
- [ ] User acceptance testing
- [ ] Deploy to production

**Deliverables:**
- Production-ready application
- Monitoring and alerting
- Deployment pipeline
- Operational documentation

---

## 🔧 Development Setup

### Prerequisites
```bash
Node.js >= 18.0.0
npm >= 9.0.0 or pnpm >= 8.0.0
```

### Installation

```bash
# Clone repository
git clone <repo-url>
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.development

# Start development server
npm run dev
```

### Environment Variables

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_MOCK_API=false
VITE_LOG_LEVEL=debug

# .env.production
VITE_API_BASE_URL=https://api.estate-chatbot.com/api/v1
VITE_WS_URL=wss://api.estate-chatbot.com/ws
VITE_ENABLE_MOCK_API=false
VITE_LOG_LEVEL=error
```

### Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "lint": "eslint src --ext ts,tsx",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "type-check": "tsc --noEmit",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  }
}
```

---

## 📊 Performance Targets

### Load Time
- **First Contentful Paint (FCP):** < 1.5s
- **Largest Contentful Paint (LCP):** < 2.5s
- **Time to Interactive (TTI):** < 3.5s
- **Cumulative Layout Shift (CLS):** < 0.1

### Bundle Size
- **Initial JS bundle:** < 200KB (gzipped)
- **CSS bundle:** < 50KB (gzipped)
- **Code splitting:** Lazy load routes

### Runtime Performance
- **Frame rate:** 60 FPS
- **Message rendering:** < 16ms per message
- **Scroll performance:** No jank
- **Memory usage:** < 50MB baseline

---

## 🔒 Security Considerations

1. **XSS Prevention**
   - Sanitize user input
   - Use `dangerouslySetInnerHTML` sparingly
   - Content Security Policy headers

2. **CSRF Protection**
   - CSRF tokens for state-changing operations
   - SameSite cookie attributes

3. **API Security**
   - HTTPS only
   - API key in headers (not URL)
   - Request rate limiting

4. **Data Privacy**
   - No sensitive data in localStorage
   - Encrypt sensitive data at rest
   - PII handling compliance

5. **Dependency Security**
   - Regular `npm audit`
   - Dependabot for updates
   - Pin critical dependencies

---

## 📈 Monitoring & Analytics

### Error Tracking
- **Sentry** for error monitoring
- Source maps upload
- User context in error reports

### Analytics
- **Plausible** or **Google Analytics 4**
- Event tracking:
  - Session creation
  - Message sent
  - Brief submission
  - Glossary searches
  - Language changes

### Performance Monitoring
- **Web Vitals** tracking
- Lighthouse CI in pipeline
- Real User Monitoring (RUM)

---

## 🎯 Success Metrics

### Technical Metrics
- [ ] 90%+ test coverage
- [ ] Lighthouse score > 90
- [ ] Zero critical security vulnerabilities
- [ ] < 2s average load time
- [ ] < 1% error rate

### User Experience Metrics
- [ ] < 100ms message send latency
- [ ] > 95% message delivery success rate
- [ ] Zero layout shifts
- [ ] WCAG 2.1 AA compliance

### Business Metrics
- [ ] Session completion rate > 70%
- [ ] Brief submission rate > 40%
- [ ] Average session duration > 5 minutes
- [ ] Return user rate > 30%

---

## 🤝 Team & Resources

### Required Skills
- **Frontend Developer (2x):** React, TypeScript, Testing
- **UI/UX Designer (1x):** Figma, Design systems
- **QA Engineer (1x):** E2E testing, Playwright

### Estimated Effort
- **Total:** 9 weeks (1 sprint = 2 weeks)
- **Development:** 7 weeks
- **Testing & QA:** 1 week
- **Deployment & Launch:** 1 week

### Dependencies
- Backend API must be complete and stable
- Design assets (icons, illustrations)
- Translation services for i18n content

---

## 📚 Additional Resources

### Documentation
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [TanStack Query Docs](https://tanstack.com/query)
- [Vitest Documentation](https://vitest.dev)
- [Playwright Documentation](https://playwright.dev)

### Design References
- [shadcn/ui](https://ui.shadcn.com)
- [Radix UI](https://www.radix-ui.com)
- [Real Estate UI Examples](https://dribbble.com/tags/real-estate-chat)

### Similar Projects
- Intercom chat widget
- Drift chat interface
- Zendesk messaging

---

## ✅ Next Steps

1. **Get approval on this plan**
2. **Set up frontend repository**
3. **Kickoff Phase 0: Setup & Foundation**
4. **Daily standups to track progress**
5. **Weekly demos to stakeholders**

---

**Last Updated:** 2025-11-10
**Version:** 1.0
**Status:** Ready for Review

