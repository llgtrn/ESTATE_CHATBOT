import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

export function BriefPage() {
  const { t } = useTranslation();
  const { briefId } = useParams();

  return (
    <div className="flex h-screen flex-col">
      <header className="border-b bg-white px-4 py-3">
        <h1 className="text-xl font-semibold">{t('brief.title')}</h1>
      </header>
      <main className="flex-1 overflow-auto p-4">
        <div className="mx-auto max-w-4xl">
          <p className="text-gray-600">Brief ID: {briefId}</p>
          <p className="mt-2 text-sm text-gray-500">Brief page - Coming in Phase 3</p>
        </div>
      </main>
    </div>
  );
}
