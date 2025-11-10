import { HeaderWidget } from '@/widgets/HeaderWidget';
import { ChatWidget } from '@/widgets/ChatWidget';

export function ChatPage() {
  return (
    <div className="flex h-screen flex-col">
      <HeaderWidget />
      <main className="flex-1 overflow-hidden">
        <ChatWidget />
      </main>
    </div>
  );
}
