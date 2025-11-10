import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { MessageList } from './MessageList';
import { MessageInput } from '@/features/send-message/ui/MessageInput';
import { useMessages, useSendMessage } from '@/entities/message/model/hooks';
import { useCreateSession } from '@/entities/session/model/hooks';
import { useSessionStore } from '@/shared/lib/store';
import { useLanguageStore } from '@/shared/lib/store';

export function ChatWidget() {
  const { t, i18n } = useTranslation();
  const currentSessionId = useSessionStore((state) => state.currentSessionId);
  const setCurrentSessionId = useSessionStore((state) => state.setCurrentSessionId);
  const addRecentSession = useSessionStore((state) => state.addRecentSession);
  const language = useLanguageStore((state) => state.language);

  const createSession = useCreateSession();
  const { data: messagesData, isLoading: isLoadingMessages, error: messagesError } = useMessages(currentSessionId);
  const sendMessage = useSendMessage(currentSessionId || '');

  // Create session on mount if none exists
  useEffect(() => {
    if (!currentSessionId && !createSession.isPending) {
      createSession.mutate(
        { language },
        {
          onSuccess: (data) => {
            setCurrentSessionId(data.session_id);
            addRecentSession(data.session_id);
          },
        }
      );
    }
  }, [currentSessionId, createSession, language, setCurrentSessionId, addRecentSession]);

  const handleSendMessage = (message: string) => {
    if (!currentSessionId) return;

    sendMessage.mutate({
      message,
      language: i18n.language as 'ja' | 'en' | 'vi',
    });
  };

  const messages = messagesData?.messages || [];

  return (
    <div className="flex h-full flex-col bg-gray-50" data-testid="chat-widget">
      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList
          messages={messages}
          isLoading={isLoadingMessages}
          error={messagesError}
        />
      </div>

      {/* Input */}
      <MessageInput
        onSend={handleSendMessage}
        isLoading={sendMessage.isPending}
        disabled={!currentSessionId}
        placeholder={
          !currentSessionId
            ? t('chat.placeholder')
            : sendMessage.isPending
            ? t('chat.typing')
            : t('chat.placeholder')
        }
      />
    </div>
  );
}
