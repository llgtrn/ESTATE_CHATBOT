import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { sessionApi } from '../api/sessionApi';
import type { CreateSessionRequest } from './types';

export const sessionKeys = {
  all: ['sessions'] as const,
  detail: (id: string) => [...sessionKeys.all, id] as const,
};

/**
 * Hook to create a new session
 */
export function useCreateSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data?: CreateSessionRequest) => sessionApi.createSession(data),
    onSuccess: (data) => {
      // Invalidate sessions list
      queryClient.invalidateQueries({ queryKey: sessionKeys.all });
      // Set the session data in cache
      queryClient.setQueryData(sessionKeys.detail(data.session_id), data);
    },
  });
}

/**
 * Hook to get session details
 */
export function useSession(sessionId: string | null) {
  return useQuery({
    queryKey: sessionKeys.detail(sessionId || ''),
    queryFn: () => sessionApi.getSession(sessionId!),
    enabled: !!sessionId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to delete a session
 */
export function useDeleteSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sessionId: string) => sessionApi.deleteSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sessionKeys.all });
    },
  });
}
