import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { messageApi } from '../api/messageApi';
import type { SendMessageRequest, Message } from './types';

export const messageKeys = {
  all: ['messages'] as const,
  bySession: (sessionId: string) => [...messageKeys.all, sessionId] as const,
};

/**
 * Hook to get messages for a session
 */
export function useMessages(sessionId: string | null) {
  return useQuery({
    queryKey: messageKeys.bySession(sessionId || ''),
    queryFn: () => messageApi.getMessages(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 5000, // Poll every 5 seconds for new messages
  });
}

/**
 * Hook to send a message
 */
export function useSendMessage(sessionId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SendMessageRequest) => messageApi.sendMessage(sessionId, data),
    onMutate: async (variables) => {
      // Cancel any outgoing refetches
      await queryClient.cancelQueries({ queryKey: messageKeys.bySession(sessionId) });

      // Snapshot the previous value
      const previousMessages = queryClient.getQueryData(messageKeys.bySession(sessionId));

      // Optimistically update to the new value
      queryClient.setQueryData(messageKeys.bySession(sessionId), (old: any) => {
        if (!old) return old;

        const optimisticMessage: Message = {
          message_id: `temp-${Date.now()}`,
          session_id: sessionId,
          role: 'user',
          content: variables.message,
          language: variables.language || 'ja',
          created_at: new Date().toISOString(),
        };

        return {
          ...old,
          messages: [...old.messages, optimisticMessage],
          total: old.total + 1,
        };
      });

      return { previousMessages };
    },
    onError: (_err, _variables, context) => {
      // Rollback to previous value on error
      if (context?.previousMessages) {
        queryClient.setQueryData(messageKeys.bySession(sessionId), context.previousMessages);
      }
    },
    onSuccess: (data) => {
      // Refetch messages to get the assistant's response
      queryClient.invalidateQueries({ queryKey: messageKeys.bySession(sessionId) });
    },
  });
}
