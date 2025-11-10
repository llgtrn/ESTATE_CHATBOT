/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_WS_URL: string;
  readonly VITE_ENABLE_MOCK_API: string;
  readonly VITE_ENABLE_DEVTOOLS: string;
  readonly VITE_LOG_LEVEL: string;
  readonly VITE_DEFAULT_LANGUAGE: string;
  readonly VITE_AVAILABLE_LANGUAGES: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
