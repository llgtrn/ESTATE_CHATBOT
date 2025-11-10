import { useState, useRef, KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from '@/shared/ui';
import { Send } from 'lucide-react';
import { cn } from '@/shared/lib';

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

export function MessageInput({ onSend, isLoading, disabled, placeholder }: MessageInputProps) {
  const { t } = useTranslation();
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!message.trim() || isLoading || disabled) return;

    onSend(message.trim());
    setMessage('');

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      const maxHeight = 5 * 24; // 5 lines max
      textareaRef.current.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    }
  };

  const canSend = message.trim().length > 0 && !isLoading && !disabled;

  return (
    <div className="border-t bg-white p-4" data-testid="message-input-container">
      <div className="mx-auto flex max-w-4xl items-end gap-2">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder={placeholder || t('chat.placeholder')}
          disabled={disabled || isLoading}
          rows={1}
          className={cn(
            'min-h-[40px] flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2.5 text-sm',
            'focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20',
            'disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500',
            'placeholder:text-gray-400'
          )}
          data-testid="message-textarea"
        />
        <Button
          onClick={handleSend}
          disabled={!canSend}
          isLoading={isLoading}
          size="icon"
          className="h-10 w-10 shrink-0"
          data-testid="send-button"
          aria-label={t('chat.send')}
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
