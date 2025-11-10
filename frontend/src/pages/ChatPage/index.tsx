import { useTranslation } from 'react-i18next';

export function ChatPage() {
  const { t } = useTranslation();

  return (
    <div className="flex h-screen flex-col">
      <header className="border-b bg-white px-4 py-3">
        <h1 className="text-xl font-semibold">{t('app.title')}</h1>
      </header>
      <main className="flex-1 overflow-hidden p-4">
        <div className="mx-auto flex h-full max-w-4xl items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900">{t('chat.title')}</h2>
            <p className="mt-2 text-gray-600">{t('app.description')}</p>
            <p className="mt-4 text-sm text-gray-500">
              Frontend is ready! Phase 0 complete. 🎉
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
