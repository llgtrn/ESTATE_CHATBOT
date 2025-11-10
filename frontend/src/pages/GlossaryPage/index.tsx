import { useTranslation } from 'react-i18next';

export function GlossaryPage() {
  const { t } = useTranslation();

  return (
    <div className="flex h-screen flex-col">
      <header className="border-b bg-white px-4 py-3">
        <h1 className="text-xl font-semibold">{t('glossary.title')}</h1>
      </header>
      <main className="flex-1 overflow-auto p-4">
        <div className="mx-auto max-w-4xl">
          <p className="text-gray-600">{t('glossary.search')}</p>
          <p className="mt-2 text-sm text-gray-500">Glossary page - Coming in Phase 4</p>
        </div>
      </main>
    </div>
  );
}
