import { Avatar } from '@/shared/ui';
import { cn, formatDate } from '@/shared/lib';
import type { Message } from '../model/types';

interface MessageItemProps {
  message: Message;
  isLatest?: boolean;
}

export function MessageItem({ message, isLatest }: MessageItemProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 animate-fade-in',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
      data-testid="message-item"
      data-role={message.role}
    >
      {/* Avatar */}
      <Avatar
        fallback={isUser ? 'U' : 'A'}
        className={cn(
          'shrink-0',
          isUser ? 'bg-primary-100 text-primary-700' : 'bg-gray-100 text-gray-700'
        )}
        size="md"
      />

      {/* Message Content */}
      <div
        className={cn(
          'flex max-w-[70%] flex-col gap-1',
          isUser ? 'items-end' : 'items-start'
        )}
      >
        {/* Message Bubble */}
        <div
          className={cn(
            'rounded-2xl px-4 py-2.5 shadow-sm',
            isUser
              ? 'bg-primary-600 text-white rounded-br-md'
              : 'bg-gray-100 text-gray-900 rounded-bl-md'
          )}
        >
          <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
            {message.content}
          </p>
        </div>

        {/* Metadata */}
        <div className="flex items-center gap-2 px-1 text-xs text-gray-500">
          <time dateTime={message.created_at}>
            {formatDate(message.created_at, message.language === 'ja' ? 'ja-JP' : 'en-US')}
          </time>
          {message.intent && (
            <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] font-medium text-gray-600">
              {message.intent}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
