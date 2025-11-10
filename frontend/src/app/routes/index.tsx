import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ChatPage } from '@/pages/ChatPage';
import { BriefPage } from '@/pages/BriefPage';
import { GlossaryPage } from '@/pages/GlossaryPage';
import { NotFoundPage } from '@/pages/NotFoundPage';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/brief/:briefId" element={<BriefPage />} />
        <Route path="/glossary" element={<GlossaryPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
