import { useTranslation } from 'react-i18next';
import { Globe, MessageSquare } from 'lucide-react';
import { Button } from '@/shared/ui';
import { useLanguageStore } from '@/shared/lib/store';
import { useState } from 'react';
import { cn } from '@/shared/lib';
import type { Language } from '@/shared/types/common';

export function HeaderWidget() {
  const { t, i18n } = useTranslation();
  const language = useLanguageStore((state) => state.language);
  const setLanguage = useLanguageStore((state) => state.setLanguage);
  const [showLanguageMenu, setShowLanguageMenu] = useState(false);

  const languages: { code: Language; name: string }[] = [
    { code: 'ja', name: '日本語' },
    { code: 'en', name: 'English' },
    { code: 'vi', name: 'Tiếng Việt' },
  ];

  const handleLanguageChange = (lang: Language) => {
    setLanguage(lang);
    i18n.changeLanguage(lang);
    setShowLanguageMenu(false);
  };

  const currentLanguageName = languages.find((l) => l.code === language)?.name || '日本語';

  return (
    <header className="border-b bg-white shadow-sm" data-testid="header">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        {/* Logo / Title */}
        <div className="flex items-center gap-2">
          <MessageSquare className="h-6 w-6 text-primary-600" />
          <h1 className="text-lg font-semibold text-gray-900">{t('app.title')}</h1>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {/* Language Selector */}
          <div className="relative">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowLanguageMenu(!showLanguageMenu)}
              className="gap-2"
              data-testid="language-selector"
            >
              <Globe className="h-4 w-4" />
              <span className="hidden sm:inline">{currentLanguageName}</span>
            </Button>

            {showLanguageMenu && (
              <>
                {/* Backdrop */}
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setShowLanguageMenu(false)}
                />

                {/* Menu */}
                <div className="absolute right-0 top-full z-20 mt-2 w-40 rounded-lg border bg-white py-1 shadow-lg">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => handleLanguageChange(lang.code)}
                      className={cn(
                        'w-full px-4 py-2 text-left text-sm hover:bg-gray-100',
                        language === lang.code && 'bg-primary-50 text-primary-700 font-medium'
                      )}
                      data-testid={`lang-${lang.code}`}
                    >
                      {lang.name}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
